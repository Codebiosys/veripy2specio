from veripy2specio.constants import Status


class Message(object):
    _global_reference_number = 0

    def __init__(self, step, source):
        Message._global_reference_number += 1
        self.reference_number = Message._global_reference_number
        self.step = step
        self.source = source

    @property
    def id(self):
        return f'{self.step.id}_{self.reference_number}'

    @property
    def status(self):
        return Status(self.step.status)

    @property
    def passed(self):
        return self.status == Status.PASSED

    @property
    def is_deviation(self):
        return False

    def serialize():
        raise NotImplementedError


class ResultMessage(Message):

    @property
    def result(self):
        return self.source.get('stored_value')

    def serialize(self):
        return {
            # Required Message properties
            'id': self.id,
            'reference_number': self.reference_number,
            'is_deviation': self.is_deviation,
            'status': self.status.value,
            'passed': self.passed,
            # Required Result properties
            'result': self.result
        }


class ErrorMessage(Message):
    _global_error_number = 0

    def __init__(self, step, source):
        super().__init__(step, source)
        ErrorMessage._global_error_number += 1
        self.error_number = ErrorMessage._global_error_number

    @property
    def is_deviation(self):
        return Status(self.step.status) == Status.FAILED

    @property
    def expected(self):
        return self.step.name

    @property
    def actual(self):
        message = f'The test was {self.status.value}; '\
            'No message was supplied'
        if self.status == Status.SKIPPED:
            message = f'The test was {self.status.value}; '\
                'this is likely because a previous step failed.'
        if self.status == Status.UNDEFINED:
            message = f'The test was {self.status.value}; '\
                'This means the plan was not valid.'
        if 'error_message' in self.source.get('result', {}):
            message = self.source['result']['error_message']
        return message

    def serialize(self):
        return {
            # Required Message properties
            'id': self.id,
            'reference_number': self.reference_number,
            'status': self.status.value,
            'passed': self.passed,
            'is_deviation': self.is_deviation,
            # Required Error properties
            'error': {
                'expected': self.expected,
                'actual': self.actual,
                'error_number': self.error_number
            }
        }


class AttachmentMessage(Message):

    def __init__(self, step, source, embed):
        super().__init__(step, source)
        self.embed = embed

    @property
    def data(self):
        return self.embed['data']

    @property
    def media_type(self):
        return self.embed['media']['type']

    def serialize(self):
        return {
            # Required Message properties
            'id': self.id,
            'reference_number': self.reference_number,
            'is_deviation': self.is_deviation,
            'status': self.status.value,
            'passed': self.passed,
            # Required Attachment properties
            'attachment': {
                'data': self.data,
                'type': self.media_type
            }
        }
