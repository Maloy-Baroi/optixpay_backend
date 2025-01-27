from app_sms.models.sms import SMSManagement
from typing import Tuple, Optional

def verify_by_sms(amount: float, txn_id: str, account: str) -> Tuple[bool, Optional[SMSManagement]]:
    sms = SMSManagement.objects.filter(amount=float(amount), txn_id=txn_id, sender=account, status='unclaimed')
    if sms.exists():
        return True, sms.first()
    else:
        return False, None
