from starkcore.utils.resource import Resource
from starkcore.utils.checks import check_datetime


class Signer(Resource):
    """# Signer object
    Signers represent each of the parties that are expected to sign a document.
    ## Parameters:
    - name [string]: Signer's name. ex: Jon Ygritte
    - contact [string]: Signer's contact information. ex: "jon@starksign.com"
    - method [string]: Signer's signature method. ex: "server", "token" or "link"
    - is_sent [bool]: If True, the signer has been notified about the signature request. ex: True
    - status [string]: Signer status. ex: "pending", "success" or "canceled"
    - document_id [string]: ID of the Document that should be signed. ex: "6785678567856785"
    - tags [list of strings, default []]: list of strings for reference when searching for the Signer. ex: tags=["always-on-time"]
    - created [datetime.datetime]: creation datetime of the Signer. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    - updated [datetime.datetime]: latest update datetime for the Signer. ex: datetime.datetime(2020, 3, 10, 10, 30, 0, 0)
    """

    def __init__(self, id, name, contact, method, is_sent, status, document_id, tags, created, updated):
        Resource.__init__(self, id=id)

        self.tags = tags
        self.name = name
        self.contact = contact
        self.method = method
        self.is_sent = is_sent
        self.status = status
        self.document_id = document_id
        self.created = check_datetime(created)
        self.updated = check_datetime(updated)


_subresource = {"class": Signer, "name": "Signer"}
