__version__ = '0.0.1'
__author__ = 'cquestor <jishi2206@gmail.com>'

__all__ = ['login']


from .datas import *
from .utils import *
from urllib.parse import urlencode
import requests
from lxml import etree
import re


def login(uname: str, password: str) -> str:
    """登录获取Cookie，用于后续需要权限的操作。Cookie的有效期为30天，任何时候`频繁的登录操作`都是最坏的选择，所以请妥善保管你的Cookie。
    :param uname: 账号（手机号）
    :param password: 登录密码
    :return: Cookie字符串
    :rtype: str
    """
    password = desEncrypt(password, DES_KEY)
    headers = {
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33"
    }
    payload = {
        'fid': -1,
        'uname': uname,
        'password': password,
        'refer': "http%3A%2F%2Fi.chaoxing.com",
        't': True,
        'forbidotherlogin': 0,
        'validate': "",
        'doubleFactorLogin': 0,
        'independentId': 0
    }
    payload = urlencode(payload)
    response = requests.post(
        LOGIN_URL, data=payload, headers=headers, timeout=10, allow_redirects=False)
    respJson = response.json()
    if not respJson.get('status'):
        raise LoginException(respJson.get('msg2'))
    return getCookieString(response.cookies)


def getUserInfo(cookie: str) -> User:
    """获取用户信息，包括个人信息、学校信息、头像
    :param cookie: 登录后获取的Cookie
    :return: 用户类
    :rtype: User
    """
    headers = {
        'Cookie': cookie,
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33"
    }
    response = requests.get(ACCOUNT_URL, headers=headers,
                            timeout=10, allow_redirects=False)
    html = etree.HTML(response.text)
    headSrc: str = re.findall(
        r'src="(http://photo\.chaoxing\.com/p/.*?)"', response.text)[0]
    userName: str = html.xpath('//p[@id="messageName"]/text()')[0]
    userId: str = html.xpath('//p[@id="uid"]/text()')[0]
    userSex: str = html.xpath(
        '//p[contains(@class, "sex")]//i[contains(@class, "checked")]/@value')[0]
    userSex: Sex = Sex(int(userSex))
    userPhone: str = html.xpath('//span[@id="messagePhone"]/text()')[0]
    schoolInfo: str = html.xpath('//ul[@id="messageFid"]/li/text()')[0]
    schoolName = schoolInfo.strip('\t').strip('\n').strip('\r').strip(' ')
    userSno: str = html.xpath(
        '//ul[@id="messageFid"]/li/p[@class="xuehao"]/text()')[0]
    userSno = userSno.split(':')[1]
    response = requests.get(headSrc, headers=headers,
                            timeout=10, allow_redirects=False)
    headUrl = response.headers.get('Location')
    return User(userName, userId, userSex, userPhone, schoolName, userSno, headUrl)


def getCourseList(cookie: str) -> list:
    payload = "courseType=1&courseFolderId=0&baseEducation=0&superstarClass=&courseFolderSize=0"
    headers = {
        'Cookie': cookie,
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33"
    }
    response = requests.post(COURSE_LISE_URL, headers=headers,
                             data=payload, timeout=10, allow_redirects=False)
    html = etree.HTML(response.text)
    courseListDom = html.xpath(
        '//ul[@id="courseList"]//li[contains(@class, "course") and contains(@class, "clearfix")]')
    courseList = []
    for course in courseListDom:
        courseId = course.xpath('./@courseid')[0]
        clazzId = course.xpath('./@clazzid')[0]
        personId = course.xpath('./@personid')[0]
        courseName = course.xpath(
            './/span[contains(@class, "course-name")]/@title')[0]
        teacherName = course.xpath('.//p[@class="line2"]/@title')[0]
        clazzName: str = course.xpath('.//p[@class="overHidden1"]/text()')[0]
        clazzName = clazzName.replace("班级：", "")
        courseList.append(Course(courseId, clazzId, personId,
                          courseName, clazzName, teacherName))
    return courseList
