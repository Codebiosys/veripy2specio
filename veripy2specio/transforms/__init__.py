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
        return {
            'all_passed': self.status_from_children(features) == constants.Status.PASSED,
            'features': [feature.serialize() for feature in features]
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
