import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# from .tasks import initiate_transfer
import requests
from django.conf import settings
from .models import Transfer


@require_POST
@csrf_exempt
def transfer(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'})
    from_iban = data.get('from_iban')
    to_iban = data.get('to_iban')
    amount = data.get('amount')

    # call Celery task
    initiate_transfer(from_iban, to_iban, amount)

    return JsonResponse({'message': 'Transfer initiated successfully'})

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
