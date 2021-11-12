import base64
import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
from .models import *

import requests


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

        hints = [
            'kawd',
            'awd',
            'kawgred',
            'erthwef',
            'esgrth',
            'kawrththed',
            'hrtrhw',
            'lwakladkjwkdjkwadjklwjdkljaklsjdkwajdk',
            '0-aw9d0-98 a8w9890w890w890 89d8w',
            'esre rgerg43 34353453 erf rgregr e324 2344324 ',
        ]

        return Response({
            'status': status.HTTP_200_OK,
            'hints': hints
        })
