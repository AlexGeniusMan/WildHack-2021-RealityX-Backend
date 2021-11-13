import base64
import datetime
import random
import time

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
from .models import *

import requests

from .ml_engine import search

from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
async def index(request):
    return HttpResponse("Hello, async Django!")


class PredictHintsView(APIView):
    """
    Predict hints
    """

    def post(self, request):
        if (letters := request.data.get('letters')) is None:
            return {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "Field 'letters' is not provided"
            }

        # response = requests.post('http://ml:8080/api/predict', timeout=10000, json={"img_base64": img_base64}).json()

        # print(request.user.is_authenticated)

        start = datetime.datetime.now()

        hints = search(status_autorization=False, query=letters, n_query=10)
        # time.sleep(0.7)
        end = datetime.datetime.now()
        print(end - start)
        # print(hints)

        return Response({
            'status': status.HTTP_200_OK,
            'hints': hints,
            'time': str(end - start)
        })
