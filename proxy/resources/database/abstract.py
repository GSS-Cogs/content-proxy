from abc import ABCMeta, abstractmethod
from typing import List, NoReturn, Union

from .models import ResourceMapped


class BaseDataLayer(metaclass=ABCMeta):
    """
    A thing that we put mapped resource into and get mapped resources
    out of.
    """

    @abstractmethod
    def clear(self) -> (NoReturn):
        """
        Blank any persisting entries from last time.
        """
        pass

    @abstractmethod
    def insert_mapped_object(self, mapped_object: ResourceMapped) -> (NoReturn):
        """
        Add a thing represenging a mapped resource into whatever
        our data persisting solution is.
        """
        pass

    @abstractmethod
    def find_map_from_landing_page(self, url: str) -> (Union[ResourceMapped, None]):
        """
        Given a url, return an (additional, from us) mapped resource
        to be inserted or none.
        """
