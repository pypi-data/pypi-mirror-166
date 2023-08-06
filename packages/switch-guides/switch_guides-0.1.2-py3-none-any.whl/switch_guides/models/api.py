# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


from typing import List, Optional, Union
import uuid
from pydantic import BaseModel
from .journey import PlatformJourney, PlatformJourneyDefinition, PlatformJourneyInstance
from .step import PlatformJourneyStepComponent, PlatformJourneyStepDefinition, PlatformJourneyStepDefinitionUiAssets, PlatformJourneyStepData, PlatformJourneyStepStatus


class PlatformJourneyExecuteApiInput(BaseModel):
    journeyInstanceId: str
    journeyInstance: PlatformJourneyInstance = None
    journeyDefinition: PlatformJourneyDefinition = None
    journeyStepDefinitions: List[PlatformJourneyStepDefinition] = []
    stepId: str = ''
    data: dict = ''


class PlatformJourneyStepApiResponse(BaseModel):
    data: dict = None
    errorMessage: str = ''
    status: PlatformJourneyStepStatus = None
    uiAssets: PlatformJourneyStepDefinitionUiAssets = None
    component: Union[PlatformJourneyStepComponent, None] = None


class PlatformJourneyApiResponse(BaseModel):
    success: bool = True
    errorMessage: str = ''
    journey: PlatformJourney = None
    journeyInstance: PlatformJourneyInstance = None


class PlatformJourneyFetchApiInput(BaseModel):
    journeyInstance: PlatformJourneyInstance = None
    journeyDefinition: PlatformJourneyDefinition = None
    journeyStepDefinitions: List[PlatformJourneyStepDefinition] = []


class PlatformJourneyFetchApiResponse(BaseModel):
    success: bool = True
    errorMessage: str = ''
    journey: PlatformJourney = None
    journeyInstance: PlatformJourneyInstance = None


class PlatformJourneyStepProcessInput(BaseModel):
    journey_id: uuid.UUID
    stepData: Optional[PlatformJourneyStepData] = {}
