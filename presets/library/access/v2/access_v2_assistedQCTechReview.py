from functools import partial
from typing import List, Dict

from access_v2_blocks import SourceStructureBlock, SourceStructureBlockType
from access_v2_enums import DisplayAspectRatio, ReviewStatusOption
from access_v2_sources import BaseTBMDSource, BaseTBMDSourceEventType


notes_block = SourceStructureBlock(
    key='tech_notes',
    name='Notes',
    type=SourceStructureBlockType.textarea,
    metadata_path=['notes'],
    )

broadcast_schedule_notes_block = SourceStructureBlock(
    key='broadcast_schedule_notes',
    name='Broadcast Schedule Notes',
    type=SourceStructureBlockType.textarea,
    metadata_path=['notes'],
    required=False,
    )

status_block = partial(
    SourceStructureBlock,
    key='report',
    name='Review Status',
    type=SourceStructureBlockType.select,
    metadata_path=['status'],
    required=True,
    options=[
        ReviewStatusOption.accept,
        ReviewStatusOption.reject,
        ],
    )

display_aspect_ratio_block = SourceStructureBlock(
    key='display_aspect_ratio',
    name='Display Aspect Ratio',
    type=SourceStructureBlockType.select,
    metadata_path=['display_aspect_ratio'],
    required=True,
    options=[{'name': v} for v in sorted(DisplayAspectRatio)],
    )

room_options = [
    {'key': 'premiere_dev', 'name': 'Premiere Dev'},
    {'key': 'other', 'name': 'Other'},
    ]
for num in range(1, 11):
    room_options.append({'key': f'premiere_{num}', 'name': f'Premiere {num}'})


def room_sort(param: Dict[str, str]) -> int:
    """Sort function for Premiere Room options"""
    key = param['key']
    if key == 'other':
        return 100
    elif key == 'premiere_dev':
        return 99
    return int(key.split('_')[-1])


room_block = SourceStructureBlock(
    key='tech_room',
    name='Room',
    type=SourceStructureBlockType.select,
    metadata_path=['room'],
    required=False,
    options=sorted(room_options, key=room_sort)
    )

qc_time_block = SourceStructureBlock(
    key='technician',
    name='QC Time',
    type=SourceStructureBlockType.select,
    metadata_path=['qc_time'],
    required=False,
    options=[
        {'key': f'{num / 100:.2f}', 'name': f'{num / 100:.2f}'}
        for num in range(25, 2025, 25)
        ]
    )

cc_offset_block = SourceStructureBlock(
    key='ccOffset',
    name='CC Offset',
    metadata_path=['metadata'],
    type=SourceStructureBlockType.boolean,
    )

include_faults_block = SourceStructureBlock(
    key='faults',
    name='Include Faults',
    metadata_path=['include'],
    type=SourceStructureBlockType.boolean,
    )

include_manual_faults_block = SourceStructureBlock(
    key='manualFaults',
    name='Include Manual Faults',
    metadata_path=['include'],
    type=SourceStructureBlockType.boolean,
    )

include_woo_faults_block = SourceStructureBlock(
    key='wooFaults',
    name='Include Window of Opportunity Faults',
    metadata_path=['include'],
    type=SourceStructureBlockType.boolean,
    )

include_branding_marks_block = SourceStructureBlock(
    key='brandingEvents',
    name='Include Branding Marks',
    metadata_path=['include'],
    type=SourceStructureBlockType.boolean,
    )

include_other_events_block = SourceStructureBlock(
    key='otherEvents',
    name='Include Credits/Textless Marks',
    metadata_path=['include'],
    type=SourceStructureBlockType.boolean,
    )

tech_review = partial(
    BaseTBMDSource,
    type=BaseTBMDSourceEventType.report,
    event_type=None,
    required=True,
    )


def generate_tech_review(
        is_broadcast: bool = False,
        review_options: List[ReviewStatusOption] = None,
        **kwargs) -> BaseTBMDSource:
    """
    Create a tech review block

    :param is_broadcast: Should include a Broadcast Schedule Notes Block
    :param review_options: Options to include in the Review Status Block
                           Defaults to Accept and Reject
    :param kwargs: Any additional kwargs to pass to BaseTBMDSource
    :return:
    """
    structure = [
        notes_block,
        broadcast_schedule_notes_block if is_broadcast else None,
        status_block(options=review_options) if review_options else status_block(),
        display_aspect_ratio_block,
        room_block,
        qc_time_block,
        cc_offset_block,
        include_faults_block,
        include_manual_faults_block,
        include_woo_faults_block,
        include_branding_marks_block,
        include_other_events_block,
        ]

    return tech_review(
        name='Assisted QC Technician Review',
        file_label=None,
        display_path=None,
        report_key=None,
        structure=[i for i in structure if i],
        **kwargs
        )
