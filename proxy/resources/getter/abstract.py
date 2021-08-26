from abc import ABCMeta, abstractmethod
from typing import List

from .models import LinkObject


class BaseLinkObjectsGetter(metaclass=ABCMeta):
    """
    A thing that gets an object of links we need.
    """

    @abstractmethod
    def get_link_objects() -> (List[LinkObject]):
        """
        Retuns a list of link
        """
        pass
