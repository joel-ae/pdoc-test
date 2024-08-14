from functools import partial

from access_v2_blocks import SourceStructureBlock, SourceStructureBlockType
from access_v2_blocks import (fix_first_domestic_block, new_issue_block, no_supplier_fix_required_block, severity_block,
                              supervisor_comment_block)
from access_v2_sources import BaseTBMDSource, BaseTBMDSourceEventType
from access_v2_enums import ReportKey


name_block = SourceStructureBlock(
    key='name',
    name='Name',
    type=SourceStructureBlockType.textarea,
    metadata_path=[],
    required=True,
    is_editable=False,
    )

baton_message_block = SourceStructureBlock(
    key='message',
    name='Baton Details',
    type=SourceStructureBlockType.textarea,
    metadata_path=[],
    required=False,
    is_editable=False,
    )

baton_technician_comment_block = partial(
    SourceStructureBlock,
    key='tech',
    name='Technician Comments',
    type=SourceStructureBlockType.textarea,
    metadata_path=[],
    required=False,
    )

provider_qc_events_source = partial(
    BaseTBMDSource,
    name='Provider QC Events',
    path=[],
    display_path=['Provider QC Events'],
    report_key=ReportKey.faults,
    event_type=BaseTBMDSourceEventType.timed,
    is_editable=True,
    is_creatable=False,
    is_deletable=False,
    structure=[
        name_block,
        baton_message_block,
        baton_technician_comment_block(is_editable=True),
        supervisor_comment_block(is_editable=False),
        severity_block(),
        new_issue_block,
        fix_first_domestic_block,
        no_supplier_fix_required_block,
        ]
    )
