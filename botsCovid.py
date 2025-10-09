import requests
from win10toast import ToastNotifier
import  json
import  time

def update():
    r = requests.get('https://covid-api.com/api/reports/total')
    datajson = r.json()
    data = datajson["data"]
    text =f'Date: {data["date"]} \nLastUpdate: {data["last_update"]}'

    while True:
        t= ToastNotifier()
        t.show_toast("Report covid",text,duration=20)
        time.sleep(10)
update()