#  Copyright (c) ZenML GmbH 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""Implementation of the MLflow experiment tracker for ZenML."""

import os
from typing import Any, ClassVar, Dict, Optional, Tuple

import mlflow  # type: ignore[import]
from mlflow.entities import Experiment  # type: ignore[import]
from mlflow.store.db.db_types import DATABASE_ENGINES  # type: ignore[import]
from pydantic import root_validator, validator

from zenml.artifact_stores import LocalArtifactStore
from zenml.environment import Environment
from zenml.experiment_trackers.base_experiment_tracker import (
    BaseExperimentTracker,
)
from zenml.integrations.mlflow import MLFLOW_MODEL_EXPERIMENT_TRACKER_FLAVOR
from zenml.logger import get_logger
from zenml.repository import Repository
from zenml.stack import StackValidator
from zenml.utils.secret_utils import SecretField

logger = get_logger(__name__)


MLFLOW_TRACKING_USERNAME = "MLFLOW_TRACKING_USERNAME"
MLFLOW_TRACKING_PASSWORD = "MLFLOW_TRACKING_PASSWORD"
MLFLOW_TRACKING_TOKEN = "MLFLOW_TRACKING_TOKEN"
MLFLOW_TRACKING_INSECURE_TLS = "MLFLOW_TRACKING_INSECURE_TLS"

DATABRICKS_HOST = "DATABRICKS_HOST"
DATABRICKS_USERNAME = "DATABRICKS_USERNAME"
DATABRICKS_PASSWORD = "DATABRICKS_PASSWORD"
DATABRICKS_TOKEN = "DATABRICKS_TOKEN"


class MLFlowExperimentTracker(BaseExperimentTracker):
    """Stores Mlflow configuration options.

    ZenML should take care of configuring MLflow for you, but should you still
    need access to the configuration inside your step you can do it using a
    step context:
    ```python
    from zenml.steps import StepContext

    @enable_mlflow
    @step
    def my_step(context: StepContext, ...)
        context.stack.experiment_tracker  # get the tracking_uri etc. from here
    ```

    Attributes:
        tracking_uri: The uri of the mlflow tracking server. If no uri is set,
            your stack must contain a `LocalArtifactStore` and ZenML will
            point MLflow to a subdirectory of your artifact store instead.
        tracking_username: Username for authenticating with the MLflow
            tracking server. When a remote tracking uri is specified,
            either `tracking_token` or `tracking_username` and
            `tracking_password` must be specified.
        tracking_password: Password for authenticating with the MLflow
            tracking server. When a remote tracking uri is specified,
            either `tracking_token` or `tracking_username` and
            `tracking_password` must be specified.
        tracking_token: Token for authenticating with the MLflow
            tracking server. When a remote tracking uri is specified,
            either `tracking_token` or `tracking_username` and
            `tracking_password` must be specified.
        tracking_insecure_tls: Skips verification of TLS connection to the
            MLflow tracking server if set to `True`.
        databricks_host: The host of the Databricks workspace with the MLflow
            managed server to connect to. This is only required if
            `tracking_uri` value is set to `"databricks"`.
    """

    tracking_uri: Optional[str] = None
    tracking_username: Optional[str] = SecretField()
    tracking_password: Optional[str] = SecretField()
    tracking_token: Optional[str] = SecretField()
    tracking_insecure_tls: bool = False
    databricks_host: Optional[str] = None

    # Class Configuration
    FLAVOR: ClassVar[str] = MLFLOW_MODEL_EXPERIMENT_TRACKER_FLAVOR

    @validator("tracking_uri")
    def _ensure_valid_tracking_uri(
        cls, tracking_uri: Optional[str] = None
    ) -> Optional[str]:
        """Ensures that the tracking uri is a valid mlflow tracking uri.

        Args:
            tracking_uri: The tracking uri to validate.

        Returns:
            The tracking uri if it is valid.

        Raises:
            ValueError: If the tracking uri is not valid.
        """
        if tracking_uri:
            valid_schemes = DATABASE_ENGINES + ["http", "https", "file"]
            if not any(
                tracking_uri.startswith(scheme) for scheme in valid_schemes
            ) and not cls.is_databricks_tracking_uri(tracking_uri):
                raise ValueError(
                    f"MLflow tracking uri does not start with one of the valid "
                    f"schemes {valid_schemes} or its value is not set to "
                    f"'databricks'. See "
                    f"https://www.mlflow.org/docs/latest/tracking.html#where-runs-are-recorded "
                    f"for more information."
                )
        return tracking_uri

    @root_validator(skip_on_failure=True)
    def _ensure_authentication_if_necessary(
        cls, values: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Ensures that credentials or a token for authentication exist.

        We make this check when running MLflow tracking with a remote backend.

        Args:
            values: The values to validate.

        Returns:
            The validated values.

        Raises:
            ValueError: If neither credentials nor a token are provided.
        """
        tracking_uri = values.get("tracking_uri")

        if tracking_uri:
            if cls.is_databricks_tracking_uri(tracking_uri):
                # If the tracking uri is "databricks", then we need the databricks
                # host to be set.
                databricks_host = values.get("databricks_host")

                if not databricks_host:
                    raise ValueError(
                        f"MLflow experiment tracking with a Databricks MLflow "
                        f"managed tracking server requires the `databricks_host` "
                        f"to be set in your stack component. To update your "
                        f"component, run `zenml experiment-tracker update "
                        f"{values['name']} --databricks_host=DATABRICKS_HOST` "
                        f"and specify the hostname of your Databricks workspace."
                    )

            if cls.is_remote_tracking_uri(tracking_uri):
                # we need either username + password or a token to authenticate to
                # the remote backend
                basic_auth = values.get("tracking_username") and values.get(
                    "tracking_password"
                )
                token_auth = values.get("tracking_token")

                if not (basic_auth or token_auth):
                    raise ValueError(
                        f"MLflow experiment tracking with a remote backend "
                        f"{tracking_uri} is only possible when specifying either "
                        f"username and password or an authentication token in your "
                        f"stack component. To update your component, run the "
                        f"following command: `zenml experiment-tracker update "
                        f"{values['name']} --tracking_username=MY_USERNAME "
                        f"--tracking_password=MY_PASSWORD "
                        f"--tracking_token=MY_TOKEN` and specify either your "
                        f"username and password or token."
                    )

        return values

    @staticmethod
    def is_remote_tracking_uri(tracking_uri: str) -> bool:
        """Checks whether the given tracking uri is remote or not.

        Args:
            tracking_uri: The tracking uri to check.

        Returns:
            `True` if the tracking uri is remote, `False` otherwise.
        """
        return any(
            tracking_uri.startswith(prefix)
            for prefix in ["http://", "https://"]
        ) or MLFlowExperimentTracker.is_databricks_tracking_uri(tracking_uri)

    @staticmethod
    def is_databricks_tracking_uri(tracking_uri: str) -> bool:
        """Checks whether the given tracking uri is a Databricks tracking uri.

        Args:
            tracking_uri: The tracking uri to check.

        Returns:
            `True` if the tracking uri is a Databricks tracking uri, `False`
            otherwise.
        """
        return tracking_uri == "databricks"

    @staticmethod
    def _local_mlflow_backend() -> str:
        """Gets the local MLflow backend inside the ZenML artifact repository directory.

        Returns:
            The MLflow tracking URI for the local MLflow backend.
        """
        repo = Repository(skip_repository_check=True)  # type: ignore[call-arg]
        artifact_store = repo.active_stack.artifact_store
        local_mlflow_backend_uri = os.path.join(artifact_store.path, "mlruns")
        if not os.path.exists(local_mlflow_backend_uri):
            os.makedirs(local_mlflow_backend_uri)
        return "file:" + local_mlflow_backend_uri

    def get_tracking_uri(self) -> str:
        """Returns the configured tracking URI or a local fallback.

        Returns:
            The tracking URI.
        """
        return self.tracking_uri or self._local_mlflow_backend()

    def configure_mlflow(self) -> None:
        """Configures the MLflow tracking URI and any additional credentials."""
        tracking_uri = self.get_tracking_uri()
        mlflow.set_tracking_uri(tracking_uri)

        if self.is_databricks_tracking_uri(tracking_uri):
            if self.databricks_host:
                os.environ[DATABRICKS_HOST] = self.databricks_host
            if self.tracking_username:
                os.environ[DATABRICKS_USERNAME] = self.tracking_username
            if self.tracking_password:
                os.environ[DATABRICKS_PASSWORD] = self.tracking_password
            if self.tracking_token:
                os.environ[DATABRICKS_TOKEN] = self.tracking_token
        else:
            if self.tracking_username:
                os.environ[MLFLOW_TRACKING_USERNAME] = self.tracking_username
            if self.tracking_password:
                os.environ[MLFLOW_TRACKING_PASSWORD] = self.tracking_password
            if self.tracking_token:
                os.environ[MLFLOW_TRACKING_TOKEN] = self.tracking_token

        os.environ[MLFLOW_TRACKING_INSECURE_TLS] = (
            "true" if self.tracking_insecure_tls else "false"
        )

    def prepare_step_run(self) -> None:
        """Sets the MLflow tracking uri and credentials."""
        self.configure_mlflow()

    def cleanup_step_run(self) -> None:
        """Resets the MLflow tracking uri."""
        mlflow.set_tracking_uri("")

    @property
    def local_path(self) -> Optional[str]:
        """Path to the local directory where the MLflow artifacts are stored.

        Returns:
            None if configured with a remote tracking URI, otherwise the
            path to the local MLflow artifact store directory.
        """
        tracking_uri = self.get_tracking_uri()
        if self.is_remote_tracking_uri(tracking_uri):
            return None
        else:
            assert tracking_uri.startswith("file:")
            return tracking_uri[5:]

    @property
    def validator(self) -> Optional["StackValidator"]:
        """Checks the stack has a `LocalArtifactStore` if no tracking uri was specified.

        Returns:
            An optional `StackValidator`.
        """
        if self.tracking_uri:
            # user specified a tracking uri, do nothing
            return None
        else:
            # try to fall back to a tracking uri inside the zenml artifact
            # store. this only works in case of a local artifact store, so we
            # make sure to prevent stack with other artifact stores for now
            return StackValidator(
                custom_validation_function=lambda stack: (
                    isinstance(stack.artifact_store, LocalArtifactStore),
                    "MLflow experiment tracker without a specified tracking "
                    "uri only works with a local artifact store.",
                )
            )

    @property
    def active_experiment(self) -> Optional[Experiment]:
        """Returns the currently active MLflow experiment.

        Returns:
            The active experiment or `None` if no experiment is active.
        """
        step_env = Environment().step_environment

        if not step_env:
            # we're not inside a step
            return None

        # If using Databricks, then we need to append an slash to the name of
        # the experiment because Databricks needs it to be an absolute path
        # within the Databricks workspace.
        experiment_name = (
            f"/{step_env.pipeline_name}"
            if self.tracking_uri
            and self.is_databricks_tracking_uri(self.tracking_uri)
            else step_env.pipeline_name
        )

        mlflow.set_experiment(experiment_name=experiment_name)
        return mlflow.get_experiment_by_name(experiment_name)

    def _find_active_run(
        self,
    ) -> Tuple[Optional[mlflow.ActiveRun], Optional[str], Optional[str]]:
        """Find the currently active MLflow run.

        Returns:
            The active MLflow run, the experiment id and the run id
        """
        step_env = Environment().step_environment

        if not self.active_experiment or not step_env:
            return None, None, None

        experiment_id = self.active_experiment.experiment_id

        # TODO [ENG-458]: find a solution to avoid race-conditions while
        #  creating the same MLflow run from parallel steps
        runs = mlflow.search_runs(
            experiment_ids=[experiment_id],
            filter_string=f'tags.mlflow.runName = "{step_env.pipeline_run_id}"',
            output_format="list",
        )

        run_id = runs[0].info.run_id if runs else None

        current_active_run = mlflow.active_run()
        if not (
            current_active_run and current_active_run.info.run_id == run_id
        ):
            current_active_run = None

        return current_active_run, experiment_id, run_id

    @property
    def active_run(self) -> Optional[mlflow.ActiveRun]:
        """Returns the currently active MLflow run.

        Returns:
            The active MLflow run.
        """
        step_env = Environment().step_environment
        current_active_run, experiment_id, run_id = self._find_active_run()
        if current_active_run:
            return current_active_run
        else:
            return mlflow.start_run(
                run_id=run_id,
                run_name=step_env.pipeline_run_id,
                experiment_id=experiment_id,
            )

    @property
    def active_nested_run(self) -> Optional[mlflow.ActiveRun]:
        """Returns a nested run in the currently active MLflow run.

        Returns:
            The nested MLflow run.
        """
        step_env = Environment().step_environment
        current_active_run, _, _ = self._find_active_run()
        if current_active_run:
            return mlflow.start_run(run_name=step_env.step_name, nested=True)
        else:
            # Return None
            return current_active_run
