from fastapi import APIRouter, HTTPException, Header, status

from app.config import settings
from app.schemas import PurchaseVerifyRequest, PurchaseVerifyResponse
from app.services.verify_iap import verify_purchase
import logging

router = APIRouter(tags=["In App Purchases"])


@router.post("/verify_purchase", response_model=PurchaseVerifyResponse)
def verify_iap(
        data: PurchaseVerifyRequest,
        x_api_key: str = Header(...),
):

    try:
        if x_api_key != settings.api_secret_key:
            print('invalid')
            raise HTTPException(status_code=403, detail="Unauthorized")

        result = verify_purchase(
            package_name=data.packageName,
            product_id=data.productId,
            purchase_token=data.purchaseToken,
        )

        if result and result.get("purchaseState") == 0:
            return PurchaseVerifyResponse(
                success=True,
                message="Purchase verified successfully",
                data=result,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or unverified purchase.",
            )

    except Exception :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong while verifying the purchase."
        )
