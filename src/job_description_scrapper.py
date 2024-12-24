from Util import Util
import os, configparser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException

config = configparser.ConfigParser()
project_path = Util.get_project_folder_path()
print(f"project_path: {project_path}")
linkedIn_properties_filepath = os.path.join(project_path,"resources","config.properties")
config.read(linkedIn_properties_filepath)


url = "https://www.linkedin.com/login"
Util.open_url(url)

jd_collection = []
jobs = []

with open('/home/sunbeanm/Documents/dbda/project/ml/Resume_Screening_System/resources/job_titles.txt', 'r') as file:
    for line in file:
        jobs.append(line.strip())

email_id = config['login_details']['email_id']
passwd = config['login_details']['passwd']


def login_to_linkedIn(email_id, passwd):

    Util.find_element_by_xpath(Util.get_property('email_id_textfield_xpath')).send_keys(email_id)
    Util.find_element_by_xpath(Util.get_property('password_textfield_xpath')).send_keys(passwd)
    Util.find_element_by_xpath(Util.get_property('sign_in_submit_btn_xpath')).click()


def search_job(job_name):
    jd_collection_by_role = {}
    Util.find_element_by_xpath(Util.get_property('jobs_btn_header_xpath')).click()
    Util.find_clickable_element(Util.get_property('job_keyword_textfield_xpath')).send_keys(job_name+Keys.ENTER)
    job_results = Util.find_elements_by_xpath(Util.get_property('job_search_results_xpath'))
    
    
    job_results = Util.find_elements_by_xpath(Util.get_property('job_search_results_xpath'))
    role_specific_jd = []
    for i in range(len(job_results)):
        try:
            Util.click_by_js(job_results[i])
        except StaleElementReferenceException:
            job_results = Util.find_elements_by_xpath(Util.get_property('job_search_results_xpath'))  # Re-locate each iteration
            continue
        jd = Util.find_visible_element(Util.get_property('job_description_container_paragraph_xpath')).text
        role_specific_jd.append(jd)
    jd_collection_by_role[job_name] = role_specific_jd
    jd_collection.append(jd_collection_by_role)
        
login_to_linkedIn(email_id, passwd)

count =0
try:
    for job in jobs:
        search_job(job)  
        count+=1 
except Exception as e:
    print(e)
print(f"Job Counts done: {count}")
with open('/home/sunbeanm/Downloads/jd_collection.txt','wt') as file:
    file.write(str(jd_collection))

# print(jd_collection)
# for key in jd_collection.keys():
#     print(f"{key} : {len(jd_collection[key])}")