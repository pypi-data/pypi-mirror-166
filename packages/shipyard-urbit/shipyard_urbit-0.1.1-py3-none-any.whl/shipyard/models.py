from pydantic import BaseModel, AnyUrl


class SshUrl(AnyUrl):
    allowed_schemes = {"ssh"}
    user_required = True


class SshRemote(BaseModel):
    url: SshUrl
