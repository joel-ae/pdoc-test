from enum import StrEnum
from functools import partial

from access_v2_blocks import SourceStructureBlock, SourceStructureBlockType
from access_v2_blocks import (fix_first_domestic_block, new_issue_block, no_supplier_fix_required_block, severity_block,
                              supervisor_comment_block, technician_comment_block)
from access_v2_enums import ReportKey, Severity
from access_v2_implications import Implication, validate_all_enums_accounted_for
from access_v2_sources import BaseTBMDSource, BaseTBMDSourceEventType


class TextlessMark(StrEnum):
    """ Types of Textless Marks/Faults """
    back_plate = 'Back Plate'
    generic_textless_error = 'Generic Textless Error'
    missing_textless_element_clean_cover = 'Missing Textless Element/Clean Cover'
    missing_textless_padding = 'Missing Textless Padding'
    text_present = 'Text Present'
    textless_log_error = 'Textless Log Error'


textless_mark_block = SourceStructureBlock(
    key='name',
    name='Type',
    type=SourceStructureBlockType.select,
    required=True,
    is_editable=True,
    options=[{'name': v} for v in sorted(TextlessMark)],
    )

textless_mark_high = [
    TextlessMark.back_plate,
    TextlessMark.missing_textless_element_clean_cover,
    TextlessMark.text_present,
    ]
textless_mark_medium = [
    TextlessMark.generic_textless_error,
    TextlessMark.missing_textless_padding,
    TextlessMark.textless_log_error,
    ]

validate_all_enums_accounted_for(
    TextlessMark,
    textless_mark_high,
    textless_mark_medium,
    )

textless_mark_implications = [
    *Implication.generate('name', textless_mark_high, Severity.high),
    *Implication.generate('name', textless_mark_medium, Severity.medium),
    ]

textless_mark_source = partial(
    BaseTBMDSource,
    name='Textless Mark',
    path=['Textless'],
    display_path=[],
    is_editable=True,
    is_creatable=True,
    is_deletable=True,
    event_type=BaseTBMDSourceEventType.timed,
    report_key=ReportKey.manual_faults,
    include_in_report='always',
    promote_on_create=True,
    select_on_create=True,
    structure=[
        textless_mark_block,
        technician_comment_block(is_editable=True),
        supervisor_comment_block(is_editable=False),
        severity_block(implications=textless_mark_implications),
        new_issue_block,
        fix_first_domestic_block,
        no_supplier_fix_required_block,
        ]
    )
