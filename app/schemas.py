from typing import Optional, Dict
from pydantic import BaseModel

class PurchaseVerifyRequest(BaseModel):
    platform: str
    packageName: Optional[str] = None
    productId: str
    purchaseToken: str
    iosSharedSecret: Optional[str] = None

class PurchaseVerifyResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict] = None
