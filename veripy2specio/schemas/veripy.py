# Components

tag = {
    'type': 'object',
    'properties': {
        'line': {'type': 'integer'},
        'name': {'type': 'string'}
    },
    'required': [
        'name'
    ]
}

media = {
    'type': 'object',
    'properties': {
        'type': {'type': 'string'}
    },
    'required': [
        'type'
    ]
}

embedding = {
    'type': 'object',
    'properties': {
        'data': {'type': 'string'},
        'media': media
    },
    'required': [
        'data',
        'media'
    ]
}

result = {
    'type': 'object',
    'properties': {
        'duration': {'type': 'integer'},
        'status': {'type': 'string'},
        'error_message': {'type': 'string'}
    },
    'required': [
        'duration',
        'status'
    ]
}

match = {
    'type': 'object',
    'properties': {
        'location': {
            'type': 'string'
        }
    },
    'required': [
        'location'
    ]
}

step_docstring = {
    'type': 'object',
    'properties': {
        'line': {'type': 'integer'},
        'value': {'type': 'string'}
    },
    'required': [
        'value'
    ]
}

step = {
    'type': 'object',
    'properties': {
        'keyword': {'type': 'string'},
        'line': {'type': 'integer'},
        'name': {'type': 'string'},
        'match': match,
        'result': result,
        'embeddings': {
          'type': 'array',
          'items': embedding
        },
        'step_type': {'type': 'string'},
        'doc_string': step_docstring,
        'table': {
            'type': 'object',
            'properties': {
                'rows': {
                    'type': 'array',
                },
            },
        },
    },
    'required': [
        'keyword',
        'line',
        'name',
        'result',
        'step_type'
    ]
}

scenario = {
    'type': 'object',
    'properties': {
        'description': {'type': 'string'},
        'id': {'type': 'string'},
        'keyword': {'type': 'string'},
        'line': {'type': 'integer'},
        'location': {'type': 'string'},
        'name': {'type': 'string'},
        'type': {'type': 'string'},
        'steps': {
            'type': 'array',
            'items': step,
        },
        'tags': {
            'type': 'array',
            'items': tag
        },
    },
    'required': [
        'keyword',
        'location',
        'name',
        'steps',
        'type'
    ]
}

feature = {
    'type': 'object',
    'properties': {
        'description': {'type': 'string'},
        'elements': {
            'type': 'array',
            'items': scenario
        },
        'id': {'type': 'string'},
        'keyword': {'type': 'string'},
        'line': {'type': 'integer'},
        'name': {'type': 'string'},
        'status': {'type': 'string'},
        'uri': {'type': 'string'},
        'tags': {
            'type': 'array',
            'items': tag
        },
    },
    'required': [
        'id',
        'keyword',
        'line',
        'name',
        'status',
        'tags',
        'uri'
    ]
}

# Overall Schema

schema = {
    'type': 'array',
    'items': feature,
}
