from urllib2 import Request, urlopen, URLError
import simplejson as json
import time
city = "los angeles"
api_url = "http://api.eventful.com/json/events/search?"
api_token = "96MwLvP5qM2g3Xfx"
clean_events_data = []

class eventData(object):
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def __init__(self,name="none",description="none",event_url="none",start_time="none",end_time="none",logo_url="none",long="null",lat="null"):
        self.name=name
        self.description=description
        self.event_url=event_url
        self.start_time=start_time
        self.end_time=end_time
        self.logo_url=logo_url
        self.long=long
        self.lat=lat
        
def collectingData():
        full_data="{"+'"events"'+":["
        print "---------------------------"
        for ecd in clean_events_data:
            try:
                full_data+=ecd.to_JSON()
                full_data+=","
            except TypeError:
                print "-------------abc--------------"
                
                print ecd.name
                print ecd.description
                print ecd.start_time
                print ecd.logo_url
                print ecd.event_url
                print ecd.long
                print ecd.lat
        
        full_data+="{}]}"
        
#        print full_data
        print json.loads(full_data)

def checkNull(string):
    if(string):
        return string
    else:
        return "none"
    
def encoding(string):
    if(string):
        return string.encode('utf-8')
    else:
        return "none"

request_url = api_url+"location="+city.replace(" ","+")+"&app_key="+api_token
print request_url
try:
	request = Request(request_url)
        response = urlopen(request)
	api_data = response.read()
        json_data = json.loads(api_data)
#	print json_data
        
        
        try:
            page_count = int(json_data['page_count'])
        except:
            page_count = 0
            
#        print page_count
            
        request_url+="&page="
        
        for this_page in range(1,3):
            
#            print request_url+str(this_page)
            request = Request(request_url+str(this_page))
            response = urlopen(request)
            api_data = response.read()
            json_data = json.loads(api_data)
            print json_data
            try:
                page_size = int(json_data['page_size'])
            except:
                page_size = 0
            for event in range(1,page_size):
                try:
                    name = encoding(checkNull(json_data['events']['event'][event]['title']))
                except:
                    name = encoding(checkNull("none"))
                
                try:
                    description = encoding(checkNull(json_data['events']['event'][event]['description']))
                except:
                    description = encoding(checkNull("none")) 
                description = description
                
                try:
                    start_time =  json_data['events']['event'][event]['start_time']
                except:
                    start_time={}
                    
                try:
                    end_time =  json_data['events']['event'][event]['stop_time']
                except:
                    end_time={}
                    
                try:
                    logo_url =  json_data['events']['event'][event]['image']['medium']['url']
                except:
                    logo_url =  encoding(checkNull("none"))
                
                logo_url = logo_url.replace(" ","")
                
                try:
                    event_url = encoding(checkNull(json_data['events']['event'][event]['url']))
                except:
                    event_url = encoding(checkNull("none")) 
                event_url = event_url.replace(" ","")
                
                try:
                    long = encoding(checkNull(json_data['events']['event'][event]['longitude']))
                except:
                    long = encoding(checkNull("none")) 
                    
                try:
                    lat = encoding(checkNull(json_data['events']['event'][event]['latitude']))
                except:
                    lat = encoding(checkNull("none")) 
                    
                clean_events_data.append(eventData(name,description,event_url,start_time,end_time,logo_url,long,lat))
        
        collectingData()
            
except URLError, e:
    print 'No kittez. Got an error code:', e
    collectingData()
    