from enum import StrEnum
from functools import partial

from access_v2_blocks import SourceStructureBlock, SourceStructureBlockType
from access_v2_sources import BaseTBMDSource, BaseTBMDSourceEventType
from access_v2_enums import ReportKey


class CreditsTextlessMark(StrEnum):
    """ Types of Credits/Textless Marks"""
    additional_content = 'Additional Content'
    bumpers = 'Bumpers'
    closing_credits = 'Closing Credits'
    credits_over_black = 'Credits Over Black'
    full_textless = 'Full Textless'
    graphics_material = 'Graphics Material'
    keyed_credits = 'Keyed Credits'
    opening_credits = 'Opening Credits'
    rolled_credits = 'Rolled Credits'
    snap_ins = 'Snap-ins'
    texted_tease_block = 'Texted Tease Block'
    textless_block = 'Textless Block'
    textless_tease_block = 'Textless Tease Block'


credits_textless_block = SourceStructureBlock(
    key='name',
    name='Type',
    type=SourceStructureBlockType.select,
    required=True,
    is_editable=True,
    options=[{'name': v} for v in sorted(CreditsTextlessMark)]
    )

credits_textless_source = partial(
    BaseTBMDSource,
    name='Credits/Textless Mark',
    path=['Credits/Textless Mark'],
    display_path=[],
    is_editable=True,
    is_creatable=True,
    is_deletable=True,
    event_type=BaseTBMDSourceEventType.timed,
    report_key=ReportKey.other_events,
    include_in_report='always',
    structure=[
        credits_textless_block
        ]
    )