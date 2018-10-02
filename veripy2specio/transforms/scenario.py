import re

from .base import SpecioBase
from .step import Step, StepGroup
from ..constants import Keyword


class Scenario(SpecioBase):

    def __init__(self, source, scenario_number):
        super().__init__(source)
        self.steps = []
        self.scenario_number = scenario_number
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
    def tags(self):
        return [tag for tag in self.tags_from_elements([self.source])]

    def _populate_from_source(self, source):
        """
        Using the given elements, enumerate through each and
        transform into a scenario
        """
        for step in source.get('steps', []):
            pass
            self.steps.append(Step(step, self.id))

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
                group = StepGroup()
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
            'number': self.scenario_number,
            'steps': [step_group.serialize() for step_group in self.group_steps()],
            'tags': self.tags,
            }

        if self.description:
            serialized['description'] = self.description

        return serialized


class Background(Scenario):
    pass


class Teardown(Scenario):
    pass
