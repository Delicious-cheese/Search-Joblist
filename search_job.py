import selenium.webdriver
import time
import pymysql

#coding: utf8

'''
�Ȼ�ȡ����ҳ��
url
��ȡÿһ�� �ٵ������ ����
�ȴ������
��ȡ��һҳ
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
            # a Ϊ��������
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
# ��ȡ��ҳ
job = toutiao()
while i < count:
    job.get_job(job.next_page)
    time.sleep(2)
    print('==========================')
    i = i + 1



conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456',db='home',charset="gbk")
#��ȡ�����α�
cursor = conn.cursor()
#ѡ�����ݿ�
# conn.select_db('home');
#ִ��SQL,����һ�����ݱ�.

cursor.execute("""create table job_list(job varchar(30) , people varchar(30) , catagory varchar(30) , place varchar(30) , publish varchar(30)) """)


data = []
for a in arr:
    data=[a[0],a[1],a[2],a[3],a[4]]
    try:
        # data = ["�㷨����ʦ", "2018��ҵ��", "�з�", "�żӴ�", "2018-03-28"]
        sql_insert = "INSERT  INTO  job_list(job,people,catagory,place,publish) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql_insert,data)
        conn.commit()
    except pymysql.Error as e:
        print(e)


cursor.close()
conn.close()
