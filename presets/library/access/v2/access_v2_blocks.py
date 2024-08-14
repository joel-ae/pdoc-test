from __future__ import annotations

from enum import StrEnum
from functools import partial
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

from access_v2_enums import SeverityOption, ReviewStatusOption
from access_v2_implications import Implication


class SourceStructureBlockType(StrEnum):
    """ Allowed values for `type` of SourceStructureBlock """
    textarea = 'textarea'
    select = 'select'
    boolean = 'boolean'


class SourceStructureBlock(BaseModel):
    """ Structure Block for use with BaseTBMDSource model """
    key: Optional[str] = Field(default=None)
    name: str
    short_name: Optional[str] = Field(default=None, serialization_alias='shortName')
    template: Optional[List[str]] = Field(default=None)
    type: SourceStructureBlockType = Field(default=SourceStructureBlockType.textarea)
    metadata_path: List[str] = Field(default_factory=list, serialization_alias='metadataPath')
    required: Optional[bool] = None
    is_editable: Optional[bool] = Field(default=None, serialization_alias='isEditable')
    options: Optional[List[SeverityOption | ReviewStatusOption | Dict[str, Any]]] = None
    implications: Optional[List[Implication]] = None

    @field_validator('implications')
    @classmethod
    def sort_implications(cls, implications: Optional[List[Implication]]) -> Optional[List[Implication]]:
        """ Sort the list of implications

        :param implications: list of Implications
        :return: Sorted list of implications
        """
        if not implications:
            return implications
        return sorted(implications, key=Implication.sort_key)


technician_comment_block = partial(
    SourceStructureBlock,
    key='message',
    name='Technician Comments',
    type=SourceStructureBlockType.textarea,
    metadata_path=[],
    required=False,
    )

supervisor_comment_block = partial(
    SourceStructureBlock,
    key='supervisor',
    name='Supervisor Comments',
    type=SourceStructureBlockType.textarea,
    metadata_path=[],
    required=False,
    )

severity_block = partial(
    SourceStructureBlock,
    key='severity',
    name='Severity',
    type=SourceStructureBlockType.select,
    required=True,
    is_editable=True,
    options=[
        SeverityOption.high,
        SeverityOption.medium,
        SeverityOption.low,
        SeverityOption.fyi,
        ]
    )

new_issue_block = SourceStructureBlock(
    key='new_issue',
    name='New Issue',
    type=SourceStructureBlockType.boolean,
    )

fix_first_domestic_block = SourceStructureBlock(
    key='fix_first_domestic',
    name='Fix for First Domestic',
    type=SourceStructureBlockType.boolean,
    implications=Implication.generate(
        'no_supplier_fix_required',
        [True],
        False,
        )
    )

no_supplier_fix_required_block = SourceStructureBlock(
    key='no_supplier_fix_required',
    name='No Supplier Fix Required',
    type=SourceStructureBlockType.boolean,
    implications=Implication.generate(
        'fix_first_domestic',
        [True],
        False,
        )
    )

