from typing import Any

from pydantic import BaseModel
from starlette.responses import JSONResponse


class PurchaseVerifyRequest(BaseModel):
    productId: str
    purchaseToken: str
    packageName: str

class PurchaseVerifyResponse(BaseModel):
    success: bool
    message: str
    data: dict[str, Any]

