import re

from .base import SpecioBase
from .step import Step, InstructionsResults
from ..constants import Keyword
from .message import DeviationMessage


class Scenario(SpecioBase):

    def __init__(self, source, scenario_number):
        super().__init__(source)
        self.steps = []
        self.scenario_number = scenario_number
        self._deviation = None
        self._populate_from_source(source)

    @property
    def id(self):
        return re.sub('\W',  '_',  self.source.get('location'))

    @property
    def status(self):
        return self.status_from_children(self.steps)

    @property
    def description(self):
        return self.source.get('doc_string', {}).get('value', None)

    @property
    def has_table(self):
        return 'table' in self.source

    @property
    def table_headers(self):
        return self.source.get('table', {}).get('headings', [])

    @property
    def table_rows(self):
        for row in self.source.get('table', {}).get('rows', []):
            yield {'data': row}

    @property
    def tags(self):
        return [tag for tag in self.tags_from_elements([self.source])]

    @property
    def is_setup(self):
        return any(tag['name'] == 'setup' for tag in self.tags)

    @property
    def is_teardown(self):
        return any(tag['name'] == 'teardown' for tag in self.tags)

    def _populate_from_source(self, source):
        """
        Using the given elements, enumerate through each and
        transform into a scenario
        """
        for step in source.get('steps', []):
            self.steps.append(Step(step, self.id))

        if any(not step.passed for step in self.steps):
            self._deviation = DeviationMessage(self.steps, self.id)

    def group_steps(self):
        """ Given a list of steps, group them into 2 bins: given_when and then
        based on their keyword.
        AND/BUT statements are lumped in with their predecesor.
        """
        if not len(self.steps):
            return []

        groups = []
        group = None
        switch = '--invalid--'
        # import pdb; pdb.set_trace()
        for step in self.steps:
            if step.keyword.name in switch:
                # We're in the same state as last iteration. Do nothing
                pass
            elif step.keyword in (Keyword.GIVEN, Keyword.WHEN):
                # GIVEN/WHEN: Toggle the switch and push a new group onto the list.
                switch = 'GIVEN_WHEN'
                group = InstructionsResults()
                groups.append(group)

            elif step.keyword == Keyword.THEN:
                # THEN: Toggle the switch
                switch = 'THEN'
            else:
                # AND/BUT: Do nothing
                pass

            # Add the current step to the ending group.
            group.add_step(step, switch)

        return groups

    @property
    def deviation(self):
        return self._deviation

    def serialize_prerequisite(self):
        serialized = {
            # Required Base properties
            'id': self.id,
            'name': self.name,
            'keyword': self.keyword.value,
            # Required Scenario properties
            'scenario_name': self.name,
            'scenario_number': self.scenario_number,
            'tags': self.tags,
            'is_setup': self.is_setup,
            'is_teardown': self.is_teardown,
            }

        if self.description:
            serialized['scenario_description'] = self.description

        if self.has_table:
            serialized['table'] = {
                'headers': self.table_headers,
                'rows': [row for row in self.table_rows]
            }
        return serialized

    def serialize(self):
        serialized = {
            # Required Base properties
            'id': self.id,
            'name': self.name,
            'keyword': self.keyword.value,
            'status': self.status.value,
            'passed': self.passed,
            # Required Scenario properties
            'scenario_name': self.name,
            'scenario_number': self.scenario_number,
            'instructions_results': [step_group.serialize() for step_group in self.group_steps()],
            'tags': self.tags,
            }

        if self.description:
            serialized['scenario_description'] = self.description

        if self.deviation:
            serialized['deviation'] = self.deviation.serialize()

        if self.has_table:
            serialized['table'] = {
                'headers': self.table_headers,
                'rows': [row for row in self.table_rows]
            }
        return serialized


class Background(Scenario):
    pass


class Teardown(Scenario):
    pass
