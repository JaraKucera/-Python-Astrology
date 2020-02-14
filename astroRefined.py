#**********     imports         **********
import requests
import json
from opencage.geocoder import OpenCageGeocode
#**********     Global          **********
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
#**********     classes         **********
class Person:
    timezone = ""
    def __init__(self, name, day, month, year, timeOfBirth, locationOfBirth):
        self.name = name
        self.day = day
        self.month = month
        self.year = year
        self.timeOfBirth = timeOfBirth
        self.locationOfBirth = locationOfBirth
        self.coords = self.getCoords(locationOfBirth) #Get lat and long of birth
        input = self.year+"-"+self.month+"-"+self.day+"T"+self.timeOfBirth+self.timezone
        self.Planets = []
        self.getPlanetPositions(input) #get planet positions
        print(self)
        

    def __str__(self):
        out = ""
        for pl in self.Planets:
            out += pl.__str__()+"\n"
        return "\nName: "+self.name+"\nDOB: "+self.day+"/"+self.month+"/"+self.year+"\nLocation of Birth: "+self.locationOfBirth+"\nTime: "+self.timeOfBirth+"\nCoords: "+self.coords+"\nTimezone: "+self.timezone+"\n"+out
    
    def getCoords(self,addr):
        results = geocoder.geocode(addr)
        self.timezone = results[0]['annotations']['timezone']['offset_string'][0:3]+":"+results[0]['annotations']['timezone']['offset_string'][-2:]  
        return str(results[0]['geometry']['lat'])+","+str(results[0]['geometry']['lng'])

    def getPlanetPositions(self,datetime):
        params = {
            "ayanamsa": "1",
            "chart_type": "rasi",
            "datetime": datetime,
            "coordinates": self.coords,
        }
        response = requests.get('https://api.prokerala.com/v1/astrology/planet-position', headers=headers, proxies=proxies, params=params)
        outs = response.json()
        for i in range (0,7):
            name = outs['response']['planet_positions'][str(i)]['name']
            retro = outs['response']['planet_positions'][str(i)]['is_reverse']
            sign = outs['response']['planet_positions'][str(i)]['rasi']
            planet = Planet(name, retro, sign)
            self.Planets.append(planet)
    
    
class Planet:
    def __init__(self, name, retrograde, sign):
        self.name = name
        self.retrograde = retrograde
        self.sign = sign
    
    def __str__(self):
        if(self.retrograde):
            return self.name +" in: "+ self.sign +" (R)"
        else:
            return self.name +" in: "+ self.sign

#**********     functions       **********
#**********     Main            **********
p1 = Person("Joe Hudson", "16","07","1999","23:30:00","Cheb,Czechia")