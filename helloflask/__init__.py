# -*- coding: utf-8 -*- 

from flask import Flask, g, Response, make_response

# Flask(app_name)
app = Flask(__name__) 
app.debug = True

# 헤더 남길 때?!
@app.route('/res1')
def res1():
    custom_res = Response("Custom Response", 200, {'test': 'ttt'})
    return make_response(custom_res)

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


@app.route("/")
def helloworld():
    return "Hello Flask World!"