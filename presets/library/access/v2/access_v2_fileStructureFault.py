from enum import StrEnum
from functools import partial

from access_v2_blocks import SourceStructureBlock, SourceStructureBlockType
from access_v2_blocks import (fix_first_domestic_block, new_issue_block, no_supplier_fix_required_block, severity_block,
                              supervisor_comment_block, technician_comment_block)
from access_v2_enums import Severity
from access_v2_implications import Implication, validate_all_enums_accounted_for
from access_v2_sources import BaseTBMDSource, BaseTBMDSourceEventType


class FileStructureFaultType(StrEnum):
    """ Types of File Structure Faults """
    black_slug_out_of_spec = 'Black Slug Out of Spec'
    file_format_error = 'File Format Error'
    file_structure_error = 'File Structure Error'


file_structure_fault_name_block = SourceStructureBlock(
    key='name',
    name='Type',
    type=SourceStructureBlockType.select,
    required=True,
    is_editable=True,
    options=[{'name': v} for v in sorted(FileStructureFaultType)],
    )

file_structure_fault_high = [
    FileStructureFaultType.black_slug_out_of_spec,
    FileStructureFaultType.file_format_error,
    FileStructureFaultType.file_structure_error,
    ]

validate_all_enums_accounted_for(
    FileStructureFaultType,
    file_structure_fault_high,
    )

file_structure_fault_implications = [
    *Implication.generate('name', file_structure_fault_high, Severity.high)
    ]

file_structure_fault_source = partial(
    BaseTBMDSource,
    name='File Structure Fault',
    file_label='Broadcast ManualFaults',
    path=['File Structure'],
    display_path=[],
    is_editable=True,
    is_creatable=True,
    is_deletable=True,
    event_type=BaseTBMDSourceEventType.timed,
    report_key='manualFaults',
    include_in_report='always',
    promote_on_create=True,
    select_on_create=True,
    structure=[
        file_structure_fault_name_block,
        technician_comment_block(is_editable=True),
        supervisor_comment_block(is_editable=False),
        severity_block(implications=file_structure_fault_implications),
        new_issue_block,
        fix_first_domestic_block,
        no_supplier_fix_required_block,
        ]
    )
