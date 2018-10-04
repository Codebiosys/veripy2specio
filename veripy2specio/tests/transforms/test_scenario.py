from fixtures import veripy_scenario
from veripy2specio import constants


def test_scenario_properties():
    from veripy2specio.transforms.scenario import Scenario
    scenario_number = 2
    valid_scenario = Scenario(veripy_scenario.scenario_no_steps, scenario_number)
    serialized_scenario = valid_scenario.serialize()
    # Base Props
    assert valid_scenario.keyword == constants.Keyword.SCENARIO
    assert serialized_scenario['keyword'] == "Scenario"
    assert valid_scenario.name == "Scenario Name"
    assert serialized_scenario['name'] == "Scenario Name"
    assert not valid_scenario.passed
    assert not serialized_scenario['passed']
    assert valid_scenario.scenario_number == 2
    assert serialized_scenario['number'] == 2
    assert valid_scenario.id == '_scenario_file_location_'
    assert serialized_scenario['id'] == '_scenario_file_location_'
    assert valid_scenario.status == constants.Status.SKIPPED
    assert serialized_scenario['status'] == 'Skipped'
    assert valid_scenario.description == "A Description of the Scenario"
    assert serialized_scenario['description'] == "A Description of the Scenario"
    assert valid_scenario.tags[0]['last']
    assert serialized_scenario['tags'][0]['last']
    assert valid_scenario.tags[0]['name'] == 'Test1'
    assert serialized_scenario['tags'][0]['name'] == 'Test1'
