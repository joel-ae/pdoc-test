from enum import StrEnum
from functools import partial

from access_v2_blocks import SourceStructureBlock, SourceStructureBlockType
from access_v2_blocks import (fix_first_domestic_block, new_issue_block, no_supplier_fix_required_block, severity_block,
                              supervisor_comment_block, technician_comment_block)
from access_v2_enums import ReportKey, Severity
from access_v2_implications import Implication, validate_all_enums_accounted_for
from access_v2_sources import BaseTBMDSource, BaseTBMDSourceEventType


class AudioFault(StrEnum):
    """ Types of Audio Faults """
    abrupt_audio_edit = 'Abrupt Audio Edit'
    audio_bleed = 'Audio Bleed'
    audio_distortion = 'Audio Distortion'
    audio_dropout = 'Audio Dropout'
    audio_hit = 'Audio Hit'
    audio_hum = 'Audio Hum'
    audio_level_high = 'Audio Level High'
    audio_level_low = 'Audio Level Low'
    background_noise = 'Background Noise'
    buzz = 'Buzz'
    channel_sync = 'Channel Sync'
    clicks = 'Clicks'
    config_error = 'Config Error'
    dialogue_dipped = 'Dialogue Dipped'
    dialogue_present = 'Dialogue Present'
    eas_tone = 'EAS Tone'
    echo = 'Echo'
    extraneous_audio = 'Extraneous Audio'
    generic_audio_fault = 'Generic Audio Fault'
    hiss = 'Hiss'
    hot_mix = 'Hot Mix'
    inconsistent_audio_level = 'Inconsistent Audio Level'
    loudness = 'Loudness'
    loudness_out_of_spec = 'Loudness Out of Spec'
    m_and_e_dipped = 'M&E Dipped'
    music_dipped = 'Music Dipped'
    missing_audio = 'Missing Audio'
    missing_dialogue = 'Missing Dialogue'
    missing_fx = 'Missing FX'
    missing_music = 'Missing Music'
    missing_sot = 'Missing SOT'
    missing_textless_audio = 'Missing Textless Audio'
    mono_audio = 'Mono Audio'
    narration_preset = 'Narration Preset'
    out_of_phase = 'Out of Phase'
    poor_quality_audio = 'Poor Quality Audio'
    pops = 'Pops'
    reference_tone_missing = 'Reference Tone Missing'
    reference_tone_incorrect = 'Reference Tone Incorrect'
    reverb = 'Reverb'
    sot_present = 'SOT Present'
    sot_sfx_dipped = 'SOT/SFX Dipped'
    sibilance = 'Sibilance'
    sync_error = 'Sync Error'
    unbalanced_audio = 'Unbalanced Audio'
    walla_fault = 'Walla Fault'


audio_fault_type_block = SourceStructureBlock(
    key='name',
    name='Type',
    type=SourceStructureBlockType.select,
    required=True,
    is_editable=True,
    options=[{'name': v} for v in sorted(AudioFault)]
    )

audio_fault_high = [
    AudioFault.audio_dropout,
    AudioFault.audio_hit,
    AudioFault.audio_level_high,
    AudioFault.channel_sync,
    AudioFault.config_error,
    AudioFault.dialogue_dipped,
    AudioFault.eas_tone,
    AudioFault.extraneous_audio,
    AudioFault.hot_mix,
    AudioFault.inconsistent_audio_level,
    AudioFault.loudness_out_of_spec,
    AudioFault.m_and_e_dipped,
    AudioFault.music_dipped,
    AudioFault.missing_audio,
    AudioFault.missing_dialogue,
    AudioFault.missing_fx,
    AudioFault.missing_music,
    AudioFault.missing_sot,
    AudioFault.mono_audio,
    AudioFault.narration_preset,
    AudioFault.out_of_phase,
    AudioFault.reference_tone_missing,
    AudioFault.reference_tone_incorrect,
    AudioFault.sot_present,
    AudioFault.sot_sfx_dipped,
    AudioFault.sync_error,
    AudioFault.unbalanced_audio,
    AudioFault.walla_fault
    ]
audio_fault_medium = [
    AudioFault.abrupt_audio_edit,
    AudioFault.audio_bleed,
    AudioFault.audio_distortion,
    AudioFault.audio_level_low,
    AudioFault.background_noise,
    AudioFault.clicks,
    AudioFault.echo,
    AudioFault.generic_audio_fault,
    AudioFault.poor_quality_audio,
    AudioFault.pops,
    AudioFault.reverb,
    AudioFault.sibilance,
    ]
audio_fault_low = [
    AudioFault.audio_hum,
    AudioFault.buzz,
    AudioFault.dialogue_present,
    AudioFault.hiss,
    AudioFault.missing_textless_audio,
    ]
audio_fault_fyi = [
    AudioFault.loudness,
    ]

validate_all_enums_accounted_for(
    AudioFault,
    audio_fault_high,
    audio_fault_medium,
    audio_fault_low,
    audio_fault_fyi,
    )

audio_fault_implications = [
    *Implication.generate('name', audio_fault_high, Severity.high),
    *Implication.generate('name', audio_fault_medium, Severity.medium),
    *Implication.generate('name', audio_fault_low, Severity.low),
    *Implication.generate('name', audio_fault_fyi, Severity.fyi),
    ]

audio_fault_source = partial(
    BaseTBMDSource,
    name='Audio Fault',
    path=['Audio'],
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
        audio_fault_type_block,
        technician_comment_block(is_editable=True),
        supervisor_comment_block(is_editable=False),
        severity_block(implications=audio_fault_implications),
        new_issue_block,
        fix_first_domestic_block,
        no_supplier_fix_required_block,
        ]
    )


def generate_audio_fault_source(supervisor: bool = False, **kwargs):
    """

    :param supervisor: Is this for a supervisor review?
    :param kwargs: Any additional kwargs to pass to BaseTBMDSource
    :return:
    """
    pass
