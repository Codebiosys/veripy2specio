from veripy2specio.constants import Keyword, Status


class SpecioBase(object):

    def __init__(self, source):
        self.source = source

    @property
    def keyword(self):
        return Keyword(self.source.get('keyword'))

    @property
    def name(self):
        return self.source.get('name')

    @property
    def passed(self):
        return self.status == Status.PASSED

    def status(self):
        raise NotImplementedError

    def tags_from_elements(self, elements):
        tags = sorted(set(
            tag['name']
            for element in elements
            for tag in element.get('tags', [])
            if tag.get('name') and tag['name'] not in ['setup', 'teardown']
        ))
        if tags:
            if len(tags) > 1:
                for tag in tags[:len(tags)-1]:
                    yield {'name': tag, 'last': False}
            yield {'name': tags[-1], 'last': True}

    def status_from_children(self, children):
        statuses = set(child.status for child in children)
        if len(children) > 0 and all(status == Status.PASSED for status in statuses):
            return Status.PASSED
        elif any(status == Status.FAILED for status in statuses):
            return Status.FAILED
        elif any(status == Status.UNDEFINED for status in statuses):
            return Status.UNDEFINED
        return Status.SKIPPED

    def serialize(self):
        raise NotImplementedError
