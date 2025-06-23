from datetime import datetime, timezone
from typing import Dict, Any
from google.oauth2 import service_account
from googleapiclient.discovery import build
from app.config import settings

SERVICE_ACCOUNT_FILE = settings.google_service_account_file
SCOPES = ['https://www.googleapis.com/auth/androidpublisher']

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
android_publisher = build('androidpublisher', 'v3', credentials=credentials)

def verify_subscription(package_name: str, subscription_id: str, purchase_token: str):
    try:
        result = android_publisher.purchases().subscriptions().get(
            packageName=package_name,
            subscriptionId=subscription_id,
            token=purchase_token
        ).execute()
        return result
    except Exception as e:
        return {"error": str(e)}

def determine_subscription_status_android(result: Dict[str, Any]) -> str:
    try:
        now = datetime.now(timezone.utc)
        expiry_time = int(result.get("expiryTimeMillis", 0)) / 1000
        is_expired = expiry_time < now.timestamp()
        cancel_reason = result.get("cancelReason")
        auto_renewing = result.get("autoRenewing", False)
        payment_state = result.get("paymentState")
        if payment_state == 1 and not is_expired and auto_renewing:
            return "active"
        elif cancel_reason == 1 and not is_expired:
            return "canceled_but_active"
        elif is_expired:
            return "expired"
        else:
            return "unverified"
    except:
        return "unverified"
