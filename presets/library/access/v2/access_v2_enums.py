from enum import Enum, StrEnum


class DisplayAspectRatio(StrEnum):
    """ A+E's definitions of Display Aspect Ratio """
    _4_3_full_height_anamorphic = '4:3 FHA'  # Full Height Anamorphic
    _4_3_full_frame_with_letterbox = '4:3 FF w/ LB'  # Full Frame with LetterBoxing
    _4_3_full_frame = '4:3 fullframe'
    _4_3_letterbox = '4:3 letterbox'
    _16_9_full_frame = '16:9 fullframe'
    _16_9_letterbox = '16:9 letterbox'
    _16_9_pillarbox = '16:9 pillarbox'


class Severity(StrEnum):
    """ Allowed Severity values in a work order """
    high = '3 - High'
    medium = '2 - Medium'
    low = '1 - Low'
    fyi = 'FYI'


class SeverityOption(Enum):
    """ Mappings of Severity name to key """
    high = {'name': Severity.high, 'key': 'high'}
    medium = {'name': Severity.medium, 'key': 'medium'}
    low = {'name': Severity.low, 'key': 'low'}
    fyi = {'name': Severity.fyi, 'key': 'FYI'}


class ReportKey(StrEnum):
    """ Report Keys used in work orders """
    branding_events = 'brandingEvents'
    validated_segments = 'validatedSegments'
    woo_events = 'wooEvents'
    other_events = 'otherEvents'
    faults = 'faults'
    manual_faults = 'manualFaults'
    woo_faults = 'wooFaults'

    @classmethod
    def sort_key(cls, report_key: ['ReportKey', str]) -> int:
        order = [
            # Metadata
            'brandingEvents',
            'validatedSegments',
            'wooEvents',
            'otherEvents',

            # Issues
            'faults',
            'manualFaults',
            'wooFaults',
            ]
        if report_key not in order:
            raise ValueError(f'Input ({report_key}) is not accounted for in the order list')
        # key = report_key
        # if isinstance(report_key, ReportKey):
        #     key = key.value
        return order.index(report_key)


class FileLabel(StrEnum):
    """ Rally Inventory Labels used for work order input/output files """
    segmentation = 'Segmentation'
    broadcast_segmentation = 'Broadcast Segmentation'
    tbmd_qc_events = 'TBMDQCEvents' # Time Based MetaData QC Events
    broadcast_tbmd_qc_events = 'Broadcast TBMDQCEvents'
    manual_faults = 'ManualFaults'
    broadcast_manual_faults = 'Broadcast ManualFaults'


class ReviewStatus(StrEnum):
    """ Allowed Review Status values """
    accept = 'Accept'
    reject = 'Reject'
    refer = 'Refer'
    defer = 'Defer'
    skip = 'Skip'


class ReviewStatusOption(Enum):
    """ Mapping of ReviewStatus values to names that show up in work orders """
    accept = {'key': ReviewStatus.accept.value.lower(), 'name': ReviewStatus.accept}
    reject = {'key': ReviewStatus.reject.value.lower(), 'name': ReviewStatus.reject}
    refer = {'key': ReviewStatus.refer.value.lower(), 'name': ReviewStatus.refer}
    defer = {'key': ReviewStatus.defer.value.lower(), 'name': 'Trigger Additional Pass'}
    skip = {'key': ReviewStatus.skip.value.lower(), 'name': ReviewStatus.skip}

