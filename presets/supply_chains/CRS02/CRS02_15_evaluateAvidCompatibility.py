"""
An Evaluator Script to test only including DE presets in docs.
"""

def is_avid_compatible():
    """Returns True if the media is compatible with an Avid editor."""
    master_info = selectAnalyzeInfo(label='Master', adjustFramerate=True)
    video_info = master_info['video'][0]
    fmt = video_info.get('formatCommercial', '')
    general_info = master_info['MediaInfo']['General']
    video_format = general_info.get('Format', '')
    if 'MXF' in video_format:
        return fmt.startswith('DNxHD') or fmt in ['IMX 50', 'XDCAM HD422']
    return False


def is_hd():
    """Returns True if the media is assumed to be HD content."""
    master_info = selectAnalyzeInfo(label='Master', adjustFramerate=True)
    video = master_info['video'][0]
    video_height = video['height']
    if video_height is None:
        raise ValueError('Master not a video, or corrupted.')
    return int(video_height) > 600


master = getBox('Master')
if not master:
    raise ValueError('Asset has no master.')
else:
    master = master[0]

if is_avid_compatible():
    # Register master as edit master
    addFileToMovie(
        uri=master.uri,
        etag=master.etag,
        size=master.size,
        label='Edit_Master',
        )
    return createDynamicWorkflow('CRS02')

next_step = 'CRS02_16{}'.format('HD' if is_hd() else 'SD')
return createDynamicWorkflow(next_step)
