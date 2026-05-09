import africastalking

from app.core.config import config
from app.core.logging import logger


class SMSService:
    """Service for sending SMS messages via Africa's Talking."""

    def __init__(self) -> None:
        # Initialize Africa's Talking
        africastalking.initialize(
            username=config.africastalking_username,
            api_key=config.africastalking_api_key
        )
        self.sms = africastalking.SMS

    def send_loan_approval_sms(self, phone_number: str, customer_name: str) -> None:
        """Send SMS notification for loan approval."""
        message = f"Dear {customer_name}, your loan application has been approved. Congratulations!"

        try:
            response = self.sms.send(message, [phone_number])
            logger.info(f"SMS sent successfully to {phone_number}: {response}")
        except Exception as e:
            logger.error(f"Failed to send SMS to {phone_number}: {str(e)}")
            # In production, you might want to implement retry logic or queue failed SMS


# Global SMS service instance
sms_service = SMSService()