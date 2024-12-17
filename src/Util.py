from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import configparser
from pathlib import Path

class Util:
    driver = webdriver.Chrome()
    config = configparser.ConfigParser() 
    cwd = Path.cwd()
    project_root = cwd
    linkedIn_properties_filepath = os.path.join(project_root,"resources","linkedIn.properties")
    config.read(linkedIn_properties_filepath)

    @classmethod
    def get_project_folder_path(cls):
        return (cls.project_root)
 
    @classmethod
    def open_url(cls,url):
        cls.driver.get(url)

    @classmethod
    def find_element_by_xpath(cls, locator):
        return cls.driver.find_element(By.XPATH,locator)
    
    @classmethod
    def find_elements_by_xpath(cls, locator):
        elements = WebDriverWait(cls.driver, 15).until(
            EC.presence_of_all_elements_located((By.XPATH, locator))
        )
        return elements
    
    @classmethod
    def find_clickable_element(cls, locator):
        element = WebDriverWait(cls.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, locator))
        )
        return element
    
    @classmethod
    def find_visible_element(cls, locator):
        element = WebDriverWait(cls.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, locator))
        )
        return element

    @classmethod
    def click_by_js(cls,element):
        cls.driver.execute_script("arguments[0].click();", element)
    
    @classmethod
    def get_property(cls,property,section="xpaths"):
        return cls.config[section][property]
