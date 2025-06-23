from fastapi import APIRouter, HTTPException, status
from app.schemas import PurchaseVerifyRequest, PurchaseVerifyResponse
from app.services import verify_iap_google, verify_iap_ios

router = APIRouter(tags=["Verify In App Purchases"])

@router.post("/verify_purchase", response_model=PurchaseVerifyResponse)
def verify_iap(data: PurchaseVerifyRequest):
    try:
        if data.platform.lower() == "android":
            result = verify_iap_google.verify_subscription(
                package_name=data.packageName,
                subscription_id=data.productId,
                purchase_token=data.purchaseToken,
            )
            subscription_status = verify_iap_google.determine_subscription_status_android(result)
            result["subscriptionStatus"] = subscription_status

        elif data.platform.lower() == "ios":
            result = verify_iap_ios.verify_ios_receipt(
                receipt_data=data.purchaseToken,
                password=data.iosSharedSecret
            )
            subscription_status = verify_iap_ios.determine_subscription_status_ios(result)
            result["subscriptionStatus"] = subscription_status

        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported platform")

        if subscription_status in ["active", "canceled_but_active"]:
            return PurchaseVerifyResponse(success=True, message="Purchase verified successfully.", data=result)

        return PurchaseVerifyResponse(success=False, message="Invalid or expired subscription.", data=result)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error verifying purchase: {str(e)}")
