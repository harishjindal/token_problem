from django.shortcuts import render
from django.http import JsonResponse, Http404
from rest_framework.decorators import api_view
from .redis_conn import connection, db2
import uuid


@api_view(['GET'])
def index(request):
    r = connection()
    r2 = db2()
    keyFinal = r.randomkey()
    try:
        if not keyFinal:
            raise Http404
    except Exception as e:
        raise Http404

    r.expire(keyFinal,1)
    r2.setex(keyFinal,60,1)
    return JsonResponse({"Result": "True", "token": keyFinal})


@api_view(['POST'])
def generate_token(request):
    r = connection()
    newToken = str(uuid.uuid4())
    r.setex(newToken,300,1)
    return JsonResponse({"Result": 'True', "Response": "Token Generated"})


@api_view(['POST'])
def keep_alive(request):
    try:
        token = request.POST['token']
        if not token:
            return JsonResponse({"Result": 'False', "Response": "Token must not be empty"})
    except Exception as e:
        return JsonResponse({"Result": 'False', "Response": "Token must not be empty"})

    r = connection()
    r2 = db2()
    response = "Token is available"
    result = "True"
    if r2.expire(token, 60)<1 and r.expire(token,300)<1:
        response = "Token is already expired"
        result = "False"

    return JsonResponse({"Result": result, "Response": response})


@api_view(['DELETE'])
def delete_token(request):
    try:
        token = request.POST['token']
        if not token:
            return JsonResponse({"Result": 'False', "Response": "Token must not be empty"})
    except Exception as e:
        return JsonResponse({"Result": 'False', "Response": "Token must not be empty"})

    r = connection()
    r2 = db2()
    r.expire(token, 1)
    r2.expire(token, 1)
    return JsonResponse({"Result": 'True', "Response": "Token Deleted"})