import re
from veripy2specio.constants import Status
from .base import SpecioBase
from .message import AttachmentMessage


class Step(SpecioBase):
    def __init__(self, source, scenario_id):
        super().__init__(source)
        self.scenario_id = scenario_id
        self._error_message = None
        self._attachment = None
        self._populate_from_source(source)

    @property
    def id(self):
        return re.sub('\W',  '_', f'{self.scenario_id}_{self.source["line"]}')

    @property
    def status(self):
        return Status(self.source['result']['status'])

    @property
    def stored_value(self):
        return self.source.get('stored_value', None)

    @property
    def note(self):
        return self.source.get('doc_string', {}).get('value', None)

    def _populate_from_source(self, source):
        for embed in source.get('embeddings', []):
            self._attachment = AttachmentMessage(self, source, embed)

    @property
    def result(self):
        if self.status != Status.PASSED:
            message = 'Unable to complete instructions.'
            if 'error_message' in self.source.get('result', {}):
                message = self.source['result']['error_message'].replace('Assertion Failed: ', '')
            elif self.status == Status.SKIPPED:
                message = "Unable to complete instructions. " \
                    "Either a previous instruction failed, or the test case" \
                    " configuration requires manual intervention."
            elif self.status == Status.UNDEFINED:
                message = "Unable to complete instructions. "\
                    "The test case is not valid."
            else:
                message = 'Unable to complete instructions.'
            if self._attachment:
                message += f" Figure {self.attachment.figure_number}."
            return message

        elif self.stored_value:
            return self.stored_value

        elif self._attachment:
            return f"Figure {self.attachment.figure_number}."
        return self.name

    @property
    def attachment(self):
        return self._attachment

    @property
    def error(self):
        return self._error_message

    def serialize_instruction(self):
        serialized = {
            # Required Base properties
            'id': self.id,
            'name': self.name,
            'keyword': self.keyword.value,
            'status': self.status.value,
            'passed': self.passed,
            # Optional List properties
        }
        if self.note:
            serialized['note'] = self.note
        return serialized

    def serialize_result(self):
        serialized = {
            # Required Base properties
            'id': self.id,
            'name': self.name,
            'keyword': self.keyword.value,
            'status': self.status.value,
            'passed': self.passed,
            # Optional List properties
            'result': self.result,
        }
        if self.note:
            serialized['note'] = self.note
        if self.attachment:
            serialized['attachment_reference_id'] = self.attachment.id
        return serialized


class InstructionsResults(object):

    def __init__(self):
        self.instructions = []
        self.results = []

    def add_step(self, step, switch):
        if switch == "GIVEN_WHEN":
            self.instructions.append(step)
        elif switch == "THEN":
            self.results.append(step)
        else:
            raise KeyError(f'StepGroup does not have a {switch}')

    def status_from_children(self, children):
        statuses = set(child.status for child in children)
        if all(status == Status.PASSED for status in statuses):
            return Status.PASSED
        elif any(status == Status.FAILED for status in statuses):
            return Status.FAILED
        return Status.SKIPPED

    @property
    def status(self):
        return self.status_from_children([*self.instructions, *self.results])

    @property
    def passed(self):
        return self.status == Status.PASSED

    @property
    def attachments(self):
        for step in [*self.instructions, *self.results]:
            if step.attachment:
                yield step.attachment

    def serialize(self):
        return {
            # Required Step Group fields
            'instructions': [
                step.serialize_instruction()
                for step in self.instructions
            ],
            'results': [
                step.serialize_result()
                for step in self.results
            ],
            'attachments': [
                attachment.serialize()
                for attachment in self.attachments
            ],
            'status': self.status.value,
            'passed': self.passed,
        }
