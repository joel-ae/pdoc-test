from functools import partial

from access_v2_blocks import SourceStructureBlock, SourceStructureBlockType
from access_v2_enums import ReportKey
from access_v2_sources import BaseTBMDSource, BaseTBMDSourceEventType


segmentation_block = SourceStructureBlock(
    key='name',
    name='Type',
    type=SourceStructureBlockType.select,
    required=True,
    is_editable=True,
    options=[
        *[{'name': f'SEG-{num:02}', 'index': 'source.segmentIndex'} for num in range(1, 26)],
        {'name': 'BarsTone', 'index': 'source.segmentIndex'}
        ]
    )

segmentation_source = partial(
    BaseTBMDSource,
    name='Segmentation',
    path=['Segmentation'],
    display_path=[],
    is_editable=False,
    is_creatable=False,
    is_deletable=False,
    event_type=BaseTBMDSourceEventType.timed,
    report_key=ReportKey.validated_segments,
    include_in_report='always',
    structure=[
        segmentation_block,
        ]
    )
