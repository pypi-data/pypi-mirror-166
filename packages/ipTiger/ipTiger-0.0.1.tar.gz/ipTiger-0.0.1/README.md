# ipTiger
ipTiger is an python package for find ip address details such as country name, city name, latitude and longitude etc

# how to install
`pip install ipTiger`

# example1
___
```
from ipTiger import find_ip_details,detect_ip_address

find_ip_details()
>>>your ip address:  195.181.162.180
{'status': 'success', 'continent': 'North America', 'continentCode': 'NA', 'country': 'United States', 'countryCode': 'US', 'region': 'FL', 'regionName': 'Florida', 'city': 'Miami', 'district': '', 'zip': '33197', 'lat': 25.7689, 'lon': -80.1946, 'timezone': 'America/New_York', 'isp': 'Datacamp Limited', 'org': '', 'as': 'AS60068 Datacamp Limited', 'asname': 'CDN77', 'reverse': 'unn-195-181-162-180.cdn77.com', 'mobile': False, 'proxy': True, 'hosting': True, 'query': '195.181.162.180'}

detect_ip_address()
>>>your ip address:  195.181.162.180



```

# find_ip_details
find_ip_details() function give you details of your ip address such as country name, city name, latitude and longitude etc.

# detect_ip_address 
detect_ip_address() function will find your ip adrress only.

# example2
here is an example if you want to find any specific details for ip address 

```
from ipTiger import detect_ip_address,find_ip_details 

data = find_ip_details() 
print("country name: ", data["country"])
```

 

