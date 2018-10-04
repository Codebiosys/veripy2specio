from fixtures import veripy_step
from veripy2specio import constants


def test_result_message_properties():
    from veripy2specio.transforms.step import Step
    from veripy2specio.transforms.message import ResultMessage
    scenario_id = 'feature_scenario_location'

    valid_step = Step(veripy_step.step_with_messages, scenario_id)

    assert len(valid_step.messages) == 3
    result_message = ResultMessage(valid_step, veripy_step.step_with_messages)
    serialized_message = result_message.serialize()
    # Base Props
    assert result_message.reference_number > 3
    assert serialized_message['reference_number'] > 3

    assert result_message.id == \
        f'feature_scenario_location_2_{result_message.reference_number}'
    assert serialized_message['id'] == \
        f'feature_scenario_location_2_{result_message.reference_number}'

    assert not result_message.is_deviation
    assert not serialized_message['is_deviation']

    assert result_message.status == constants.Status.FAILED
    assert serialized_message['status'] == 'Failed'

    assert result_message.result == "A message from the step"
    assert serialized_message['result'] == "A message from the step"


def test_error_message_properties():
    from veripy2specio.transforms.step import Step
    from veripy2specio.transforms.message import ErrorMessage
    scenario_id = 'feature_scenario_location'

    valid_step = Step(veripy_step.step_with_messages, scenario_id)

    assert len(valid_step.messages) == 3  # 3 messages created with Step init
    error_message = ErrorMessage(valid_step, veripy_step.step_with_messages)
    serialized_message = error_message.serialize()
    # Base Props
    assert error_message.reference_number > 3
    assert serialized_message['reference_number'] > 3

    # One was created during the Step init, and previous steps update as well
    assert serialized_message['error']['error_number'] == error_message.error_number

    assert error_message.id == \
        f'feature_scenario_location_2_{error_message.reference_number}'
    assert serialized_message['id'] == \
        f'feature_scenario_location_2_{error_message.reference_number}'

    assert error_message.is_deviation
    assert serialized_message['is_deviation']

    assert error_message.status == constants.Status.FAILED
    assert serialized_message['status'] == 'Failed'

    assert error_message.expected == "Step Name"
    assert serialized_message['error']['expected'] == "Step Name"

    assert error_message.actual == "an error occurred"
    assert serialized_message['error']['actual'] == "an error occurred"


def test_skipped_error_message_properties():
    from veripy2specio.transforms.step import Step
    from veripy2specio.transforms.message import ErrorMessage
    scenario_id = 'feature_scenario_location'

    valid_step = Step(veripy_step.step_skipped, scenario_id)

    error_message = ErrorMessage(valid_step, veripy_step.step_skipped)
    serialized_message = error_message.serialize()
    # Base Props
    assert error_message.reference_number > 3
    assert serialized_message['reference_number'] > 3

    # One was created during the Step init, and previous steps update as well
    assert serialized_message['error']['error_number'] == error_message.error_number

    assert not error_message.is_deviation
    assert not serialized_message['is_deviation']

    assert error_message.status == constants.Status.SKIPPED
    assert serialized_message['status'] == 'Skipped'

    assert error_message.expected == "Step Name"
    assert serialized_message['error']['expected'] == "Step Name"

    assert error_message.actual == "This is likely because a previous step failed."
    assert serialized_message['error']['actual'] == \
        "This is likely because a previous step failed."


def test_undefined_error_message_properties():
    from veripy2specio.transforms.step import Step
    from veripy2specio.transforms.message import ErrorMessage
    scenario_id = 'feature_scenario_location'

    valid_step = Step(veripy_step.step_undefined, scenario_id)

    error_message = ErrorMessage(valid_step, veripy_step.step_undefined)
    serialized_message = error_message.serialize()
    # Base Props
    assert error_message.reference_number > 3
    assert serialized_message['reference_number'] > 3

    # One was created during the Step init, and previous steps update as well
    assert serialized_message['error']['error_number'] == error_message.error_number

    assert not error_message.is_deviation
    assert not serialized_message['is_deviation']

    assert error_message.status == constants.Status.UNDEFINED
    assert serialized_message['status'] == 'Undefined'

    assert error_message.expected == "Step Name"
    assert serialized_message['error']['expected'] == "Step Name"

    assert error_message.actual == "This means the plan was not valid."
    assert serialized_message['error']['actual'] == \
        "This means the plan was not valid."


def test_attachment_message_properties():
    from veripy2specio.transforms.step import Step
    from veripy2specio.transforms.message import AttachmentMessage
    scenario_id = 'feature_scenario_location'

    valid_step = Step(veripy_step.step_with_messages, scenario_id)

    assert len(valid_step.messages) == 3  # 3 messages created with Step init
    attachment_message = AttachmentMessage(
        valid_step,
        veripy_step.step_with_messages,
        veripy_step.step_with_messages['embeddings'][0]
        )
    serialized_message = attachment_message.serialize()
    # Base Props
    assert attachment_message.reference_number > 3
    assert serialized_message['reference_number'] > 3

    assert attachment_message.id == \
        f'feature_scenario_location_2_{attachment_message.reference_number}'
    assert serialized_message['id'] == \
        f'feature_scenario_location_2_{attachment_message.reference_number}'

    assert attachment_message.id == \
        f'feature_scenario_location_2_{attachment_message.reference_number}'
    assert serialized_message['id'] == \
        f'feature_scenario_location_2_{attachment_message.reference_number}'

    assert not attachment_message.is_deviation
    assert not serialized_message['is_deviation']

    assert attachment_message.status == constants.Status.FAILED
    assert serialized_message['status'] == 'Failed'

    assert attachment_message.data == "AAABBBB"
    assert serialized_message['attachment']['data'] == "AAABBBB"

    assert attachment_message.media_type == "image/gif"
    assert serialized_message['attachment']['type'] == "image/gif"
