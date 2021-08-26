
# TODO: better, this is nasty
try:
    from resources.database.json import JsonDatabase
except ImportError:
    from proxy.resources.database.json import JsonDatabase

try:   
    from resources.getter.stub import StubLinkObjectsGetter
except ImportError:
    from proxy.resources.getter.stub import StubLinkObjectsGetter

linked_object_getter = StubLinkObjectsGetter()
db = JsonDatabase()
