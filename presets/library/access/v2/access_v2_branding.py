from functools import partial

from access_v2_blocks import SourceStructureBlock, SourceStructureBlockType
from access_v2_enums import ReportKey
from access_v2_sources import BaseTBMDSource, BaseTBMDSourceEventType
# from ae_branding_mapping import BRANDING_OPTIONS # todo: import from ae_branding_mapping


BRANDING_OPTIONS = [
    'A Lifetime Original Documentary',
    'A Lifetime Original Movie',
    'A Lifetime Original Series',
    'An A&E Original Documentary',
    'An A&E Original Movie',
    'An A&E Original Series',
    'An FYI Original Documentary',
    'An FYI Original Movie',
    'An FYI Original Series',
    'A Home.Made.Nation Original Documentary',
    'A Home.Made.Nation Original Movie',
    'A Home.Made.Nation Original Series',
    'The History Channel Original Documentary',
    'The History Channel Original Movie',
    'The History Channel Original Series',
    'No Branding Required',
    'To Be Determined',
    ]

branding_name_block = SourceStructureBlock(
    key='name',
    name='Type',
    type=SourceStructureBlockType.select,
    required=True,
    is_editable=True,
    options=[
        {'name': 'Network Originals Credit'}
        ]
    )


def branding_sort_key(value: str) -> str:
    """ Function used with `sorted` for branding values

    :param value: Branding value
    :return: string to sort with
    """
    override = {
        'To Be Determined': 'Z',
        'No Branding Required': 'Y',
        }
    return override.get(value, value)


branding_message_block = SourceStructureBlock(
    key='message',
    name='Branding Message',
    type=SourceStructureBlockType.select,
    required=True,
    is_editable=True,
    options=[
        {'name': value}
        for value in sorted(BRANDING_OPTIONS, key=branding_sort_key)
        ],
    )

prebranded_block = SourceStructureBlock(
    key='prebranded',
    name='Prebranded',
    type=SourceStructureBlockType.boolean,
    required=False,
    is_editable=True,
    )

network_originals_credit_source = partial(
    BaseTBMDSource,
    name='Branding',
    path=['Branding'],
    display_path=[],
    is_editable=True,
    is_creatable=True,
    is_deletable=True,
    event_type=BaseTBMDSourceEventType.timed,
    report_key=ReportKey.branding_events,
    include_in_report='always',
    structure=[
        branding_name_block,
        branding_message_block,
        prebranded_block,
        ]
    )
