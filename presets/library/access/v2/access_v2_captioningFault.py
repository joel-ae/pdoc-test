from enum import StrEnum
from functools import partial

from access_v2_blocks import SourceStructureBlock, SourceStructureBlockType
from access_v2_blocks import (fix_first_domestic_block, new_issue_block, no_supplier_fix_required_block, severity_block,
                              supervisor_comment_block, technician_comment_block)
from access_v2_enums import ReportKey, Severity
from access_v2_implications import Implication, validate_all_enums_accounted_for
from access_v2_sources import BaseTBMDSource, BaseTBMDSourceEventType


class CaptioningFault(StrEnum):
    cc_offset = 'CC Offset'
    extraneous = 'Extraneous'
    mismatch = 'Mismatch'
    missing = 'Missing'
    misspelling_grammar = 'Misspelling/Grammar'
    obstruction = 'Obstruction'
    placement = 'Placement'
    s_and_p_language_in_cc_only = 'S&P (Language in CC only)'
    synchronicity = 'Synchronicity'


captioning_fault_type_block = SourceStructureBlock(
    key='name',
    name='Type',
    type=SourceStructureBlockType.select,
    required=True,
    is_editable=True,
    options=[{'name': i} for i in sorted(CaptioningFault)]
    )

captioning_fault_high = [
    CaptioningFault.cc_offset,
    CaptioningFault.extraneous,
    CaptioningFault.mismatch,
    CaptioningFault.missing,
    CaptioningFault.obstruction,
    CaptioningFault.s_and_p_language_in_cc_only,
    CaptioningFault.synchronicity,
    ]
captioning_fault_medium = [
    CaptioningFault.misspelling_grammar,
    CaptioningFault.placement,
    ]

validate_all_enums_accounted_for(
    CaptioningFault,
    captioning_fault_high,
    captioning_fault_medium,
    )

captioning_fault_implications = [
    *Implication.generate('name', captioning_fault_high, Severity.high),
    *Implication.generate('name', captioning_fault_medium, Severity.medium),
    ]

captioning_fault_source = partial(
    BaseTBMDSource,
    name='Captioning Fault',
    path=['Captioning'],
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
        captioning_fault_type_block,
        technician_comment_block(is_editable=True),
        supervisor_comment_block(is_editable=False),
        severity_block(implications=captioning_fault_implications),
        new_issue_block,
        fix_first_domestic_block,
        no_supplier_fix_required_block,
        ]
    )
