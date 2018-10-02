import re
import markdown2
from veripy2specio.constants import Keyword
from .base import SpecioBase
from .scenario import Background, Teardown, Scenario


class Feature(SpecioBase):
    _feature_number = 0

    def __init__(self, source):
        super().__init__(source)
        self.scenarios = []
        self.prerequisites = []
        self.cleanup = []
        Feature._feature_number += 1
        self.feature_number = self._feature_number
        self._populate_from_source(source)

    @property
    def id(self):
        return re.sub('\W',  '_', self.source.get('id'))

    @property
    def status(self):
        return self.status_from_children(self.scenarios)

    @property
    def description(self):
        """ Trim off the injected <pre> tags and parse the description
        as markdown.
        """
        description = self.source.get('description', '')
        if description:
            return markdown2.markdown(description[5:-6])
        return description

    def _populate_from_source(self, source):
        """
        Using the given elements, enumerate through each and
        transform into a scenario
        """
        # import pdb; pdb.set_trace()
        scenario_number = 0
        for element in source.get('elements', []):
            if Keyword(element.get('type')) == Keyword.BACKGROUND:
                potential_background = Background(element, 0)
                if not any([
                        prereq.id == potential_background.id
                        for prereq in self.prerequisites]):
                    self.prerequisites.append(potential_background)
            elif any([
                    tag.get('name', '') == 'prerequisite'
                    for tag in element.get('tags', [])]):
                potential_background = Background(element, 0)
                if not any([
                        prereq.id == potential_background.id
                        for prereq in self.prerequisites]):
                            self.prerequisites.append(potential_background)
            elif any([
                    tag.get('name', '') == 'cleanup'
                    for tag in element.get('tags', [])]):
                potential_cleanup = Teardown(element, 0)
                if not any([
                        cleanup.id == potential_cleanup.id
                        for cleanup in self.teardown]):
                    self.cleanup.append(Teardown(element, 0))
            else:
                scenario_number += 1
                self.scenarios.append(Scenario(element, scenario_number))

    @property
    def tags(self):
        return [tag for tag in self.tags_from_elements([self.source])]

    def get_scenario_tags(self):

        all_tags = []
        for scenario in self.scenarios:
            all_tags.extend(scenario.tags)

        tags = sorted(set(
            tag['name']
            for tag in all_tags
            if tag.get('name') and tag['name'] not in ['prerequisite', 'cleanup']
        ))

        if tags:
            if len(tags) > 1:
                for tag in tags[:len(tags)-1]:
                    yield {'name': tag, 'last': False}
            yield {'name': tags[-1], 'last': True}

    @property
    def scenario_tags(self):
        return [tag for tag in self.get_scenario_tags()]

    @property
    def has_scenarios(self):
        return len(self.scenarios) > 0

    @property
    def has_prerequisites(self):
        return len(self.prerequisites) > 0

    @property
    def has_cleanup(self):
        return len(self.cleanup) > 0

    def serialize(self):
        serialized = {
            # Required Base properties
            'id': self.id,
            'name': self.name,
            'keyword': self.keyword.value,
            'status': self.status.value,
            'passed': self.passed,
            # Required Feature properties
            'feature_name': self.name,
            'scenarios': [scenario.serialize() for scenario in self.scenarios],
            'has_scenarios': self.has_scenarios,
            'tags': self.tags,
            'scenario_tags': self.scenario_tags,
            'prerequisites': [prereq.serialize() for prereq in self.prerequisites],
            'has_prerequisites': self.has_prerequisites,
            'cleanup': [teardown.serialize() for teardown in self.cleanup],
            'has_cleanup': self.has_cleanup,
            'feature_number': self.feature_number
            }

        if self.description:
            serialized['description'] = self.description

        return serialized
