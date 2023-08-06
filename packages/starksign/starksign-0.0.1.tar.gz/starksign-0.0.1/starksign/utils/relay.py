import starksign
from starkcore.user import PublicUser
from starkcore.utils.host import StarkHost


_api_version = "v2"


def set_relay(func):
    def wrapper(*args, **kwargs):
        if not starksign.environment:
            raise AssertionError("An environment ('sandbox' or 'production') must be configured in starksign.environment.")
        kwargs.update({
            "sdk_version": starksign.version,
            "host": StarkHost.sign,
            "api_version": kwargs.get("version") or _api_version,
            "user": PublicUser(environment=starksign.environment),
            "language": kwargs.get("language") or starksign.language,
            "timeout": kwargs.get("timeout") or starksign.timeout,
        })
        return func(*args, **kwargs)
    return wrapper
