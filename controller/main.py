import sys

sys.path.insert(0, '/Users/ming.zhou/Python/workspace/Digweb')
sys.path.insert(0, '/Users/ming.zhou/Python/workspace/Digweb/dao')
print(sys.path)
from  controller import emailController
# from dao.pojo import School
# from dao.pojo import Mode
from pojo import School
from pojo import Mode
import urllib.request
from bs4 import BeautifulSoup
import re
import time

global_whu_url = 'http://www.whu.edu.cn/'
global_hust_url = 'http://uzone.univs.cn/'


def get_url_content(url):
    return urllib.request.urlopen(url).read().decode('UTF-8')


def get_url_content_hust(url):
    return urllib.request.urlopen(url).read()


def write_to_file(file_path, data):
    with open(file_path, 'w') as f:
        f.write(data)


def insert_school(school, params):
    if Mode.insert(school, params) > 0:
        return True
    return False


def delete_school(school, params):
    if Mode.delete(school, params) > 0:
        return True
    return False


def update_school(school, set_params, where_params):
    if Mode.update(school, set_params, where_params) > 0:
        return True
    return False


def find_school(school, params):
    return Mode.findFirstByParams(school, params)

#爬取武汉大学的通知通告
def lecture_whu():
    #定义返回给用户或调用者的反馈信息
    result = {}
    # 定义发送email内容信息
    email = {}
    # 定义通知通告的列表
    lectures_list = []
    result['flag'] = 1  # flag为0代表成功，-1代表数据库更新失败，-2代表发送email失败，1代表没有新通知
    url = 'http://www.whu.edu.cn/tzgg.htm'
    #得到指定url的网页源代码数据
    url_content = get_url_content(url)
    # 使用BeautifulSoup来解析网页源代码数据
    soup = BeautifulSoup(url_content)
    #得到学校名称
    school_name = soup.title.string
    #设置email主题
    email['subject'] = school_name
    # 获取通知通告的总条数
    lectures_num_str = soup.find_all(id="fanye46693")[0].string
    lectures_num = int(lectures_num_str.split()[0][1:(len(lectures_num_str.split()[0]) - 1)])

    # 获取指定正则表达式的通知通告
    lectures = soup.find_all(id=re.compile("lineu9_"))

    # 查询指定条件的school，并返回school实例
    find_params = {'school_name': school_name}
    school = find_school(School.School, find_params)
    if school is None:
        for i in range(20):
            lecture = (lectures[i].a.string + ' : ' + (global_whu_url + lectures[i].a['href']))
            lectures_list.append(lecture)
        insert_params = {'school_name': school_name, 'lectures_num': lectures_num}
        email['content'] = lectures_list
        if emailController.send(email):
            result['flag'] = 0
            if insert_school(School.School, insert_params) is not True:
                result['flag'] = -1
                result['msg'] = '数据库操作失败！'
        else:
            result['flag'] = -2
            result['msg'] = '邮件发送失败！'

    # 数据库中通知通告的条数比网页上最新更新的还多，则可判断为数据出错
    # TODO update,需要将数据库中通知通告的条数更新为与网页上的一致。
    elif school.getLecturesNum() > lectures_num:
        result['flag'] = -3
        result['msg'] = '数据库数据有问题，请联系管理员:zhoum1118@163.com！'

    # 假如网页的通知通告有更新
    elif school.getLecturesNum() < lectures_num:
        new_lectures_num = lectures_num - school.getLecturesNum()

        for i in range(new_lectures_num):
            lecture = (lectures[i].a.string + ' : ' + (global_whu_url + lectures[i].a['href']))
            lectures_list.append(lecture)
        #将更新的通知通告设置为email的内容
        email['content'] = lectures_list

        if emailController.send(email):
            set_params = {'lectures_num': lectures_num}
            where_params = {'school_name': school_name}
            update_result = update_school(School.School, set_params, where_params)
            if update_result:
                result['flag'] = 0
            else:
                result['flag'] = -1
                result['msg'] = '数据库操作失败！'
        else:
            result['flag'] = -2
            result['msg'] = '邮件发送失败！'
    else:
        result['flag'] = 1
        result['msg'] = '没有新通知！'

    return result


#爬取华科的讲座信息
def lecture_hust():
    result = {}
    email = {}
    lectures_list = []
    result['flag'] = 1  # flag为0代表成功，-1代表数据库更新失败，-2代表发送失败，-3代表数据库数据有问题，1代表没有新通知
    url = 'http://uzone.univs.cn/schNewsList.action?univId=2566&fId=1733&sId=4460'
    url_content = get_url_content_hust(url)
    soup = BeautifulSoup(url_content)
    school_name = soup.title.string
    email['subject'] = school_name
    lectures_num = int(soup.find_all(id="pageTop")[0].b.string)
    find_params = {'school_name': school_name}
    lectures = soup.find_all(id="vr")

    school = find_school(School.School, find_params)
    if school is None:
        for i in range(20):
            lecture = (lectures[i].a.string + ' : ' + (global_hust_url + lectures[i].a['href']))
            lectures_list.append(lecture)
        insert_params = {'school_name': school_name, 'lectures_num': lectures_num}
        email['content'] = lectures_list
        if emailController.send(email):
            result['flag'] = 0
            if insert_school(School.School, insert_params) is not True:
                result['flag'] = -1
                result['msg'] = '数据库操作失败！'
        else:
            result['flag'] = -2
            result['msg'] = '邮件发送失败！'

    elif school.getLecturesNum() > lectures_num:
        result['flag'] = -3
        result['msg'] = '数据库数据有问题，请联系管理员:zhoum1118@163.com！'

    elif school.getLecturesNum() < lectures_num:
        new_lectures_num = lectures_num - school.getLecturesNum()
        for i in range(new_lectures_num):
            lecture = (lectures[i].a.string + ' : ' + (global_hust_url + lectures[i].a['href']))
            lectures_list.append(lecture)
        email['content'] = lectures_list

        if emailController.send(email):
            set_params = {'lectures_num': lectures_num}
            where_params = {'school_name': school_name}
            update_result = update_school(School.School, set_params, where_params)
            if update_result:
                result['flag'] = 0
            else:
                result['flag'] = -1
                result['msg'] = '数据库操作失败！'
        else:
            result['flag'] = -2
            result['msg'] = '邮件发送失败！'
    else:
        result['flag'] = 1
        result['msg'] = '没有新通知！'

    return result


# def application(environ, start_response):
#     while True:
#         print("[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'Starting...'))
#         start_response('200 OK', [('Content-Type', 'text/html')])
#         result = lecture_whu()
#         print(result)
#         time.sleep(10)
#         body = '<h2>message is , %s</h2>' % result['msg']
#         print(body)
#         return [bytes(body,'gbk')]

def timing_test():
    while True:
        print("[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'Starting...'))
        result_whu = lecture_whu()
        result_hust = lecture_hust()
        print('result_whu is ' + str(result_whu) + ' , result_hust is ' + str(result_hust))
        time.sleep(10)


def test():
    url = 'http://www.whu.edu.cn/tzgg.htm'
    url_content = get_url_content(url)
    # print(url_content)
    print('=========start===========')
    soup = BeautifulSoup(url_content)
    # print(soup)
    school_name = soup.title.string.split('-')[0]
    print(school_name)
    lectures_num_str = soup.find_all(id="fanye46693")[0].string
    lectures_num = int(lectures_num_str.split()[0][1:(len(lectures_num_str.split()[0]) - 1)])
    # # li = soup.find_all(re.compile('lineu9_\d'))
    # # print(li)
    # li = soup.find_all(id=re.compile("lineu9_"))
    # print(len(li))
    # print(type(li))
    # print(li[0])
    # print(type(li[0]))
    # print(li[0].children)
    # print('1111111111111')
    # # print(li[0].children.div)
    # # for c in li[0].children:
    # #     print('--------')
    # #     print(c)
    # lis = [c for c in li[0].children]
    # print(lis[1].a.string)
    # print(lis[1].a['href'])
    # print(type(lis[1]))
    # i = 1
    # for s in lis:
    #     print(i)
    #     print(s)
    #     i += 1
    # for c in li[0].children[0].children:
    #     print(c)
    # for tag in soup.find_all(id=re.compile("lineu9_")):
    #     print(tag)
    # for re in li:
    #     print(re)

    # -----insert-------
    # s = School.School(school_name, lectures_num)
    # print(type(s))
    # print(type(School.School))
    # print(s.__class__)
    # print(s.__dict__)
    #
    # a = Mode.insert(s.__class__, s.__dict__)
    # print(a)

    # -----find-------
    # params = {'school_name': school_name}
    # school = findSchool(School.School, params)
    # print(school.getLecturesNum())

    # -----update-----
    # where_params = {'id': 1}
    # set_params = {'school_name': school_name + 'test', 'lectures_num': lectures_num + 12}
    # update_result = updateSchool(School.School, set_params, where_params)
    # print(update_result)

    # -----delete-----
    # delete_params = {'school_name': school_name + 'test', 'lectures_num': lectures_num + 12}
    # update_result = deleteSchool(School.School, delete_params)
    # print(update_result)


if __name__ == '__main__':
    # test()
    # timing_test()
    # print(result)
    print(lecture_whu())
