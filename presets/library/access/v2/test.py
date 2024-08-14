import json

from access_v2_assistedQCTechReview import ReviewStatusOption, generate_tech_review
from access_v2_audioFault import audio_fault_source
from access_v2_baton import provider_qc_events_source
from access_v2_branding import network_originals_credit_source
from access_v2_captioningFault import captioning_fault_source
from access_v2_contentSPMark import content_sp_mark_source
from access_v2_creditsTextlessMark import credits_textless_source
from access_v2_enums import FileLabel
from access_v2_fileStructureFault import file_structure_fault_source
from access_v2_implications import Implication
from access_v2_segmentation import segmentation_source
from access_v2_textGraphicsMark import text_graphics_mark_source
from access_v2_textlessMark import textless_mark_source
from access_v2_timecodeFault import timecode_fault_source
from access_v2_videoFault import video_fault_source
from access_v2_woo import woo_source
from access_v2_wooFault import woo_fault_source
from access_v2_workOrder import AQCOptions, EDL, ExtraData, LegacyAccessWorkOrder, OutputPrefs


audio_fault = audio_fault_source(file_label=FileLabel.broadcast_manual_faults)
provider_qc_events = provider_qc_events_source(file_label=FileLabel.broadcast_tbmd_qc_events)
branding = network_originals_credit_source(file_label=FileLabel.broadcast_segmentation)
captioning_fault = captioning_fault_source(file_label=FileLabel.broadcast_manual_faults)
content_sp_mark = content_sp_mark_source(file_label=FileLabel.broadcast_manual_faults)
credits_textless = credits_textless_source(file_label=FileLabel.broadcast_segmentation)
file_structure_fault = file_structure_fault_source(file_label=FileLabel.broadcast_manual_faults)
segmentation = segmentation_source(file_label=FileLabel.broadcast_segmentation)
text_graphics_mark = text_graphics_mark_source(file_label=FileLabel.broadcast_manual_faults)
textless_mark = textless_mark_source(file_label=FileLabel.broadcast_manual_faults)
timecode_fault = timecode_fault_source(file_label=FileLabel.broadcast_manual_faults)
video_fault = video_fault_source(file_label=FileLabel.broadcast_manual_faults)
woo = woo_source(file_label=FileLabel.broadcast_segmentation)
woo_fault = woo_fault_source(file_label=FileLabel.broadcast_manual_faults)

output_prefs = OutputPrefs(
    workorder_outputs=[
        generate_tech_review(is_broadcast=True),
        ],
    extra_data=ExtraData(),
    )

aqc_options = AQCOptions(
    time_based_metadata_sources=[
        provider_qc_events,
        segmentation,
        branding,
        woo,
        credits_textless,
        file_structure_fault,
        audio_fault,
        captioning_fault,
        content_sp_mark,
        text_graphics_mark,
        textless_mark,
        timecode_fault,
        video_fault,
        woo_fault,
        ],
    output_prefs=output_prefs,
    extra_data=ExtraData(),
    )

broadcast = LegacyAccessWorkOrder(
    aqc_options=aqc_options,
    edl=EDL(label='broadcastQC_EDL'),
    )

with open('test_output_broadcast.json', 'w') as f:
    f.write(broadcast.model_dump_json(by_alias=True, indent=2, exclude_none=True))

# This next section is for a techEval01 work order

audio_fault = audio_fault_source(file_label=FileLabel.manual_faults)
provider_qc_events = provider_qc_events_source(file_label=FileLabel.tbmd_qc_events)
branding = network_originals_credit_source(file_label=FileLabel.segmentation)
captioning_fault = captioning_fault_source(file_label=FileLabel.manual_faults)
content_sp_mark = content_sp_mark_source(file_label=FileLabel.manual_faults)
credits_textless = credits_textless_source(file_label=FileLabel.segmentation)
file_structure_fault = file_structure_fault_source(file_label=FileLabel.manual_faults)
segmentation = segmentation_source(file_label=FileLabel.segmentation, is_editable=True, is_creatable=True,
                                   is_deletable=True)
text_graphics_mark = text_graphics_mark_source(file_label=FileLabel.manual_faults)
textless_mark = textless_mark_source(file_label=FileLabel.manual_faults)
timecode_fault = timecode_fault_source(file_label=FileLabel.manual_faults)
video_fault = video_fault_source(file_label=FileLabel.manual_faults)
woo = woo_source(file_label=FileLabel.segmentation)
woo_fault = woo_fault_source(file_label=FileLabel.manual_faults)

output_prefs = OutputPrefs(
    workorder_outputs=[
        generate_tech_review(
            is_broadcast=False,
            short_name='SinglePass_QC_Review',
            review_options=[
                ReviewStatusOption.accept,
                ReviewStatusOption.reject,
                ReviewStatusOption.skip,
                ],
            is_editable=None,
            is_creatable=None,
            is_deletable=None,
            path=None,
            required=True,

            )
        ],
    extra_data=ExtraData(),
    )

aqc_options = AQCOptions(
    proxy_file_label='QCProxy',
    time_based_metadata_sources=[
        provider_qc_events,
        segmentation,
        branding,
        woo,
        credits_textless,
        file_structure_fault,
        audio_fault,
        captioning_fault,
        content_sp_mark,
        text_graphics_mark,
        textless_mark,
        timecode_fault,
        video_fault,
        woo_fault,
        ],
    output_prefs=output_prefs,

    )

techEval01 = LegacyAccessWorkOrder(
    aqc_options=aqc_options,
    )


with open('test_output_techEval01.json', 'w') as f:
    f.write(techEval01.model_dump_json(by_alias=True, indent=2, exclude_none=True))


# This next section is for a CRS07 technician work order

audio_fault = audio_fault_source(file_label=FileLabel.manual_faults)
provider_qc_events = provider_qc_events_source(file_label=FileLabel.tbmd_qc_events)
branding = network_originals_credit_source(file_label=FileLabel.segmentation)
captioning_fault = captioning_fault_source(file_label=FileLabel.manual_faults)
content_sp_mark = content_sp_mark_source(file_label=FileLabel.manual_faults)
credits_textless = credits_textless_source(file_label=FileLabel.segmentation)
file_structure_fault = file_structure_fault_source(file_label=FileLabel.manual_faults)
segmentation = segmentation_source(file_label=FileLabel.segmentation, is_editable=True, is_creatable=True,
                                   is_deletable=True)
text_graphics_mark = text_graphics_mark_source(file_label=FileLabel.manual_faults)
textless_mark = textless_mark_source(file_label=FileLabel.manual_faults)
timecode_fault = timecode_fault_source(file_label=FileLabel.manual_faults)
video_fault = video_fault_source(file_label=FileLabel.manual_faults)
woo = woo_source(file_label=FileLabel.segmentation)
woo_fault = woo_fault_source(file_label=FileLabel.manual_faults)

output_prefs = OutputPrefs(
    workorder_outputs=[
        generate_tech_review(
            is_broadcast=False,
            short_name='QC_Review',
            review_options=[
                ReviewStatusOption.accept,
                ReviewStatusOption.refer,
                ],
            is_editable=None,
            is_creatable=None,
            is_deletable=None,
            path=None,
            required=True,

            )
        ],
    extra_data=ExtraData(),
    )

aqc_options = AQCOptions(
    proxy_file_label='QCProxy',
    time_based_metadata_sources=[
        provider_qc_events,
        segmentation,
        branding,
        woo,
        credits_textless,
        file_structure_fault,
        audio_fault,
        captioning_fault,
        content_sp_mark,
        text_graphics_mark,
        textless_mark,
        timecode_fault,
        video_fault,
        woo_fault,
        ],
    output_prefs=output_prefs,

    )

crs07_tech = LegacyAccessWorkOrder(
    aqc_options=aqc_options,
    )

with open('test_output_crs07_tech.json', 'w') as f:
    f.write(crs07_tech.model_dump_json(by_alias=True, indent=2, exclude_none=True))

# CRS07 supervisor

audio_fault = audio_fault_source(file_label=FileLabel.manual_faults)
provider_qc_events = provider_qc_events_source(file_label=FileLabel.tbmd_qc_events)
branding = network_originals_credit_source(file_label=FileLabel.segmentation)
captioning_fault = captioning_fault_source(file_label=FileLabel.manual_faults)
content_sp_mark = content_sp_mark_source(file_label=FileLabel.manual_faults)
credits_textless = credits_textless_source(file_label=FileLabel.segmentation)
file_structure_fault = file_structure_fault_source(file_label=FileLabel.manual_faults)
segmentation = segmentation_source(file_label=FileLabel.segmentation, is_editable=True, is_creatable=True,
                                   is_deletable=True)
text_graphics_mark = text_graphics_mark_source(file_label=FileLabel.manual_faults)
textless_mark = textless_mark_source(file_label=FileLabel.manual_faults)
timecode_fault = timecode_fault_source(file_label=FileLabel.manual_faults)
video_fault = video_fault_source(file_label=FileLabel.manual_faults)
woo = woo_source(file_label=FileLabel.segmentation)
woo_fault = woo_fault_source(file_label=FileLabel.manual_faults)

output_prefs = OutputPrefs(
    workorder_outputs=[
        generate_tech_review(
            is_broadcast=False,
            short_name='QC_Review',
            review_options=[
                ReviewStatusOption.accept,
                ReviewStatusOption.reject,
                ReviewStatusOption.defer,
                ],
            is_editable=None,
            is_creatable=None,
            is_deletable=None,
            path=None,
            required=True,

            )
        ],
    extra_data=ExtraData(),
    )

aqc_options = AQCOptions(
    proxy_file_label='QCProxy',
    time_based_metadata_sources=[
        provider_qc_events,
        segmentation,
        branding,
        woo,
        credits_textless,
        file_structure_fault,
        audio_fault,
        captioning_fault,
        content_sp_mark,
        text_graphics_mark,
        textless_mark,
        timecode_fault,
        video_fault,
        woo_fault,
        ],
    output_prefs=output_prefs,

    )

crs07_sup = LegacyAccessWorkOrder(
    aqc_options=aqc_options,
    )

with open('test_output_crs07_sup.json', 'w') as f:
    f.write(crs07_sup.model_dump_json(by_alias=True, indent=2, exclude_none=True))



# sample_name, b = 'broadcast', broadcast
# sample_name, b = ('techEval01', techEval01)
sample_name, b = ('crs07_tech', crs07_tech)
# sample_name, b = ('crs07_sup', crs07_sup)


if True:
    mine = b.model_dump(by_alias=True, mode='json', exclude_none=True)

    with open(f'test_sample_{sample_name}.json', 'r') as f:
        sample = json.load(f)
    print(sample_name)

    def sort_options(opt):
        override = {
            '3 - High': 0,
            '2 - Medium': 1,
            '1 - Low': 2,
            'FYI': 3,
            'BarsTone': 'ZZZZ',
            'No Branding Required': 'X',
            'To Be Determined': 'Z'
            }
        try:
            return float(opt['name'])
        except:
            pass
        return override.get(opt['name'], opt['name'])


    def sort_implication(imp):
        return imp['when'][2]


    sources = sample['AQCOptions']['timeBasedMetadataSources']
    for source in sources:
        for structure in source['structure']:
            if 'options' in structure:
                structure['options'] = sorted(structure['options'], key=sort_options)
            if 'implications' in structure:
                structure['implications'] = sorted(structure['implications'], key=sort_implication)
            structure = {k: structure[k] for k in sorted(structure.keys())}

    sources = sample['AQCOptions']['OutputPrefs']['workorderOutputs']
    for source in sources:
        for structure in source['structure']:
            if 'options' in structure:
                structure['options'] = sorted(structure['options'], key=sort_options)
            if 'implications' in structure:
                structure['implications'] = sorted(structure['implications'], key=sort_implication)
            structure = {k: structure[k] for k in sorted(structure.keys())}

    with open(f'test_sample_output_{sample_name}.json', 'w') as f:
        json.dump(sample, f, indent=2)

    print(f'Outputs match: {sample == mine}')
    print(type(sample), type(mine))

    same = True
    for tbmd_sample in sample['AQCOptions']['timeBasedMetadataSources']:
        for tbmd_mine in mine['AQCOptions']['timeBasedMetadataSources']:
            if tbmd_sample['name'] != tbmd_mine['name']:
                continue
            if tbmd_sample != tbmd_mine:
                print(tbmd_sample['name'])
                print(tbmd_sample)
                print(tbmd_mine)
                same = False
                break
    if same:
        print('AQCOptions tbmd sources are equal')

    same = True
    for tbmd_sample in sample['AQCOptions']['OutputPrefs']['workorderOutputs']:
        for tbmd_mine in mine['AQCOptions']['OutputPrefs']['workorderOutputs']:
            if tbmd_sample['name'] != tbmd_mine['name']:
                continue
            if tbmd_sample != tbmd_mine:
                print(tbmd_sample['name'])
                print(tbmd_sample)
                print(tbmd_mine)
                same = False
                break
    if same:
        print('Output prefs are equal')

    # for
