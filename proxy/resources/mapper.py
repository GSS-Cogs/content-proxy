import requests
from rdflib import Graph, Dataset

from .database.models import ResourceMapped
from .getter.abstract import BaseLinkObjectsGetter
from .getter.models import LinkObject


class ResourceMapper:
    """
    A thing that maps csvw resources we've created to external
    landing pages we need to insert them into via the proxy
    """

    def __init__(self, metadata_getter):
        self.metdata_links: BaseLinkObjectsGetter = metadata_getter
        self.dataset: Dataset = Dataset()
        self.dataset_url = None

    def set_dataset_from_url(self, url: str):
        self.dataset_url = url
        r: requests.Response = requests.get(url)
        if not r.ok:
            raise Exception(
                "Failed to get response from {url} with status code {r.status_code}"
            )

        # TODO: use tempfile to avoid kruft/overhead
        with open("dump.trig", "wb") as f:
            f.write(r.content)
        self.dataset.parse("dump.trig")

    def create_resource_mapped(self, linked_object: LinkObject) -> (ResourceMapped):
        """
        Create create and return a populated ResourceMapped to create
        a relationship between a given landing page and our
        supplementary resource (dataset(s)) for it.
        """
        self.set_dataset_from_url(linked_object.trig_url)
        resource_mapped = ResourceMapped(
            landing_page=self.get_landing_page(), csvw=linked_object.csvw_url
        )
        return resource_mapped

    def get_landing_page(self):
        """
        Get the distribution object/value from our metadata graph.
        """
        assert self.dataset
        landing_pages = []
        for _, p, o, _ in self.dataset.quads((None, None, None, None)):
            if str(p) == "http://www.w3.org/ns/dcat#landingPage":
                landing_pages.append(str(o))
        assert (
            len(landing_pages) == 1
        ), f"Could not find dcat:landingPage in : {self.dataset_url}"
        return landing_pages[0]

    def get_next_map(self):
        """
        Take a url represeneting metadata and put it in a graph.
        """
        for linked_object in self.metdata_links.get_link_objects():
            yield self.create_resource_mapped(linked_object)
