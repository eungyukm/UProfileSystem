from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from unityprofile.models import DeviceInfo

class TopMenuMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    # 요청 정보 처리를 위해 호출되는 메소드
    def process_request(self, request):
        return None

    # 응답 처리를 위해 호출되는 메소드
    def process_response(self, request, response):
        return response

    # 미들웨어 동작 코드
    def __call__(self, request):
        response = self.process_request(request)

        if response is None:
            response = self.get_response(request)

        response = self.process_response(request, response)
        return response