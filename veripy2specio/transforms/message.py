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

    def serialize():  # pragma: no cover
        raise NotImplementedError


class DeviationMessage(object):
    _global_deviation_number = 0

    def __init__(self, steps, scenario_id):
        self.steps = steps
        self.errors = []
        self.has_skipped = False
        self.scenario_id = scenario_id
        self._populate_from_steps(steps)
        DeviationMessage._global_deviation_number += 1
        self.deviation_number = DeviationMessage._global_deviation_number

    @property
    def id(self):
        return f'deviation_{self.scenario_id}_{self.deviation_number}'

    @property
    def status(self):
        return self._status

    @property
    def passed(self):
        return self._status == Status.PASSED

    def _populate_from_steps(self, steps):
        self._status = Status.SKIPPED
        for step in steps:
            if step.status != Status.PASSED:
                error = {
                    'expected': step.name,
                    'actual': step.result,
                    'status': step.status.value
                }
                if hasattr(step.attachment, 'id'):
                    error['attachment_reference_id'] = step.attachment.id

                if step.status == Status.SKIPPED and self.has_skipped:
                    continue
                elif step.status == Status.SKIPPED:
                    self.has_skipped = True

                if self._status != Status.FAILED:
                    self._status = step.status

                self.errors.append(error)

    def serialize(self):
        return {
            # Required Message properties
            'id': self.id,
            'deviation_number': self.deviation_number,
            'status': self.status.value,
            'passed': self.passed,
            # Required Error properties
            'errors': [error for error in self.errors]
            }


class ErrorMessage(Message):
    _global_error_number = 0

    def __init__(self, step, source):
        super().__init__(step, source)
        ErrorMessage._global_error_number += 1
        self.error_number = ErrorMessage._global_error_number

    @property
    def expected(self):
        return self.step.name

    @property
    def actual(self):
        message = ''
        if 'error_message' in self.source.get('result', {}):
            message = self.source['result']['error_message']
        elif self.status == Status.SKIPPED:
            message = "This is likely because a previous step failed."
        elif self.status == Status.UNDEFINED:
            message = "This means the plan was not valid."

        return message

    def serialize(self):
        return {
            # Required Message properties
            'id': self.id,
            'reference_number': self.reference_number,
            'status': self.status.value,
            'passed': self.passed,
            # Required Error properties
            'error': {
                'expected': self.expected,
                'actual': self.actual,
                'error_number': self.error_number
            }
        }


class AttachmentMessage(Message):
    _global_figure_number = 0

    def __init__(self, step, source, embed):
        super().__init__(step, source)
        AttachmentMessage._global_figure_number += 1
        self.figure_number = AttachmentMessage._global_figure_number
        self.embed = embed

    @property
    def id(self):
        return f'figure_{self.step.id}_{self.figure_number}'

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
            'figure_number': self.figure_number,
            'status': self.status.value,
            'passed': self.passed,
            # Required Attachment properties
            'data': self.data,
            'type': self.media_type
        }
