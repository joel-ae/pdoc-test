from typing import Any, Dict, List, Optional
from functools import partial

from pydantic import BaseModel, ConfigDict, Field, field_validator

from access_v2_blocks import SourceStructureBlock, SourceStructureBlockType
from access_v2_enums import ReportKey, ReviewStatusOption
from access_v2_sources import BaseTBMDSource, BaseTBMDSourceEventType
from access_v2_pdfTemplate import pdf_jinja_template


def generate_template(template: List[str] = pdf_jinja_template):
    """ Generate a jinja template structure for PDF generation in an Access Work Order

    :param template: Template code in a list format, potentially with excess spacing
    :return: Updated template code list
    """
    template = list(template)
    return [x.strip() for x in template]


class ExtraData(BaseModel):
    """ Model representing additional metadata passed to an Access work order """
    model_config: ConfigDict = ConfigDict(extra='allow')
    include: Dict[ReportKey, Any] = Field(
        default_factory=lambda: {k: True for k in sorted(ReportKey, key=ReportKey.sort_key)})


class OutputPrefs(BaseModel):
    """ Model representing the output preferences passed to an Access work order """
    workorder_outputs: List[BaseTBMDSource] = Field(serialization_alias='workorderOutputs')
    template: List[str] = Field(default_factory=generate_template)
    extra_data: ExtraData = Field(serialization_alias='extraData')

    @field_validator('workorder_outputs')
    @classmethod
    def sort_workorder_outputs(cls, outputs: List[BaseTBMDSource]) -> List[BaseTBMDSource]:
        """ Sort workorder outputs list

        :param outputs: List of BaseTBMDSource objects to sort
        :return: Sorted list of BaseTBMDSource
        """
        return sorted(outputs, key=BaseTBMDSource.sort_key)


class AQCOptions(BaseModel):
    """ Model representing AQCOptions passed to an Access work order """
    reset_project: str = Field(default='always', frozen=True, serialization_alias='resetProject')
    proxy_file_label: Optional[str] = Field(default=None, serialization_alias='proxyFileLabel')
    reference_file_labels: Optional[List[str]] = Field(default=None, serialization_alias='referenceFileLabels')
    use_ppro_api: bool = Field(default=True, frozen=True, serialization_alias='usePProAPI')
    time_based_metadata_sources: List[BaseTBMDSource] = Field(serialization_alias='timeBasedMetadataSources')
    user_prefs: dict = Field(default_factory=lambda: {'hotkeys': []}, serialization_alias='UserPrefs')
    output_prefs: OutputPrefs = Field(serialization_alias='OutputPrefs')
    view_prefs: dict = Field(default_factory=lambda: {'fileIdentifier': 'name'}, serialization_alias='ViewPrefs')

    @field_validator('time_based_metadata_sources')
    @classmethod
    def sort_time_based_metadata_sources(cls, sources: List[BaseTBMDSource]) -> List[BaseTBMDSource]:
        """ Ensure the TBMD Sources are in the same order in every Work Order

        :param sources: List of TBMD Sources
        :return: Sorted list of TBMD Sources
        """
        return sorted(sources, key=BaseTBMDSource.sort_key)


class EDL(BaseModel):
    """ Model representing the EDL options passed to an Access work order """
    label: str


class LegacyAccessWorkOrder(BaseModel):
    """ Model representing the base structure of an Access work order """
    edl: Optional[EDL] = Field(default=None, serialization_alias='EDL', )
    aqc_options: AQCOptions = Field(serialization_alias='AQCOptions')
