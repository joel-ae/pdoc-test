from enum import StrEnum
from functools import partial

from access_v2_blocks import SourceStructureBlock, SourceStructureBlockType
from access_v2_blocks import (fix_first_domestic_block, new_issue_block, no_supplier_fix_required_block, severity_block,
                              supervisor_comment_block, technician_comment_block)
from access_v2_enums import ReportKey, Severity
from access_v2_implications import Implication, validate_all_enums_accounted_for
from access_v2_sources import BaseTBMDSource, BaseTBMDSourceEventType


class TextGraphicsMark(StrEnum):
    """ Types of Text/Graphics Mark """
    copyright_marking = 'Copyright Marking'
    graphic_error = 'Graphic Error'
    text_misspelling_grammar = 'Text - Misspelling/Grammar'
    text_out_of_90_safety_on_all_sides = 'Text - Out of 90% Safety On All Sides'
    text_out_of_85_safety_on_left_and_right = 'Text - Out of 85% Safety On Left And Right'


text_graphics_mark_block = SourceStructureBlock(
    key='name',
    name='Type',
    type=SourceStructureBlockType.select,
    required=True,
    is_editable=True,
    options=[{'name': v} for v in sorted(TextGraphicsMark)]
    )

text_graphics_mark_high = [
    TextGraphicsMark.copyright_marking,
    TextGraphicsMark.graphic_error,
    TextGraphicsMark.text_misspelling_grammar,
    TextGraphicsMark.text_out_of_90_safety_on_all_sides,
    ]
text_graphics_mark_medium = [
    TextGraphicsMark.text_out_of_85_safety_on_left_and_right,
    ]

validate_all_enums_accounted_for(
    TextGraphicsMark,
    text_graphics_mark_high,
    text_graphics_mark_medium,
    )

text_graphics_mark_implications = [
    *Implication.generate('name', text_graphics_mark_high, Severity.high),
    *Implication.generate('name', text_graphics_mark_medium, Severity.medium),
    ]

text_graphics_mark_source = partial(
    BaseTBMDSource,
    name='Text/Graphics Mark',
    path=['Text - Graphics'],
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
        text_graphics_mark_block,
        technician_comment_block(is_editable=True),
        supervisor_comment_block(is_editable=False),
        severity_block(implications=text_graphics_mark_implications),
        new_issue_block,
        fix_first_domestic_block,
        no_supplier_fix_required_block,
        ]
    )
