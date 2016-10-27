class School():
    '''学校表
    school_name 学校名称，根据页面的title来确定
    lectures_num 讲座数量
    '''
    def __init__(self, school_name, lectures_num):
        self.__school_name = school_name
        self.__lectures_num = lectures_num

    def gene(self,params):
        return School(params[0], params[1])

    def setSchoolName(self, school_name):
        self.__school_name = school_name
    def setLecturesNum(self, lectures_num):
        self.__lectures_num = lectures_num

    def getSchoolName(self):
        return self.__school_name
    def getLecturesNum(self):
        return  self.__lectures_num

if __name__ == '__main__':
    print("here")
    s = School('whu', 123)
    print(s)
    print(School('whu', 123))
    print(type(s))
    print(type(School('whu', 123)))
    print(s.__dict__)
