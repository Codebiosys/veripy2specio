# Base Components

# app_base = {
#     'type': 'object',
#     'properties': {
#         'name': 'string',
#         'version': 'string',
#     },
#     'required': [
#         'name'
#     ]
# }

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
        'value': {'type': 'number'},
        'last': {'type': 'boolean'},
    },
    'required': [
        'value',
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

step_message = {
    'type': 'object',
    'properties': {
        'type': {'type': 'string'},
        'reference_number': {'type': 'number'},
        'content': {'type': 'string'},
        'attachment': attachment
    },
    'required': [
        'type',
        'reference_number',
    ]
}

step = {
    'type': 'object',
    'properties': {
        **specio_base.get('properties'),
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
        }
    },
    'required': [
        'given_when',
        'then',
        'messages',
    ],
}

scenario = {
    'type': 'object',
    'properties': {
        **specio_base.get('properties'),
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
        'number',
        'steps',
        'tags'
    ],
}

feature = {
    'type': 'object',
    'properties': {
        **specio_base.get('properties'),
        'description': {'type': 'string'},
        'scenarios': {
            'type': 'array',
            'items': scenario,
        },
        'tags': {
            'type': 'array',
            'items': tag,
        },
        'scenario_tags': {
            'type': 'array',
            'items': tag,
        }
    },
    'required': [
        *specio_base.get('required'),
        'scenarios',
        'tags',
        'scenario_tags'
    ],
}

# Report Schema

# specio = {
#     'type': 'object',
#     'properties': {
#         'os': app_base,
#         'browser': app_base,
#         'user': 'string',
#         'report_date': 'string',
#         'specio_version': 'string'
#     }
# }
#
# application = app_base
#
# organization = {
#     'type': 'object',
#     'required': [
#         'name'
#     ],
#     'properties': {
#         'name': {
#             'type': 'string'
#         },
#         'logo': {
#             'type': 'string'
#         }
#     }
# }

# Overall Schema
schema = {
    'type': 'object',
    'required': [
        'features',
        # 'organization'
    ],
    'properties': {
        # 'organization': organization,
        # 'application': application,
        # 'specio': specio,
        'features': {
            'type': 'array',
            'items': feature,
        },
    },
}
