DES_KEY = "u2oh6Vu^HWe40fj"
LOGIN_URL = "http://passport2.chaoxing.com/fanyalogin"
ACCOUNT_URL = "http://passport2.chaoxing.com/mooc/accountManage"
COURSE_LISE_URL = "http://mooc1-1.chaoxing.com/visit/courselistdata"

MALE = 1
FEMALE = 0


class Sex:
    def __init__(self, value: int) -> None:
        """性别类，value为值（`1男` `0女`），text为字符串（男||女）
        :param value: 性别值
        """
        self.value = value
        self.text = "男" if value == MALE else "女"


class User:
    def __init__(self, name: str, userId: str, sex: Sex, phone: str, school: str, sno: str, head: str) -> None:
        """用户类，保存用户个人信息
        :param name: 用户姓名
        :param userId: 学习通中用户的id
        :param sex: 性别类，包含性别值和性别字
        :param phone: 用户的手机号
        :param school: 学校名
        :param sno: 学号/工号
        :param head: 用户头像URL
        """
        self.name = name
        self.userId = userId
        self.sex = sex
        self.phone = phone
        self.school = school
        self.sno = sno
        self.head = head

    def toString(self):
        return f"姓名: {self.name}, id: {self.userId}, 性别: {self.sex.text}, 手机号: {self.phone}, 学校: {self.school}, 学号: {self.sno}, 头像URL: {self.head}"


class Course:
    def __init__(self, courseId: str, clazzId: str, personId: str, courseName: str, clazzName: str, teacherName: str) -> None:
        """课程类，存储课程基本信息
        :param courseId: 课程编号
        :param clazzId: 班级编号
        :param personId: 班级成员编号（根据变量名猜测，不可参考）
        :param courseName: 课程名
        :param clazzName: 班级名
        :param teacherName: 教师名
        """
        self.courseId = courseId
        self.clazzId = clazzId
        self.personId = personId
        self.courseName = courseName
        self.clazzName = clazzName
        self.teacherName = teacherName

    def toString(self):
        return f"课程编号: {self.courseId}, 班级编号: {self.clazzId}, 成员编号: {self.personId}, 课程名: {self.courseName}, 班级名: {self.clazzName}, 教师名: {self.teacherName}"
