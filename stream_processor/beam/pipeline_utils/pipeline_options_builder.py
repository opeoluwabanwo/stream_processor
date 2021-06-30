"""Pipeline options builder.

This module is responsible for setting the default and
custom options for beam pipelines.
"""
import re
from datetime import datetime
from os import getenv

from apache_beam.options.pipeline_options import (
    DebugOptions,
    DirectOptions,
    GoogleCloudOptions,
    PipelineOptions,
    SetupOptions,
    StandardOptions,
    WorkerOptions,
)


class BASEPIPELINESETTINGS:
    """Encapsulates baseline project settings."""

    PROJECT = getenv("GCP_PROJECT_ID")
    DF_BUCKET = getenv("GCS_BUCKET_DATAFLOW")
    REGION = getenv("GCP_REGION")
    MACHINE_TYPE = getenv("MACHINE_TYPE")
    RUNNER = getenv("PIPELINE_RUNNER")
    SUBNETWORK = getenv("DATAFLOW_SUBNETWORK")
    SUBNET_PATH = "regions/{REGION}/subnetworks/{SUBNETWORK}"
    SUBNETWORK_FULL = SUBNET_PATH.format(REGION=REGION, SUBNETWORK=SUBNETWORK)
    JOB_NAME = "test"


class BaseOptions(GoogleCloudOptions, StandardOptions, WorkerOptions, SetupOptions):
    """Base pipeline execution options."""

    @classmethod
    def _add_argparse_args(cls, parser):

        parser.add_argument(
            "--df_bucket",
            type=str,
            default=BASEPIPELINESETTINGS.DF_BUCKET,
            help="dataflow bucket for staging",
        )


class PipelineOptionsBuilder:
    """Encapsulates logic for building custom pipeline options."""

    @classmethod
    def build_pipe_options(cls, argv, pipeline_type):
        """Build the baseline options for dataflow.

        Implements the process function which builds the baseline options for
        all pipelines

        Args:
            argv(dict): dictionary of custom defined options
            pipeline_type(str): name of the specific pipeline being executed

        Returns:
            pipeline_options(PipelineOptions): object of PipelineOptions with
            baseline settings

        """
        pipeline_options = PipelineOptions(flags=argv)
        pipeline_options = pipeline_options.view_as(BaseOptions)
        pipeline_options.save_main_session = True
        pipeline_options.setup_file = "./setup.py"
        pipeline_options.use_public_ips = False
        pipeline_options.subnetwork = BASEPIPELINESETTINGS.SUBNETWORK_FULL
        pipeline_options.disk_size_gb = 30
        pipeline_options.machine_type = BASEPIPELINESETTINGS.MACHINE_TYPE
        pipeline_options.view_as(DebugOptions).experiments = [
            "shuffle_mode=service",
            "use_runner_v2",
        ]
        pipeline_options.view_as(DirectOptions).direct_num_workers = 1
        pipeline_options.project = (
            pipeline_options.project or BASEPIPELINESETTINGS.PROJECT
        )
        pipeline_options.job_name = cls._build_dataflow_job_name(
            pipeline_options, pipeline_type
        )
        pipeline_options.region = BASEPIPELINESETTINGS.REGION
        pipeline_options.runner = pipeline_options.runner or BASEPIPELINESETTINGS.RUNNER
        pipeline_options.staging_location = (
            f"gs://{pipeline_options.df_bucket}/staging/"
        )
        pipeline_options.temp_location = f"gs://{pipeline_options.df_bucket}/temp/"
        pipeline_options.streaming = True
        return pipeline_options

    @staticmethod
    def _build_dataflow_job_name(job_options, pipeline_type):
        ts = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")

        job_name = (
            job_options.job_name
            or f"{BASEPIPELINESETTINGS.JOB_NAME}-{pipeline_type}-{ts}"
        )
        base_job_name = str(job_name).replace("_", "-")

        if not re.match(r"^[a-z]([-a-z0-9]*[a-z0-9])?$", base_job_name):
            raise ValueError(
                f"Invalid job_name ({base_job_name}); the name must consist of"
                "only the characters [-a-z0-9], starting with a "
                "letter and ending with a letter or number"
            )

        return base_job_name
