from ast import Or
from asyncio.windows_events import NULL
from ctypes import  c_bool, c_double, c_int, c_long, c_uint, WINFUNCTYPE, c_void_p, windll
from pytz import country_names, country_timezones,timezone,UnknownTimeZoneError,exceptions
from datetime import datetime
from ctypes.wintypes import HWND, LPCWSTR, POINT, UINT
from gettext import find
import struct
import requests 
import exoticwondrous.jsonex
import json
import os

# ExoDigital from exoticwondrous
# Telegram: https//exoticwondrous
# Ahmed Mohammmed
# ahmdsmhmmd@gmail.com   

class ExoDigital: 
         __xLoad = NULL
         __cityname= NULL
         def __init__(self,is_dark=None, is24Hour=None,is_Fahrenheit=None,time_out_delay=1000,showlogs=True):
              self.__drak = is_dark
              self.__Is24H = is24Hour
              self.__IsFahrenheit = is_Fahrenheit
              self.__TimeoutDelay = time_out_delay
              self.___showlogs = showlogs

              if (struct.calcsize("P")==8):    
                  dllname=str(os.path.dirname(__file__)) + '\\exodigitl.dll'
              else: dllname=str(os.path.dirname(__file__)) + '\\exodigitl32.dll'

              self.__showmsg("finding package exiting: " + str(os.path.isfile(dllname)))

              try: 
                     __xLoad = windll.LoadLibrary(dllname)
              except:
                 self.__showmsg('Error:cannot loading required files to run digialtclock')     

              __ExoCMain = WINFUNCTYPE(c_int,c_bool,c_bool,c_bool,c_int)
              __Weather = WINFUNCTYPE(c_int,LPCWSTR)
              __Weather_custom = WINFUNCTYPE(c_int,LPCWSTR,c_double,c_int)
              __Date_custom = WINFUNCTYPE(c_int,c_int,c_int)
              __Time_custom = WINFUNCTYPE(c_int,c_int,c_int,c_int)
              __Clock_elements  = WINFUNCTYPE(None,c_void_p)
              __Date_elements=WINFUNCTYPE(None,c_void_p)

              if __xLoad !=NULL:
                    self.__rundigitclock = __ExoCMain(("ExoDigitCMain",__xLoad))
                    self.__weather = __Weather(("weatherfromJosn",__xLoad))
                    self.__weather_custom = __Weather_custom(("weather_custom",__xLoad))      
                    self.__date_custom = __Date_custom(("date_custom",__xLoad))
                    self.__time_custom = __Time_custom(("time_custom",__xLoad))
                    self.__clock_elements = __Clock_elements(("get_clockelements",__xLoad))
                    self.__date_elements = __Date_elements(("get_datelements",__xLoad))
                    self.FUNC = WINFUNCTYPE(None,c_int,c_int,c_int)

              else:
                    self.__showmsg("Error: cannot get instance of __xload object: is equal to null")       

         def   __getweather__ (self,city):
               url = 'https://wttr.in/{0}?format=j2'.format(city)
               txt =  requests.get(url).text
               jso = json.loads(txt)
               self.__cityname = city
               return exoticwondrous.jsonex.Root.from_dict(jso)

         def __getcoutrycity_name(self,city_countryname=None,callback=False):                    
                          
                  if city_countryname!=None:city_countryname=str(city_countryname).lower()
                  ret =None         
                  countrykey = None
                  for k,v in country_names.items():
                     cn =cn= k.lower() if len(city_countryname)==2 else v.lower().replace('_',' ')
                     if cn.find(city_countryname)!=-1: 
                        countrykey = k.lower()
                        break

                  city_countryname= countrykey if countrykey!= None  else city_countryname               
                  for k,v in country_timezones.items():
                     cn = k.lower() if countrykey!= None else v[0].lower().replace('_',' ') 
                     if cn.find(city_countryname)!=-1: 
                           ret = v[0]
                           self.__showmsg('resp.by: country code['+k+']: '+ str(country_names[k]) +"/"+ str(v[0].split('/')[1]))
                           break      
                  
                  if callback == False:
                     if ret == None:
                        self.__showmsg('city not found in timezones trying getting from country name ....')
                        root= self.__getweather__(city_countryname)
                        wccountryname =  root.nearest_area.country.value 
                        return self.__getcoutrycity_name(wccountryname,True)      
                  return [ret,ret.split('/')[1],callback]


         def __gettime_location(self,citynametimezone):
            tz=None
            try:
                     tz = timezone(citynametimezone)
            except exceptions.Error as e:
                  self.__showmsg('Warring:Unknown zone response,a local time zone is using instead.')
            except Exception as e:
                  self.__showmsg('Warring:Unknown zone response,a local time zone is using instead.. ')            
            return tz
                  
                  
         def __showmsg(self,prt):
              if self.___showlogs:
                 print(prt)
               
         def RunAndWait(self): 
              ret = self.__rundigitclock(self.__drak,self.__Is24H,self.__IsFahrenheit,self.__TimeoutDelay)
              if ret== 0:
                  return 'launched digital clock.' 
              if ret == -1:
                   return 'Error: not valid weather value set'
              if ret ==-2: 
                   return 'Error: not valid delay set, is should be from 0-30000 millisecond'
              if ret == -3:
                   return  'Error not valid date set, please check custom date set'       
              if ret == -4:
                  return 'Error not valid time set, please check custom time set' 
              if ret == -5:
                   return 'Error not valid custom weather index set it should be from 0 to 9 only'
              if ret == -6:
                   return   'Error not valid weather data setup!'
              

         def SetWeather(self,city_name,live_timezone=False):
              self.__showmsg('Initialize...\nDone.')
              self.__showmsg('checking internet connection...Please wait...')
              try:
                 cityname = self.__getcoutrycity_name(city_name)
                 
                 root = self.__getweather__(city_name)
                 self.__showmsg('Done.')
                 if live_timezone:
                    self.__showmsg('waiting response from a live server...')
                    __timenow =self.__gettime_location(cityname[0])
                    if __timenow!=None:
                     __tm= datetime.now(__timenow)
                     self.SetTime(__tm.hour,__tm.minute,__tm.second)
                     self.SetDate(__tm.day,__tm.month)
                     self.__showmsg('Done.')
                    else: self.__showmsg('Warring:Unknown zone response,a local time zone is using instead')

                 return self.__weather(str(root.nearest_area.country.value)+"*"+str(
                    root.nearest_area.region.value if cityname[2] else cityname[1])+'-'+str(root.nearest_area.areaName.value)+'*'+str(root.current_condition.FeelsLikeC)+'*'+ str(root.current_condition.weatherCode+'*'+str(root.current_condition.weatherDesc.value))) 
              except Exception as e:
                 if str(e).find('HTTPSConnectionPool')!=-1 or str(e).find('Connection aborted.')!=-1:
                    self.__showmsg('Error: cannot connect to live weather server! Please check your internet connection and try again')
                 elif str(e).find('NoneType')!=-1:
                    self.__showmsg('Error: cannot find city or..country name /or data cannot set correctly')
                 else:
                    self.__showmsg(' Error: package-module might be corrupted,Please request pip uninstall  \'exodigital\' then type pip install  \'exodigital\' again')  

         def SetDate(self,Day, Month):
              return self.__date_custom(Day,Month)
          
         def SetTime(self, Hour,Minute=None,Second=None):
              return self.__time_custom(Hour,Minute,Second)

         def SetDateTime(self,Country_CityName):
             cityname = self.__getcoutrycity_name(Country_CityName)
             __timenow =self.__gettime_location(cityname[0])
             if __timenow!=None:
                __tm= datetime.now(__timenow)
                self.SetTime(__tm.hour,__tm.minute,__tm.second)
                self.SetDate(__tm.day,__tm.month)
             else: self.__showmsg('Warring:Unknown zone response,a local time zone is using instead.')

         def SetWeather_custom(self,city_name,temperature,weather_index):
             return self.__weather_custom(city_name,temperature,weather_index)
             
         def GetClockElements(self,fun):
            if fun!=None:
                self.__clock_elements(fun)
            else: self.__showmsg('Error: in GetClockElements function calling-back is required here')   

         def GetDateElements(self,fun):
            if fun!=None:
                self.__date_elements(fun)
            else: self.__showmsg('Error: in GetDateElements function calling-back is required here')   


         def GetWeatherElements(self,all=False,coutryname=None,temp=None,maxtemp=None,mintemp=None,
                              desc=None,uvindex=None,humidity=None,
                              pressure=None,pressureInches=None,precipMM=None,
                              cloudcover=None,localObsDateTime=None,winddirDegree=None,
                              windspeedKmph=None,windspeedMiles=None,windDirection=None,
                              areaName=None,region=None,latitude=None,longitude=None,totalSnow_cm=None,sunHour=None,
                              sunrise=None,sunset= None,moonset=None,
                              moon_phase=None,
                              moonrise=None,
                              moon_illumination=None
                             ):
             if self.__cityname!=NULL:
               try:
                 __xRetData =[]
                 root = self.__getweather__(self.__cityname) 
                  
                 if coutryname!=None or all==True:
                    __xRetData.append(root.nearest_area.country.value)  
                 if temp !=None or all==True:
                    __xRetData.append( root.current_condition.temp_F if self.__IsFahrenheit else root.current_condition.temp_C ) 
                 if uvindex!=None or all==True:     
                    __xRetData.append( root.current_condition.uvIndex) 
                 if humidity!=None or all==True:
                  __xRetData.append(root.current_condition.humidity)   
                 if desc!=None or all==True:     
                    __xRetData.append( root.current_condition.weatherDesc.value)
                 if pressure!=None or all==True:     
                    __xRetData.append( root.current_condition.pressure)
                 if pressureInches!=None or all==True:     
                    __xRetData.append( root.current_condition.pressureInches)
                 if precipMM!=None or all==True:     
                    __xRetData.append( root.current_condition.precipMM)
                 if cloudcover!=None or all==True:     
                    __xRetData.append( root.current_condition.cloudcover)
                 if localObsDateTime!=None or all==True:     
                    __xRetData.append( root.current_condition.localObsDateTime)
                 if winddirDegree!=None or all==True:     
                    __xRetData.append( root.current_condition.winddirDegree)
                 if windspeedKmph!=None or all==True:     
                    __xRetData.append( root.current_condition.windspeedKmph)
                 if windspeedMiles!=None or all==True:     
                    __xRetData.append( root.current_condition.windspeedMiles)
                 if windDirection or all==True:
                     __xRetData.append(root.current_condition.winddir16Point)  
                 if areaName!=None or all==True:     
                    __xRetData.append( root.nearest_area.areaName.value)
                 if region!=None or all==True:     
                    __xRetData.append( root.nearest_area.region.value)
                 if latitude!=None or all==True:     
                    __xRetData.append( root.nearest_area.latitude)
                 if longitude!=None or all==True:     
                    __xRetData.append( root.nearest_area.longitude)
                 if totalSnow_cm!=None or all==True:     
                    __xRetData.append( root.weather.totalSnow_cm)
                 if maxtemp!=None or all==True:     
                    __xRetData.append( root.weather.maxtempF if self.__IsFahrenheit else root.weather.maxtempC)
                 if mintemp!=None or all==True:     
                    __xRetData.append( root.weather.mintempF if self.__IsFahrenheit else root.weather.mintempC)
                 if sunHour!=None or all==True:
                    __xRetData.append( root.weather.sunHour)
                 if sunrise!=None or all==True:     
                    __xRetData.append( root.weather.astronomy.sunrise)
                 if moonset!=None or all==True:     
                    __xRetData.append( root.weather.astronomy.moonset)
                 if moon_phase!=None or all==True:     
                    __xRetData.append( root.weather.astronomy.moon_phase)
                 if moonrise!=None or all==True:     
                    __xRetData.append( root.weather.astronomy.moonrise)
                 if sunset!=None or all==True:     
                    __xRetData.append( root.weather.astronomy.sunset)
                 if moon_illumination!=None or all==True:     
                    __xRetData.append( root.weather.astronomy.moon_illumination)
                 return __xRetData
               
               except Exception as e:
                 if str(e).find('HTTPSConnectionPool')!=-1 or str(e).find('Connection aborted.')!=-1:
                    self.__showmsg('Error: cannot connect to live weather server! Please check your internet connection and try again')
                 elif str(e).find('NoneType')!=-1:
                    self.__showmsg('Error: cannot find city or..country name or data cannot set correctly')
                 else:
                    self.__showmsg(' Error: package-module might be corrupted,Please request pip uninstall  \'exodigital\' then type pip install  \'exodigital\' again.')  

             else: self.__showmsg( 'Error: cannot find city name,Please call SetWeather before calling this function')
 