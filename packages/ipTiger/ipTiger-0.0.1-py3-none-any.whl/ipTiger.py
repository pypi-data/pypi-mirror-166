import requests
from bs4 import BeautifulSoup

def detect_ip_address():
   url = "https://www.myip.com/"
   r = requests.get(url).text
   soup = BeautifulSoup(r,'lxml')
   ip = soup.select("#ip")[0].text
   print(f"your ip address: ",ip)
   return ip


def find_ip_details():
    ip = detect_ip_address()    
    url =f'http://ip-api.com/json/{ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,isp,org,as,asname,reverse,mobile,proxy,hosting,query'
    response = requests.get(url) 
    data = response.json()
    print(data)
    return data


    
    
  
