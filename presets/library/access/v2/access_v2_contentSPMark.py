from enum import StrEnum
from functools import partial

from access_v2_blocks import SourceStructureBlock, SourceStructureBlockType
from access_v2_blocks import (fix_first_domestic_block, new_issue_block, no_supplier_fix_required_block, severity_block,
                              supervisor_comment_block, technician_comment_block)
from access_v2_enums import ReportKey, Severity
from access_v2_implications import Implication, validate_all_enums_accounted_for
from access_v2_sources import BaseTBMDSource, BaseTBMDSourceEventType


class ContentSPMark(StrEnum):
    """ Types of Content and S&P Marks """
    blur_error = 'Blur Error'
    child_molestation = 'Child Molestation'
    drug_use = 'Drug Use'
    famous_person_reference = 'Famous Person Reference'
    general_s_and_p_fault = 'General S&P Fault'
    graphic_violence = 'Graphic Violence'
    improper_eas_use = 'Improper EAS Use'
    language_audio_only = 'Language - Audio Only'
    language_audio_and_text_graphic = 'Language - Audio and Text/Graphic'
    language_audio_and_closed_caption = 'Language - Audio and Closed Caption'
    language_text_graphic_only = 'Language - Text/Graphic Only'
    language_incorrect_bleep_drop = 'Language - Incorrect Bleep/Drop'
    language_in_video = 'Language - In Video'
    natural_disaster = 'Natural Disaster'
    nudity = 'Nudity'
    nudity_in_art = 'Nudity in Art'
    plane_crash = 'Plane Crash'
    questionable_religious_comment = 'Questionable Religious Comment'
    racial = 'Racial'
    school_shooting = 'School Shooting'
    sexual_content = 'Sexual Content'
    terrorism = 'Terrorism'
    wtc_or_911 = 'WTC or 9/11'
    wwii_audio = 'WWII Audio'
    wwii_audio_video = 'WWII Audio/Video'
    wwii_video = 'WWII Video'
    war_military = 'War/Military'


content_sp_mark_block = SourceStructureBlock(
    key='name',
    name='Type',
    type=SourceStructureBlockType.select,
    required=True,
    is_editable=True,
    options=[{'name': v} for v in sorted(ContentSPMark)]
    )

content_sp_mark_high = [
    ContentSPMark.blur_error,
    ContentSPMark.child_molestation,
    ContentSPMark.improper_eas_use,
    ]
content_sp_mark_medium = [
    ContentSPMark.drug_use,
    ContentSPMark.famous_person_reference,
    ContentSPMark.graphic_violence,
    ContentSPMark.language_audio_only,
    ContentSPMark.language_audio_and_text_graphic,
    ContentSPMark.language_audio_and_closed_caption,
    ContentSPMark.language_text_graphic_only,
    ContentSPMark.language_incorrect_bleep_drop,
    ContentSPMark.language_in_video,
    ContentSPMark.nudity,
    ContentSPMark.nudity_in_art,
    ContentSPMark.questionable_religious_comment,
    ContentSPMark.racial,
    ContentSPMark.school_shooting,
    ContentSPMark.terrorism,
    ContentSPMark.wtc_or_911,
    ContentSPMark.wwii_audio,
    ContentSPMark.wwii_audio_video,
    ContentSPMark.wwii_video,
    ContentSPMark.war_military,
    ]
content_sp_mark_low = [
    ContentSPMark.natural_disaster,
    ContentSPMark.plane_crash,
    ContentSPMark.sexual_content,
    ]
content_sp_mark_fyi = [
    ContentSPMark.general_s_and_p_fault,
    ]

validate_all_enums_accounted_for(
    ContentSPMark,
    content_sp_mark_high,
    content_sp_mark_medium,
    content_sp_mark_low,
    content_sp_mark_fyi,
    )

content_sp_mark_implications = [
    *Implication.generate('name', content_sp_mark_high, Severity.high),
    *Implication.generate('name', content_sp_mark_medium, Severity.medium),
    *Implication.generate('name', content_sp_mark_low, Severity.low),
    *Implication.generate('name', content_sp_mark_fyi, Severity.fyi),
    ]

content_sp_mark_source = partial(
    BaseTBMDSource,
    name='Content / S&P Mark',
    path=['Content - S&P'],
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
        content_sp_mark_block,
        technician_comment_block(is_editable=True),
        supervisor_comment_block(is_editable=False),
        severity_block(implications=content_sp_mark_implications),
        new_issue_block,
        fix_first_domestic_block,
        no_supplier_fix_required_block,
        ]
    )
