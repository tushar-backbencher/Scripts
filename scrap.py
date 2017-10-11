#!/usr/bin/python2

import sys
import urllib2
import urllib
import json
import os 
import socket


from BeautifulSoup import BeautifulSoup

def scrap_data(marathon_type, max_page, image_directory, fp):
    """
    """
    cnt = 1
    dict1 = {}
    print "max_page==>", max_page
    for i  in range(1, max_page+1):
        quote_page = 'http://www.active.com/running/' + marathon_type + '?page='+str(i)
        print quote_page

        page = urllib2.urlopen(quote_page)
        soup = BeautifulSoup(page)
    
        event = soup.findAll('article', attrs={'class':'activity-feed ie-activity-list activity with-anchor'})
    
        half_marathon = {}
        
        for aa in event:

            dict2 = {}
            hr = aa.find('a', attrs={'class':"ie-article-link"})

            if "http://www." in hr['href']:
                nest_url = hr['href']
            else:
                nest_url = 'http://www.active.com' + hr['href']

            print nest_url

            nest_page = urllib2.urlopen(nest_url)
            nest_soup = BeautifulSoup(nest_page)
            nest_evnt = soup.find('div', attrs={'class':'ed-images-inner'})
            ns = nest_soup.find('h1', attrs={'itemprop' : 'name'})
            
            try:
                title = ns.text
            except Exception as ex:
                title = None
            
            try:
                distance = aa.find('h6', attrs={'class':'secondary-text desc-info'}).text
            except Exception as ex:
                distance = None
            try:
                address = ns.findNext('span', attrs={'class' : 'ed-address-text'}).text
            except Exception as ex:
                address = None
            
            try:
                event_date = ns.findNext('h5').text
            except Exception as ex:
                event_date = None
            
            try:    
                start_date = nest_soup.find('meta', attrs={'itemprop' : 'startDate'})['content']
                end_date = nest_soup.find('meta', attrs={'itemprop' : 'endDate'})['content']
            except Exception as ex:
                start_date = None
                end_date = None
                
            try:
                description = nest_soup.find('section', attrs={'id':'about-this-event'}).text
            except Exception as ex:
                description = None
#             import ipdb; ipdb.set_trace()
            try:
                web_anchor = nest_soup.find('section', attrs={'class':'section widget org-info'})
                website = web_anchor.find('a', attrs={'itemprop':"url"})['href']
            except Exception as ex:
                website = None
            
            try:
                img_attr = nest_soup.find('div', attrs={'class':'ed-images-inner'})
                img_url = img_attr.first().get('src')
                img_file_name = img_url.split('/')[-1]
                urllib.urlretrieve(img_url, image_directory+img_url.split('/')[-1])
            except Exception as ex:
                pass
            
            l1 = []
            
            try:
                aaa = nest_soup.findAll('p', attrs={'class':"p1"})
                l11 = len(aaa)
                if l11>0:
                    ak = aaa[l11-1]
                    sb = ak.findNextSiblings()
                    event_time = []
                    for ak in sb:
                        if ('am:' or 'pm:') in ak.text:
                            event_time.append(ak.text)
                else:
                    event_time = None
            except Exception as ex:
                event_time = None

            try:            
                dict2.update({'id' : cnt,
                               "nested_page" : nest_url,
                              "event_title" : str(title.encode('utf-8').strip()),
                               "distance": str(distance),
                               "address": str(address.replace("&nbsp;", ' ')) if address else None,
                               "event_date" : str(event_date),
                               "start_date" : str(start_date),
                               "end_date" : str(end_date),
                               "event_website" : website, 
                              "event_image" : str(img_file_name),
                              "description" : description.replace("&nbsp;", ' ') if description else None,
                              "event_time" : event_time
                         })
                
                l1.append(dict2)
        
                dict1.update({cnt:l1})
            except Exception as ex:
                dict2.update({"nested_page" : nest_url})
                l1.append(dict2)
                dict1.update({cnt:l1})
            
            cnt += 1
            
            jsn = json.dumps(dict1)
            
    return jsn


if __name__ == "__main__":
    """
    """
    try:
        os.mkdir(os.getcwd()+ '/run2gio')
    except OSError:
        pass
    
    if sys.argv[1] == '1':
        marathon_type = "marathon"
    elif sys.argv[1] == '2':
        marathon_type = "half-marathon"
    else:
        print "Please enter valid choice, 1 for Full-marathon & 2 for Half-marathon"
    
    if sys.argv[1] == '1' or sys.argv[1] == '2':    
        image_directory = os.getcwd() + '/run2gio/'
        
        quote_page = 'http://www.active.com/running/' + marathon_type #sys.argv[1] 
        page = urllib2.urlopen(quote_page)
        soup = BeautifulSoup(page)
        
        pg = soup.find('ul', attrs={'class':"visible-mobile"})
        max_page = int(pg.findChildren('li')[-1].text)
        fp = open(os.getcwd()+'/'+ marathon_type+'.json', 'a+')
        json = scrap_data(marathon_type, max_page, image_directory, fp)
        fp.write(json)
        print json
