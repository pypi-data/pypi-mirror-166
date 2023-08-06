version = "0.0.1"
language = "en-US"
timeout = 15
environment = None

from starkcore import error

from . import document
from .document.__document import Document

from . import signaturerequest
from .signaturerequest.__signaturerequest import SignatureRequest
