from fastapi import APIRouter, HTTPException
from starlette import status

from app.schemas import PurchaseVerifyRequest
from app.services.verify_iap import verify_purchase

router = APIRouter(tags=["In App Purchases"])


# Existing login route
@router.post("/verify_purchase")
def verify_iap(data: PurchaseVerifyRequest):
    result = verify_purchase(
        package_name=data.packageName,
        product_id=data.productId,
        purchase_token=data.purchaseToken,
    )

    if result and result.get("purchaseState") == 0:  # 0 = Purchased
        return {"success": True, "message": "Purchase verified", "data": result}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or unverified purchase.")