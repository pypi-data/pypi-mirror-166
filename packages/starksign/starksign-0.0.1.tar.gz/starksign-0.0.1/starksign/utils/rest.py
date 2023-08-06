from .relay import set_relay
from starkcore.utils import rest


get_id = set_relay(rest.get_id)
post_sub_resource = set_relay(rest.post_sub_resource)
