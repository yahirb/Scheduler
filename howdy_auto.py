from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import time

URL = "https://cas.tamu.edu/cas/login?service=https://howdy.tamu.edu/uPortal/Login&renew=true"
username = "yahirb"
password = "2085353Yb$"
department = "CSCE"
course_number = "420"

# Create a new instance of the ChromeDriver driver
#driver = webdriver.Chrome('/Users/yahir/Downloads/chromedriver' )

# Headless Browser
driver = webdriver.PhantomJS()
def start(URL):
    # go to the howdy home page
    driver.get(URL)
def login():
    # find the element that's ID attribute is username (the username box)
    inputElement = driver.find_element_by_id("username")
    # type in the username
    inputElement.send_keys(username)
    # find the element that's ID attribute is password (the password box)
    inputElement = driver.find_element_by_id("password")
    # type in the password
    inputElement.send_keys(password)
    # submit the form (although google automatically searches now without submitting)
    inputElement.submit()
def search(department,course_number):
    # find the element that's ID attribute is tabLink_u42l1s10 (the 'My Record' box)
    inputElement = driver.find_element_by_id("tabLink_u42l1s10")

    #click the 'My Records' tab
    inputElement.click()

    # find the 'Search Class Schedule' button
    buttonElement = driver.find_element_by_link_text("Search Class Schedule")

    buttonElement.click()

    driver.implicitly_wait(10)

    # find the submit button for the year and click it
    driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))
    elem = driver.find_element_by_xpath("/html/body/div[3]/form/input[2]")
    elem.submit()

    ### find the correct department, i.e. "CSCE"
    element = driver.find_element_by_xpath("//*[@id='subj_id']/option[@value='" + department + "']")
    element.click()
    element = driver.find_element_by_xpath("//*[@id='courseBtnDiv']/input[2]")
    element.click()


    ### click on course element
    element = driver.find_element_by_xpath("/html/body/div[3]/table[1]/tbody")
    elements = element.find_elements_by_tag_name("tr")
    elements.pop(0) # removes the first useless element of list

    for e in elements: # finds course number row
        if (e.find_elements_by_tag_name("td")[1].text == course_number):
            element = e
    element = element.find_elements_by_tag_name("td")[3]
    element = element.find_element_by_tag_name("form")
    element2 = element.find_element_by_css_selector("input[value='View Sections']")
    element2.click() # clicks the "view sections" button

    # finds section information
    element = driver.find_element_by_class_name("datadisplaytable")
    element = element.find_element_by_tag_name("tbody")
    # creates an array from the table holding sections
    rows = element.find_elements_by_tag_name("tr")
    # removes the two header element from table array
    rows.pop(0)
    rows.pop(0)
    # goes through each section row
    for row in rows:
        columns = row.find_elements_by_tag_name("td")
        # goes through each section searching for data
        section_status = columns[0].find_element_by_tag_name("abbr").text
        crn = columns[1].find_element_by_tag_name("a").text
        department = columns[2].find_element_by_tag_name("a").text
        course_number = columns[3].text
        section = columns[4].find_element_by_tag_name("a").text
        title = columns[7].text
        days = columns[8].text
        time = columns[9].text
        capacity = columns[10].text, "department: "
        active = columns[11].text
        remaining = columns[12].text
        instructor = columns[13].find_element_by_tag_name("a").text
        print (section_status)

try:
    start(URL)
    login()
    search(department,course_number)

except TimeoutException:
    print ("Timed out waiting for page to load")

finally:
    driver.quit()
