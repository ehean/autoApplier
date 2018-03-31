import re
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium
import time


BASEURL = "https://www.indeed.com"
NAME = "Erik Heaney"
EMAIL = "test@email.com"
PHONE = "9195995674"
PASSWORD = "XXX"
SEARCHWORDS = "python developer C C++"
ADDRESS = "Raleigh, NC"
FILEPATH = "C:\Erik Heaney Python Resume.pdf"

def checkMandatoryFields():
    try:
        find = frame.find_element_by_xpath("//label[text()='Resume *']")
        attachButton = frame.find_element_by_xpath("//input[@name='questionAttachments']") 
        attachButton.clear()
        attachButton.send_keys(FILEPATH)
    except:
        pass
    try:
        find = frame.find_element_by_xpath("//label[text()='Name *']")   
        nameForm = frame.find_element_by_xpath("//input[@id='input-applicant.name']")
        nameForm.clear()
        nameForm.send_keys(NAME)
    except:
        pass
    try:
        find = frame.find_element_by_xpath("//label[text()='Email *']")
        emailForm = frame.find_element_by_xpath("//input[@id='input-applicant.email']")
        emailForm.clear()
        emailForm.send_keys(EMAIL)
    except:
        pass
    try:
        find = frame.find_element_by_xpath("//label[text()='Phone Number *']")
        numberForm = frame.find_element_by_xpath("//input[@id='input-applicant.phoneNumber']")
        numberForm.clear()
        numberForm.send_keys(PHONE)
    except:
        pass
    try:
        span = frame.find_element_by_xpath("//label[text()='Address *']")
        numberForm = span.find_element_by_xpath("../../../..//input")
        numberForm.clear()
        numberForm.send_keys(ADDRESS)
    except:
        pass

        
def checkApplyButton():
    try: 
        # scroll to bottom
        scrollButton = frame.find_element_by_xpath("//button[@class='icl-Button--transparent icl-Button--md ia-ScrollToBottom-link']")
        frame.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Hover = ActionChains(frame).move_to_element(checkbox)
        # Hover.click().perform()
        
        # select i'm not a robot
        checkbox = frame.find_element_by_xpath("//div[@class='recaptcha-checkbox-checkmark']")
        Hover = ActionChains(frame).move_to_element(checkbox)
        Hover.click().perform()
        
        # hit apply 
        applyButton = frame.find_element_by_xpath("//button[@id='form-action-submit']")
        applyButton.click()
        return True
    except:
        return False

# Open indeed page that's already logged in and has filters set
# open browser using selenium in order to render the HTML document
# (JS only renders for browsers)
try:
    driver = webdriver.Chrome('C:/scripts/chromedriver_win32 (2)/chromedriver.exe')
except:
    binary = ChromeBinary('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe')
    driver = webdriver.Chrome(chrome_binary=binary)
    
#implicit wait 20 sec
# driver = webdriver.Firefox(executable_path=r'C:/scripts/geckodriver.exe')
driver.implicitly_wait(10)

driver.get(BASEURL)


# find login button
loginButton = driver.find_element_by_xpath("/html/body/div[@class='jobsearch-Layout']/div[@class='jobsearch-Content icl-Container icl-Container--centered icl-u-xs-p--sm']/div[@class='icl-Grid icl-Grid--gutters'][6]/div[@id='profileLinks']/div[@class='icl-NavigationList icl-NavigationList--inline']/ul[@class='icl-NavigationList-items']/li[@class='icl-NavigationList-item'][1]/a[@class='icl-NavigationList-link icl-NavigationList--primary']/div[@class='icl-NavigationList-text']/span[@class='icl-NavigationList-primaryText']")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# click login button
Hover = ActionChains(driver).move_to_element(loginButton)
Hover.click().perform()


# Fill login forms
emailForm = driver.find_element_by_xpath("//input[@id='signin_email']")
emailForm.send_keys(EMAIL)
passwordForm = driver.find_element_by_xpath("//input[@id='signin_password']")
passwordForm.send_keys(PASSWORD)

# click sign in button
signInButton = driver.find_element_by_xpath("/html/body[@class='ltr']/div[@id='container']/div[@class='login-page']/div[@class='page-content']/section[@class='form-content']/form[@id='loginform']/button[@class='sg-btn sg-btn-primary btn-signin']")
Hover = ActionChains(driver).move_to_element(signInButton)
Hover.click().perform()


# Go to advanced search
driver.get(BASEURL + "/advanced_search")
orSearchForm = driver.find_element_by_xpath("/html/body[@id='advanced_search_page']/form/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]/input[@id='as_any']")
orSearchForm.send_keys(SEARCHWORDS)
ageForm = Select(driver.find_element_by_xpath("/html/body[@id='advanced_search_page']/form/table/tbody/tr[2]/td/table/tbody/tr[15]/td/select[@id='fromage']"))
ageForm.select_by_value("last")
displayForm = Select(driver.find_element_by_xpath("/html/body[@id='advanced_search_page']/form/table/tbody/tr[2]/td/table/tbody/tr[16]/td/select[@id='limit']"))
displayForm.select_by_value("50")
sortForm = Select(driver.find_element_by_xpath("/html/body[@id='advanced_search_page']/form/table/tbody/tr[2]/td/table/tbody/tr[16]/td/select[@id='sort']"))
sortForm.select_by_value("date")

findJobButton = driver.find_element_by_xpath("/html/body[@id='advanced_search_page']/form/table/tbody/tr[2]/td/table/tbody/tr[16]/td/span[@class='inwrapBorder']/span[@class='inwrapBorderTop']/input[@id='fj']")
findJobButton.click()

# Get list of all jobs on current page
soup = BeautifulSoup(driver.page_source, "lxml")
jobResults = soup.findAll(True, attrs={'class': ['row', 'result', 'clickcard']})


# parse all job results that can be applied via Indeed
resultsWithIndeedApply = []

for result in jobResults:
    if result.find(True, attrs={'class': 'iaP'}):
        link = result.find("a", attrs={'class': ['jobtitle', 'turnstileLink']})['href']
        target = result.find("a", attrs={'class': ['jobtitle', 'turnstileLink']})['target']
        # open browser using selenium in order to render the HTML document
        # (JS only renders for browsers)
        
        # check for pop ups to close
        try:
            find = driver.find_element_by_xpath("//div[@id='prime-popover-div']")
            closePopUp = driver.find_element_by_xpath("//button[@id='prime-popover-close-button']")
            closePopUp.click()
        except:
            pass
        
        # click job link
        xPathString = "//a[@href='" + link + "']"
        jobLink = driver.find_element_by_xpath(xPathString)
        Hover = ActionChains(driver).move_to_element(jobLink)
        Hover.click().perform()

        #switch window w/ explicit wait
        jobWindowIndex = 1
        listWindowIndex = 0
        driver.switch_to.window(driver.window_handles[jobWindowIndex])
        
        # find apply button
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        applyButton = driver.find_element_by_xpath("//a[@class='indeed-apply-button']")        
        
        # click apply button
        Hover = ActionChains(driver).move_to_element(applyButton)
        Hover.click().perform()
        
        # switch iframe
        time.sleep(1)
        driver.switch_to.frame(driver.find_element_by_css_selector("div > iframe"))
        time.sleep(1)
        frame = driver.find_element_by_css_selector("body > iframe")
        driver.switch_to.frame(frame)
        
        # check fields and hit the continue button until the 'apply'
        # button is clicked
        appSent = False
        while not appSent:
            # check for mandatory fields
            checkMandatoryFields()
            
                
            # Continue
            continueButton = driver.find_element_by_xpath("//button[@id='form-action-continue']")
            continueButton.click()

            appSent = checkApplyButton()
            
        pause = input()
        
        driver.quit()
        exit()
        
        
        
        

        

        
