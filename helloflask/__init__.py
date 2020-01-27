# -*- coding: utf-8 -*- 

from flask import Flask, g, request, Response, make_response
from flask import session, render_template, Markup
from datetime import datetime, date, timedelta

# ascii 에러(128)가 나서 추가한 코드!
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Flask(app_name)
app = Flask(__name__) 
app.debug = True
#app.jinja_env.trim_blocks = True


app.config.update(
    SECRET_KEY='X1243yRH!mMwf', #암호화 키
    SESSION_COOKIE_NAME='pyweb_flask_session', 
    PERMANENT_SESSION_LIFETIME=timedelta(31) # 31days
)

@app.route('/main')
def main():
    return render_template('main.html')

# # 이거는 highchart 사용 예제!
# @app.route('/chart')
# def main2():
#     return render_template('chart.html')

@app.route('/')
def idx():
    return render_template('app.html')

@app.route('/top100')
def top100():
    return render_template('application.html', title="MAIN!!")

@app.route("/tmpl")
def t():
    # 많이 사용되는것은 모듈화
    tit = Markup("<strong>Title</strong")
    mu = Markup("<h1>iii = <i>%s</i></h1>")
    h = mu % "Italic"
    print("h=",h)

    return render_template('index.html', title=tit, mu=h)



@app.route('/tmpl2')
def tmpl2():
    a = (1, "psycho", "레드벨벳", False, [])
    b = (2, "아무노래", "지코", True, [a])
    c = (3, "Blueming", "아이유", False, [a, b])
    d = (4, "다시 난, 여기", "백예린", False, [a, b, c])

    return render_template('index.html', lst=[a, b, c, d])



# 다음 형태로 요청했을때 해당 key로 Cookie를 굽는 코드를 작성하시오. 
# http://localhost:5000/wc?key=token&val=abc
@app.route('/wc')
def wc():
    key = request.args.get('key')
    val = request.args.get('val')
    res = Response("SET COOKIE")
    res.set_cookie(key, val)
    session['Token'] = '123X'
    return make_response(res)

@app.route('/rc')
def rc():
    key = request.args.get('key')
    val = request.cookies.get(key)
    return "cookie[" + key + "] = " + val + ", " + session.get('Token')


# escape 예제
@app.route('/escape')
def escape():
    bold = Markup("<b>Bold</b>")
    bold2 = Markup.escape("<b>Bold</b>")
    bold3 = bold2.unescape()
    
    return bold + " / " + bold2 + " / " + bold3


@app.route('/setsess') 
def setsess():
    session['Token'] = '123X' 
    return "Session이 설정되었습니다!"

@app.route('/getsess') 
def getsess():
    return session.get('Token')

@app.route('/delsess') 
def delsess():
    if session.get('Token'): 
        del session['Token']
    return "Session이 삭제되었습니다!"
 



# request 처리 용 함수 
def ymd(fmt):
    def trans(date_str):
        return datetime.strptime(date_str, fmt)
    return trans

@app.route('/dt') 
def dt():
    datestr = request.values.get('date', date.today(), type=ymd('%Y-%m-%d')) 
    return "우리나라 시간 형식: " + str(datestr)



# 헤더 남길 때?!
@app.route('/res1')
def res1():
    custom_res = Response("Custom Response", 200, {'test': 'ttt'})
    return make_response(custom_res)

# URL에 parameter 넘겨줄 때!
# args : 주소창, form : 내용에서 찾음
@app.route('/rp')
def rp():
    # q = request.args.get('q')
    q = request.args.getlist('q')
    return "q= %s" % str(q)

# WSGI (WebServer Gateway Interface)
@app.route('/test_wsgi')
def wsgi_test():
    def application(environ, start_response): # environ : flask의 환경변수
        body = 'The request method was %s' % environ['REQUEST_METHOD']
        headers = [ ('Content-Type', 'text/plain'),
                    ('Content-Length', str(len(body))) ]
        start_response('200 OK', headers) # make stream
        return [body]
    
    return make_response(application)


# g 변수 사용하기 예제 

# @app.before_request
# def before_request():
#     print("befor_request!")
#     g.str = "korean"


# # route = define URI
# @app.route("/gg")
# def helloworld2():
#     return "Hello Flask World!" + getattr(g, 'str', '111')

