import datetime
from config import *
from bs4 import BeautifulSoup
from bsoup import BSoup


def get_todays_date():
    return datetime.datetime.now()

 #Create date obj from date string provided  in the required format
def get_date_obj(date_str:str,date_str_format:str):
    try:
        when_dt_object = datetime.datetime.strptime(date_str, date_str_format)
        return when_dt_object
    except ValueError:
        raise ValueError("Incorrect date format or in valid date")

# Extract the week for the data displayed on the Netflix Tudum web page
def get_the_week(soup_obj:BeautifulSoup):
    week = soup_obj.find("div", class_="section-eyebrow-heading").text
    
    [start_date,end_date] = week.split(' - ')
    # print(start_date,end_date)
    end_date_obj = datetime.datetime.strptime(end_date,web_page_dispaly_date_format)
    # start_date = start_date.split(',')[0]+', '+str(end_date_obj.year)
    start_date_obj = datetime.datetime.strptime(start_date,web_page_dispaly_date_format)
    
    return start_date_obj,end_date_obj

# Check if date is not beyond which data is available
def is_date_valid_to_query(when_dt_object):
    soup_obj = BSoup(base_url)
    
    start,end = get_the_week(soup_obj.get_soup_obj())
    
    if end>=when_dt_object:
        return True
    return False

def construct_url(base_url, geography:str, of_what:str, when:str):
    url = base_url

    if geography == 'Global' and of_what in global_lists_url_additions.values() and of_what!="":
        url += '/'+of_what
    elif geography in countries.keys():
        url += '/'+countries[geography]
        if of_what in country_lists_url_additions.values() and of_what!="":
            url += '/'+of_what
   
    url += '?week='+when

    return url

def get_media_type_geo(geography,media_type):
    if geography == 'Global':
        return list(filter(lambda key: global_lists_url_additions[key] == media_type, global_lists_url_additions))[0]
    else:
        return list(filter(lambda key: country_lists_url_additions[key] == media_type, country_lists_url_additions))[0]




    
