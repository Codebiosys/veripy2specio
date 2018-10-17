from enum import Enum


class CaseInsensitiveEnum(Enum):
    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value.lower() == value.lower():
                return member


class Status(CaseInsensitiveEnum):
    PASSED = 'Passed'
    FAILED = 'Failed'
    SKIPPED = 'Skipped'
    UNDEFINED = 'Undefined'


class Keyword(CaseInsensitiveEnum):
    #  Feature Type Keywords
    FEATURE = 'Feature'
    #  Scenario Type Keywords
    BACKGROUND = 'Background'
    SCENARIO_OUTLINE = 'Scenario Outline'
    SCENARIO = 'Scenario'

    #  Step Type Keywords
    WHEN = 'When'
    THEN = 'Then'
    GIVEN = 'Given'
    AND = 'And'
    BUT = 'But'
