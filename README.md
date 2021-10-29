# propero_rpa_challenge
This project is created for Propero RPA challenge.

The project goal was to automate a process from a website https://prsinsdia.org

The steps are :
1. Launch
2. Click COVID19 link
3. Click Number of cases
4. Download the csv spreadsheet
5. From the page extract a table in the local system as a csv spreadsheet
6. From downloaded csv, create e sub-sheet with the data of Madhya Pradesh and prepare a spreadsheet
7. Attach the sheets prepared in step 5 and step 6 and email it to two email ids

<br><br><b>Note</b> : Sender and recipient information are extracted from <b>task.robot</b> file.<br><br>



Used programming language : Python 3<br>
Used libraries : selenium, pandas, glob, os, email, smtplib, ssl
