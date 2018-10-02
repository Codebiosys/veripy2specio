import re
from veripy2specio.constants import Status
from .base import SpecioBase
from .message import ErrorMessage, ResultMessage, AttachmentMessage


class Step(SpecioBase):
    def __init__(self, source, scenario_id):
        super().__init__(source)
        self.messages = []
        self.scenario_id = scenario_id
        self._populate_from_source(source)

    @property
    def id(self):
        return re.sub('\W',  '_', f'{self.scenario_id}_{self.source["line"]}')

    @property
    def status(self):
        return Status(self.source['result']['status'])

    @property
    def note(self):
        return self.source.get('doc_string', {}).get('value', None)

    def references(self):
        if len(self.messages):
            if len(self.messages) > 1:
                for message in self.messages[:len(self.messages)-1]:
                    yield {
                            'id': message.id,
                            'reference_number': message.reference_number,
                            'last': False
                        }
            yield {
                    'id': self.messages[-1].id,
                    'reference_number': self.messages[-1].reference_number,
                    'last': True
                 }

    def _populate_from_source(self, source):
        if 'stored_value' in source:
            self.messages.append(ResultMessage(self, source))

        if Status(source.get('result').get('status')) != Status.PASSED:
            self.messages.append(ErrorMessage(self, source))

        for embed in source.get('embeddings', []):
            self.messages.append(AttachmentMessage(self, source, embed))

    def serialize(self):
        serialized = {
            # Required Base properties
            'id': self.id,
            'name': self.name,
            'keyword': self.keyword.value,
            'status': self.status.value,
            'passed': self.passed,
            # Optional List properties
            'references': [reference for reference in self.references()],
        }
        if self.note:
            serialized['note'] = self.note
        return serialized


class StepGroup(object):

    def __init__(self):
        self.given_when = []
        self.then = []

    def add_step(self, step, switch):
        if switch == "GIVEN_WHEN":
            self.given_when.append(step)
        elif switch == "THEN":
            self.then.append(step)
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
        return self.status_from_children([*self.given_when, *self.then])

    @property
    def passed(self):
        return self.status == Status.PASSED

    @property
    def messages(self):
        for step in self.given_when:
            for message in step.messages:
                yield message
        for step in self.then:
            for message in step.messages:
                yield message

    def serialize(self):
        return {
            # Required Step Group fields
            'given_when': [step.serialize() for step in self.given_when],
            'then': [step.serialize() for step in self.then],
            'messages': [message.serialize() for message in self.messages],
            'status': self.status.value,
            'passed': self.passed,
        }
