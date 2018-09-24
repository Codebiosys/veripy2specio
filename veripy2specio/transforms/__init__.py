import re
import markdown2

from veripy2specio import constants


class Veripy2SpecioTransform(object):
    """ A general transformation class that converts data from the VeriPy
    (cucumber.json) format into a Specio format for later user by a templating
    engine or further processing.

    **Sample Usage**
    ::
        veripy_input = get_input()
        transform = Veripy2SpecioTransform()
        specio_output = transform(veripy_input)

    **Subclassing Notes**
    Methods are broken up into sub-generators for easily modified behavior.
    Typically, the methods take the form <element>_from_<parent_element>
    and return a generator.
    """

    def __init__(self):
        self.reference_number = 1

    def __call__(self, input):
        return {
            'features': [feature for feature in self.features_from_input(input)],
        }

    # Transformation Methods

    def generate_reference_number(self):
        reference = self.reference_number
        self.reference_number += 1
        return reference

    def group_steps(self, steps):
        """ Given a list of steps, group them into 2 bins: given_when and then
        based on their keyword.

        AND/BUT statements are lumped in with their predecesor.
        """
        groups = []
        switch = '--invalid--'

        for step in steps:
            step_type = step['keyword'].lower()
            if step_type in switch:
                # We're in the same state as last iteration. Do nothing
                pass
            elif step_type in (constants.GIVEN, constants.WHEN):
                # GIVEN/WHEN: Toggle the switch and push a new group onto the list.
                switch = 'given_when'
                groups.append({'given_when': [], 'then': [], 'messages': []})
            elif step_type == constants.THEN:
                # THEN: Toggle the switch
                switch = 'then'
            else:
                # AND/BUT: Do nothing
                pass

            # Add the current step to the ending group.
            groups[-1][switch].append(step)
            groups[-1]['messages'].extend(step.pop('messages'))
        return groups

    def description_from_feature(self, feature):
        """ Trim off the injected <pre> tags and parse the description
        as markdown.
        """
        description = feature.pop('description', '')
        return markdown2.markdown(description[5:-6])

    def passed_from_children(self, children):
        for child in children:
            yield child['passed']

    def steps_from_element(self, element):
        for step in element.pop('steps'):
            step_result = {
                'id': re.sub('\W',  '_', f'{element["location"]}_{step["line"]}'),
                'name': step['name'],
                'keyword': step['keyword'],
                'status': step['result']['status'],
                'passed': step['result']['status'] == constants.PASSED,
                'references': [],
                'messages': []

            }
            if step.get('doc_string', {}).hasattr('value'):
                step_result['messages'].append({
                    'type': 'message',
                    'reference_number': self.generate_reference_number(),
                    'content': step.get('doc_string', {}).get('value')
                })
            if step.hasattr('stored_value'):
                step_result['messages'].append({
                    'type': 'result',
                    'reference_number': self.generate_reference_number(),
                    'content': step.get('stored_value')
                })
            if step['result']['status'] != constants.PASSED:
                message = f'The test resulted in a {step["result"]["status"]}, '\
                    'but no message was supplied'
                if step.get('result', {}).hasattr('error_message'):
                    message = step['result']['error_message']
                step_result['messages'].append({
                    'type': 'error',
                    'reference_number': self.generate_reference_number(),
                    'content': message
                })
            for embed in step.get('embeddings', []):
                step_result['messages'].append({
                    'type': 'attachment',
                    'reference_number': self.generate_reference_number(),
                    'attachment': {
                        'data': embed['data'],
                        'type': embed['media']['type']
                    }
                })
            if len(step_result['messages']):
                if len(step_result['messages']) > 1:
                    for message in step_result['messages'][:len(step_result['messages'])-1]:
                        step_result['references'].append(
                            {'value': message['reference_number'],
                             'last': False}
                        )
                step_result['references'].append(
                    {'value': step_result['messages'][-1]['reference_number'],
                     'last': True}
                )
            yield step_result

    def tags_from_elements(self, elements):
        tags = sorted(set(
            tag['name']
            for element in elements
            for tag in element.get('tags', [])
            if tag.get('name')
        ))
        if tags:
            if len(tags) > 1:
                for tag in tags[:len(tags)-1]:
                    yield {'name': tag, 'last': False}
            yield {'name': tags[-1], 'last': True}

    def scenarios_from_feature(self, feature):
        for i, element in enumerate(feature.pop('elements')):

            steps = [step for step in self.steps_from_element(element)]
            passed = all(self.passed_from_children(steps))
            tags = [tag for tag in self.tags_from_elements([element])]
            yield {
                'id': re.sub('\W',  '_', element.get('location')),
                'name': element.get('name'),
                'keyword': element.get('keyword'),
                'status': 'passed' if passed else 'failed',
                'passed': passed,
                'description': element.get('doc_string', {}).get('value', ''),
                'number': i + 1,
                'steps': self.group_steps(steps),
                'tags': tags
            }

    def features_from_input(self, input):
        """ Given an input VeriPy file, retrieve the Specio formatted features.

        This function returns an iterable generator that can be used to progressively
        parse the input configuration.
        """
        for feature in input:
            # scenarios = [scenario for scenario in self.scenarios_from_feature(feature)]
            # scenario_tags = [tag for tag in self.tags_from_scenarios(scenarios)]
            scenarios = [
                scenario for scenario
                in self.scenarios_from_feature(feature)
            ]
            tags = self.tags_from_elements([feature])
            scenario_tags = self.tags_from_elements(scenarios)
            passed = all(self.passed_from_children(scenarios))
            yield {
                'id': re.sub('\W',  '_', feature.get('id')),
                'name': feature.get('name'),
                'keyword': feature.get('keyword'),
                'status': 'passed' if passed else 'failed',
                'passed': passed,
                'description': self.description_from_feature(feature),
                'scenarios': scenarios,
                'tags': [tag for tag in tags],
                'scenario_tags': [tag for tag in scenario_tags],
            }
