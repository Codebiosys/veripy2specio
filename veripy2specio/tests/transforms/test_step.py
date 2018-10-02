from veripy2specio.tests.fixtures import veripy_step
from veripy2specio import constants


def test_step_properties():
    from veripy2specio.transforms.step import Step
    scenario_id = 'feature_scenario_location'
    valid_step = Step(veripy_step.given_step, scenario_id)
    serialized_step = valid_step.serialize()
    # Base Props
    assert valid_step.keyword == constants.Keyword.GIVEN
    assert serialized_step['keyword'] == "Given"
    assert valid_step.name == "Step Name"
    assert serialized_step['name'] == "Step Name"
    assert valid_step.passed
    assert serialized_step['passed']
    assert valid_step.id == 'feature_scenario_location_2'
    assert serialized_step['id'] == 'feature_scenario_location_2'
    assert valid_step.status == constants.Status.PASSED
    assert serialized_step['status'] == 'Passed'
    assert valid_step.note == "some description"
    assert serialized_step['note'] == "some description"


def test_step_reference_properties():
    from veripy2specio.transforms.step import Step
    scenario_id = 'feature_scenario_location'
    valid_step = Step(veripy_step.step_with_messages, scenario_id)
    serialized_step = valid_step.serialize()
    references = [reference for reference in valid_step.references()]
    assert len(references) == 3
    assert len(serialized_step['references']) == 3
    assert not serialized_step['references'][1]['last']
    assert serialized_step['references'][2]['last']
    # Base Props
