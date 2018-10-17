import pytest


@pytest.fixture
def feature_no_doc():
    return {
      "elements": [],
      "id": "id-123",
      "keyword": "Feature",
      "line": 1,
      "name": "veripy outputs a result",
      "status": "Passed",
      "uri": "/veripy/feature/location",
      "tags": [
        {
          "line": 2,
          "name": "Test1"
        }
      ]
    }


@pytest.fixture
def feature_empty_doc():
    return {
      "elements": [],
      "description": "",
      "id": "id-123",
      "keyword": "Feature",
      "line": 1,
      "name": "veripy outputs a result",
      "status": "Passed",
      "uri": "/veripy/feature/location",
      "tags": [
        {
          "line": 2,
          "name": "Test1"
        }
      ]
    }


@pytest.fixture
def feature_pre_only_doc():
    return {
      "elements": [],
      "description": "<pre></pre>",
      "id": "id-123",
      "keyword": "Feature",
      "line": 1,
      "name": "veripy outputs a result",
      "status": "Passed",
      "uri": "/veripy/feature/location",
      "tags": [
        {
          "line": 2,
          "name": "Test1"
        }
      ]
    }


@pytest.fixture
def feature_no_scenarios():
    return {
      "description": "<pre>A description of the test</pre>",
      "elements": [],
      "id": "id-123",
      "keyword": "Feature",
      "line": 1,
      "name": "veripy outputs a result",
      "status": "Passed",
      "uri": "/veripy/feature/location",
      "tags": [
        {
          "line": 2,
          "name": "Test1"
        }
      ]
    }


@pytest.fixture
def scenario_no_steps():
    return {

        'id': 'Test-Id-123',
        'name': "Scenario Name",
        'keyword': "Scenario",
        'status': "Passed",
        'passed': True,
        'doc_string': {
            "value": "A Description of the Scenario"
        },
        'line': 2,
        'location': "/scenario/file/location/",
        'type': "Scenario Type",
        'steps': [],
        "tags": [
          {
            "line": 2,
            "name": "Test1"
          }]
      }


@pytest.fixture
def step_no_doc():
    return {
        'name': "Step Name",
        'keyword': "Given",
        'status': "Passed",
        'result': {
            'status': 'Passed'
        },
        'line': 2,
        'location': "/scenario/file/location/",
        'step_type': "Given",
        'embeddings': [],
        "tags": [
          {
            "line": 2,
            "name": "Test1"
          }]
    }


@pytest.fixture
def given_step(step_no_doc):
    return {
        **step_no_doc,
        'doc_string': {
            "value": "some description"
        },
      }


@pytest.fixture
def step_with_messages(given_step):
    return {
        **given_step,
        'embeddings': [{
            'data': 'AAABBBB',
            'media': {
                'type': 'image/gif'
            }
        }],
        'result': {
            'status': 'failed',
            'duration': 2,
            'error_message': 'an error occurred'
        },
        'stored_value': 'A message from the step'
     }


@pytest.fixture
def step_skipped(given_step):
    return {
        **given_step,
        'result': {
            'status': 'skipped',
            'duration': 2,
        },
     }


@pytest.fixture
def step_undefined(given_step):
    return {
         **given_step,
         'result': {
             'status': 'undefined',
             'duration': 2,
         },
      }
