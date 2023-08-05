from pydantic import BaseModel


class MerchantTransformRequest(BaseModel):
    store_name: str
