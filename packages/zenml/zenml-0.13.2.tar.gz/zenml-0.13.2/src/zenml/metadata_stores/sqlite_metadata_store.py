#  Copyright (c) ZenML GmbH 2020. All Rights Reserved.
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
"""Metadata store for SQLite."""

import os
from pathlib import Path
from typing import Any, ClassVar, Dict, Union

from ml_metadata.proto import metadata_store_pb2
from pydantic import root_validator, validator
from tfx.orchestration import metadata

from zenml.config.global_config import GlobalConfiguration
from zenml.constants import LOCAL_STORES_DIRECTORY_NAME
from zenml.metadata_stores import BaseMetadataStore
from zenml.utils import io_utils


class SQLiteMetadataStore(BaseMetadataStore):
    """SQLite backend for ZenML metadata store."""

    uri: str = ""

    # Class Configuration
    FLAVOR: ClassVar[str] = "sqlite"

    @property
    def local_path(self) -> str:
        """Path to the local directory where the SQLite DB is stored.

        Returns:
            The path to the local directory where the SQLite DB is stored.
        """
        return str(Path(self.uri).parent)

    def get_tfx_metadata_config(
        self,
    ) -> Union[
        metadata_store_pb2.ConnectionConfig,
        metadata_store_pb2.MetadataStoreClientConfig,
    ]:
        """Return tfx metadata config for sqlite metadata store.

        Returns:
            The tfx metadata config.
        """
        return metadata.sqlite_metadata_connection_config(self.uri)

    @root_validator
    def _default_local_uri(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Generates a local SQLite URI if not configured.

        Args:
            values: The values to validate.

        Returns:
            The validated values.
        """
        uri = values.get("uri")
        metadata_store_id = values.get("uuid")
        if uri == "" and metadata_store_id:
            metadata_store_path = os.path.join(
                GlobalConfiguration().config_directory,
                LOCAL_STORES_DIRECTORY_NAME,
                str(metadata_store_id),
            )
            io_utils.create_dir_recursive_if_not_exists(metadata_store_path)
            uri = os.path.join(metadata_store_path, "metadata.db")
            values["uri"] = uri

        return values

    @validator("uri")
    def ensure_uri_is_local(cls, uri: str) -> str:
        """Ensures that the metadata store uri is local.

        Args:
            uri: The metadata store uri.

        Returns:
            The metadata store uri.

        Raises:
            ValueError: If the uri is not local.
        """
        if io_utils.is_remote(uri):
            raise ValueError(
                f"Uri '{uri}' specified for SQLiteMetadataStore is not a "
                f"local uri."
            )

        return uri
