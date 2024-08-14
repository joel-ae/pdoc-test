from enum import StrEnum
from functools import partial

from access_v2_blocks import SourceStructureBlock, SourceStructureBlockType
from access_v2_blocks import (fix_first_domestic_block, new_issue_block, no_supplier_fix_required_block, severity_block,
                              supervisor_comment_block, technician_comment_block)
from access_v2_enums import ReportKey, Severity
from access_v2_implications import Implication, validate_all_enums_accounted_for
from access_v2_sources import BaseTBMDSource, BaseTBMDSourceEventType


class WindowOfOpportunityFault(StrEnum):
    """ Window of Opportunity Fault types """
    bug_covers_l3_graphic = 'Bug covers L3 / Graphic'
    bug_duration_less_than_19s13 = 'Bug duration less than 19;13'
    bug_falls_out_of_som_eom = 'Bug falls out of SOM / EOM'
    bug_within_1_min_of_som_eom = 'Bug within 1 min of SOM / EOM'
    bugs_entered_incorrectly = 'Bugs entered incorrectly'
    bugs_within_1_min_of_each_other = 'Bugs within 1 min of each other'


window_of_opportunity_fault_block = SourceStructureBlock(
    key='name',
    name='Type',
    type=SourceStructureBlockType.select,
    required=True,
    is_editable=True,
    options=[{'name': v} for v in sorted(WindowOfOpportunityFault)],
    )

window_of_opportunity_fault_high = [
    WindowOfOpportunityFault.bug_covers_l3_graphic,
    WindowOfOpportunityFault.bug_duration_less_than_19s13,
    WindowOfOpportunityFault.bug_falls_out_of_som_eom,
    WindowOfOpportunityFault.bug_within_1_min_of_som_eom,
    WindowOfOpportunityFault.bugs_entered_incorrectly,
    WindowOfOpportunityFault.bugs_within_1_min_of_each_other,
    ]
window_of_opportunity_fault_medium = [

    ]
window_of_opportunity_fault_low = [

    ]
window_of_opportunity_fault_fyi = [

    ]

validate_all_enums_accounted_for(
    WindowOfOpportunityFault,
    window_of_opportunity_fault_high,
    window_of_opportunity_fault_medium,
    window_of_opportunity_fault_low,
    window_of_opportunity_fault_fyi,
    )

window_of_opportunity_fault_implications = [
    *Implication.generate('name', window_of_opportunity_fault_high, Severity.high),
    *Implication.generate('name', window_of_opportunity_fault_medium, Severity.medium),
    *Implication.generate('name', window_of_opportunity_fault_low, Severity.low),
    *Implication.generate('name', window_of_opportunity_fault_fyi, Severity.fyi),
    ]

woo_fault_source = partial(
    BaseTBMDSource,
    name='Window of Opportunity Fault',
    path=['Window of Opportunity Fault'],
    display_path=[],
    is_editable=True,
    is_creatable=True,
    is_deletable=True,
    event_type=BaseTBMDSourceEventType.timed,
    report_key=ReportKey.woo_faults,
    include_in_report='always',
    promote_on_create=True,
    select_on_create=True,
    structure=[
        window_of_opportunity_fault_block,
        technician_comment_block(is_editable=True),
        supervisor_comment_block(is_editable=False),
        severity_block(implications=window_of_opportunity_fault_implications),
        new_issue_block,
        fix_first_domestic_block,
        no_supplier_fix_required_block,

        ]
    )
