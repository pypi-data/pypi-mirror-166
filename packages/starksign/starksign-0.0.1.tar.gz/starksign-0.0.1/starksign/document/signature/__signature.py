from starkcore.utils.checks import check_datetime
from starkcore.utils.subresource import SubResource


class Signature(SubResource):
    """# Signature object
    Whenever a Document is signed by any of its Signers, a document Signature object is registered.
    When all Signatures are received, the Document status changes to "success".
    ## Parameters:
    - signer_id [string]: ID of the document signer that has created this Signature. ex: "6785678567856785"
    - name [string]: Document signer's name. ex: name="Edward Stark"
    - contact [string]: signer's contact information. ex: "tony@starkinfra.com"
    - signature [string]: base-64 ECDSA digital signature generated to sign the document. ex: "MEUCIQD6cymQq40/06XuIelkv2t9qd9rPACooRH8faCB8SuPIQIgOqIil/1Vm/jni8eTDsoO5ytdoDitZocm3KSLzUYHCrQ\u003d"
    - public_key [string]: public key that was used to validate the signature against the HTML content of the document. ex: "-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEgHEBU5JNNgoJ1pWNUaEM7PvRbDvvNw3W\n+rZPqVhor/2vEqB5+fpYjTQp3EdGlKtEtSizeHsL9Vwm5MSt3CQrzA\u003d\u003d\n-----END PUBLIC KEY-----"
    - ip [string]: IP that sent the signature to Stark Infra. ex: "2804:14c:6a:85d3:b8a3:ddb4:a4e9:e11e"
    - created [datetime.datetime]: creation datetime for the Signature. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, signer_id, name, contact, signature, public_key, ip, created):
        self.signer_id = signer_id
        self.name = name
        self.contact = contact
        self.signature = signature
        self.public_key = public_key
        self.ip = ip
        self.created = check_datetime(created)


_subresource = {"class": Signature, "name": "Signature"}
