from .. import constants
from .feature import Feature


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

    def __call__(self, input):
        features = [Feature(feature) for feature in input]
        result = {
            'defines': [],
            'features': [],
            'prerequisite_scripts': []
        }
        for feature in features:
            if feature.is_define:
                result['defines'].append(feature)
            elif feature.is_setup:
                result['prerequisite_scripts'].append(feature)
            else:
                result['features'].append(feature)

        for feature in result['features']:
            if len(feature.setup_tags) > 0:
                feature.add_prerequisite_scripts(result['prerequisite_scripts'])

        return {
            'all_tags': [],  # TODO: pull all tags so commas work
            'all_passed': self.status_from_children(result['features']) == constants.Status.PASSED,
            'features': [
                feature.serialize() for feature in result['features']
            ],
            'defines': [
                feature.serialize() for feature in result['defines']
            ],
            'setup_scripts': [
                feature.serialize_prerequisite_script()
                for feature in result['prerequisite_scripts']
            ],
        }

    def status_from_children(self, children):
        statuses = set(child.status for child in children)
        if all(status == constants.Status.PASSED for status in statuses):
            return constants.Status.PASSED
        elif any(status == constants.Status.FAILED for status in statuses):
            return constants.Status.FAILED
        elif any(status == constants.Status.UNDEFINED for status in statuses):
            return constants.Status.UNDEFINED
        return constants.Status.SKIPPED
