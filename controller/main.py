import sys
sys.path.insert(0, '/Users/ming.zhou/Python/workspace/Digweb')
sys.path.insert(0, '/Users/ming.zhou/Python/workspace/Digweb/dao')
print(sys.path)
from  controller import emailController
from pojo import School
from pojo import Mode
import urllib.request
from bs4 import BeautifulSoup
import re
import time

global_url = 'http://www.whu.edu.cn/'

def getUrlContent(url):
    return urllib.request.urlopen(url).read().decode('UTF-8')

def writeToFile(filePath, data):
    with open(filePath, 'w') as f:
        f.write(data)

def insertSchool(school,params):
    if Mode.insert(school, params)>0:
        return True
    return False

def deleteSchool(school, params):
    if Mode.delete(school, params)>0:
        return True
    return False

def updateSchool(school, set_params, where_params):
    if Mode.update(school, set_params, where_params)>0:
        return True
    return False

def findSchool(school, params):
    return Mode.findFirstByParams(school, params)

def lecture_whu():
    result = {}
    email = {}
    lectures_list = []
    result['flag'] = 1  # flag为0代表成功，-1代表数据库更新失败，-2代表发送失败，1代表没有新通知
    url = 'http://www.whu.edu.cn/tzgg.htm'
    url_content = getUrlContent(url)
    soup = BeautifulSoup(url_content)
    school_name = soup.title.string
    email['subject'] = school_name
    lectures_num_str = soup.find_all(id="fanye46693")[0].string
    lectures_num = int(lectures_num_str.split()[0][1:(len(lectures_num_str.split()[0]) - 1)])
    findParams = {'school_name': school_name}

    school = findSchool(School.School, findParams)
    if school.getLecturesNum() < lectures_num:
        new_lectures_num = lectures_num - school.getLecturesNum()
        lectures = soup.find_all(id=re.compile("lineu9_"))
        for i in range(new_lectures_num):
            lis = [c for c in lectures[i].children]
            print(lectures[i])
            lecture = (lis[1].a.string + ' : ' + (global_url + lis[1].a['href']))
            lectures_list.append(lecture)
        email['content'] = lectures_list

        if emailController.send(email):
            set_params = {'lectures_num': lectures_num}
            where_params = {'school_name': school_name}
            update_result = updateSchool(School.School, set_params, where_params)
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

def application(environ, start_response):
    while True:
        print("[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'Starting...'))
        start_response('200 OK', [('Content-Type', 'text/html')])
        result = lecture_whu()
        print(result)
        time.sleep(10)
        body = '<h2>message is , %s</h2>' % result['msg']
        print(body)
        return [bytes(body,'gbk')]

def timing_test():
    while True:
        print("[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'Starting...'))
        result = lecture_whu()
        print(result)
        time.sleep(10)

def test():
    url = 'http://www.whu.edu.cn/tzgg.htm'
    url_content = getUrlContent(url)
    print('=========start===========')
    soup = BeautifulSoup(url_content)
    school_name = soup.title.string
    lectures_num_str = soup.find_all(id="fanye46693")[0].string
    lectures_num = int(lectures_num_str.split()[0][1:(len(lectures_num_str.split()[0]) - 1)])
    # school_name ='通知公告-武汉大学'
    # lectures_num = 744
    # li = soup.find_all(re.compile('lineu9_\d'))
    # print(li)
    li = soup.find_all(id=re.compile("lineu9_"))
    print(len(li))
    print(type(li))
    print(li[0])
    print(type(li[0]))
    print(li[0].children)
    print('1111111111111')
    # print(li[0].children.div)
    # for c in li[0].children:
    #     print('--------')
    #     print(c)
    lis = [c for c in li[0].children]
    print(lis[1].a.string)
    print(lis[1].a['href'])
    print(type(lis[1]))
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

    ###insert#######
    s = School.School(school_name, lectures_num)
    # print(type(s))
    # print(type(School.School))
    # a = insertSchool(s.__class__, s.__dict__)
    # print(a)

    ####find#########
    params = {'school_name': school_name}
    # school = findSchool(School.School, params)
    # print(school.getLecturesNum())

    ####update#########
    where_params = {'id': 1}
    set_params = {'school_name': school_name + 'test', 'lectures_num': lectures_num + 12}
    # update_result = updateSchool(School.School, set_params, where_params)
    # print(update_result)

    ####delete#########
    delete_params = {'school_name': school_name + 'test', 'lectures_num': lectures_num + 12}
    # update_result = deleteSchool(School.School, delete_params)
    # print(update_result)

if __name__ == '__main__':
    timing_test()
    # print(result)
