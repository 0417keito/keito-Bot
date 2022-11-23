from selenium import webdriver
from time import sleep 
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import requests 
from . import models
import chromedriver_binary
from django.http import HttpResponse

def ScrapingView(self):
    chrome_path =  'C:\\Users\\mnooh\\OneDrive\\デスクトップ\\chromedriver.exe'
    options = Options()
    options.add_argument('--incognitio')
    driver = webdriver.Chrome(executable_path=chrome_path, options=options)
    url =  'https://www.yotsuyaotsuka.com/chugaku_kakomon/system'
    driver.get(url)
    sleep(10)
    a = driver.find_element_by_tag_name('td')
    b = a.find_element_by_tag_name('a')
    b.click()
    login_form = driver.find_elements_by_tag_name('form')[1]
    login_ID_box = login_form.find_elements_by_class_name('login_form_element')[0]
    password_box = login_form.find_elements_by_class_name('login_form_element')[1]
    login_ID = login_ID_box.find_element_by_tag_name('input')
    password = password_box.find_element_by_tag_name('input')
    login_ID.send_keys('0417itsuki')
    password.send_keys('car1021Ak')
    submits = login_form.find_elements_by_tag_name('input')[2]
    submits.click()
    sleep(10)
    #ログインまで

    source = driver.page_source
    soup = BeautifulSoup(source,'html.parser')
    d_list = []
    content = soup.find_all('table')[1]
    sleep(15)
    infos = content.find_all('a')
    for info in infos:
        sleep(15)
        link = info.get('href')
        school_name = info.text
        d= {
            'link':link,
            'school_name':school_name
            }
        d_list.append(d)
    origin_url = 'https://www.yotsuyaotsuka.com{}'
    empty_list = []

    for dic in d_list:
        target_url = origin_url.format(dic['link'])
        driver.get(target_url)
        secound_source = driver.page_source
        sleep(15)
        soup = BeautifulSoup(secound_source, "html.parser")
        conts = soup.find_all('div', class_='subjecttable')
        for cont in conts:
            sleep(10)
            subject_name = cont.find('div', class_='subject').text
            subject_pdf = cont.find('a').get('href')
            subject = {
                'subject_name':subject_name,
                'subject_pdf':subject_pdf
                }
            empty_list.append(subject)
        ys = soup.find_all('div', class_='detail_year')
        subject_years = []
        for y in ys:
            sleep(15)
            year = y.text
            subject_years.append(year)

        subject_japaneses = [item['subject_pdf'] for item in empty_list if item['subject_name']=='\n                  国語                ']
        subject_maths = [item['subject_pdf'] for item in empty_list if item['subject_name']=='\n                  算数                ']
        subject_sciences = [item['subject_pdf'] for item in empty_list if item['subject_name']=='\n                  理科                ']
        subject_societys = [item['subject_pdf'] for item in empty_list if item['subject_name']=='\n                  社会                ']
        j = len(subject_japaneses)
        m = len(subject_maths)
        sc = len(subject_sciences)
        so = len(subject_societys)
        y = len(subject_years)
        exam_by_school = []
        for i in range(0,min([j,m,sc,so,y])):
            subject_by_year={
                'school_name':dic['school_name'] + subject_years[i],
                'japanese':subject_japaneses[i],
                'math':subject_maths[i],
                'science':subject_sciences[i],
                'society':subject_societys[i]
                }
            exam_by_school.append(subject_by_year)

    driver.quit()

    for object in exam_by_school:
        models.School_exam.objects.create(
            school_name = object['school_name'],
            year = object['year'],
            japanese = 'https://www.yotsuyaotsuka.com' +  object['japanese'],
            math = 'https://www.yotsuyaotsuka.com' + object['math'],
            science = 'https://www.yotsuyaotsuka.com'+ object['science'],
            society = 'https://www.yotsuyaotsuka.com' + object['society'])
    
    return HttpResponse('Hello World')