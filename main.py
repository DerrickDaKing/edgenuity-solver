import os
import time
import errno
import psutil
import atexit
import platform
import subprocess
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from googlesearch import search

found = False
# Assign correct os commands
if platform.system() == 'Windows':
    clear = lambda: os.system('cls') # For Windows
elif platform.system() == 'Linux':
    clear = lambda: os.system('clear') # For linux

if os.path.isfile('geckodriver.exe') or os.path.isfile('geckodriver'):
    driver_path = 'geckodriver'
    found = True
    # Initialize browsers
    quizletOptions = Options()
    quizletOptions.headless = True
    browser = webdriver.Firefox(executable_path=driver_path)
    quizletDriver = webdriver.Firefox(options=quizletOptions, executable_path=driver_path)
elif os.path.isfile('chromedriver.exe') or os.path.isfile('chromedriver'):
    driver_path = 'chromedriver'
    found = True
    # Initialize browsers
    quizletOptions = Options()
    quizletOptions.headless = True
    browser = webdriver.Chrome(executable_path=driver_path)
    quizletDriver = webdriver.Chrome(options=quizletOptions, executable_path=driver_path)
elif found == False:
    try:      
        p = subprocess.Popen("geckodriver", stdout=subprocess.PIPE, shell=True)
        quizletOptions = Options()
        quizletOptions.headless = True
        browser = webdriver.Firefox()
        quizletDriver = webdriver.Firefox(options=quizletOptions)
        p.kill()
    except FileNotFoundError as e:
        if e.errno == errno.ENOENT:
            pass
        else:
            pass
else:
    try:      
        p = subprocess.Popen("chromedriver", stdout=subprocess.PIPE, shell=True)
        p.kill()
        quizletOptions = Options()
        quizletOptions.headless = True
        browser = webdriver.Chrome()
        quizletDriver = webdriver.Chrome(options=quizletOptions)
    except OSError as e:
        if e.errno == errno.ENOENT:
            print('Webdriver not found!')
        else:
            print('Webdriver not found!')

browser.get("https://auth.edgenuity.com/Login/Login/Student")        

def searchGoogle(query):
    for j in search(query, tld="co.in", num=10, stop=10, pause=1): 
        if j.find('quizlet') != -1:
            return j
    return 'Not found'

def findAnswer(question):
    clear()
    print('Loading...')
    print('Scanned!')
    question = question.strip('\n')
    question = question.strip('\t')
    # Keep only first line unless multiple choice question (helps with search results)
    if question.find('A.') == -1:
        question = question.partition('\n')[0]
    question = question[:-3]

    # Search google for quizlet url
    quizletUrl = searchGoogle(question)
    if quizletUrl == 'Not found':
        print('Could not find quizlet url')
        return
    # Keep only first line for every question type (helps with parsing)
    question = question.partition('\n')[0]
    print('Googled!')

    # Download and parse quizlet data
    quizletDriver.get(quizletUrl)
    print('Loaded quizlet!')
    try:
        answerElement = quizletDriver.find_element_by_xpath("//span[contains(text(),'" + question + "')]/../../../..//a[@class='SetPageTerm-definitionText']/span")
        print('Parsed!')
        answer = answerElement.text
        # If answer and question are flipped
        if answer.find(question) != -1:
            answerElement = quizletDriver.find_element_by_xpath("//span[contains(text(),'" + question + "')]/../../../..//a[@class='SetPageTerm-wordText']/span")
            answer = answerElement.text
    except:
        answer = 'Failed to parse!'
    clear()
    print(answer)
    # print('DEBUG INFO:')
    # print('question: ' + question)
    # print('quizletUrl: ' + quizletUrl)

def scan():
    ready = True
    lastQuestion = ''
    while True:
        if ready:
            # Parse out question text
            try:
                iframe = browser.find_element_by_id('stageFrame')
            except:
                continue
            browser.switch_to_frame(iframe)
            questions = browser.find_elements_by_class_name('Practice_Question_Body')
            for i in range(len(questions)):
                if questions[i].text != '':
                    if lastQuestion != questions[i].text:
                        lastQuestion = questions[i].text
                        findAnswer(questions[i].text)
                        break
                    else:
                        ready = False
                        break
            browser.switch_to.default_content()
        else:
            ready = True
            time.sleep(.5)       

def exit_handler():
    print ('Exiting!')
    browser.quit()
    quizletDriver.quit()
atexit.register(exit_handler)

while True:
    # print('?')
    # x = input()
    # if x == 'run':
    #     scan()
    clear()
    scan()