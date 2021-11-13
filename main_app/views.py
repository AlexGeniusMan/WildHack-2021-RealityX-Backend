import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .ml_engine import search


# @csrf_exempt
# async def index(request):
#     return HttpResponse("Hello, async Django!")


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
        if request.user.is_authenticated:
            print('---TRUE')
            hints = search(status_autorization=False, user_id='5c6522a6ee2ea6ddedd1efb3e0f8e7c4', query=letters,
                           n_query=10)
        else:
            print('---FALSE')
            hints = search(status_autorization=False, user_id='', query=letters, n_query=10)
        # time.sleep(0.7)
        end = datetime.datetime.now()
        print(end - start)
        # print(hints)

        return Response({
            'status': status.HTTP_200_OK,
            'hints': hints,
            'time': end - start
        })
