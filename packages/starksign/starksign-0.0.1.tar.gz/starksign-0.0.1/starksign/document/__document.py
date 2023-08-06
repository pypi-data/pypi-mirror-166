from hashlib import sha256
from ellipticcurve import Ecdsa, PrivateKey
from starkcore.utils.api import from_api_json
from starkcore.utils.resource import Resource
from ..utils import rest
from .signer.__signer import _subresource as _signer_subresource
from .signature.__signature import _subresource as _signature_subresource


class Document(Resource):
    """# Document object
    Documents represent the contracts that should be signed by all parties.
    ## Parameters:
    - content [string]: HTML content of the document. This is also the message that should be signed by the provided ECDSA private key.
    - status [string]: Document status. ex: "pending", "success", "canceled" or "expired"
    - signers [list of document.Signers]: list with parties that are or were expected to sign the contract.
    - signatures [list of document.Signatures]: list with current Signatures the contract has received.
    """

    def __init__(self, id, content, status, signers, signatures):
        Resource.__init__(self, id=id)

        self.content = content
        self.status = status
        self.signers = [from_api_json(resource=_signer_subresource, json=signer) for signer in signers]
        self.signatures = [from_api_json(resource=_signature_subresource, json=signature) for signature in signatures]


_resource = {"class": Document, "name": "Document"}


def get(id):
    """# Retrieve a specific Document
    Receive a single Document object previously created in the Stark Sign API by its id
    ## Parameters (required):
    - id [string]: object unique id. ex: "d186044b38be41598aaccfc5770b991a"
    ## Return:
    - Document object with updated attributes
    """
    return rest.get_id(resource=_resource, id=id)


def sign(id, content, signer_id, private_key=None, token=None):
    """# Sign a specific Document
    Add a Signer's Signature to a specific document. Either a private_key or a token must be informed.
    ## Parameters (required):
    - id [string]: ID of the Document that is being signed. ex: "d186044b38be41598aaccfc5770b991a"
    - content [string]: HTML content of the document that is being signed.
    - signer_id [string]: ID of the document Signer that is creating the Signature. ex: "6785678567856785"
    ## Parameters (conditionally-required):
    - private_key [string]: Private key PEM content that was received on the registered endpoint. Only valid for "server" signatures. ex: "-----BEGIN EC PRIVATE KEY-----\nMHQCAQEEICldfevoktjOcGGbeLZFn4VjmQAI7H4A2o3XwI6nA1mtoAcGBSuBBAAK\noUQDQgAEb0YLOXkxyF266wSD/yA0NBKVclBuyBaIEsvYnT6MCUppngXUMgrzqA+A\nXgUSnsWcPSy+mhnDJF6qtEaXHyoidQ==\n-----END EC PRIVATE KEY-----"
    - token [string]: Token received via email, SMS, etc. by a non-server signer. ex: "a8B1kxJ"
    ## Return:
    - Signature object
    """
    if private_key:
        private_key = PrivateKey.fromPem(private_key)
    if not private_key:
        private_key = PrivateKey(secret=int(sha256(":".join([id, signer_id, token]).encode("utf-8")).hexdigest(), 16))
    return rest.post_sub_resource(
        resource=_resource,
        id=id,
        sub_resource=_signature_subresource,
        entity={
            "signer_id": signer_id,
            "signature": Ecdsa.sign(message=content, privateKey=private_key).toBase64(),
        }
    )
