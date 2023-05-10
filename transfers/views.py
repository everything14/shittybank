from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .tasks import initiate_transfer


@require_POST
@csrf_exempt
def transfer(request):
    from_iban = request.POST.get('from_iban')
    to_iban = request.POST.get('to_iban')
    amount = request.POST.get('amount')

    # call Celery task
    initiate_transfer.delay(from_iban, to_iban, amount)

    return JsonResponse({'message': 'Transfer initiated successfully'})
