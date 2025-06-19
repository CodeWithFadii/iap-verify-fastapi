from pydantic import BaseModel


class PurchaseVerifyRequest(BaseModel):
    productId: str
    purchaseToken: str
    packageName: str