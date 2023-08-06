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
"""Slack integration for alerter components."""

from typing import List

from zenml.enums import StackComponentType
from zenml.integrations.constants import SLACK
from zenml.integrations.integration import Integration
from zenml.zen_stores.models import FlavorWrapper

SLACK_ALERTER_FLAVOR = "slack"


class SlackIntegration(Integration):
    """Definition of a Slack integration for ZenML.

    Implemented using [Slack SDK](https://pypi.org/project/slack-sdk/).
    """

    NAME = SLACK
    REQUIREMENTS = ["slack-sdk>=3.16.1", "aiohttp>=3.8.1"]

    @classmethod
    def flavors(cls) -> List[FlavorWrapper]:
        """Declare the stack component flavors for the Slack integration.

        Returns:
            List of new flavors defined by the Slack integration.
        """
        return [
            FlavorWrapper(
                name=SLACK_ALERTER_FLAVOR,
                source="zenml.integrations.slack.alerters.slack_alerter.SlackAlerter",
                type=StackComponentType.ALERTER,
                integration=cls.NAME,
            )
        ]


SlackIntegration.check_installation()
