from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from typing import List, Dict, TypeVar, Any

import yaml
from pydantic import Field
from pydantic_yaml import YamlStrEnum

from bigeye_sdk import DatawatchObject
from bigeye_sdk.exceptions.exceptions import BigConfigValidationException
from bigeye_sdk.generated.com.torodata.models.generated import MetricSuiteResponse, Source, CohortDefinition
from bigeye_sdk.log import get_logger
from bigeye_sdk.serializable import File

# TODO: Add error stats to API Execution Messages.
FAILED_API_EXECUTION_MSG = '\nBigConfig plan includes errors and report files have been generated.\n' \
                           '\n-=- Report files -=-\n{report_file_list}'

SUCCESSFUL_API_EXECUTION_MSG = '\nBigConfig plan executed successfully and report files have been generated.\n' \
                               '\n-=- Report files -=-\n{report_file_list}'

FILES_CONTAIN_ERRORS_EXCEPTION_STATEMENT = '\nBigConfig plan includes errors and FIXME files have been generated.\n' \
                                           'Number of Errors: {err_cnt}\n' \
                                           '\n-=- FIXME files -=-\n{fixme_file_list}'

BIGCONFIG_REPORT = TypeVar('BIGCONFIG_REPORT', bound='BigConfigReport')
REPORTS: List[BIGCONFIG_REPORT] = []

log = get_logger(__file__)


def process_reports(output_path: str, sources_ix: Dict[int, Source]):
    report_files = []
    errors_reported = False

    for report in REPORTS:
        file_name = f'{output_path}/{sources_ix[report.source_id].name}_{report.process_stage}.yml'
        report.save(file_name)
        report_files.append(file_name)
        errors_reported = errors_reported or report.has_errors()
        report.log_errors()

    if errors_reported:
        raise BigConfigValidationException(
            FAILED_API_EXECUTION_MSG.format(report_file_list=yaml.safe_dump(report_files))
        )
    else:
        print(
            SUCCESSFUL_API_EXECUTION_MSG.format(report_file_list=yaml.safe_dump(report_files))
        )


class BigConfigReport(File, ABC):
    @classmethod
    @abstractmethod
    def from_datawatch_object(cls, obj: DatawatchObject, source_id: int,
                              process_stage: ProcessStage) -> BIGCONFIG_REPORT:
        pass

    @abstractmethod
    def tot_error_count(self) -> int:
        """returns a total error count for this report."""
        pass

    @abstractmethod
    def log_errors(self):
        pass

    def has_errors(self):
        return self.tot_error_count() > 0

    # TODO
    # @abstractmethod
    # def get_stats(self) -> str:
    #     """Returns string formatted stats for this report."""
    #     pass


def raise_files_contain_error_exception(err_cnt: int, fixme_file_list: List[str]):
    sys.exit(FILES_CONTAIN_ERRORS_EXCEPTION_STATEMENT.format(
        err_cnt=str(err_cnt),
        fixme_file_list=yaml.safe_dump(fixme_file_list)
    ))


class ProcessStage(YamlStrEnum):
    APPLY = 'APPLY'
    PLAN = 'PLAN'


class MetricSuiteReport(BigConfigReport, type='BIG_CONFIG_REPORT'):
    type = 'BIG_CONFIG_REPORT'
    _exclude_defaults = False
    process_stage: ProcessStage
    source_id: int

    row_creation_time_upserted_count: int = 0

    created_metric_count: int = 0
    updated_metric_count: int = 0
    deleted_metric_count: int = 0
    unchanged_metric_count: int = 0

    row_creation_time_upsert_failure_count: int = 0
    metric_application_error_count: int = 0
    invalid_asset_identifier_count: int = 0

    total_error_count: int = 0

    row_creation_time_report: dict = Field(default_factory=lambda: {})

    metric_application_errors: List[dict] = Field(default_factory=lambda: [])
    invalid_asset_identifier_errors: List[dict] = Field(default_factory=lambda: [])

    created_metrics: List[dict] = Field(default_factory=lambda: [])
    updated_metrics: List[dict] = Field(default_factory=lambda: [])
    deleted_metrics: List[dict] = Field(default_factory=lambda: [])
    unchanged_metrics: List[dict] = Field(default_factory=lambda: [])

    def log_errors(self):
        if self.metric_application_errors:
            mae = f"\n-=- Metric Application Errors -=-\n{yaml.safe_dump(self.metric_application_errors)}"
        if self.invalid_asset_identifier_errors:
            mae = f"\n-=- Metric Application Errors -=-\n{yaml.safe_dump(self.invalid_asset_identifier_errors)}"
        if self.row_creation_time_upsert_failure_count:
            mae = f"\n-=- Metric Application Errors -=-\n" \
                  f"{yaml.safe_dump(self.row_creation_time_report.get('row_creation_time_upsert_failures'))}"

    def tot_error_count(self) -> int:
        return self.total_error_count

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.total_error_count = self.row_creation_time_upsert_failure_count \
                                 + self.metric_application_error_count \
                                 + self.invalid_asset_identifier_count
        REPORTS.append(self)

    @classmethod
    def from_datawatch_object(cls, obj: MetricSuiteResponse, source_id: int,
                              process_stage: ProcessStage) -> MetricSuiteReport:
        row_creation_time_upserted_count = 0
        row_creation_time_upsert_failure_count = 0

        if obj.row_creation_time_response:
            row_creation_time_upserted_count = len(obj.row_creation_time_response.columns_set_as_row_creation_time)
            row_creation_time_upsert_failure_count = len(
                obj.row_creation_time_response.row_creation_time_upsert_failures
            )

        metric_application_errors = []

        def is_wildcard_search(cohort: CohortDefinition):
            return '*' in cohort.column_name_pattern or \
                   '*' in cohort.table_name_pattern or \
                   '*' in cohort.schema_name_pattern

        for mae in obj.metric_application_errors:
            if not is_wildcard_search(mae.from_cohort):
                "Only adding error reporting where the metrics were not applied to a asset name containing wild cards." \
                "This reduces the noise around reporting.  Customers will understand that assets matched using wild" \
                "cards are likely to produce invlaid metric applications."

                metric_application_errors.append(mae.to_dict())
                # TODO add validation error.  Problem is that I cannot match back to the full fq pattern.

        invalid_asset_identifier_errors = [ice.to_dict() for ice in obj.invalid_cohort_errors]

        pr = MetricSuiteReport(
            process_stage=process_stage,
            source_id=source_id,
            created_metrics=[i.to_dict() for i in obj.created_metrics],
            updated_metrics=[i.to_dict() for i in obj.updated_metrics],
            deleted_metrics=[i.to_dict() for i in obj.deleted_metrics],
            unchanged_metrics=[i.to_dict() for i in obj.unchanged_metrics],
            metric_application_errors=metric_application_errors,
            invalid_asset_identifier_errors=invalid_asset_identifier_errors,
            created_metric_count=len(obj.created_metrics),
            updated_metric_count=len(obj.updated_metrics),
            deleted_metric_count=len(obj.deleted_metrics),
            unchanged_metric_count=len(obj.unchanged_metrics),
            metric_application_error_count=len(metric_application_errors),
            invalid_asset_identifier_count=len(invalid_asset_identifier_errors),
            row_creation_time_report=obj.row_creation_time_response.to_dict(),
            row_creation_time_upserted_count=row_creation_time_upserted_count,
            row_creation_time_upsert_failure_count=row_creation_time_upsert_failure_count,
        )

        return pr
