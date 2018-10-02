# Base Components

specio_base = {
    'properties': {
        'id': {'type': 'string'},
        'name': {'type': 'string'},
        'keyword': {'type': 'string'},
        'status': {'type': 'string'},
        'passed': {'type': 'boolean'},
    },
    'required': [
        'id',
        'name',
        'keyword',
        'status',
        'passed',
    ]
}

message_base = {
    'type': 'object',
    'required': [
        'id',
        'reference_number',
        'status',
        'passed',
        'is_deviation',
    ],
    'properties': {
        'id': {'type': 'string'},
        'reference_number': {'type': 'string'},
        'status': {'type': 'string'},
        'passed': {'type': 'boolean'},
        'is_deviation': {'type': 'boolean'},
    },
}

tag = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'last': {'type': 'boolean'},
    },
    'required': [
        'name',
        'last',
    ],
}

reference = {
    'type': 'object',
    'properties': {
        'id': {'type': 'string'},
        'reference_number': {'type': 'number'},
        'last': {'type': 'boolean'},
    },
    'required': [
        'id',
        'reference_number',
        'last',
    ],
}

# Components
attachment = {
    'type': 'object',
    'required': [
        'data',
        'type'
    ],
    'properties': {
        'data': {'type': 'string'},
        'type': {'type': 'string'}
    },
}

error = {
    'type': 'object',
    'required': [
        'error_number',
        'expected',
        'actual',
    ],
    'properties': {
        'expected': {'type': 'string'},
        'actual': {'type': 'string'},
        'error_number': {'type': 'number'}
    },
}

step_message = {
    'type': 'object',
    'properties': {
        'id': {'type': 'string'},
        'reference_number': {'type': 'number'},
        'is_deviation': {'type': 'boolean'},
        'status': {'type': 'string'},
        'passed': {'type': 'boolean'},
        'attachment': attachment,
        'error': error,
        'result': {'type': 'string'}
    },
    'required': [
        'id',
        'reference_number',
        'is_deviation',
        'status',
        'passed'
    ]
}

step = {
    'type': 'object',
    'properties': {
        **specio_base.get('properties'),
        'note': {'type': 'string'},
        'references': {
            'type': 'array',
            'items': reference
            },
    },
    'required': [
        *specio_base.get('required'),
    ],
}

step_group = {
    'type': 'object',
    'properties': {
        'given_when': {
            'type': 'array',
            'items': step,
        },
        'then': {
            'type': 'array',
            'items': step,
        },
        'messages': {
            'type': 'array',
            'items': step_message,
        },
        'status': {'type': 'string'},
        'passed': {'type': 'boolean'}
    },
    'required': [
        'given_when',
        'then',
        'messages',
        'passed',
        'status'
    ],
}

scenario = {
    'type': 'object',
    'properties': {
        **specio_base.get('properties'),
        'scenario_name': {'type': 'string'},
        'description': {'type': 'string'},
        'number': {'type': 'number'},
        'steps': {
            'type': 'array',
            'items': step_group,
        },
        'tags': {
            'type': 'array',
            'items': tag,
        },
    },
    'required': [
        *specio_base.get('required'),
        'scenario_name',
        'number',
        'steps',
        'tags'
    ],
}

feature = {
    'type': 'object',
    'properties': {
        **specio_base.get('properties'),
        'feature_name': {'type': 'string'},
        'description': {'type': 'string'},
        'scenarios': {
            'type': 'array',
            'items': scenario,
        },
        'has_scenarios': {'type': 'boolean'},
        'prerequisites': {
            'type': 'array',
            'items': scenario,
        },
        'has_prerequisites': {'type': 'boolean'},
        'cleanup': {
            'type': 'array',
            'items': scenario,
        },
        'has_cleanup': {'type': 'boolean'},
        'tags': {
            'type': 'array',
            'items': tag,
        },
        'scenario_tags': {
            'type': 'array',
            'items': tag,
        },
        'feature_number': {'type': 'number'}
    },
    'required': [
        *specio_base.get('required'),
        'feature_name',
        'scenarios',
        'tags',
        'scenario_tags',
        'feature_number'
    ],
}

# Report Schema


# Overall Schema
schema = {
    'type': 'object',
    'required': [
        'features',
        'all_passed',
    ],
    'properties': {
        'all_passed': {'type': 'boolean'},
        'features': {
            'type': 'array',
            'items': feature,
        },
    },
}
