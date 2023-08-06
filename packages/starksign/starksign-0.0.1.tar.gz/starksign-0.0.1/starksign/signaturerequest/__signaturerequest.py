from ..utils.parse import parse_and_verify
from starkcore.utils.subresource import SubResource


class SignatureRequest(SubResource):
    """# SignatureRequest object
    SignatureRequests are received when a signer with the "server" method is called to sign a specific document.
    You should use the signaturequest.parse() method safely verify if this is a legitimate request and then use its
    information to sign the document, if adequate.
    ## Parameters:
    - signer_id [string]: ID of the document signer that has been requested. ex: "6785678567856785"
    - document_id [string]: ID of the document that is being signed. ex: "5678567856785678"
    - private_key [string]: ECDSA private key generated specifically for the signer to sign this document. ex: "-----BEGIN EC PRIVATE KEY-----\nMHQCAQEEICldfevoktjOcGGbeLZFn4VjmQAI7H4A2o3XwI6nA1mtoAcGBSuBBAAK\noUQDQgAEb0YLOXkxyF266wSD/yA0NBKVclBuyBaIEsvYnT6MCUppngXUMgrzqA+A\nXgUSnsWcPSy+mhnDJF6qtEaXHyoidQ==\n-----END EC PRIVATE KEY-----"
    """

    def __init__(self, signer_id, document_id, private_key):
        self.signer_id = signer_id
        self.document_id = document_id
        self.private_key = private_key


_resource = {"class": SignatureRequest, "name": "SignatureRequest"}


def parse(content, signature):
    """# Create a single verified SignatureRequest object from a content string
    Create a single SignatureRequest object from a content string received from a handler listening at the request url.
    If the provided digital signature does not check out with the StarkSign public key, a
    starksign.error.InvalidSignatureError will be raised.
    ## Parameters (required):
    - content [string]: response content from request received at user endpoint (not parsed)
    - signature [string]: base-64 digital signature received at response header "Digital-Signature"
    ## Parameters (optional):
    - user [Organization/Project object, default None]: Organization or Project object. Not necessary if starksign.user was set before function call.
    ## Return:
    - Parsed SignatureRequest object
    """
    return parse_and_verify(
        content=content,
        signature=signature,
        resource=_resource
    )
