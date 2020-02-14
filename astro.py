#**********     imports     **********
import requests
import json
from opencage.geocoder import OpenCageGeocode
#**********     classes     **********
class Planet:
    Name = ""
    Retrograde = False
    Sign = ""
    def __str__(self):
        if(self.Retrograde):
            return self.Name +" in: "+ self.Sign +" (R)"
        else:
            return self.Name +" in: "+ self.Sign 
        
class Chart:
    Name = ""
    DOB = ""
    Planets = []
    def __str__(self):
        out = ""
        for pl in self.Planets:
            out += pl.__str__()+"\n"
        
        return "\n\nName: "+self.Name+"\nDOB: "+self.DOB+"\nChart:\n"+ out

class ResultComp:
    sign1 = ""
    sign2 = ""
    result = ""
    comment = ""
    def __str__(self):
        return self.sign1+":"+self.sign2+"\nResult: "+self.result +"\nComment: "+self.comment+"\n\n"

class Compability:
    partner1 = Chart()
    partner2 = Chart()
    res = []
    def __str__(self):
        out = ""
        for res in self.res:
            out += res.__str__()
        return out


#**********     Global        **********
proxies = {
    "http":"#",
    "https":"#"
}

headers = {
    'Authorization': 'Bearer #',
    "Accept": "application/json",
    "Content-Type": "application/json",
}
key = "#"
geocoder = OpenCageGeocode(key)
global results

#**********     functions     **********
def saveAsJson(response):
    s = response.json()
    with open('astrology.json', 'a', encoding='utf-8') as f:
        json.dump(s,f, ensure_ascii=False, indent=4)

def timezone():
    global results
    return results[0]['annotations']['timezone']['offset_string'][0:3]+":"+results[0]['annotations']['timezone']['offset_string'][-2:]  

def getCoords(address):
    res = geocoder.geocode(address)
    global results 
    results = res
    return str(res[0]['geometry']['lat'])+","+str(res[0]['geometry']['lng'])

def horoscopeMatching(system,bride_dob,bride_coordinates,bridegroom_dob,bridegroom_coordinates):
    params = {
       "system": system,
        "ayanamsa": "1",
        "bride_dob": bride_dob,
        "bride_coordinates": bride_coordinates,
        "bridegroom_dob": bridegroom_dob,
        "bridegroom_coordinates": bridegroom_coordinates, 
    }
    response = requests.get('https://api.prokerala.com/v1/astrology/horoscope-matching', headers=headers, proxies=proxies, params=params)
    saveAsJson(response)
    out = response.json()
    c = Compability()
    porutham = ['dina_porutham',"gana_porutham","mahendra_porutham","stree_dhrirgham_porutham","yoni_porutham","veda_porutham","rajju_porutham","vasya_porutham","rasi_porutham","rashyadhipa_porutham"]
    for i in porutham:
        r = ResultComp()
        r.sign1 = out['response']['detailed_information'][i]['bridegroom']
        r.sign2 = out['response']['detailed_information'][i]['bride']
        r.result = out['response']['detailed_information'][i]['result']
        r.comment = out['response']['detailed_information'][i]['comment']
        c.res.append(r)
    return c      


def kundliMatching(bride_dob,bride_coordinates,bridegroom_dob,bridegroom_coordinates):
    params = {
        "ayanamsa": "1",
        "bride_dob": bride_dob,
        "bride_coordinates": bride_coordinates,
        "bridegroom_dob": bridegroom_dob,
        "bridegroom_coordinates": bridegroom_coordinates, 
    }
    response = requests.get('https://api.prokerala.com/v1/astrology/kundli-matching', headers=headers, proxies=proxies, params=params)
    saveAsJson(response)

def planetPosition(chart_type,datetime,coordinates):
    params = {
        "ayanamsa": "1",
        "chart_type": chart_type,
        "datetime": datetime,
        "coordinates": coordinates,
    }
    response = requests.get('https://api.prokerala.com/v1/astrology/planet-position', headers=headers, proxies=proxies, params=params)
    saveAsJson(response)
    out = response.json()
    p = Chart()
    for i in range (0,7):
        planet = Planet()
        planet.Name = out['response']['planet_positions'][str(i)]['name']
        planet.Retrograde = out['response']['planet_positions'][str(i)]['is_reverse']
        planet.Sign = out['response']['planet_positions'][str(i)]['rasi']
        p.Planets.append(planet)
    
    #print(out['response']['planet_positions'])
    return p


def panchang(datetime,coordinates):
    params = {
        "ayanamsa": "1",
        "datetime": datetime,
        "coordinates": coordinates,
    }
    response = requests.get('https://api.prokerala.com/v1/astrology/panchang', headers=headers, proxies=proxies, params=params)
    saveAsJson(response)
    

#**********     Main     **********
c = horoscopeMatching("kerala","2004-02-12T15:19:21+00:00","10.214747,78.097626","2004-02-12T15:19:21+00:00","10.214747,78.097626")
kundliMatching("2004-02-12T15:19:21+00:00","10.214747,78.097626","2004-02-12T15:19:21+00:00","10.214747,78.097626")
planetPosition("rasi", "2004-02-12T15:19:21+00:00","10.214747,78.097626")
panchang("2004-02-12T15:19:21+00:00","10.214747,78.097626")
person = planetPosition("rasi","1999-07-16T23:30:00+01:00",getCoords("Cheb,Czechia"))
person.Name = "JK"
person.DOB = "1999-07-16T23:30:00"
print(person)
print(c)
