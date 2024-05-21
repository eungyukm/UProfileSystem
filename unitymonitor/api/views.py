from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
import unityprofile.models
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.template import loader
import json
from rest_framework import status

@api_view(['GET'])
def getData(request):
    person = {'name': 'Dennis', 'age': 28}
    return Response(person)


@api_view(['POST'])
def api_profile_result(request):
    # 사용자가 입력한 파라미터를 추출합니다.
    body = json.loads(request.body)
    # print(body)
    # print(request.data)
    device_name = body['device_name']
    profile_count = body['profile_count']
    scene_name = body['scene_name']
    project_name = body['project_name']
    fps = body['fps']
    min_fps = body['min_fps']
    avg_fps = body['avg_fps']
    max_fps = body['max_fps']
    set_pass_call = body['set_pass_call']
    draw_call = body['draw_call']
    tris = body['tris']
    vertices = body['vertices']

    total_memory = body['total_memory']
    system_memory = body['system_memory']
    texture_memory = body['texture_memory']
    mesh_memory = body['mesh_memory']
    # date = body['date']

    user_nickname = body['user_nickname']
    build_version = body['build_version']
    system_os = body['system_os']

    print(fps)
    # print(min_fps)

    profile_data = unityprofile.models.ProfileData()
    profile_data.device_name = device_name
    profile_data.profile_count = profile_count
    profile_data.scene_name = scene_name
    profile_data.project_name = project_name

    profile_data.fps = fps
    profile_data.min_fps = min_fps
    profile_data.avg_fps = avg_fps
    profile_data.max_fps = max_fps

    profile_data.set_pass_call = set_pass_call
    profile_data.draw_call = draw_call
    profile_data.tris = tris
    profile_data.vertices = vertices

    profile_data.total_memory = total_memory
    profile_data.system_memory = system_memory
    profile_data.texture_memory = texture_memory
    profile_data.mesh_memory = mesh_memory

    profile_data.user_nickname = user_nickname
    profile_data.build_version = build_version
    profile_data.system_os = system_os

    profile_data.save()


    # try:
    #     user_model = user_app.models.UserTable.objects.get(user_id=user_id)
    #     # print(user_model)

    #     # 로그인한 사용자와 데이터베이스에서 가져온 데이터의 비밀번호가 같을 경우
    #     if user_pw == user_model.user_pw:
    #         # 로그인에 성공할 경우 세셔에 로그인 여부값을 저장합니다.
    #         res_message = '200'
    #         return Response(res_message, status=status.HTTP_200_OK)
    #     # 비밀번호가 다를 경우
    #     else:
    #         res_message = '210'
    #         return Response(res_message, status=status.HTTP_200_OK)
    # except:
    #     # 아이디가 없는 경우
    #     res_message = '220'
    #     return Response(res_message, status=status.HTTP_200_OK)

    res_message = '200'
    return Response(res_message, status=status.HTTP_200_OK)