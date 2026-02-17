import os, requests

inquiry_webhook: str|None = os.getenv("INQUIRY_WEBHOOK")
inquiry_webhook_enabled: bool = inquiry_webhook is not None and inquiry_webhook.strip() != ""

def send_inquiry(data) -> None :
	if inquiry_webhook_enabled:
		requests.post(inquiry_webhook, "inquiry form", data)
