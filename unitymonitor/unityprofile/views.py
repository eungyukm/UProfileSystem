from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from unityprofile.models import ProfileData
from .models import DeviceInfo
from .models import ProfileRecord
from .models import ProfileRecordInfo
from datetime import datetime
from django.http import JsonResponse
from datetime import datetime


def index(request):
    queryset = ProfileData.objects.order_by('-profile_idx')[:10]
    
    content_list =[]
    for q1 in queryset:
        # 리스트에 담는다.
        content_list.append(q1)

    render_data = {
        'device' : 'GalaxyS10',
        'content_list': content_list,
    }

    template = loader.get_template('profile.html')
    return HttpResponse(template.render(render_data, request))
    

# profileData를 출력
def profile_page(request):
    device_info_query = DeviceInfo.objects.order_by('-device_idx')[:10]
    profile_data_list = ProfileData.objects.order_by('-profile_idx')
    
    content_list =[]
    for q1 in profile_data_list:
        content_list.append(q1)

    device_info_list =[]
    for q1 in device_info_query:
        device_info_list.append(q1)

    # content_list에 FPS 소수점 둘째 자리까지만 표시
    for content in content_list:
        content.fps = round(content.fps, 2)
        content.min_fps = round(content.min_fps, 2)
        content.avg_fps = round(content.avg_fps, 2)
        content.max_fps = round(content.max_fps, 2)

    # Total Memory GB로 표현 후 소수 셋째 짜리까지만 표시
    for content in content_list:
        content.total_memory = content.total_memory / (1024 * 1024 * 1024)
        content.total_memory = round(content.total_memory, 3)

    # Tris와 Vertex 정수 표현
    for content in content_list:
        content.tris = int(content.tris)
        content.vertices = int(content.vertices)

    render_data = {
        'device' : 'GalaxyS10',
        'device_info_list': device_info_list,
        'content_list': content_list,
    }

    template = loader.get_template('index.html')
    return HttpResponse(template.render(render_data, request))

def main_page(request):
    profile_data_query = ProfileData.objects.order_by('-profile_idx')[:10]

    # profileData 테이블에서 가져온 데이터를 담을 리스트
    profile_data_list = []
    for q1 in profile_data_query:
        profile_data_list.append(q1)

    device_info_list = request.device_info_list
    
    render_data = {
        'device' : 'GalaxyS10',
        'device_info_list': device_info_list,
        'content_list': profile_data_list,
    }


    template = loader.get_template('index.html')
    return HttpResponse(template.render(render_data, request))

# galaxy10profiledata 출력
def galaxy_s10_profiledata(request):
    device_info_query = DeviceInfo.objects.order_by('-device_idx')[:10]
    profile_data_list = ProfileData.objects.filter(device_name='galaxy10').order_by('-profile_idx')[:10]
    
    content_list = [q1 for q1 in profile_data_list]
    device_info_list = [q1 for q1 in device_info_query]

    render_data = {
        'device' : 'Galaxy S10 5G',
        'device_info_list': device_info_list,
        'content_list': content_list,
    }

    template = loader.get_template('index.html')
    return HttpResponse(template.render(render_data, request))

def add_device(request):
    # 새로운 DeviceInfo 객체 생성
    new_device = DeviceInfo(
        device_name='Galaxy S10 5G',
        device_profile_name='galaxy_s10_profiledata'
    )
    # 객체 저장
    new_device.save()

    template = loader.get_template('index.html')
    return HttpResponse(template.render())

# 프로파일 기록 결과 저장하는 페이지
def profile_record_write(request):
    profile_data_list = ProfileData.objects.filter(device_name='galaxy10').order_by('-profile_idx')[:10]
    content_list = [q1 for q1 in profile_data_list]

    render_data = {
        'device' : 'GalaxyS10',
        'content_list': content_list,
    }

    template = loader.get_template('profile_record_form.html')
    return HttpResponse(template.render(render_data, request))

def profile_record_result(request):
    # POST 요청으로 받은 데이터 profile record에 저장
    profile_record_title = request.POST['profile_record_title']
    profile_device_name = request.POST['profile_device_name']
    profile_record_contents = request.POST['profile_record_contents']
    profile_record_start_idx = request.POST['profile_record_start_idx']
    profile_record_end_idx = request.POST['profile_record_end_idx']

    current_date_time = datetime.now()

    # 로그인 했는지 체크
    if 'login_user_name' not in request.session:
        message = f'''
        <script>
            alert('로그인이 필요합니다')
            location.href = '/profile_record_write'
        </script>
        '''
        return HttpResponse(message)

    profile_record_model = ProfileRecordInfo(
        profile_record_title=profile_record_title,
        profile_record_contents=profile_record_contents,
        profile_record_start_idx=profile_record_start_idx,
        date = current_date_time,
        profile_record_end_idx=profile_record_end_idx,
        user_name=request.session['login_user_name']
    )    

    profile_record_model.save()

    # 변수 명 profile_data_list으로 설정하고, ProfileData 테이블에서 device_name이 profile_device_name이고, profile_idx가 profile_record_start_idx와 profile_record_end_idx 사이에 있는 데이터를 가져옴
    profile_data_list = ProfileData.objects.filter(device_name=profile_device_name, profile_idx__gte=profile_record_start_idx, profile_idx__lte=profile_record_end_idx)
    
    # 가져온 프로파일 데이터를 기록된 프로파일로 저장
    for profile_data in profile_data_list:
        profile_record = ProfileRecord(
            profile_count=profile_data.profile_count,
            device_name=profile_data.device_name,
            project_name=profile_data.project_name,
            scene_name=profile_data.scene_name,
            date=profile_data.date,
            fps=profile_data.fps,
            min_fps=profile_data.min_fps,
            avg_fps=profile_data.avg_fps,
            max_fps=profile_data.max_fps,
            set_pass_call=profile_data.set_pass_call,
            draw_call=profile_data.draw_call,
            tris=profile_data.tris,
            vertices=profile_data.vertices,
            total_memory=profile_data.total_memory,
            system_memory=profile_data.system_memory,
            texture_memory=profile_data.texture_memory,
            mesh_memory=profile_data.mesh_memory,
            profile_record_info=profile_record_model
        )
        profile_record.save()

    # ProfileData에서 profile_data_list에 저장된 데이터 제거
    profile_data_list.delete()

    message = f'''
            <script>
                alert('저장되었습니다')
                location.href = '/profile_record_table'
            </script>
            '''
    return HttpResponse(message)

# profile_record_table
def profile_record_table(request):
    profile_record_info_query = ProfileRecordInfo.objects.order_by('-profile_record_info_idx')
    profile_record_list = ProfileRecord.objects.order_by('-profile_record_idx')
    
    content_list =[]
    for q1 in profile_record_list:
        content_list.append(q1)
        
    profile_record_info_list =[]
    for q1 in profile_record_info_query:
        profile_record_info_list.append(q1)

    # date 소수점 표현하지 않음
    for content in profile_record_info_list:
        content.date = content.date.split('.')[0]

    render_data = {
        'device' : 'GalaxyS10',
        'profile_record_info_list': profile_record_info_list,
        'content_list': content_list,
    }

    template = loader.get_template('profile_record_table.html')
    return HttpResponse(template.render(render_data, request))


# profile_record_read
def profile_record_read(request):
    profile_record_info_id = request.GET['profile_record_info_id']
    profile_record_info_query = ProfileRecordInfo.objects.order_by('-profile_record_info_idx')
    profile_record_title = ProfileRecordInfo.objects.get(profile_record_info_idx=profile_record_info_id).profile_record_title
    profile_record_contents = ProfileRecordInfo.objects.get(profile_record_info_idx=profile_record_info_id).profile_record_contents

    # ProfileRecord 테이블에서 profile_record_info_id에 해당하는 데이터를 가져옵니다.
    profile_record_list = ProfileRecord.objects.filter(profile_record_info=profile_record_info_id).order_by('-profile_record_idx')
    
    content_list =[]
    for q1 in profile_record_list:
        content_list.append(q1)

    # content_list에 FPS 소수점 둘째 자리까지만 표시
    for content in content_list:
        content.fps = round(content.fps, 2)
        content.min_fps = round(content.min_fps, 2)
        content.avg_fps = round(content.avg_fps, 2)
        content.max_fps = round(content.max_fps, 2)

    # Total Memory GB로 표현 후 소수 셋째 짜리까지만 표시
    for content in content_list:
        content.total_memory = content.total_memory / (1024 * 1024 * 1024)
        content.total_memory = round(content.total_memory, 3)

    # Tris와 Vertex 정수 표현
    for content in content_list:
        content.tris = int(content.tris)
        content.vertices = int(content.vertices)

    profile_record_info_list =[]
    for q1 in profile_record_info_query:
        profile_record_info_list.append(q1)

    render_data = {
        'device' : 'GalaxyS10',
        'profile_record_info_list': profile_record_info_list,
        'content_list': content_list,
        'profile_record_info_id': profile_record_info_id,
        'profile_record_title': profile_record_title,
        'profile_record_contents': profile_record_contents,
    }

    print(profile_record_info_list)

    template = loader.get_template('profile_record_read.html')
    return HttpResponse(template.render(render_data, request))

# profile_record_update
def profile_record_update(request):
    profile_record_info_id = request.GET['profile_record_info_id']
    profile_record_info_query = ProfileRecordInfo.objects.order_by('-profile_record_info_idx')

    # ProfileRecord 테이블에서 profile_record_info_id에 해당하는 데이터를 가져옵니다.
    profile_record_list = ProfileRecord.objects.filter(profile_record_info=profile_record_info_id).order_by('-profile_record_idx')
    profile_record_title = ProfileRecordInfo.objects.get(profile_record_info_idx=profile_record_info_id).profile_record_title
    profile_record_contents = ProfileRecordInfo.objects.get(profile_record_info_idx=profile_record_info_id).profile_record_contents
    
    content_list =[]
    for q1 in profile_record_list:
        content_list.append(q1)

    # content_list에 FPS 소수점 둘째 자리까지만 표시
    for content in content_list:
        content.fps = round(content.fps, 2)
        content.min_fps = round(content.min_fps, 2)
        content.avg_fps = round(content.avg_fps, 2)
        content.max_fps = round(content.max_fps, 2)

    # Total Memory GB로 표현 후 소수 셋째 짜리까지만 표시
    for content in content_list:
        content.total_memory = content.total_memory / (1024 * 1024 * 1024)
        content.total_memory = round(content.total_memory, 3)

    # Tris와 Vertex 정수 표현
    for content in content_list:
        content.tris = int(content.tris)
        content.vertices = int(content.vertices)

    profile_record_info_list =[]
    for q1 in profile_record_info_query:
        profile_record_info_list.append(q1)

    render_data = {
        'device' : 'GalaxyS10',
        'profile_record_info_list': profile_record_info_list,
        'content_list': content_list,
        'profile_record_info_id': profile_record_info_id,
        'profile_record_title': profile_record_title,
        'profile_record_contents': profile_record_contents,
    }

    template = loader.get_template('profile_record_update.html')
    return HttpResponse(template.render(render_data, request))

# profile_record_update_result
def profile_record_update_result(request):
    # POST 요청으로 받은 데이터 profile record에 저장
    profile_record_info_id = request.POST['profile_record_info_id']
    profile_record_title = request.POST['profile_record_title']
    profile_record_contents = request.POST['profile_record_contents']
    current_date_time = datetime.now()

    # ProfileRecord 테이블에서 profile_record_info_id에 해당하는 데이터를 가져옵니다.
    profile_record_info = ProfileRecordInfo.objects.get(profile_record_info_idx=profile_record_info_id)
    profile_record_info.profile_record_title = profile_record_title
    profile_record_info.profile_record_contents = profile_record_contents
    profile_record_info.date = current_date_time
    profile_record_info.save()

    message = f'''
            <script>
                alert('수정되었습니다')
                location.href = '/profile_record_table'
            </script>
            '''
    return HttpResponse(message)


# live_profile_remove
def live_profile_remove(request):
    profile_data_list_query = ProfileData.objects.all()
    profile_data_list_query.delete()

    message = f'''
        <script>
            alert('삭제되었습니다')
            location.href = '/profile/'
        </script>
         '''
    return HttpResponse(message)

def profile_record_chart(request):
    profile_record_info_id = request.GET.get('profile_record_info_id')
    profile_record_list = ProfileRecord.objects.filter(profile_record_info_id=profile_record_info_id).order_by('profile_count')

    profile_record_title = ProfileRecordInfo.objects.get(profile_record_info_idx=profile_record_info_id).profile_record_title
    profile_record_contents = ProfileRecordInfo.objects.get(profile_record_info_idx=profile_record_info_id).profile_record_contents

    # 차트에 사용할 데이터 리스트 초기화
    profile_counts = []
    fps_values = []

    # 프로필 레코드 정보를 반복하며 데이터 추출
    for record in profile_record_list:
        profile_counts.append(record.profile_count)
        fps_values.append(record.fps)

    # 차트 템플릿에 전달할 컨텍스트 설정
    render_data = {
        'profile_record_info_id': profile_record_info_id,
        'profile_counts': profile_counts,
        'fps_values': fps_values,
        'profile_record_title': profile_record_title,
        'profile_record_contents': profile_record_contents,
    }

    template = loader.get_template('profile_record_charts.html')
    return HttpResponse(template.render(render_data, request))

def profile_record_chart_FPS_data(request):
    profile_record_info_id = request.GET.get('profile_record_info_id')
    profile_record_list = ProfileRecord.objects.filter(profile_record_info_id=profile_record_info_id).order_by('profile_count')

    # 차트에 사용할 데이터 리스트 초기화
    profile_counts = []
    fps_values = []
    profile_scenes = []

    # 프로필 레코드 정보를 반복하며 데이터 추출
    for record in profile_record_list:
        profile_counts.append(record.profile_count)
        fps_values.append(record.fps)

    # profile_counts를 1부터 20까지의 값으로 설정
    max_profile_count = max(profile_counts)
    min_profile_count = min(profile_counts)
    num_intervals = 20
    interval_size = (max_profile_count - min_profile_count) // num_intervals
    profile_counts_avg = [min_profile_count + i * interval_size for i in range(num_intervals)]

    # fps_values도 동일하게 처리
    fps_values_avg = [sum(fps_values[i:i + interval_size]) / interval_size for i in range(0, len(fps_values), interval_size)]

    # 프로필 레코드 정보를 반복하며 scene_name을 추출하는데, num_intervals 간격으로 scene_name을 추출
    for i in range(0, len(profile_record_list), interval_size):
        profile_scenes.append(profile_record_list[i].scene_name)

    # JSON 응답 데이터 구성
    data = {
        'profile_record_info_id': profile_record_info_id,
        'profile_counts': profile_counts_avg,
        'fps_values': fps_values_avg,
        'profile_scenes': profile_scenes,
    }

    # JsonResponse를 사용하여 JSON 응답 생성
    return JsonResponse(data)

def profile_record_chart_Memory_data(request):
    profile_record_info_id = request.GET.get('profile_record_info_id')
    profile_record_list = ProfileRecord.objects.filter(profile_record_info_id=profile_record_info_id).order_by('profile_count')

    # 차트에 사용할 데이터 리스트 초기화
    profile_counts = []
    total_memory_value = []
    profile_scenes = []

    # 프로필 레코드 정보를 반복하며 데이터 추출
    for record in profile_record_list:
        profile_counts.append(record.profile_count)
        total_memory_value.append(record.total_memory)

    # profile_counts를 1부터 20까지의 값으로 설정
    max_profile_count = max(profile_counts)
    min_profile_count = min(profile_counts)
    num_intervals = 20
    interval_size = (max_profile_count - min_profile_count) // num_intervals
    profile_counts_avg = [min_profile_count + i * interval_size for i in range(num_intervals)]

    # fps_values도 동일하게 처리
    memory_values_avg = [sum(total_memory_value[i:i + interval_size]) / interval_size for i in range(0, len(total_memory_value), interval_size)]

    # total_memory_value를 1024 * 1024로 나누어 GB 단위로 변환
    memory_values_avg = [value / (1024 * 1024 * 1024) for value in memory_values_avg]

    # 프로필 레코드 정보를 반복하며 scene_name을 추출하는데, num_intervals 간격으로 scene_name을 추출
    for i in range(0, len(profile_record_list), interval_size):
        profile_scenes.append(profile_record_list[i].scene_name)

    # JSON 응답 데이터 구성
    data = {
        'profile_record_info_id': profile_record_info_id,
        'profile_counts': profile_counts_avg,
        'avg_values': memory_values_avg,
        'profile_scenes': profile_scenes,
    }

    # JsonResponse를 사용하여 JSON 응답 생성
    return JsonResponse(data)

# profile_record_chart_Tris_data
def profile_record_chart_Tris_data(request):
    profile_record_info_id = request.GET.get('profile_record_info_id')
    profile_record_list = ProfileRecord.objects.filter(profile_record_info_id=profile_record_info_id).order_by('profile_count')

    # 차트에 사용할 데이터 리스트 초기화
    profile_counts = []
    tris_values = []
    profile_scenes = []

    # 프로필 레코드 정보를 반복하며 데이터 추출
    for record in profile_record_list:
        profile_counts.append(record.profile_count)
        tris_values.append(record.tris)

    # profile_counts를 1부터 20까지의 값으로 설정
    max_profile_count = max(profile_counts)
    min_profile_count = min(profile_counts)
    num_intervals = 20
    interval_size = (max_profile_count - min_profile_count) // num_intervals
    profile_counts_avg = [min_profile_count + i * interval_size for i in range(num_intervals)]

    # fps_values도 동일하게 처리
    tris_values_avg = [sum(tris_values[i:i + interval_size]) / interval_size for i in range(0, len(tris_values), interval_size)]

    # 프로필 레코드 정보를 반복하며 scene_name을 추출하는데, num_intervals 간격으로 scene_name을 추출
    for i in range(0, len(profile_record_list), interval_size):
        profile_scenes.append(profile_record_list[i].scene_name)

    # JSON 응답 데이터 구성
    data = {
        'profile_record_info_id': profile_record_info_id,
        'profile_counts': profile_counts_avg,
        'avg_values': tris_values_avg,
        'profile_scenes': profile_scenes,
    }

    # JsonResponse를 사용하여 JSON 응답 생성
    return JsonResponse(data)

# profile_record_chart_Vertices_data
def profile_record_chart_Vertices_data(request):
    profile_record_info_id = request.GET.get('profile_record_info_id')
    profile_record_list = ProfileRecord.objects.filter(profile_record_info_id=profile_record_info_id).order_by('profile_count')

    # 차트에 사용할 데이터 리스트 초기화
    profile_counts = []
    vertices_values = []
    profile_scenes = []

    # 프로필 레코드 정보를 반복하며 데이터 추출
    for record in profile_record_list:
        profile_counts.append(record.profile_count)
        vertices_values.append(record.vertices)

    # profile_counts를 1부터 20까지의 값으로 설정
    max_profile_count = max(profile_counts)
    min_profile_count = min(profile_counts)
    num_intervals = 20
    interval_size = (max_profile_count - min_profile_count) // num_intervals
    profile_counts_avg = [min_profile_count + i * interval_size for i in range(num_intervals)]

    # fps_values도 동일하게 처리
    vertices_values_avg = [sum(vertices_values[i:i + interval_size]) / interval_size for i in range(0, len(vertices_values), interval_size)]

    # 프로필 레코드 정보를 반복하며 scene_name을 추출하는데, num_intervals 간격으로 scene_name을 추출
    for i in range(0, len(profile_record_list), interval_size):
        profile_scenes.append(profile_record_list[i].scene_name)

    # JSON 응답 데이터 구성
    data = {
        'profile_record_info_id': profile_record_info_id,
        'profile_counts': profile_counts_avg,
        'avg_values': vertices_values_avg,
        'profile_scenes': profile_scenes,
    }

    # JsonResponse를 사용하여 JSON 응답 생성
    return JsonResponse(data)

# profile_record_chart_DrawCall_data
def profile_record_chart_DrawCall_data(request):
    profile_record_info_id = request.GET.get('profile_record_info_id')
    profile_record_list = ProfileRecord.objects.filter(profile_record_info_id=profile_record_info_id).order_by('profile_count')

    # 차트에 사용할 데이터 리스트 초기화
    profile_counts = []
    draw_call_values = []
    profile_scenes = []

    # 프로필 레코드 정보를 반복하며 데이터 추출
    for record in profile_record_list:
        profile_counts.append(record.profile_count)
        draw_call_values.append(record.draw_call)

    # profile_counts를 1부터 20까지의 값으로 설정
    max_profile_count = max(profile_counts)
    min_profile_count = min(profile_counts)
    num_intervals = 20
    interval_size = (max_profile_count - min_profile_count) // num_intervals
    profile_counts_avg = [min_profile_count + i * interval_size for i in range(num_intervals)]

    # fps_values도 동일하게 처리
    draw_call_values_avg = [sum(draw_call_values[i:i + interval_size]) / interval_size for i in range(0, len(draw_call_values), interval_size)]

    # 프로필 레코드 정보를 반복하며 scene_name을 추출하는데, num_intervals 간격으로 scene_name을 추출
    for i in range(0, len(profile_record_list), interval_size):
        profile_scenes.append(profile_record_list[i].scene_name)

    # JSON 응답 데이터 구성
    data = {
        'profile_record_info_id': profile_record_info_id,
        'profile_counts': profile_counts_avg,
        'avg_values': draw_call_values_avg,
        'profile_scenes': profile_scenes,
    }

    # JsonResponse를 사용하여 JSON 응답 생성
    return JsonResponse(data)

# profile_record_chart_SetPassCall_data
def profile_record_chart_SetPassCall_data(request):
    profile_record_info_id = request.GET.get('profile_record_info_id')
    profile_record_list = ProfileRecord.objects.filter(profile_record_info_id=profile_record_info_id).order_by('profile_count')

    # 차트에 사용할 데이터 리스트 초기화
    profile_counts = []
    set_pass_call_values = []
    profile_scenes = []

    # 프로필 레코드 정보를 반복하며 데이터 추출
    for record in profile_record_list:
        profile_counts.append(record.profile_count)
        set_pass_call_values.append(record.set_pass_call)

    # profile_counts를 1부터 20까지의 값으로 설정
    max_profile_count = max(profile_counts)
    min_profile_count = min(profile_counts)
    num_intervals = 20
    interval_size = (max_profile_count - min_profile_count) // num_intervals
    profile_counts_avg = [min_profile_count + i * interval_size for i in range(num_intervals)]

    # fps_values도 동일하게 처리
    set_pass_call_values_avg = [sum(set_pass_call_values[i:i + interval_size]) / interval_size for i in range(0, len(set_pass_call_values), interval_size)]

    # 프로필 레코드 정보를 반복하며 scene_name을 추출하는데, num_intervals 간격으로 scene_name을 추출
    for i in range(0, len(profile_record_list), interval_size):
        profile_scenes.append(profile_record_list[i].scene_name)

    # JSON 응답 데이터 구성
    data = {
        'profile_record_info_id': profile_record_info_id,
        'profile_counts': profile_counts_avg,
        'avg_values': set_pass_call_values_avg,
        'profile_scenes': profile_scenes,
    }

    # JsonResponse를 사용하여 JSON 응답 생성
    return JsonResponse(data)

# profile_record_chart_TextureMemory_data
def profile_record_chart_TextureMemory_data(request):
    profile_record_info_id = request.GET.get('profile_record_info_id')
    profile_record_list = ProfileRecord.objects.filter(profile_record_info_id=profile_record_info_id).order_by('profile_count')

    # 차트에 사용할 데이터 리스트 초기화
    profile_counts = []
    texture_memory_values = []
    profile_scenes = []

    # 프로필 레코드 정보를 반복하며 데이터 추출
    for record in profile_record_list:
        profile_counts.append(record.profile_count)
        texture_memory_values.append(record.texture_memory)

    # profile_counts를 1부터 20까지의 값으로 설정
    max_profile_count = max(profile_counts)
    min_profile_count = min(profile_counts)
    num_intervals = 20
    interval_size = (max_profile_count - min_profile_count) // num_intervals
    profile_counts_avg = [min_profile_count + i * interval_size for i in range(num_intervals)]

    # fps_values도 동일하게 처리
    texture_memory_values_avg = [sum(texture_memory_values[i:i + interval_size]) / interval_size for i in range(0, len(texture_memory_values), interval_size)]

    # texture_memory_values를 1024 * 1024로 나누어 GB 단위로 변환
    texture_memory_values_avg = [value / (1024 * 1024 * 1024) for value in texture_memory_values_avg]

    # 프로필 레코드 정보를 반복하며 scene_name을 추출하는데, num_intervals 간격으로 scene_name을 추출
    for i in range(0, len(profile_record_list), interval_size):
        profile_scenes.append(profile_record_list[i].scene_name)

    # JSON 응답 데이터 구성
    data = {
        'profile_record_info_id': profile_record_info_id,
        'profile_counts': profile_counts_avg,
        'avg_values': texture_memory_values_avg,
        'profile_scenes': profile_scenes,
    }

    # JsonResponse를 사용하여 JSON 응답 생성
    return JsonResponse(data)

# profile_record_chart_MeshMemory_data
def profile_record_chart_MeshMemory_data(request):
    profile_record_info_id = request.GET.get('profile_record_info_id')
    profile_record_list = ProfileRecord.objects.filter(profile_record_info_id=profile_record_info_id).order_by('profile_count')

    # 차트에 사용할 데이터 리스트 초기화
    profile_counts = []
    mesh_memory_values = []
    profile_scenes = []

    # 프로필 레코드 정보를 반복하며 데이터 추출
    for record in profile_record_list:
        profile_counts.append(record.profile_count)
        mesh_memory_values.append(record.mesh_memory)

    # profile_counts를 1부터 20까지의 값으로 설정
    max_profile_count = max(profile_counts)
    min_profile_count = min(profile_counts)
    num_intervals = 20
    interval_size = (max_profile_count - min_profile_count) // num_intervals
    profile_counts_avg = [min_profile_count + i * interval_size for i in range(num_intervals)]

    # fps_values도 동일하게 처리
    mesh_memory_values_avg = [sum(mesh_memory_values[i:i + interval_size]) / interval_size for i in range(0, len(mesh_memory_values), interval_size)]

    # mesh_memory_values를 1024 * 1024로 나누어 GB 단위로 변환
    mesh_memory_values_avg = [value / (1024 * 1024 * 1024) for value in mesh_memory_values_avg]

    # 프로필 레코드 정보를 반복하며 scene_name을 추출하는데, num_intervals 간격으로 scene_name을 추출
    for i in range(0, len(profile_record_list), interval_size):
        profile_scenes.append(profile_record_list[i].scene_name)

    # JSON 응답 데이터 구성
    data = {
        'profile_record_info_id': profile_record_info_id,
        'profile_counts': profile_counts_avg,
        'avg_values': mesh_memory_values_avg,
        'profile_scenes': profile_scenes,
    }

    # JsonResponse를 사용하여 JSON 응답 생성
    return JsonResponse(data)

# profile_fps_donut_chart_data
def profile_fps_donut_chart_data(request):
    profile_record_info_id = request.GET.get('profile_record_info_id')
    profile_record_list = ProfileRecord.objects.filter(profile_record_info_id=profile_record_info_id).order_by('profile_count')

    # 씬 이름을 기준으로 FPS의 평균값을 계산
    scene_fps_avg = {}
    for record in profile_record_list:
        if record.scene_name == 'SceneIntro':
            continue
        elif record.scene_name == 'SceneLoading':
            continue
        elif record.scene_name not in scene_fps_avg:
            scene_fps_avg[record.scene_name] = [record.fps]
        else:
            scene_fps_avg[record.scene_name].append(record.fps)
    
    # 차트에 사용할 데이터 리스트 초기화
    profile_scenes = []
    fps_values = []

    # profile_scenes 설정
    profile_scenes = list(scene_fps_avg.keys())

    # fps_values 설정
    fps_values = [sum(scene_fps_avg[scene_name]) / len(scene_fps_avg[scene_name]) for scene_name in profile_scenes]

    # JSON 응답 데이터 구성
    data = {
        'profile_record_info_id': profile_record_info_id,
        'scene_fps_avg': scene_fps_avg,
        'profile_scenes': profile_scenes,
        'avg_values': fps_values,
    }

    # JsonResponse를 사용하여 JSON 응답 생성
    return JsonResponse(data)

# profile_total_memory_donut_chart_data
def profile_total_memory_donut_chart_data(request):
    profile_record_info_id = request.GET.get('profile_record_info_id')
    profile_record_list = ProfileRecord.objects.filter(profile_record_info_id=profile_record_info_id).order_by('profile_count')

    # 씬 이름을 기준으로 total_memory의 평균값을 계산
    scene_total_memory_avg = {}
    for record in profile_record_list:
        if record.scene_name == 'SceneIntro':
            continue
        elif record.scene_name == 'SceneLoading':
            continue
        elif record.scene_name not in scene_total_memory_avg:
            scene_total_memory_avg[record.scene_name] = [record.total_memory]
        else:
            scene_total_memory_avg[record.scene_name].append(record.total_memory)
    
    # 차트에 사용할 데이터 리스트 초기화
    profile_scenes = []
    total_memory_values = []

    # profile_scenes 설정
    profile_scenes = list(scene_total_memory_avg.keys())

    # total_memory_values 설정
    total_memory_values = [sum(scene_total_memory_avg[scene_name]) / len(scene_total_memory_avg[scene_name]) for scene_name in profile_scenes]

    # total_memory_values를 1024 * 1024로 나누어 GB 단위로 변환
    total_memory_values = [value / (1024 * 1024 * 1024) for value in total_memory_values]

    # JSON 응답 데이터 구성
    data = {
        'profile_record_info_id': profile_record_info_id,
        'scene_total_memory_avg': scene_total_memory_avg,
        'profile_scenes': profile_scenes,
        'avg_values': total_memory_values,
    }

    # JsonResponse를 사용하여 JSON 응답 생성
    return JsonResponse(data)

# profile_tris_donut_chart_data
def profile_tris_donut_chart_data(request):
    profile_record_info_id = request.GET.get('profile_record_info_id')
    profile_record_list = ProfileRecord.objects.filter(profile_record_info_id=profile_record_info_id).order_by('profile_count')

    # 씬 이름을 기준으로 tris의 평균값을 계산
    scene_tris_avg = {}
    for record in profile_record_list:
        if record.scene_name == 'SceneIntro':
            continue
        elif record.scene_name == 'SceneLoading':
            continue
        elif record.scene_name not in scene_tris_avg:
            scene_tris_avg[record.scene_name] = [record.tris]
        else:
            scene_tris_avg[record.scene_name].append(record.tris)
    
    # 차트에 사용할 데이터 리스트 초기화
    profile_scenes = []
    tris_values = []

    # profile_scenes 설정
    profile_scenes = list(scene_tris_avg.keys())

    # tris_values 설정
    tris_values = [sum(scene_tris_avg[scene_name]) / len(scene_tris_avg[scene_name]) for scene_name in profile_scenes]

    # JSON 응답 데이터 구성
    data = {
        'profile_record_info_id': profile_record_info_id,
        'scene_tris_avg': scene_tris_avg,
        'profile_scenes': profile_scenes,
        'avg_values': tris_values,
    }

    # JsonResponse를 사용하여 JSON 응답 생성
    return JsonResponse(data)

# profile_vertices_donut_chart_data
def profile_vertices_donut_chart_data(request):
    profile_record_info_id = request.GET.get('profile_record_info_id')
    profile_record_list = ProfileRecord.objects.filter(profile_record_info_id=profile_record_info_id).order_by('profile_count')

    # 씬 이름을 기준으로 vertices의 평균값을 계산
    scene_vertices_avg = {}
    for record in profile_record_list:
        if record.scene_name == 'SceneIntro':
            continue
        elif record.scene_name == 'SceneLoading':
            continue
        elif record.scene_name not in scene_vertices_avg:
            scene_vertices_avg[record.scene_name] = [record.vertices]
        else:
            scene_vertices_avg[record.scene_name].append(record.vertices)
    
    # 차트에 사용할 데이터 리스트 초기화
    profile_scenes = []
    vertices_values = []

    # profile_scenes 설정
    profile_scenes = list(scene_vertices_avg.keys())

    # vertices_values 설정
    vertices_values = [sum(scene_vertices_avg[scene_name]) / len(scene_vertices_avg[scene_name]) for scene_name in profile_scenes]

    # JSON 응답 데이터 구성
    data = {
        'profile_record_info_id': profile_record_info_id,
        'scene_vertices_avg': scene_vertices_avg,
        'profile_scenes': profile_scenes,
        'avg_values': vertices_values,
    }

    # JsonResponse를 사용하여 JSON 응답 생성
    return JsonResponse(data)

# profile_texture_memory_donut_chart_data
def profile_texture_memory_donut_chart_data(request):
    profile_record_info_id = request.GET.get('profile_record_info_id')
    profile_record_list = ProfileRecord.objects.filter(profile_record_info_id=profile_record_info_id).order_by('profile_count')

    # 씬 이름을 기준으로 texture_memory의 평균값을 계산
    scene_texture_memory_avg = {}
    for record in profile_record_list:
        if record.scene_name == 'SceneIntro':
            continue
        elif record.scene_name == 'SceneLoading':
            continue
        elif record.scene_name not in scene_texture_memory_avg:
            scene_texture_memory_avg[record.scene_name] = [record.texture_memory]
        else:
            scene_texture_memory_avg[record.scene_name].append(record.texture_memory)
    
    # 차트에 사용할 데이터 리스트 초기화
    profile_scenes = []
    texture_memory_values = []

    # profile_scenes 설정
    profile_scenes = list(scene_texture_memory_avg.keys())

    # texture_memory_values 설정
    texture_memory_values = [sum(scene_texture_memory_avg[scene_name]) / len(scene_texture_memory_avg[scene_name]) for scene_name in profile_scenes]

    # texture_memory_values를 1024 * 1024로 나누어 GB 단위로 변환
    texture_memory_values = [value / (1024 * 1024 * 1024) for value in texture_memory_values]

    # JSON 응답 데이터 구성
    data = {
        'profile_record_info_id': profile_record_info_id,
        'scene_texture_memory_avg': scene_texture_memory_avg,
        'profile_scenes': profile_scenes,
        'avg_values': texture_memory_values,
    }

    # JsonResponse를 사용하여 JSON 응답 생성
    return JsonResponse(data)

# profile_mesh_memory_donut_chart_data
def profile_mesh_memory_donut_chart_data(request):
    profile_record_info_id = request.GET.get('profile_record_info_id')
    profile_record_list = ProfileRecord.objects.filter(profile_record_info_id=profile_record_info_id).order_by('profile_count')

    # 씬 이름을 기준으로 mesh_memory의 평균값을 계산
    scene_mesh_memory_avg = {}
    for record in profile_record_list:
        if record.scene_name == 'SceneIntro':
            continue
        elif record.scene_name == 'SceneLoading':
            continue
        elif record.scene_name not in scene_mesh_memory_avg:
            scene_mesh_memory_avg[record.scene_name] = [record.mesh_memory]
        else:
            scene_mesh_memory_avg[record.scene_name].append(record.mesh_memory)
    
    # 차트에 사용할 데이터 리스트 초기화
    profile_scenes = []
    mesh_memory_values = []

    # profile_scenes 설정
    profile_scenes = list(scene_mesh_memory_avg.keys())

    # mesh_memory_values 설정
    mesh_memory_values = [sum(scene_mesh_memory_avg[scene_name]) / len(scene_mesh_memory_avg[scene_name]) for scene_name in profile_scenes]

    # mesh_memory_values를 1024 * 1024로 나누어 GB 단위로 변환
    mesh_memory_values = [value / (1024 * 1024 * 1024) for value in mesh_memory_values]

    # JSON 응답 데이터 구성
    data = {
        'profile_record_info_id': profile_record_info_id,
        'scene_mesh_memory_avg': scene_mesh_memory_avg,
        'profile_scenes': profile_scenes,
        'avg_values': mesh_memory_values,
    }

    # JsonResponse를 사용하여 JSON 응답 생성
    return JsonResponse(data)

# profile_draw_call_donut_chart_data
def profile_draw_call_donut_chart_data(request):
    profile_record_info_id = request.GET.get('profile_record_info_id')
    profile_record_list = ProfileRecord.objects.filter(profile_record_info_id=profile_record_info_id).order_by('profile_count')

    # 씬 이름을 기준으로 draw_call의 평균값을 계산
    scene_draw_call_avg = {}
    for record in profile_record_list:
        if record.scene_name == 'SceneIntro':
            continue
        elif record.scene_name == 'SceneLoading':
            continue
        elif record.scene_name not in scene_draw_call_avg:
            scene_draw_call_avg[record.scene_name] = [record.draw_call]
        else:
            scene_draw_call_avg[record.scene_name].append(record.draw_call)
    
    # 차트에 사용할 데이터 리스트 초기화
    profile_scenes = []
    draw_call_values = []

    # profile_scenes 설정
    profile_scenes = list(scene_draw_call_avg.keys())

    # draw_call_values 설정
    draw_call_values = [sum(scene_draw_call_avg[scene_name]) / len(scene_draw_call_avg[scene_name]) for scene_name in profile_scenes]

    # JSON 응답 데이터 구성
    data = {
        'profile_record_info_id': profile_record_info_id,
        'scene_draw_call_avg': scene_draw_call_avg,
        'profile_scenes': profile_scenes,
        'avg_values': draw_call_values,
    }

    # JsonResponse를 사용하여 JSON 응답 생성
    return JsonResponse(data)

# profile_set_pass_call_donut_chart_data
def profile_set_pass_call_donut_chart_data(request):
    profile_record_info_id = request.GET.get('profile_record_info_id')
    profile_record_list = ProfileRecord.objects.filter(profile_record_info_id=profile_record_info_id).order_by('profile_count')

    # 씬 이름을 기준으로 set_pass_call의 평균값을 계산
    scene_set_pass_call_avg = {}
    for record in profile_record_list:
        if record.scene_name == 'SceneIntro':
            continue
        elif record.scene_name == 'SceneLoading':
            continue
        elif record.scene_name not in scene_set_pass_call_avg:
            scene_set_pass_call_avg[record.scene_name] = [record.set_pass_call]
        else:
            scene_set_pass_call_avg[record.scene_name].append(record.set_pass_call)
    
    # 차트에 사용할 데이터 리스트 초기화
    profile_scenes = []
    set_pass_call_values = []

    # profile_scenes 설정
    profile_scenes = list(scene_set_pass_call_avg.keys())

    # set_pass_call_values 설정
    set_pass_call_values = [sum(scene_set_pass_call_avg[scene_name]) / len(scene_set_pass_call_avg[scene_name]) for scene_name in profile_scenes]

    # JSON 응답 데이터 구성
    data = {
        'profile_record_info_id': profile_record_info_id,
        'scene_set_pass_call_avg': scene_set_pass_call_avg,
        'profile_scenes': profile_scenes,
        'avg_values': set_pass_call_values,
    }

    # JsonResponse를 사용하여 JSON 응답 생성
    return JsonResponse(data)


# profile_record_delete
def profile_record_delete(request):
    # 세션에서 사용자의 정보를 가져와 login_user_permission 3이상인 경우에만 삭제 가능
    login_user_permission = request.session['login_user_permission']
    profile_record_info_id = request.GET['profile_record_info_id']

    if login_user_permission >= 3:
        profile_record_info_query = ProfileRecordInfo.objects.get(profile_record_info_idx=profile_record_info_id)
        profile_record_info_query.delete()
        message = f'''
        <script>
            alert('삭제 되었습니다.')
            location.href = '/profile_record_table/'
        </script>
         '''
        return HttpResponse(message)

    message = f'''
        <script>
            alert('관리자만 삭제할 수 있습니다.')
            location.href = '/profile_record_table/'
        </script>
         '''
    return HttpResponse(message)

def print_device_names(device_info_list):
    # 각 디바이스의 이름을 출력합니다.
    for device_info in device_info_list:
        print(device_info.device_name)
