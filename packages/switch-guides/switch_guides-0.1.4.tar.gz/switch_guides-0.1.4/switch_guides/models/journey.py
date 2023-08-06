# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


from typing import List, Optional, Union
from pydantic import BaseModel
from .literals import STATUS_STATE
from .step import PlatformJourneyStep, PlatformJourneyStepComponent, PlatformJourneyStepDependency, PlatformJourneyStepOverrides


class PlatformJourneyStatus(BaseModel):
    state: STATUS_STATE
    percentageCompleted: int = 0


class PlatformJourneyDefinitionOptions(BaseModel):
    enable_live_notification: bool = False


class PlatformJourneySummaryStepEvents(BaseModel):
    componentOnCompletion: Union[PlatformJourneyStepComponent, None]


class PlatformJourneySummaryStepConfigDefinition(BaseModel):
    events: Optional[PlatformJourneySummaryStepEvents]

class PlatformJourneySummaryStepConfig(BaseModel):
    component: Optional[PlatformJourneyStepComponent]

class PlatformJourneyDefinition(BaseModel):
    id: str = ''
    name: str
    description: str
    instructions: str
    summaryStep: Optional[PlatformJourneySummaryStepConfigDefinition]
    steps: List[PlatformJourneyStepDependency]
    options: Optional[PlatformJourneyDefinitionOptions]


class PlatformJourneyInstance(BaseModel):
    id: str
    status: PlatformJourneyStatus
    steps: List[PlatformJourneyStepOverrides]


class PlatformJourney(PlatformJourneyDefinition, PlatformJourneyInstance, BaseModel):
    id: str
    summaryStep: Optional[PlatformJourneySummaryStepConfig]
    steps: List[PlatformJourneyStep]


class PlatformJourneySummary(BaseModel):
    id: str
    name: str
    createdOnUtc: str
    modifiedOnUtc: str
    description: str
    instructions: str
    status: PlatformJourneyStatus
