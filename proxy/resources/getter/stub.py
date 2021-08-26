from typing import List

from .abstract import BaseLinkObjectsGetter
from .models import LinkObject


class StubLinkObjectsGetter(BaseLinkObjectsGetter):
    """
    A thing that gets metadata resources.
    """

    def get_link_objects(self) -> (List[LinkObject]):
        """
        Retuns a hard coded list of LinkObjects
        """
        return [
            LinkObject(
                trig_url="https://ci.floop.org.uk/job/GSS_data/job/EDVP/job/BEIS-RHI-monthly-deployment-data-Month-Year-Annual-edition/lastSuccessfulBuild/artifact/datasets/BEIS-RHI-monthly-deployment-data-Month-Year-Annual-edition/out/rhi-deployment-data-application-numbers-domestic-and-non-domestic.csv-metadata.trig",
                csvw_url="https://ci.floop.org.uk/job/GSS_data/job/EDVP/job/BEIS-RHI-monthly-deployment-data-Month-Year-Annual-edition/lastSuccessfulBuild/artifact/datasets/BEIS-RHI-monthly-deployment-data-Month-Year-Annual-edition/out/rhi-deployment-data-application-numbers-domestic-and-non-domestic.csv-metadata.json",
            )
        ]
