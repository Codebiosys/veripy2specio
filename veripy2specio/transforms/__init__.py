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
        self.error_number = 1

    def __call__(self, input):
        features = [feature for feature in self.features_from_input(input)]
        return {
            'all_passed': all(self.passed_from_children(features)),
            'features': features,
        }

    # Transformation Methods

    def generate_reference_number(self):
        reference = self.reference_number
        self.reference_number += 1
        return reference

    def generate_error_number(self):
        reference = self.error_number
        self.error_number += 1
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
                groups.append({
                    'given_when': [],
                    'then': [],
                    'messages': [],
                    'status': step['status'],
                    'passed': step['passed']
                })
            elif step_type == constants.THEN:
                # THEN: Toggle the switch
                switch = 'then'
            else:
                # AND/BUT: Do nothing
                pass

            # Add the current step to the ending group.
            groups[-1][switch].append(step)
            if not step['passed']:
                # Trip the status only if the step didn't pass
                groups[-1]['status'] = step['status']
                groups[-1]['passed'] = step['passed']
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
            step_id = re.sub('\W',  '_', f'{element["location"]}_{step["line"]}')
            step_result = {
                'id': step_id,
                'name': step['name'],
                'keyword': step['keyword'],
                'status': step['result']['status'],
                'passed': step['result']['status'] == constants.PASSED,
                'references': [],
                'messages': []

            }
            if 'value' in step.get('doc_string', {}):
                # reference_number = self.generate_reference_number()
                step_result['note'] = step.get('doc_string', {}).get('value')
                # ['messages'].append({
                #     'type': 'note',
                #     'id': f'{step_id}_{reference_number}',
                #     'reference_number': reference_number,
                #     'note': step.get('doc_string', {}).get('value'),
                #     'is_deviation': False
                # })
            if 'stored_value' in step:
                reference_number = self.generate_reference_number()
                step_result['messages'].append({
                    'type': 'result',
                    'id': f'{step_id}_{reference_number}',
                    'reference_number': reference_number,
                    'result': step.get('stored_value'),
                    'is_deviation': False
                })
            if step['result']['status'] != constants.PASSED:
                message = f'The test was {step["result"]["status"]}, '\
                    'and no message was supplied'
                is_deviation = False
                if 'error_message' in step.get('result', {}):
                    message = step['result']['error_message']
                if step['result']['status'] == constants.FAILED:
                    is_deviation = True

                reference_number = self.generate_reference_number()
                error_message = {
                    'type': 'error',
                    'id': f'{step_id}_{reference_number}',
                    'reference_number': reference_number,
                    'is_deviation': is_deviation,
                    'status': step['result']['status'],
                    'passed': False,
                    'error': {
                        'expected': step['name'],
                        'actual': message
                    }
                }
                if is_deviation:
                    error_number = self.generate_error_number()
                    error_message['error']['error_number'] = error_number
                step_result['messages'].append(error_message)

            for embed in step.get('embeddings', []):
                reference_number = self.generate_reference_number()
                step_result['messages'].append({
                    'type': 'attachment',
                    'id': f'{step_id}_{reference_number}',
                    'reference_number': reference_number,
                    'is_deviation': False,
                    'status': step['result']['status'],
                    'passed': step['result']['status'] == constants.PASSED,
                    'attachment': {
                        'data': embed['data'],
                        'type': embed['media']['type']
                    }
                })
            if len(step_result['messages']):
                if len(step_result['messages']) > 1:
                    for message in step_result['messages'][:len(step_result['messages'])-1]:
                        step_result['references'].append(
                            {
                                'id': message['id'],
                                'reference_number': message['reference_number'],
                                'last': False
                            }
                        )
                step_result['references'].append(
                    {
                        'id': step_result['messages'][-1]['id'],
                        'reference_number': step_result['messages'][-1]['reference_number'],
                        'last': True
                     }
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
                'scenario_name': element.get('name'),
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
                'feature_name': feature.get('name'),
                'keyword': feature.get('keyword'),
                'status': 'passed' if passed else 'failed',
                'passed': passed,
                'description': self.description_from_feature(feature),
                'scenarios': scenarios,
                'tags': [tag for tag in tags],
                'scenario_tags': [tag for tag in scenario_tags],
            }
