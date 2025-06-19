
from google.oauth2 import service_account
from googleapiclient.discovery import build
from app.config import settings

SERVICE_ACCOUNT_FILE = settings.google_service_account_file
SCOPES = ['https://www.googleapis.com/auth/androidpublisher']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

android_publisher = build('androidpublisher', 'v3', credentials=credentials)


def verify_purchase(package_name: str, product_id: str, purchase_token: str):
    try:
        result = android_publisher.purchases().products().get(
            packageName=package_name,
            productId=product_id,
            token=purchase_token
        ).execute()

        return result
    except Exception as e:
        print(f"Google Play verification failed: {e}")
        return None
