from abc import ABC, abstractmethod
import uuid


class JourneyTask(ABC):
    """An Abstract Base Class called Task.

    Attributes
    ----------
    id : uuid.UUID
        Unique identifier of the task. This is an abstract property that needs to be overwritten when sub-classing.
        A new unique identifier can be created using uuid.uuid4()
    description : str
        Brief description of the task
    mapping_entities : List[MAPPING_ENTITIES]
        The type of entities being mapped. An example is:

        ``['Installations', 'Devices', 'Sensors']``
    author : str
        The author of the task.
    version : str
        The version of the task.

    """

    @property
    @abstractmethod
    def id(self) -> uuid.UUID:
        """Unique identifier of the task. Create a new unique identifier using uuid.uuid4() """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Brief description of the task"""
        pass

    @property
    @abstractmethod
    def author(self) -> str:
        """"The author of the task."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """The version of the task"""
        pass