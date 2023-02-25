import requests
from csv_ical import Convert
import pandas as pd

calendar_url = "https://calendar.google.com/calendar/ical/b690bd9f34069826183e27df4d68fb7f941fd5f1b789247ea74772e1553f45f7%40group.calendar.google.com/public/basic.ics";

def get_calender_data():
    r = requests.get(calendar_url)
    # data = r.content
    with open("calender_data.ics", mode="wb") as file:
        file.write(r.content);

def convert_ics2csv():
    convert = Convert()
    convert.read_ical('calender_data.ics')
    convert.make_csv()
    convert.save_csv('calender_data.csv')

def make_sevendays_csv(time_start):
    dataFrame = pd.read_csv('calender_data.csv', header=None)
    # format_dataFrame = pd.DataFrame()
    dataFrame.drop(2, axis=1, inplace=True)
    dataFrame.drop(4, axis=1, inplace=True)
    dataFrame.columns = ['title', 'start', 'feat']
    dataFrame.sort_values(['start'],axis=0, ascending=False ,inplace=True, na_position='first')
    # dataFrame = dataFrame[(dataFrame['start'] >= time_start) & (dataFrame['start'] <= time_end)]
    dataFrame['type'] = dataFrame['title'].str[1].map({'工': 'work',
                                            '遊': 'game',
                                            '特': 'special'
                                            })
    dataFrame['title'] = dataFrame['title'].str[3::]
    dataFrame['feat'] = dataFrame['feat'].str[6:-7:]
    dataFrame['time'] = dataFrame['start'].str[11:16:]
    
    dataFrame['start'] = pd.to_datetime(dataFrame['start']).dt.date
    date_range = pd.date_range(start=time_start, periods=7, freq="D")
    dataFrame = dataFrame.set_index('start') 
    dataFrame = dataFrame.reindex(date_range)
    
    dataFrame['month'] = dataFrame.index.month
    dataFrame['day'] = dataFrame.index.day
    print(dataFrame)
    
    with open('週表.json', 'w', encoding='utf-8') as file:
        dataFrame.to_json(file, orient='records', force_ascii=False)
    # print(format_dataFrame)
    

get_calender_data()
convert_ics2csv()
make_sevendays_csv('2023-02-27')

# webbrowser.open("index.html")


