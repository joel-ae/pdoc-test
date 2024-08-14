from enum import StrEnum
from typing import Any, List

from pydantic import BaseModel, Field

from access_v2_enums import Severity


class Implication(BaseModel):
    """ Model representing an implication for options in a SourceStructureBlock """
    when: List[str | bool]
    set_value: str | bool = Field(serialization_alias='setValue')

    @classmethod
    def sort_key(cls, implication: 'Implication') -> str:
        """ Sort implication based on field value

        :param implication: Implication to sort
        :return: field value in the implication
        """
        return implication.when[2]

    @classmethod
    def generate(cls, field_name: str, field_values: List[Any], set_value: Severity | bool) -> List['Implication']:
        """ Generate a list of Implication objects

        :param field_name: Name of the field to match against
        :param field_values: Field value to match
        :param set_value: Value to set this field to
        :return: List of Implications
        """
        implications = []
        for value in field_values:
            implications.append(
                Implication(
                    set_value=set_value,
                    when=[
                        '${form.' + field_name + '}',
                        '=',
                        value
                        ]
                    )
                )
        return implications


class EnumNotAccountedForException(Exception):
    """ Custom exception to ensure that all options are covered """
    ...


def validate_all_enums_accounted_for(enum_class: StrEnum, *args: List[Any]) -> None:
    """ Ensure that all the enum values are contained within the rest of the lists in args

    :param enum_class: Enum Class to validate
    :param args: List of lists of values of the enum class
    :raises EnumNotAccountedForException: Values aren't accounted for
    """
    total = []
    [total.extend(lst) for lst in args]
    missing = []
    for enum in enum_class:
        if enum not in total:
            missing.append(enum)
    if missing:
        msg = f'Missing Enum values: {missing=}'
        raise EnumNotAccountedForException(msg)
