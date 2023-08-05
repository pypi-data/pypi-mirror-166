from pydantic import BaseModel


class UserMerchantTransformsGetResponse(BaseModel):
    merchants: list[str]
