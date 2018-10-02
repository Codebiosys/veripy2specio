step_no_doc = {
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

given_step = {
    **step_no_doc,
    'doc_string': {
        "value": "some description"
    },
  }

step_with_messages = {
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

step_skipped = {
    **given_step,
    'result': {
        'status': 'skipped',
        'duration': 2,
    },
 }

step_undefined = {
     **given_step,
     'result': {
         'status': 'undefined',
         'duration': 2,
     },
  }
