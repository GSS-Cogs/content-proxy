""" A script that does the actual populating of resources the proxy is aware of """

from proxy.resources.mapper import ResourceMapper
from proxy.drivers import linked_object_getter, db

db.clear()

resource_mapping = ResourceMapper(linked_object_getter)

for mapped_object in resource_mapping.get_next_map():
    db.insert_mapped_object(mapped_object)