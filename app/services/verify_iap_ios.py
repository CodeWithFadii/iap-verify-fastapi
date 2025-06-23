import requests
from typing import Dict
from app.config import settings
from datetime import datetime, timezone

def verify_ios_receipt(receipt_data: str, password: str) -> Dict:
    url = "https://buy.itunes.apple.com/verifyReceipt"
    payload = {
        "receipt-data": receipt_data,
        "password": password
    }
    response = requests.post(url, json=payload)
    result = response.json()

    if result.get("status") == 21007:
        sandbox_url = "https://sandbox.itunes.apple.com/verifyReceipt"
        response = requests.post(sandbox_url, json=payload)
        result = response.json()

    print("🍏 Apple receipt verification response:", result)
    return result

def determine_subscription_status_ios(result: Dict) -> str:
    try:
        latest_receipt_info = result.get("latest_receipt_info", [])
        if not latest_receipt_info:
            return "unverified"
        latest = sorted(latest_receipt_info, key=lambda x: x["expires_date_ms"], reverse=True)[0]
        expiry = int(latest["expires_date_ms"]) / 1000
        now = datetime.now(timezone.utc).timestamp()
        if expiry > now:
            return "active"
        return "expired"
    except:
        return "unverified"
