import requests
import module
discord_webhook_url = 'Webhook Link'

# Log-in data to the spaggiari site
payload = {
    'uid': 'mail.example@example.com',
    'pwd': 'Password'
}

# Log in to the spaggiari website and download the agenda
module.login(payload)

# Update the date on the file and delete the links of the day before
module.aggiorna_data()

# Extrapolation of the links from the diary file and writing to a separate file
module.serch()

# Array with all onlyLinks.txt file line by line
file = open("onlyLinks.txt", "r")
linee = file.readlines()
file.close()

# Extrapolation of the correct link using the time slot entered by the professor
y = 0
for x in range(0, len(linee) - 1, 3):
    ora_inizio = int(linee[y + 1][0:2])
    ora_fine = int(linee[y + 2][0:2])
    if ora_inizio <= module.ora() < ora_fine:
        f = open('linkToSave.txt', 'r')
        linea = f.readline()
        if linea != linee[y + 3][0:36]:
            message = {
                "content": linee[y + 3][0:36] + " @everyone"
            }
            fw = open('linkToSave.txt', 'w')
            fw.write(linee[y + 3][0:36])
            fw.close()
        else:
            break
        f.close()
        requests.post(discord_webhook_url, data=message)
        break
    y = y + 3
