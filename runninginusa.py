
"""
Created on 11-Sep-2017
@author: tushar
"""
import sys
import urllib2
import urllib
import json
import os 
import socket
import re
import time

from BeautifulSoup import BeautifulSoup

STATES = ['CA', 'WA', 'OR', 'AK', 'NV', 'ID', 'NV', 'UT', 'AZ', 'MT', 'WY', 'CO', 'NM', 'NH', 'VT', 'MA', 'NC',] 
#               'ND', 'SD',  'NE', 'KS', 'OK', 'TX', 'MN', 'IA', 'MO', 'AR', 'LA', 'WI', 'IL', 'NY', 'ME','RI','CT', 'NJ',
#               'MS', 'HI', 'FL', 'AL', 'GA', 'TN', 'SC', 'NV', 'KY', 'VA', 'WV', 'OH', 'IN', 'MI','PA', 'DE', 'MD', 'DC']

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def scrap_data(month, state, fp):
    """
    """
    dict1 = {}
    run_list = []
    dict2 = {}
    try:
        for pg in range(1, 21):
            quote_page = "http://www.runningintheusa.com/Classic/List.aspx?Month={}&State={}&Page={}".format(month, state, str(pg))
            print quote_page 
            page = urllib2.urlopen(quote_page)
            soup = BeautifulSoup(page)
            table = soup.find('table', style='background-color: Silver;margin-top:5px; margin-bottom:5px')
            tr_list = table.findAll('tr')
            tr_len = len(tr_list)
            for i in range(1,  tr_len-1):
                time.sleep(3)
                try:
                    tr = tr_list[i]
                    hr_attr = tr.find('div', style="padding:2px 1px 2px 1px; white-space:nowrap")
                    hr = 'http://www.runningintheusa.com' + hr_attr.find('a')['href']
                    nest_page = urllib2.urlopen(hr)
                    nest_soup = BeautifulSoup(nest_page)
                    
#                     try:
#                         RaceID = hr.split('?RaceID=')[-1]
#                         title = nest_soup.find('span', attrs={'id':"ctl00_ctl00_lblPageTitle"}).text
#                         td_list = nest_soup.findAll('td', attrs={'class':"ViewData"})
#                         date_st = td_list[0].text.replace('\r\n\t&nbsp', '')
#                         date = re.sub('[\n\t\r&nbsp;]', '', date_st)
#                         city = td_list[1].text.split(',')[0]
#                         event_state = td_list[1].text.split(',')[1]
#                         distance = td_list[3].text
#                     except Exception as ex:
#                         print ex
                            
                    try:
                        RaceID = hr.split('?RaceID=')[-1]
                    except Exception as ex:
                        RaceID = None
                     
                    try:        
                        title = nest_soup.find('span', attrs={'id':"ctl00_ctl00_lblPageTitle"}).text
                    except:
                        title = None
                        
                    td_list = nest_soup.findAll('td', attrs={'class':"ViewData"})
                    try:
                        date_st = td_list[0].text.replace('\r\n\t&nbsp', '')
                        date = re.sub('[\n\t\r&nbsp;]', '', date_st)
                    except:
                        date = None
                     
                    try:
                        city = td_list[1].text.split(',')[0]
                        event_state = td_list[1].text.split(',')[1]
                    except:
                        city = None
                        state = None
                         
                    try:   
                        distance = td_list[3].text
                    except:
                        distance = None
#                         
                    dict2 = {'RaceID' : RaceID,
                             'title' : title,
                             'date':date,
                             "city":city,
                             "distance" : distance,
                             'state' : event_state.replace(' ', '')}
                    
                    run_list.append(dict2)
                    
                except Exception as ex:
                    print ex
    except Exception as ex:
        print ex
    finally:        
        return run_list
    
if __name__ == "__main__":
    """
    """
    try:
        os.mkdir(os.getcwd()+ '/runningusa')
    except OSError:
        pass
    month_json = {}
    for state in STATES:
        fp = open(os.getcwd()+ '/runningusa/'+ str(state) + '.json', 'a+')
        for month in MONTHS:
            jsn = scrap_data(month, state, fp)
            month_json.update({str(month):jsn})
            
        jsn = json.dumps(month_json)
        fp.write(jsn)
    
