import re
from io import StringIO
from html.parser import HTMLParser
import html
import nepali_datetime
from datetime import datetime

def escape(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def word_60(data:str=None):
    s = MLStripper()
    s.feed(data)
    text = s.get_data()
    text = data.split(" ")
    if len(text)<60:
        return
    text = text[:60]
    text = ' '.join(text)
    text = re.sub('<.*?>', '', text)
    text = re.sub('\n', '', text)
    text = re.sub('&zwj;', '', text)
    text = re.sub(r'\[&#\d+;\]', '', text)
    text = html.unescape(text)
    return text

def annapurnapost_datetime(ndate):
    nepali_month_mapping = {
    "वैशाख": 1,
    "जेठ": 2,
    "असार": 3,
    "साउन": 4,
    "भदौ": 5,
    "असोज": 6,
    "कात्तिक": 7,
    "मंसिर": 8,
    "पुष": 9,
    "माघ": 10,
    "फागुन": 11,
    "चैत": 12
    }

    date_string = ndate
    date_parts = date_string.split(" ")
    nepali_day = int(date_parts[1].strip(','))
    nepali_month = nepali_month_mapping[date_parts[0]]
    nepali_year = int(date_parts[2])

    formatted_date = f"{nepali_month:02d} {nepali_day:02d} {nepali_year}"
    dateobject = nepali_datetime.datetime.strptime(formatted_date,"%m %d %Y")
    english_date = dateobject.to_datetime_date()
    formatted_date = english_date.strftime("%Y-%m-%d")
    return str(formatted_date)

def kathmandupost_conversion(date):
    test_date = 'Published at : June 26, 2023'
    date_object = datetime.strptime(date, '%B %d, %Y')
    formatted_date = date_object.strftime('%Y-%m-%d')
    return formatted_date

def bbcnepali_date_conversion(cleaned_time):
    print(cleaned_time)
    date_object = datetime.strptime(cleaned_time, "%m/%d/%Y")
    formatted_date = date_object.strftime("%Y-%m-%d")
    return str(formatted_date)

def ekantipur_conversion(time):
    nepali_month_mapping = {
    "वैशाख": 1,
    "जेष्ठ": 2,
    "असार": 3,
    "श्रावण": 4,
    "भाद्र": 5,
    "आश्विन": 6,
    "कार्तिक": 7,
    "मंसिर": 8,
    "पुस": 9,
    "माघ": 10,
    "फाल्गुन": 11,
    "चैत्र": 12
    }

    date_string = time

    date_parts = date_string.split(" ")
    nepali_day = int(date_parts[1].strip(','))
    nepali_month = nepali_month_mapping[date_parts[0]]
    nepali_year = int(date_parts[2])

    formatted_date = f"{nepali_month:02d}/{nepali_day:02d}/{nepali_year}"
    dateobject = nepali_datetime.datetime.strptime(formatted_date,"%m/%d/%Y")
    english_date = dateobject.to_datetime_date()
    formatted_date = english_date.strftime('%Y-%m-%d')
    return str(formatted_date)

def gorkhapatraonline_datetime_parser(nepali_date):
    nepali_month_mapping = {
        "वैशाख": 1,
        "जेठ": 2,
        "असार": 3,
        "साउन": 4,
        "भदौ": 5,
        "असोज": 6,
        "कात्तिक": 7,
        "मंसिर": 8,
        "पुस": 9,
        "माघ": 10,
        "फागुन": 11,
        "चैत": 12
    }
    date_parts = nepali_date.split()
    nepali_day = int(date_parts[0])
    nepali_month = nepali_month_mapping[date_parts[1]]
    nepali_year = int(date_parts[2].strip(','))
    formatted_date = f"{nepali_month:02d}/{nepali_day:02d}/{nepali_year}"
    date_object = nepali_datetime.datetime.strptime(formatted_date, "%m/%d/%Y")
    english_date = date_object.to_datetime_date()
    formatted_date = english_date.strftime("%Y-%m-%d")
    return formatted_date


def tht_timeconversion(date):
    date_time = datetime.strptime(date, "Published: %I:%M %p %b %d, %Y")
    formatted_date = date_time.strftime("%Y-%m-%d")
    return formatted_date

def nagariknews__dateconverter(date_string):
    nepali_month_mapping = {
        "वैशाख": 1,
        "जेष्ठ": 2,
        "असार": 3,
        "श्रावण": 4,
        "भाद्र": 5,
        "आश्विन": 6,
        "कार्तिक": 7,
        "मंसिर": 8,
        "पुस": 9,
        "माघ": 10,
        "फाल्गुन": 11,
        "चैत्र": 12
    }

    date_parts = date_string.split()
    nepali_day = int(date_parts[1])
    nepali_month = nepali_month_mapping[date_parts[2]]
    nepali_year = int(date_parts[3])
    formatted_date = f"{nepali_month:02d}/{nepali_day:02d}/{nepali_year}"
    date_object = nepali_datetime.datetime.strptime(formatted_date, "%m/%d/%Y")
    english_date = date_object.to_datetime_date()
    formatted_datetime = english_date.strftime("%Y-%m-%d")
    return formatted_datetime

def online_khabar_conversion(time):
    # test_date = '२०८० असार १० गते ११:२४'
    nepali_month_mapping = {
            "बैशाख": '०१',
            "जेष्ठ": '०२',
            "असार": '०३',
            "श्रावण": '०४',
            "भाद्र": '०५',
            "आश्वीन": '०६',
            "कात्तिक": '०७',
            "मंसिर": '०८',
            "पौष": '०९',
            "माघ": '१०',
            "फागुन": '११',
            "चैत्र": '१२'
        }
    date = time.split()
    nepali_year = date[0]
    nepali_month = nepali_month_mapping[date[1]]
    nepali_day = date[2]
    # Format the Nepali date as yyyy-mm-dd
    formatted_date = f"{nepali_year}-{nepali_month}-{nepali_day}"
    # Convert the Nepali date to English date
    english_date = nepali_datetime.date(int(nepali_year), int(nepali_month), int(nepali_day))
    english_date = english_date.to_datetime_date()
    # Format the English date as mm/dd/yyyy
    formatted_date = english_date.strftime("%Y-%m-%d")
    return formatted_date

def ratopati_date_conversion(dt):
    date = dt.split(',')
    new_date = date[1]
    date = new_date[1:]
    nepali_month_mapping = {
        "बैशाख": 1,
        "जेष्ठ": 2,
        "असार": 3,
        "श्रावण": 4,
        "भाद्र": 5,
        "आश्विन": 6,
        "कार्तिक": 7,
        "कात्तिक": 7,
        "मङ्सिर": 8,
        "पुष": 9,
        "माघ": 10,
        "फागुन": 11,
        "चैत्र": 12
    }
    date = date.split()
    nepali_month = nepali_month_mapping[date[1]]
    nepali_day = date[0]
    nepali_year = date[2]

    # Convert the Nepali date to an English date
    english_date = nepali_datetime.date(int(nepali_year), int(nepali_month), int(nepali_day))
    english_date = english_date.to_datetime_date()
    # Format the English date as mm/dd/yyyy
    formatted_date = english_date.strftime("%Y-%m-%d")
    return formatted_date

def republica_conversion(cleaned_time):
    date_object = datetime.strptime(cleaned_time, "%B %d, %Y %I:%M %p ")
    formatted_date = date_object.strftime("%Y-%m-%d")
    return str(formatted_date)