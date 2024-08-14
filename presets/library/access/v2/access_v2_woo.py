from enum import Enum, StrEnum
from functools import partial

from access_v2_blocks import SourceStructureBlock, SourceStructureBlockType
from access_v2_enums import ReportKey
from access_v2_sources import BaseTBMDSource, BaseTBMDSourceEventType


class WindowOfOpportunity(StrEnum):
    """ Types of Windows of Opportunity """
    animated_bug = 'Animated Bug'
    custom_logo = 'Custom Logo'
    in_program_message = 'In-Program Message'
    virtual_overlay = 'Virtual Overlay'


woo_name_block = SourceStructureBlock(
    key='name',
    name='Type',
    type=SourceStructureBlockType.select,
    required=True,
    is_editable=True,
    options=[{'name': v} for v in sorted(WindowOfOpportunity)],
    )

notes_block = SourceStructureBlock(
    key='notes',
    name='Notes',
    metadata_path=['notes'],
    type=SourceStructureBlockType.textarea
    )

woo_source = partial(
    BaseTBMDSource,
    name='Window of Opportunity',
    path=['Window of Opportunity'],
    display_path=[],
    is_editable=True,
    is_creatable=True,
    is_deletable=True,
    event_type=BaseTBMDSourceEventType.timed,
    report_key=ReportKey.woo_events,
    include_in_report='always',
    structure=[
        woo_name_block,
        notes_block,
        ]
    )
