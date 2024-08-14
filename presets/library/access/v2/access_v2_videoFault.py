from enum import StrEnum
from functools import partial

from access_v2_blocks import SourceStructureBlock, SourceStructureBlockType
from access_v2_blocks import (fix_first_domestic_block, new_issue_block, no_supplier_fix_required_block, severity_block,
                              supervisor_comment_block, technician_comment_block)
from access_v2_enums import ReportKey, Severity
from access_v2_implications import Implication, validate_all_enums_accounted_for
from access_v2_sources import BaseTBMDSource, BaseTBMDSourceEventType


class VideoFault(StrEnum):
    """ Types of Video Faults for TE Work Orders """
    abrupt_video_edit = 'Abrupt Video Edit'
    aliasing = 'Aliasing'
    anamorphic = 'Anamorphic'
    aspect_ratio_error = 'Aspect Ratio Error'
    banding = 'Banding'
    chroma_key_error = 'Chroma Key Error'
    continuity_error = 'Continuity Error'
    copyright_error = 'Copyright Error'
    credits_error = 'Credits Error'
    credits_missing = 'Credits Missing'
    dead_pixel = 'Dead Pixel'
    dropout_video = 'Dropout Video'
    eas_graphic_or_visual = 'EAS Graphic or Visual'
    flash_frame = 'Flash Frame'
    frame_shift = 'Frame Shift'
    flicker = 'Flicker'
    generic_video_fault = 'Generic Video Fault'
    high_black_levels = 'High Black Levels'
    image_doubling = 'Image Doubling'
    image_not_filling_frame = 'Image Not Filling Frame'
    interlacing = 'Interlacing'
    jump_cut = 'Jump Cut'
    letterbox = 'Letterbox'
    low_black_levels = 'Low Black Levels'
    low_resolution = 'Low Resolution'
    lower_third_error = 'Lower Third Error'
    macro_blocking = 'Macro Blocking'
    matte_shift = 'Matte Shift'
    media_offline = 'Media Offline'
    moire = 'Moire'
    network_originals_credit_fault = 'Network Originals Credit Fault'
    no_graphic_mortise = 'No Graphic Mortise'
    pillar_box = 'Pillar Box'
    poor_transition = 'Poor Transition'
    postage_stamp = 'Postage Stamp'
    production_crew = 'Production Crew'
    production_equipment_in_shot = 'Production Equipment in Shot'
    reference_bars_incorrect = 'Reference Bars Incorrect'
    reference_bars_missing = 'Reference Bars Missing'
    slate_incorrect = 'Slate Incorrect'
    stuck_pixel = 'Stuck Pixel'
    video_distortion = 'Video Distortion'
    video_dropped_frames = 'Video Dropped Frames'
    video_freeze_frame = 'Video Freeze Frame'
    video_ghosting = 'Video Ghosting'
    video_hit = 'Video Hit'
    video_noise = 'Video Noise'
    video_repeated_frames = 'Video Repeated Frames'
    video_skipped_frames = 'Video Skipped Frames'
    video_tearing = 'Video Tearing'
    video_warping = 'Video Warping'


video_fault_block = SourceStructureBlock(
    key='name',
    name='Type',
    type=SourceStructureBlockType.select,
    required=True,
    is_editable=True,
    options=[{'name': v} for v in sorted(VideoFault)],
    )

video_fault_high = [
    VideoFault.anamorphic,
    VideoFault.aspect_ratio_error,
    VideoFault.banding,
    VideoFault.copyright_error,
    VideoFault.credits_error,
    VideoFault.credits_missing,
    VideoFault.dropout_video,
    VideoFault.eas_graphic_or_visual,
    VideoFault.low_black_levels,
    VideoFault.lower_third_error,
    VideoFault.matte_shift,
    VideoFault.media_offline,
    VideoFault.network_originals_credit_fault,
    VideoFault.postage_stamp,
    VideoFault.reference_bars_incorrect,
    VideoFault.reference_bars_missing,
    VideoFault.slate_incorrect,
    VideoFault.video_ghosting,
    VideoFault.video_hit,
    VideoFault.video_warping,

    ]
video_fault_medium = [
    VideoFault.abrupt_video_edit,
    VideoFault.chroma_key_error,
    VideoFault.dead_pixel,
    VideoFault.flash_frame,
    VideoFault.flicker,
    VideoFault.generic_video_fault,
    VideoFault.high_black_levels,
    VideoFault.image_doubling,
    VideoFault.image_not_filling_frame,
    VideoFault.interlacing,
    VideoFault.jump_cut,
    VideoFault.letterbox,
    VideoFault.low_resolution,
    VideoFault.macro_blocking,
    VideoFault.no_graphic_mortise,
    VideoFault.pillar_box,
    VideoFault.poor_transition,
    VideoFault.production_crew,
    VideoFault.production_equipment_in_shot,
    VideoFault.video_distortion,
    VideoFault.video_dropped_frames,
    VideoFault.video_repeated_frames,
    VideoFault.video_skipped_frames,
    VideoFault.video_tearing,

    ]
video_fault_low = [
    VideoFault.aliasing,
    VideoFault.continuity_error,
    VideoFault.frame_shift,
    VideoFault.moire,
    VideoFault.stuck_pixel,
    VideoFault.video_freeze_frame,
    VideoFault.video_noise,

    ]
video_fault_fyi = [

    ]

validate_all_enums_accounted_for(
    VideoFault,
    video_fault_high,
    video_fault_medium,
    video_fault_low,
    video_fault_fyi,
    )

video_fault_implications = [
    *Implication.generate('name', video_fault_high, Severity.high),
    *Implication.generate('name', video_fault_medium, Severity.medium),
    *Implication.generate('name', video_fault_low, Severity.low),
    *Implication.generate('name', video_fault_fyi, Severity.fyi),
    ]

video_fault_source = partial(
    BaseTBMDSource,
    name='Video Fault',
    file_label='Broadcast ManualFaults',
    path=['Video'],
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
        video_fault_block,
        technician_comment_block(is_editable=True),
        supervisor_comment_block(is_editable=False),
        severity_block(implications=video_fault_implications),
        new_issue_block,
        fix_first_domestic_block,
        no_supplier_fix_required_block,
        ]
    )
