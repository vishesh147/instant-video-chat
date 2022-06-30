from msilib.schema import AppId
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from agora_token_builder import RtcTokenBuilder
import random
import time
import json

from .models import RoomMember
# Create your views here.


def getToken(request):
    appId = "d195c985077f46b084af154d0874eea3"
    appCertificate = "c52b44c8bb094822a000b080cee6d67e"
    roomName = request.GET.get('room')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600*24
    privilegeExpiredTs = time.time() + expirationTimeInSeconds
    role = 1                # 1 = Host, 2 = Guest
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, roomName, uid, role, privilegeExpiredTs)
    return JsonResponse({"token":token, "uid":uid}, safe=False)

def lobby(request):
    return render(request, 'base/lobby.html')

def room(request):
    return render(request, 'base/room.html')

@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    ) 
    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name'],
    )
    member.delete()
    return JsonResponse("Member Deleted", safe=False)
