from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel, Field

from access_v2_blocks import SourceStructureBlock


class BaseTBMDSourceEventType(StrEnum):
    """ Types of BaseTBMDSource """
    timed = 'timed'
    report = 'report'


class BaseTBMDSource(BaseModel):
    """ Model for TBMD Sources in an Access Work Order """
    name: str
    short_name: Optional[str] = Field(default=None, serialization_alias='shortName')
    file_label: Optional[str] = Field(default=None, serialization_alias='fileLabel')
    path: Optional[List[str]] = Field(default_factory=list)
    display_path: Optional[List[str]] = Field(default=None, serialization_alias='displayPath')
    report_key: Optional[str] = Field(default=None, serialization_alias='reportKey')
    event_type: Optional[BaseTBMDSourceEventType] = Field(default=BaseTBMDSourceEventType.timed,
                                                          serialization_alias='eventType')
    type: Optional[BaseTBMDSourceEventType] = Field(default=None)
    is_editable: Optional[bool] = Field(default=True, serialization_alias='isEditable')
    is_creatable: Optional[bool] = Field(default=True, serialization_alias='isCreatable')
    is_deletable: Optional[bool] = Field(default=True, serialization_alias='isDeletable')
    include_in_report: Optional[str] = Field(default=None, serialization_alias='includeInReport')
    promote_on_create: Optional[bool] = Field(default=None, serialization_alias='promoteOnCreate')
    select_on_create: Optional[bool] = Field(default=None, serialization_alias='selectOnCreate')
    structure: List[SourceStructureBlock]

    @classmethod
    def sort_key(cls, source: 'BaseTBMDSource') -> int:
        """ Function used with `sorted` to sort list of BaseTBMDSources based on name

        :param source: BaseTBMDSource
        :return: Integer representing order
        """
        order = [
            # Baton automated errors
            'Provider QC Events',

            # Metadata to collect and validate
            'Segmentation',
            'Branding',
            'Credits/Textless Mark',
            'Window of Opportunity',

            # Faults/Issues
            'File Structure Fault',
            'Audio Fault',
            'Captioning Fault',
            'Content / S&P Mark',
            'Text/Graphics Mark',
            'Textless Mark',
            'Timecode Fault',
            'Video Fault',
            'Window of Opportunity Fault',

            # Output sources
            'Assisted QC Technician Review',
            ]
        if source.name not in order:
            raise ValueError(f'Unhandled BaseTBMDSource ({source.name}) in sorting method')
        return order.index(source.name)

