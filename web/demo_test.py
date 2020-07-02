import pandas as pd
import json

data = pd.read_csv('商家資料 - 清單.csv')
el = dict([])
el['name'] = dict(data['NAME'])
el['google_name'] = dict(data[''])
el['store_type'] = dict(data['STORE TYPE ID'])
el['phone'] = dict(data['PHONE'])
el['person'] = dict(data['PERSON'])
el['email'] = dict(data['EMAIL'])
el['website'] = dict(data['WEBSITE'])
el['address'] = dict(data['ADDRESS'])
el['storediscount'] = dict(data['DISCOUNT TYPE ID'])
el['latitude'] = None
el['longitude'] = None
el['location'] = None
el['county'] = None
el['district'] = None
el['google_status'] = None
el = json.dumps(el)
print(el)

