from enum import StrEnum
from functools import partial

from access_v2_blocks import SourceStructureBlock, SourceStructureBlockType
from access_v2_blocks import (fix_first_domestic_block, new_issue_block, no_supplier_fix_required_block, severity_block,
                              supervisor_comment_block, technician_comment_block)
from access_v2_enums import ReportKey, Severity
from access_v2_implications import Implication, validate_all_enums_accounted_for
from access_v2_sources import BaseTBMDSource, BaseTBMDSourceEventType


class TimecodeFault(StrEnum):
    """ Types of Timecode Faults for TE Work Orders """
    timecode_error = 'Timecode Error'


timecode_fault_block = SourceStructureBlock(
    key='name',
    name='Type',
    type=SourceStructureBlockType.select,
    required=True,
    is_editable=True,
    options=[{'name': i} for i in sorted(TimecodeFault)],
    )

timecode_fault_high = [
    TimecodeFault.timecode_error,
    ]

validate_all_enums_accounted_for(
    TimecodeFault,
    timecode_fault_high,
    )

timecode_fault_implications = [
    *Implication.generate('name', timecode_fault_high, Severity.high),
    ]

timecode_fault_source = partial(
    BaseTBMDSource,
    name='Timecode Fault',
    path=['Timecode'],
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
        timecode_fault_block,
        technician_comment_block(is_editable=True),
        supervisor_comment_block(is_editable=False),
        severity_block(implications=timecode_fault_implications),
        new_issue_block,
        fix_first_domestic_block,
        no_supplier_fix_required_block,
        ]
    )
