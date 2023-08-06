try:
    from .core import log, aws, tunnel, db
except ImportError:
    from core import log, aws, tunnel, db

try:
    from . import config, io, transform
except ImportError:
    import config, io, transform

session = {}

def useConnection(alias):
    db.session[alias]

def fromDB():
    pass
    