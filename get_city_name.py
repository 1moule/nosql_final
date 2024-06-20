import csv
import json
import jsonpath
import urllib.request as ur 

# 使用jsonpath解析淘票票获取城市列表
url = 'https://dianying.taobao.com/cityAction.json?activityId&_ksTS=1662244862648_108&jsoncallback=jsonp109&action=cityAction&n_s=new&event_submit_doGetAllRegion=true'
headers = {
    'referer': 'https://dianying.taobao.com/',
}
req = ur.Request(url=url, headers=headers)
resp = ur.urlopen(req)
content = resp.read().decode('utf-8')
content = content.split('(')[1].split(')')[0]
# 因为jsonpath只能解析本地文件，所以需要先保存
with open('city_name.json', 'w', encoding='utf-8') as f:
    f.write(content)

# 加载淘票票数据文件    
obj = json.load(open('city_name.json', 'r', encoding='utf-8'))
# $表示根节点，.or[]取子节点，@表示现行节点，..表示不管位置选择所有符合条件的节点，
# *匹配所有元素节点，[]表示迭代器指示、比如下标，?()支持过滤操作，()分组
cities = jsonpath.jsonpath(obj, '$..regionName')
with open('city_name.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for city in cities:
        city_csv = []
        city_csv.append(city)
        writer.writerow(city_csv)
