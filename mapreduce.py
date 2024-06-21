import pymongo
import json
from bson.code import Code 

client = pymongo.MongoClient('mongodb://192.168.1.200:27018/?directConnection=true&appName=mongosh+2.2.9')
db=client['data']
col=db['col']

citys = []  
with open('city_name.csv', 'r', encoding='utf-8') as f:  
    for line in f:  
        city = line.strip()
        citys.append(f'"{city}"')
citys_json = '[' + ', '.join(citys) + ']'  

#  city-news_count
cityMapFun = Code("""    
    function() {    
        var keywords = this.raw_key_words.split(/[\\s,]+/); // 假设raw_key_words是空格或逗号分隔的  
        var citys_names = %s; // 使用JSON.parse解析城市名称数组  
        for(var i = 0; i < keywords.length; i++){  
            for(var j = 0; j < citys_names.length; j++){  
                if(keywords[i] === citys_names[j]){  
                    emit(keywords[i], 1);  
                }  
                if(keywords[i].slice(0, 2)===citys_names[j]){
                    emit(keywords[i].slice(0,2),1);
                }
            }        
        }  
    }  
""" % citys_json)  

# month-news_count
timeMapFun = Code("""    
    function() {    
        var keywords = this.raw_key_words.split(/[\\s,]+/); // 假设raw_key_words是空格或逗号分隔的   
        var date = new Date(Number(this.ctime) * 1000);
        var year = date.getUTCFullYear();  
        var month = date.getMonth();
        const quarter = Math.ceil((month + 1) / 3);  
        var formattedTimeCustom = `${year}-${quarter}`;
        emit(formattedTimeCustom, 1);   
    }  
""")  

# time-news_count
monthMapFun = Code("""    
    function() {    
        var keywords = this.raw_key_words.split(/[\\s,]+/); // 假设raw_key_words是空格或逗号分隔的   
        var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]; 
        for(var i = 0; i < keywords.length; i++){              
            if(keywords[i] === '新冠肺炎'){  
                var date = new Date(Number(this.ctime) * 1000);
                var month = date.getMonth(); 
                emit(monthNames[month], 1);  
            }        
        }  
    }  
""")

# cate-news_count
cateMapFun = Code("function (){"
              "emit(this.cate,1);"
              "}")

reducefun = Code("""
                function(key,values){
                    return Array.sum(values);
                 };
                 """) 

# city_result = col.map_reduce(cityMapFun, reducefun, "city_results")  
# month_result=col.map_reduce(monthMapFun,reducefun,"month_results")
time_result=col.map_reduce(timeMapFun,reducefun,"time_results")
# cate_resule=col.map_reduce(cateMapFun,reducefun,"cate_results")

# for doc in db.city_results.find():
#     print(doc)
# for doc in db.month_results.find():
#     print(doc)
# for doc in db.cate_results.find():
#     print(doc)
for doc in db.time_results.find():
    print(doc)