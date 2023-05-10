from celery import shared_task
import requests
from django.conf import settings

from .models import Transfer


@shared_task
def initiate_transfer(from_iban, to_iban, amount):
    transfer = Transfer.objects.create(
        from_iban=from_iban,
        to_iban=to_iban,
        amount=amount,
        status='initiated'
    )

    # initiate payout
    response = requests.post(settings.SETTLEMENTS_API_BASE_URL + 'settle/', json={
        'wallet_id': from_iban,
        'type': 'payout',
        'iban': from_iban,
        'amount': amount
    })
    if response.status_code != 200:
        # update transfer status
        transfer.status = 'failed'
        transfer.save()
        return {'error': 'Payout failed'}

    # initiate payin
    response = requests.post(settings.SETTLEMENTS_API_BASE_URL + 'settle/', json={
        'wallet_id': to_iban,
        'type': 'payin',
        'iban': to_iban,
        'amount': amount
    })
    if response.status_code != 200:
        # update transfer status
        transfer.status = 'failed'
        transfer.save()
        return {'error': 'Payin failed'}

    # update transfer status
    transfer.status = 'completed'
    transfer.save()

    return {'message': 'Transfer initiated successfully'}
