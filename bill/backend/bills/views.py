# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .utils import generate_bills


# class BillViewSet(APIView):
#     def get(self, request):
#         return Response([x.to_dict() for x in generate_bills(50)])


from django.http import JsonResponse #, HttpResponse
from .models import Bill
from .models import Instalment
from .serializers import BillSerializer
from .serializers import InstalmentSerializer
from asgiref.sync import sync_to_async

async def get_bill(request, id):
    try:
        bill = await Bill.objects.aget(pk=id)
        serializer_data = await sync_to_async(lambda: BillSerializer(bill).data)()
        return JsonResponse(serializer_data)
    except Bill.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

async def get_bills(request):
    limit = int(request.GET.get("limit", 10))
    
    # the last cursor where the next batch needs to be greater
    cursor = request.GET.get("cursor")
    
    qs = Bill.objects.all()

    # cursor is provided, filter with id greater than 
    if cursor:
        qs = qs.filter(id__gt=cursor)

    # apply limit
    qs = qs[:limit]
    bills = [bill async for bill in qs]
    serializer_data = await sync_to_async(lambda: BillSerializer(bills, many=True).data)()

    # access last bill if available
    next_cursor = bills[-1].id if bills else None

    return JsonResponse({
        "results": serializer_data,
        "next_cursor": next_cursor
    })
    
async def get_instalments(request, bill_id):
   
    limit = int(request.GET.get("limit", 10))
    # the last cursor where the next batch needs to be greater
    cursor = request.GET.get("cursor")
    
    qs = Instalment.objects.filter(bill_id=bill_id)

    # cursor is provided, filter with id greater than 
    if cursor:
        qs = qs.filter(id__gt=cursor)

    # apply limit
    qs = qs[:limit]
    instalments = [instalment async for instalment in qs]
    serializer = InstalmentSerializer(instalments, many=True)

    # access last instalment if available
    next_cursor = instalments[-1].id if instalments else None

    return JsonResponse({
        "results": serializer.data,
        "next_cursor": next_cursor
    })
   
async def get_all_bill_instalments(request, bill_id):
    qs = Instalment.objects.filter(bill_id=bill_id)
    instalments = [instalment async for instalment in qs]
    serializer = InstalmentSerializer(instalments, many=True)
    
    return JsonResponse({
        "results": serializer.data,
    })