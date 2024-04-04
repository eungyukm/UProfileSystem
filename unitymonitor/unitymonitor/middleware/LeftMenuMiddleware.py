from unityprofile.models import DeviceInfo

# 왼쪽 메뉴에 대한 미들웨어
class LeftMenuMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    # 요청 정보 처리를 위해 호출되는 메소드
    def process_request(self, request):
        device_info_query = DeviceInfo.objects.order_by('-device_idx')[:10]

        device_info_list =[]
        for q1 in device_info_query:
            # 리스트에 담는다.
            device_info_list.append(q1)
        
        request.device_info_list = device_info_list
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