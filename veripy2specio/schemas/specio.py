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
        'status',
        'passed',
    ],
    'properties': {
        'id': {'type': 'string'},
        'status': {'type': 'string'},
        'passed': {'type': 'boolean'},
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

# Components
attachment = {
    'type': 'object',
    'required': [
        *message_base.get('required'),
        'data',
        'type'
    ],
    'properties': {
        **message_base.get('properties'),
        'data': {'type': 'string'},
        'type': {'type': 'string'}
    },
}

error = {
    'type': 'object',
    'required': [
        'expected',
        'actual',
    ],
    'properties': {
        'expected': {'type': 'string'},
        'actual': {'type': 'string'},
    },
}

deviation = {
    'type': 'object',
    'required': [
        *message_base.get('properties'),
        'deviation_number',
        'errors',
    ],
    'properties': {
        **message_base.get('properties'),
        'errors': {
            'type': 'array',
            'items': error,
        },
        'deviation_number': {'type': 'number'}
    },
}


error = {
    'type': 'object',
    'required': [
        *message_base.get('properties'),
        'error_number',
        'expected',
        'actual',
    ],
    'properties': {
        **message_base.get('properties'),
        'expected': {'type': 'string'},
        'actual': {'type': 'string'},
        'error_number': {'type': 'number'}
    },
}

instruction = {
    'type': 'object',
    'properties': {
        **specio_base.get('properties'),
        'note': {'type': 'string'},
        'error_reference_id': {'type': 'string'}
    },
    'required': [
        *specio_base.get('required'),
    ],
}

result = {
    'type': 'object',
    'properties': {
        **specio_base.get('properties'),
        'result': {'type': 'string'},
        'error_reference_id': {'type': 'string'},
        'attachment_reference_id': {'type': 'string'},
        'note': {'type': 'string'},
    },
    'required': [
        *specio_base.get('required'),
        'result'
    ],
}

instructions_results = {
    'type': 'object',
    'properties': {
        'instructions': {
            'type': 'array',
            'items': instruction,
        },

        'results': {
            'type': 'array',
            'items': result,
        },
        'attachments': {
            'type': 'array',
            'items': attachment,
        },
        'status': {'type': 'string'},
        'passed': {'type': 'boolean'}
    },
    'required': [
        'instructions',
        'results',
        'passed',
        'status'
    ],
}

scenario = {
    'type': 'object',
    'properties': {
        **specio_base.get('properties'),
        'scenario_name': {'type': 'string'},
        'scenario_description': {'type': 'string'},
        'scenario_number': {'type': 'number'},
        'instructions_results': {
            'type': 'array',
            'items': instructions_results,
        },
        'tags': {
            'type': 'array',
            'items': tag,
        },
        'deviation': deviation,
        'scenario_table': {
            'type': 'object',
            'properties': {
                'headers': {
                    'type': 'array',
                },
                'rows': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'cells': {
                                'type': 'array'
                            }
                        }
                    }
                },
            },
        },
    },
    'required': [
        *specio_base.get('required'),
        'scenario_name',
        'scenario_number',
        'instructions_results',
        'tags'
    ],
}

prerequisite_scenario = {
    'type': 'object',
    'properties': {
            'id': {'type': 'string'},
            'name': {'type': 'string'},
            'keyword': {'type': 'string'},

        'scenario_name': {'type': 'string'},
        'scenario_description': {'type': 'string'},
        'scenario_number': {'type': 'number'},
        'is_setup': {'type': 'boolean'},
        'is_teardown': {'type': 'boolean'},
        'tags': {
            'type': 'array',
            'items': tag,
            },
        'table': {
            'type': 'object',
            'properties': {
                'headers': {
                    'type': 'array',
                },
                'rows': {
                    'type': 'array',
                },
            },
            },
    },
    'required': [
        'id',
        'name',
        'keyword',
        'scenario_name',
        'scenario_number',
    ],
}

prerequisite_script = {
    'type': 'object',
    'properties': {
        'id': {'type': 'string'},
        'name': {'type': 'string'},
        'keyword': {'type': 'string'},
        'feature_name': {'type': 'string'},
        'description': {'type': 'string'},
        'has_scenarios': {'type': 'boolean'},
        'feature_number': {'type': 'number'},
        'has_setup': {'type': 'boolean'},
        'has_teardown': {'type': 'boolean'},
        'scenarios': {
            'type': 'array',
            'items': prerequisite_scenario,
        },
    },
    'required': [
        'id',
        'name',
        'keyword',
        'feature_name',
        'scenarios',
        'feature_number'
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
        'skipped_scenarios': {
            'type': 'array',
            'items': scenario,
        },
        'has_skipped_scenarios': {'type': 'boolean'},
        'prerequisites': {
            'type': 'array',
            'items': scenario,
        },
        'has_prerequisites': {'type': 'boolean'},
        'prerequisite_scripts': {
            'type': 'array',
            'items': prerequisite_script,
        },
        'has_prerequisite_scripts': {'type': 'boolean'},
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
        'setup_scripts': {
            'type': 'array',
            'items': prerequisite_script,
        },
        'defines': {
            'type': 'array',
            'items': feature,
        },
        'features': {
            'type': 'array',
            'items': feature,
        },
    },
}
