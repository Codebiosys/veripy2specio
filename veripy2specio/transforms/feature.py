import re
import markdown2
from veripy2specio.constants import Keyword, Status
from .base import SpecioBase
from .scenario import Background, Scenario


class Feature(SpecioBase):
    _feature_number = 0

    def __init__(self, source):
        super().__init__(source)
        self._scenarios = []
        self._skipped_scenarios = []
        self._prerequisites = []
        self._prerequisite_scripts = []
        self._feature_number = 0
        self._populate_from_source(source)

    @property
    def id(self):
        return re.sub('\W',  '_', self.source.get('id'))

    @property
    def status(self):
        return self.status_from_children(self.scenarios)

    @property
    def feature_number(self):
        return self._feature_number

    def set_feature_number(self, feature_number):
        self._feature_number = feature_number

    @property
    def description(self):
        """ Trim off the injected <pre> tags and parse the description
        as markdown.
        """
        description = self.source.get('description', None)
        if description:
            stripped = re.sub(
                        r"<[/]?pre>",
                        "",
                        description
                        ).strip()
            if stripped:
                return markdown2.markdown(stripped)
        return None

    def _populate_from_source(self, source):
        """
        Using the given elements, enumerate through each and
        transform into a scenario
        """
        scenario_number = 0
        for element in source.get('elements', []):
            if Keyword(element.get('type')) == Keyword.BACKGROUND:
                potential_background = Background(element, 0)
                if not any([
                        prereq.id == potential_background.id
                        for prereq in self._prerequisites]):
                    self._prerequisites.append(potential_background)
            else:
                scenario_number += 1
                new_scenario = Scenario(element, scenario_number)
                if new_scenario.status != Status.SKIPPED:
                    self._scenarios.append(new_scenario)
                else:
                    self._skipped_scenarios.append(new_scenario)

    @property
    def scenarios(self):
        return self._scenarios

    @property
    def skipped_scenarios(self):
        return self._skipped_scenarios

    @property
    def all_scenarios(self):
        return [*self._scenarios, *self._skipped_scenarios]

    def add_prerequisite_scripts(self, all_setup_features):
        """
        """
        for setup_feature in all_setup_features:
            if any(tag['name'] == setup_feature.setup_name for tag in self.setup_tags):
                self._prerequisite_scripts.append(setup_feature)

    @property
    def has_prerequisite_scripts(self):
        return len(self.prerequisite_scripts) > 0

    @property
    def prerequisite_scripts(self):
        return self._prerequisite_scripts

    @property
    def tags(self):
        for tag in self.tags_from_elements([self.source]):
            if not tag['name'].startswith('configure') and \
               not tag['name'].startswith('setup') and \
               not tag['name'].startswith('define') and \
               not tag['name'].startswith('skip'):
                yield tag

    @property
    def is_setup(self):
        return any([
            tag['name'].startswith('configure')
            for tag in self.tags_from_elements([self.source])
            ])

    @property
    def setup_name(self):
        return next((
            tag['name'].replace('configure.', '')
            for tag in self.tags_from_elements([self.source])
            if tag['name'].startswith('configure.')),
            '')

    @property
    def is_define(self):
        return any([
            tag['name'].startswith('define')
            for tag in self.tags_from_elements([self.source])
        ])

    @property
    def setup_tags(self):
        return [tag for tag in self.setup_tags_from_elements([self.source])]

    def get_scenario_tags(self):
        all_tags = []
        for scenario in self.scenarios:
            all_tags.extend(scenario.tags)

        tags = sorted(set(
            tag['name']
            for tag in all_tags
            if tag.get('name') and not tag['name'].startswith('fixture')
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
    def has_skipped_scenarios(self):
        return len(self.skipped_scenarios) > 0

    @property
    def has_deviations(self):
        return any(
            scenario.deviation is not None
            for scenario in self.scenarios
        )

    @property
    def has_attachments(self):
        return any(
            step.attachment is not None
            for scenario in self.scenarios
            for step in scenario.steps
        )

    @property
    def has_prerequisites(self):
        return len(self.prerequisites) > 0

    @property
    def prerequisites(self):
        return self._prerequisites

    def serialize_prerequisite_script(self):
        serialized = {
            # Required Base properties
            'id': self.id,
            'name': self.name,
            'keyword': self.keyword.value,
            # Required Feature properties
            'feature_name': self.name,
            'has_scenarios': self.has_scenarios,
            'feature_number': self.feature_number,
            'scenarios': [scenario.serialize_prerequisite() for scenario in self.all_scenarios],
            }

        if self.description:
            serialized['description'] = self.description

        return serialized

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
            'skipped_scenarios': [scenario.serialize() for scenario in self.skipped_scenarios],
            'has_scenarios': self.has_scenarios,
            'has_skipped_scenarios': self.has_skipped_scenarios,
            'has_deviations': self.has_deviations,
            'has_attachments': self.has_attachments,
            'tags': [tag for tag in self.tags],
            'scenario_tags': self.scenario_tags,
            'prerequisites': [prereq.serialize() for prereq in self.prerequisites],
            'prerequisite_scripts': [
                prereq.serialize_prerequisite_script()
                for prereq in self.prerequisite_scripts
            ],
            'has_prerequisites': self.has_prerequisites,
            'has_prerequisite_scripts': self.has_prerequisite_scripts,
            'feature_number': self.feature_number
            }

        if self.description:
            serialized['description'] = self.description

        return serialized
