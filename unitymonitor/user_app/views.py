from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import user_app.models
from django.contrib.auth.hashers import check_password

# Create your views here.
def index(request):
    render_data = {
        'device' : 'GalaxyS10',
    }

    template = loader.get_template('register.html')
    return HttpResponse(template.render(render_data, request))

def join_result(request):
    # 파라미터 데이터를 추출합니다.
    user_name = request.POST['user_name']
    user_email = request.POST['user_email']
    user_pw = request.POST['user_pw']

    # 데이터 저장 처리
    user_model = user_app.models.UserData()
    user_model.user_name = user_name
    user_model.user_email = user_email
    user_model.user_pw = user_pw
    user_model.user_permission = 0
    user_model.save()

    confirm = '''
                <script>
                    alert('가입이 완료되었습니다')
                    location.href = '/profile/'
                </script>
            '''

    return HttpResponse(confirm)

def login(request):
    # 로그인 확인 여부를 나타내는 파라미터를 추출합니다.
    # 지정된 파라미터가 없을 수 도 있다면 get함수를 사용합니다.
    login_chk = request.GET.get('login_chk')
    # print(login_chk)

    render_data = {
        'login_chk': login_chk
    }

    template = loader.get_template('login.html')
    return HttpResponse(template.render(render_data, request))

# 로그인 처리 함수
@csrf_exempt
def login_result(request):
    # 파라미터 데이터를 추출합니다.
    user_email = request.POST.get('user_email')
    user_pw = request.POST.get('user_pw')
    print(user_email)

    # 이메일을 기준으로 사용자 조회
    user = user_app.models.UserData.objects.filter(user_email=user_email).first()

    if user:
        # 사용자가 존재할 때, 비밀번호를 비교합니다.
        if user_pw == user.user_pw:
            # 로그인에 성공할 경우 세션에 로그인 정보를 저장합니다.
            request.session['login_chk'] = True
            request.session['login_user_email'] = user.user_email
            request.session['login_user_name'] = user.user_name
            confirm = '''
                        <script>
                            alert('로그인이 완료되었습니다')
                            location.href = '/profile/'
                        </script>
                    '''
        else:
            # 비밀번호가 일치하지 않을 때의 처리
            confirm = '''
                        <script>
                            alert('비밀번호가 일치하지 않습니다')
                            location.href = '/user/login'
                        </script>
                    '''
    else:
        # 사용자가 존재하지 않을 때의 처리
        confirm = '''
                    <script>
                        alert('존재하지 않는 사용자입니다')
                        location.href = '/user/login'
                    </script>
                '''

    return HttpResponse(confirm)

def logout(request):
    # 세션 영역에 저장되어 있는 로그인 값을 삭제합니다.
    del request.session['login_chk']
    del request.session['login_user_email']

    message = '''
            <script>
                alert('로그아웃 되었습니다.')
                location.href = '/'
            </script>
            '''

    return HttpResponse(message)
