import pymongo

client = pymongo.MongoClient('mongodb://192.168.1.200:27018/?directConnection=true&appName=mongosh+2.2.9')
db=client['data']
col=db['col']

data_list = [] 
count=0 
# 打开文件并读取内容  
with open("data.txt", 'r', encoding='utf-8') as file:  # 使用编码'utf-8'  
    for line in file:  
        if(count==0):
            count+=1
            continue
        else:
            # _id & cate
            parts = line.split(',', 2)  # 只分割一次，得到_id和其他内容的列表  
            _id = parts[0]  
            cate = parts[1]
            rest_of_line = parts[2] 
            # print(_id)
            # print(cate)

            # ctime
            temp_line=rest_of_line
            s=temp_line.split(',')
            ctime_index=0
            ctime=0
            for index, part in enumerate(s):  
                if (len(part) == 10 and part.isdigit()):  
                    ctime = part  
                    ctime_index = index
            # print(ctime)

            # content
            content=','.join(s[:ctime_index])
            # print(content)

            # key_word
            raw_key_words_end_index=0
            raw_key_words=s[ctime_index+1]
            if(len(s[ctime_index+1])!=0 and s[ctime_index+1][0]=='"' and s[ctime_index+1][-1]!='"'):
                raw_key_words=raw_key_words[1:]
                for i,part in enumerate(s[ctime_index+2:-1]):
                    raw_key_words+=','+part
                    if(part[-1]=='"'):
                        raw_key_words=raw_key_words[:-1]
                        raw_key_words_end_index=ctime_index+2+i
                        break
            else:
                raw_key_words_end_index=ctime_index+1
            # print(raw_key_words)


            #title
            title=','.join(s[raw_key_words_end_index+1:-1])
            # print(title)
            
            # 提取url（从http开始到行尾）  
            url=s[-1]
            # print(url)

            data = {  
                    '_id': _id,  
                    'cate': cate,
                    'content': content,  
                    'ctime': ctime,  
                    'raw_key_words': raw_key_words,  
                    'title': title,  
                    'url': url  
                    } 
            data_list.append(data)


col.insert_many(data_list)
