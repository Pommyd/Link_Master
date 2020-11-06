from datetime import date as dt
import datetime
import re
import requests


# Log in to the spaggiari website and download the day's class register
def login(payload):
    d4 = dt.today().strftime("%Y-%m-%d")
    #Opening a session
    with requests.Session() as s:
        p = s.post('https://web.spaggiari.eu/auth-p7/app/default/AuthApi4.php?a=aLoginPwd', data=payload)
        # File download and storage in agenda.txt
        r = s.get('https://web.spaggiari.eu/fml/app/default/xml_export.php?stampa=%3Astampa%3A&report_name=&tipo=agenda&data=03+11+20&autore_id=6583250&tipo_export=EVENTI_AGENDA_STUDENTI&quad=%3Aquad%3A&materia_id=&classe_id=%3Aclasse_id%3A&gruppo_id=%3Agruppo_id%3A&ope=RPT&dal=' + d4 + '&al=' + d4 + '&formato=xls')
        print(p)
        excel = open('agenda.txt', 'w')
        excel.write(r.text)
        excel.close()


# Updating the date on the file and deleting the links of the previous day
def aggiorna_data():
    # Extrapolating the date from the first line of the file
    link = open('onlyLinks.txt', 'rt')
    data_scritta = link.readline(0)
    link.close()
    # If the file date is different from today, delete and write the new date
    if dt.today().strftime("%d%m%Y") != data_scritta:
        link = open('onlyLinks.txt', 'wt')
        link.write(dt.today().strftime("%d%m%Y") + '\n')
        link.close()


# Search for links from the excel file and write to the txt file
def serch():
    no_link = 0
    counter_date = 0
    with open("agenda.txt", "rt") as file:
        for line in file:
            ora_inizio_fine = re.findall(r'>\d\d:\d\d:\d\d', line)
            url = re.findall(r'https://meet.google.com/\w\w\w-\w\w\w\w-\w\w\w', line)
            # Writing the link
            if len(url) != 0:
                link = open('onlyLinks.txt', 'at')
                link.write(url[0] + '\n')
                link.close()
                # Notify that the link has been written
                no_link = no_link + 1
            # Writing the timetable
            if len(ora_inizio_fine) != 0:
                link = open('onlyLinks.txt', 'at')
                link.write(ora_inizio_fine[0][1:8] + '\n')
                link.close()
                # Counting of two lines of timetables
                counter_date = counter_date + 1
            # If there are two timetable lines and there is no link, leave one line blank
            if counter_date == 2 and no_link == 0:
                link = open('onlyLinks.txt', 'at')
                link.write('\n')
                link.close()
                # Data reset
                counter_date = 0
                no_link = 1


# Only the current time returns
def ora():
    current_time = datetime.datetime.now()
    return current_time.hour

