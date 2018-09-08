"""框架代码"""
import time
from contextlib import contextmanager
from pymysql import connect
# Django添加路由的方式
# route_list = [
#     ('/gettime.html', gettime()),
#     ('/index.html', index_html()),
#     ('/center.html', center_html()),
#     ]

# flask添加路由方式
route_list = [
]

@contextmanager
def mysql():
    conn = connect(
            host="localhost",
            port=3306,
            db="stock_db",
            user="root",
            password="mysql",
            charset="utf8")
    cur = conn.cursor()
    yield cur
    conn.commit()
    # 关闭
    cur.close()
    conn.close()


def route(path):
    def warrpper(func):
        route_list.append((path, func))

        def inner():
            pass

        return inner

    return warrpper


@route('/gettime.html')
def gettime():
    return time.ctime()


@route('/index.html')
def index_html():
    with open("template/index.html", 'r', encoding='utf-8') as file:
        html_data = file.read()
    with mysql() as cur:
        sql = "select * from info"
        cur.execute(sql)
        from_mysql_data = ""
    for each_line in cur.fetchall():
        each_line_str = """<tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td><input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="000007"></td>
        </tr>"""%each_line
        from_mysql_data += each_line_str
    html_data = html_data.replace("{%content%}", from_mysql_data)
    return html_data


@route('/center.html')
def center_html():
    with open("template/center.html") as file:
        html_data = file.read()

    # 2 查询数据库
    # data_from_mysql = "have fun"
    data_from_mysql = ""
    with mysql() as cur:
        sql = "select i.code,i.short,i.chg,i.turnover,i.price,i.highs,focus.note_info from focus inner join info i on focus.info_id = i.id;"
        cur.execute(sql)
        from_mysql_data = ""
        for each_line in cur.fetchall():
            each_line_str = """<tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td><a type="button" class="btn btn-default btn-xs" href="/update/000007.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a></td>
                <td> <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="000007"></td>
            </tr>""" % each_line
            data_from_mysql += each_line_str
        html_data = html_data.replace("{%content%}", from_mysql_data)
    return html_data


def app(evn):
    request_path = evn["path_info"]
    print("收到用户请求路径为:", request_path)
    for path, func in route_list:
        if path == request_path:
            # Django和flask不同,flask这里的返回值func要加括号
            return '200 OK', [("Server", "pythonBWS/1.1")], func()

    # 未添加路由前,直接判断路径是什么就执行对应的函数
    # if request_path == '/gettime.html':
    #     return '200 OK', [("Server", "pythonBWS/1.1")], gettime()
    # if request_path == '/index.html':
    #     return '200 OK', [("Server", "pythonBWS/1.1")], index_html()
    # if request_path == '/center.html':
    #     return '200 OK', [("Server", "pythonBWS/1.1")], center_html()

    return '200 OK', [("Server", "pythonBWS/1.1")], "from response_body"
