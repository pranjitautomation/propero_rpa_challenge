from selenium import webdriver
import time
import glob
import os
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

filelist = []

def fetch_task_robot():
    output = []
    sender_details = []
    
    f = open("task.robot", "r")
    details = f.readlines()
    f.close()
    sender_email = details[0].split("=")[-1]
    sender_password = details[1].split("=")[-1]
    sender_details.append(sender_email)
    sender_details.append(sender_password)
    recipient_ids = details[2].split("=")[-1].split(",")
    
    output.append(sender_details)
    output.append(recipient_ids)
    
    return output


def send_email(filelist):
    subject = "PROPERO RPA CHALLENGE EMAIL"
    body = "Hi. This is the final check for PROPERO RPA CHALLENGE."
    sender_email = fetch_task_robot()[0][0]
    receiver_email = fetch_task_robot()[1]
    password = fetch_task_robot()[0][1]

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))
    for file in filelist:
        with open(file, "rb") as attachment:
            attachment_part = MIMEBase("application", "octet-stream")
            attachment_part.set_payload(attachment.read())
            encoders.encode_base64(attachment_part)
            attachment_part.add_header(
                "Content-Disposition",
                f"attachment; filename = {file}",
            )
        message.attach(attachment_part)
        text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
        
        
def extract_list(m):
    l = []
    s = ""
    n=0
    while n<len(m[0]):
        k=n
        while k<n+6:
            s += m[0][k] +","
            k+=1
        s = s+"\n"
        n=n+6
        
    l = s.split("\n")
    l.pop()
    f = l[0]
    l.remove(l[0])
    l.append(f)
    s1 = ""

    l1 = []
    for y in l:
        l1.append(y[0:len(y)-1])
    return l1

driver = webdriver.Chrome(executable_path="driver/chromedriver.exe")

url = "https://prsindia.org/"

driver.get(url)
driver.maximize_window()
time.sleep(5)


covid_19_link = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/nav/div[1]/ul/li[8]/a")
covid_19_link.click()
time.sleep(15)

no_of_cases = driver.find_element_by_xpath("/html/body/div[3]/div[2]/aside/div/section/ul/li[3]")
no_of_cases.click()
time.sleep(15)

download_sheet = driver.find_element_by_xpath("//*[@id=\"mptrack-expor-link\"]")
download_sheet.click()
time.sleep(15)

data = []
for tr in driver.find_elements_by_xpath('//*[@id="w0"]/table'):
    tds = tr.find_elements_by_tag_name('td')
    if tds: 
        data.append([td.text for td in tds])

l = []       
l = extract_list(data)

head = []
for tr in driver.find_elements_by_xpath('/html/body/div[3]/div[2]/section/div[2]/section/div/div[4]/div[2]/div/table/thead/tr'):
    tds = tr.find_elements_by_tag_name('th')
    if tds: 
        head.append([td.text for td in tds])

driver.close()
s = ""
for x in head[0]:
    s = s + x + ","

s = s[0:len(s)-1]

l.insert(0,s)

main = ""
for el in l:
    main += el + "\n"

table_filename = "State_wise_data_India.csv"
filelist.append(table_filename)

try:
    f = open(table_filename, "w")
    f.write(main)
    f.close()
    print("**********************************************")
    print("TABLE FROM THE WEBPAGE EXPORTED")
    print("**********************************************")
    
except:
    print("**********************************************")
    print("ERROR IN TABLE EXPORTING")
    print("**********************************************")
    
    
# DOWNLOAD LOCATION
download_path = "enter/the/path/of/download/folder" # e.g. : C:/Users/Pranjit/Downloads

list_of_files = glob.glob(f"{download_path}/*")
latest_file = max(list_of_files, key=os.path.getctime)

exp_file = "Pranjit_Covid_19_Cases.csv"
filelist.append(exp_file)
try:
    df = pd.read_csv(latest_file)
    df_mp = df[df["Region"] == "Madhya Pradesh"]
    df_mp.to_csv(exp_file)
    print("**********************************************")
    print("MADHYA PRADESH DETAILS CSV EXTRACTED")
    print("**********************************************")
    
except:
    print("**********************************************")
    print("ERROR IN EXPORTING")
    print("**********************************************")
    

try:
    send_email(filelist)
    print("**********************************************")
    print("EMAIL SENT")
    print("**********************************************")
    
except:
    print("**********************************************")
    print("EMAIL SENDING FAILED")
    print("**********************************************")
    