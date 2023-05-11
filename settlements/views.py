from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
import decimal
import json

from .models import Wallet, Settlement


@require_POST
@csrf_exempt
def create_wallet(request, id):
    try:
        wallet = Wallet.objects.get(id=id)
        return JsonResponse({'error': 'Wallet already exists'})
    except Wallet.DoesNotExist:
        wallet = Wallet(id=id)
        wallet.save()
        return JsonResponse({'message': 'Wallet created successfully'})

@require_POST
@csrf_exempt
def initiate_settlement(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'})
    wallet_id = data['wallet_id']
    settlement_type = data['type']
    iban = data['iban']
    amount = data['amount']

    try:
        wallet = Wallet.objects.get(id=wallet_id)
    except Wallet.DoesNotExist:
        return JsonResponse({'error': 'Wallet does not exist'})

    if settlement_type == 'payin':
        wallet.balance += decimal.Decimal(amount)
        wallet.save()
        settlement = Settlement(wallet=wallet, settlement_type='payin', iban=iban, amount=amount)
        settlement.save()
        return JsonResponse({'message': 'Pay-in initiated successfully'})
    elif settlement_type == 'payout':
        print(wallet.balance)
        if wallet.balance < decimal.Decimal(amount):
            return JsonResponse({'error': 'Insufficient funds'})
        else:
            wallet.balance -= decimal.Decimal(amount)
            print(wallet.balance)
            wallet.save()
            settlement = Settlement(wallet=wallet, settlement_type='payout', iban=iban, amount=amount)
            settlement.save()
            return JsonResponse({'message': 'Pay-out initiated successfully'})
    else:
        return JsonResponse({'error': 'Invalid settlement type'})

@require_GET
def get_settlement_events(request, from_id):
    try:
        from_id_int = int(from_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid from ID'})

    events = Settlement.objects.filter(id__gte=from_id_int).order_by('id')
    events_data = []
    for event in events:
        events_data.append({
            'id': event.id,
            'wallet_id': event.wallet.id,
            'timestamp': event.timestamp.isoformat(),
            'settlement_type': event.settlement_type,
            'iban': event.iban,
            'amount': str(event.amount),
            'is_confirmed': event.is_confirmed
        })
    return JsonResponse({'events': events_data})
