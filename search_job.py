import selenium.webdriver
import time
import pymysql

#coding: utf8

'''
先获取单个页面
url
爬取每一条 再点击进入 详情
等待几秒后
爬取下一页
'''

dr = selenium.webdriver.Chrome()
url = 'https://job.toutiao.com/campus/position?city=&position_type=&q1=&summary=873#page=1'

dr.get(url)

arr = []
# # obj = {}
class toutiao:
    def get_job(self,callback):
        job_list = dr.find_elements_by_class_name('job-item')
        for job_item in job_list:
            # a 为详情链接
            a = job_item.find_element_by_css_selector(':nth-child(1)').find_element_by_tag_name('a').text
            face_people = job_item.find_element_by_css_selector(':nth-child(2)').text
            catagory = job_item.find_element_by_css_selector(':nth-child(3)').text
            work_place = job_item.find_element_by_css_selector(':nth-child(4)').text
            publish = job_item.find_element_by_css_selector(':nth-child(5)').text
            print(a,face_people,catagory,work_place,publish)
            arr.append([a,face_people,catagory,work_place,publish])
        callback()


    def next_page(self):
        page = dr.find_element_by_id('pager')
        next = page.find_element_by_css_selector('span + a')
        next.click()



start = time.time()

i = 0
count = 5
# 爬取五页
job = toutiao()
while i < count:
    job.get_job(job.next_page)
    time.sleep(2)
    print('==========================')
    i = i + 1



conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456',db='home',charset="gbk")
#获取操作游标
cursor = conn.cursor()
#选择数据库
# conn.select_db('home');
#执行SQL,创建一个数据表.

cursor.execute("""create table job_list(job varchar(30) , people varchar(30) , catagory varchar(30) , place varchar(30) , publish varchar(30)) """)


data = []
for a in arr:
    data=[a[0],a[1],a[2],a[3],a[4]]
    try:
        # data = ["算法工程师", "2018毕业生", "研发", "雅加达", "2018-03-28"]
        sql_insert = "INSERT  INTO  job_list(job,people,catagory,place,publish) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql_insert,data)
        conn.commit()
    except pymysql.Error as e:
        print(e)


cursor.close()
conn.close()
