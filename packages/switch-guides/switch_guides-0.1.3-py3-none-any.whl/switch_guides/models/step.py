# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


from typing import Any, Optional, Union
from typing import List
from pydantic import BaseModel
from .literals import STATUS_STATE, STATUS_TYPE


class PlatformJourneyStepComponent(BaseModel):
    type: str
    id: str
    attributes: dict


class PlatformJourneyStepCallToAction(BaseModel):
    path: str
    step: Optional[str] = ''
    description: Optional[str] = ''
    autoRedirectOnStepCompletion: Optional[bool] = False


class PlatformJourneyStepStatusProgress(BaseModel):
    """Contains properties that help build the full picture of the status of a step. Not all properties might be relevant for each step.

    Args:
        BaseModel (_type_): Helper type for managing validations and serialization of the model
    """
    count: int = 0
    completionPercentage: int = 0
    numerator: int = 0
    denominator: int = 0


class PlatformJourneyStepData(dict):
    pass


class PlatformJourneyStepStatusUiState(BaseModel):
    """Keep the step locked on the UI when True; otherwise unlock it.
    Attribute relevant for UI
    """
    lockStep: bool = False


class PlatformJourneyStepStatus(BaseModel):
    """Status of the Journey Step
    """

    """Type of status this is. Based on the type different property values would be relevant

    Available types and their relevant properties:

    Percentage
        progress.percentageCompleted    [int]
        messages.default                [str]

    StateBased
        messages.completed      [str]   (when state == Completed)
        messages.pending        [str]   (when state == Pending)
        messages.actionRequired [str]   (when state == ActionRequired)
        messages.failed         [str]   (when state == Failed)

    Count
        progress.count [int]
        messages.count [str]

    Fraction
        progress.numerator   [int]
        progress.denominator [int]
        messages.default     [str]

    Simple
        messages.default     [str]

    """
    type: STATUS_TYPE = 'Percentage'

    """State of the step"""
    state: STATUS_STATE = 'Queued'

    """Messages associated with the step. Contains at least 'default' message"""
    messages: dict = {}

    """Progress data"""
    progress: PlatformJourneyStepStatusProgress = PlatformJourneyStepStatusProgress()

    """UI State
    Dynamically control UI state of the step.
    """
    uiState: PlatformJourneyStepStatusUiState = PlatformJourneyStepStatusUiState()


class PlatformJourneyStepDefinitionUiAssets(BaseModel):
    stepContinueButtonText: str = 'Get Started'


class PlatformJourneyStepDefinition(BaseModel):
    """Shape of the a Step. This defines what a step is and the data is shared by instances of the step.

    Args:
        BaseModel (_type_): Helper type for managing validations and serialization of the model
    """
    stepId: str = ''
    name: str
    description: str
    status: PlatformJourneyStepStatus = PlatformJourneyStepStatus()
    icon: str
    isEnabled: bool = True
    isHidden: bool = False
    callToAction: Union[PlatformJourneyStepCallToAction, None] = None
    component: Union[PlatformJourneyStepComponent, None] = None
    uiAssets: PlatformJourneyStepDefinitionUiAssets = PlatformJourneyStepDefinitionUiAssets()


class PlatformJourneyStepDependencyEvents(BaseModel):
    checkStatusOnJourneyCreation: bool = True
    triggerProcessOnStepCompletion: List[str] = []


class PlatformJourneyStepDependency(BaseModel):
    """Represents the instance of a step where the state might not be the same as other instances of the same step

    Args:
        BaseModel (_type_): Helper type for managing validations and serialization of the model
    """
    stepId: str

    """Order to appear on the Frontend UIs.
        Optional when when Step is marked as a Background Step
    """
    order: Optional[int]

    """When a step depends on another step, the step is only unlocked on UI when the other step is completed.
    """
    dependsOn: List[str] = []

    """Events associated with the step in relation to the journey or other steps within the journey.
    """
    events: PlatformJourneyStepDependencyEvents = PlatformJourneyStepDependencyEvents()

    """When True, step is expected to run on event trigger and will not be returned to the frontend.
    """
    isBackgroundStep: bool = False


class PlatformJourneyStepOverrides(BaseModel):
    """Represents the simplest view of a step. Useful for maintain overrides for the step without duplicating the data.

    Args:
        BaseModel (_type_): Helper type for managing validations and serialization of the model
    """

    stepId: str
    status: PlatformJourneyStepStatus
    component: Union[PlatformJourneyStepComponent, None] = None
    uiAssets: Optional[PlatformJourneyStepDefinitionUiAssets]
    data: Optional[PlatformJourneyStepData] = {}


class PlatformJourneyStep(PlatformJourneyStepDefinition, PlatformJourneyStepDependency):
    """Full Journey Step Model

    Args:
        PlatformJourneyStepDefinition (_type_): Represents the step shape
        PlatformJourneyStepDependency (_type_): Represents the shape of a step within a Journey dependency
    """
    stepId: str
    data: Optional[PlatformJourneyStepData] = {}
