from app_sms.models.sms import SMSManagement


def verify_by_sms(amount, txn_id, account):
    sms = SMSManagement.objects.filter(txn_id=txn_id, sender=account, amount=amount, status='Unclaimed')
    if sms.exists():
        return True
    else:
        return False

