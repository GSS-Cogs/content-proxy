import json
import os
from pathlib import Path

from typing import Union, NoReturn

from .abstract import BaseDataLayer
from .models import ResourceMapped

this_dir = Path(os.path.dirname(os.path.realpath(__file__)))


class JsonDatabase(BaseDataLayer):
    """
    The good old "chuck it all in some json" approach.
    """

    def clear(self) -> (NoReturn):
        """
        Blank any persisting entries from last time.
        """
        db_path = Path(this_dir / "db.json")
        if os.path.exists(db_path):
            os.remove(db_path)

    def insert_mapped_object(self, mapped_object: ResourceMapped) -> (NoReturn):
        """
        Insert a json k,v representing this mapped resource
        """
        db_path = Path(this_dir / "db.json")

        if os.path.exists(db_path):
            with open(db_path) as f:
                db_json = json.load(f)
        else:
            db_json = {}

        db_json[mapped_object.landing_page] = {"csvw": mapped_object.csvw}
        with open(Path(this_dir / "db.json"), "w") as f:
            json.dump(db_json, f)

    def get_mapped_resource_from_landing_page(self, url: str) -> (Union[ResourceMapped, None]):
        """
        Given a url, return an (additional, from us) mapped resource
        to be inserted or none.
        """

        # Only load from disk on the first query
        if not hasattr(self, "db"):
            db_path = Path(this_dir / "db.json")
            with open(db_path) as f:
                self.db = json.load(f)

        resource_mapped_value = self.db.get(url, None)
        if not resource_mapped_value:
            return None

        # Avoid confusion if/when we extend the fields we're tracking
        # beyond just the associated csvw
        assert len(resource_mapped_value) == 1

        return ResourceMapped(
            csvw = resource_mapped_value["csvw"],
            landing_page = url
        )
