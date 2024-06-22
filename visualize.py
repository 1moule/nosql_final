import pymongo
import matplotlib.pyplot as plt  
from matplotlib.font_manager import FontProperties
import numpy as np 
from datetime import datetime  

# connect to mongodb
client = pymongo.MongoClient('mongodb://192.168.1.200:27018/?directConnection=true&appName=mongosh+2.2.9')
db=client['data']
 
# setup plot
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
TNR = {'fontname':'Times New Roman'}
Fs = {'fontname':'Fangsong'}
cmap = plt.get_cmap('viridis')  # 使用'viridis'或其他颜色映射  

# draw bar
def drawBar(x_data,y_data,x_label,y_label,title):
    colors = cmap(np.linspace(0, 1, len(y_data)))  # 为每个柱子生成颜色 
    ax=plt.axes()
    plt.grid(axis='y',c='#d2c9eb',linestyle='--',zorder=0)
    plt.bar(x_data, y_data,zorder=10,tick_label=x_data,color=colors) 
    for a,b in zip(x_data,y_data):
        plt.text(a,b+0.03,b, ha='center', va= 'bottom',fontsize=10,**TNR)
    [ax.spines[loc_axis].set_visible(False) for loc_axis in ['top','right','bottom','left']]
    plt.xticks(rotation=-45)
    # 设置图表标题和轴标签  
    plt.title(title,**TNR)  
    plt.xlabel(x_label,**TNR)  
    plt.ylabel(y_label,**TNR)
    plt.plot(x_data,y_data,'o-',zorder=20,color = '#006400',label="CNN-RLSTM")#o-:圆形  
    # 显示图表  
    plt.tight_layout()
    plt.savefig('./pictures/'+x_label+'.png')
    plt.show()

def drawManyBar(x_lists,y_lists,x_label,y_label,title):
    fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(19.2, 10.8), dpi=100) 
    axs = axs.flatten()
    fig.suptitle(title,**TNR)
    for ax, (x_list, y_list) in zip(axs, zip(x_lists, y_lists)):  
        # 在子图上绘制柱状图  
        colors = cmap(np.linspace(0, 1, len(y_list)))  # 为每个柱子生成颜色 
        ax.grid(axis='y',c='#d2c9eb',linestyle='--',zorder=0)
        for spine in ['top', 'right', 'bottom', 'left']:  
            ax.spines[spine].set_visible(False) 
        ax.bar(x_list, y_list, color=colors,zorder=10)  
        ax.set_xticks(x_list)  
        ax.set_xticklabels(x_list, rotation=-50)
        ax.set_xlabel(x_label,**TNR)  
        ax.set_ylabel(y_label,**TNR)  
        # ax.set_title('Bar Chart')  
        # ax.legend() 
    plt.tight_layout()  
    # 显示画布  
    plt.subplots_adjust(wspace=0.15, hspace=0.6)
    plt.subplots_adjust(bottom=0.1,top=0.95)
    plt.savefig('./pictures/'+x_label+'.png')
    plt.show()

def drawPie(x_data,y_data,title):
    colors = cmap(np.linspace(0, 1, len(y_data)))  # 生成颜色 
    # 突出显示部分
    max_index = y_data.index(max(y_data))  
    explode = [0.08 if i == max_index else 0 for i in range(len(x_data))] 
    # 创建饼图
    plt.pie(y_data,              # 数据数组，表示每个部分的大小
            explode=explode,    # 偏移量数组
            labels=x_data,    # 标签数组
            colors=colors,      # 颜色数组
            autopct='%.1f%%',  # 控制百分比显示格式
            shadow=True,        # 阴影效果
            startangle=140)     # 起始角度，以逆时针方向测量，从x轴正方向开始计算角度
    # 设置图表标题
    plt.title(title,**TNR)
    plt.legend(bbox_to_anchor=(0,1.05))
    plt.savefig('./pictures/'+x_label+'.png')
    # 显示图表
    plt.show()

# month-news
month_order = {  
    'January': 1, 'February': 2, 'March': 3, 'April': 4,  
    'May': 5, 'June': 6, 'July': 7, 'August': 8,  
    'September': 9, 'October': 10, 'November': 11, 'December': 12  
}   
months = [doc['_id'] for doc in db.month_results.find()]  
sorted_indices = sorted(range(len(months)), key=lambda k: month_order[months[k]])
x=[]
y=[]
for index in sorted_indices:
    x.append(db.month_results.find()[index]['_id'])
    y.append(db.month_results.find()[index]['value'])
x_label='Month'
y_label='News Count'
title='News Count by Month Related to Epidemic'
drawBar(x,y,x_label,y_label,title)

# cate-news
x=[]
y=[]
for doc in db.cate_results.find():
    x.append(doc['_id'])
    y.append(doc['value'])
x_label='Cate'
y_label='News Count'
title='Diffrient Cate News Proportion'
drawPie(x,y,title)

# city-news
parts = []  
current_part = []  
city_parts = []  
current_city_part = [] 
value_parts = []  
current_value_part = [] 
part_index = 0  
cursor = db.city_results.find().sort('value', pymongo.ASCENDING)  
total_records = db.city_results.count_documents({})  # 传入查询条件作为参数  
records_per_part = total_records // 11  
remainder = total_records % 11  
# 遍历cursor并分割记录  
for record in cursor:  
    current_part.append(record)  
    current_city_part.append(record['_id'])
    current_value_part.append(record['value'])
    if len(current_part) == records_per_part:  
        # 如果当前部分已满，将其添加到parts列表中，并初始化新部分  
        parts.append(current_part)  
        city_parts.append(current_city_part)
        value_parts.append(current_value_part)
        current_part = []  
        current_city_part = [] 
        current_value_part = [] 
        part_index += 1  
        # 如果还有余数且当前是最后一个部分，添加额外的记录  
        if part_index == 10 and remainder > 0:  
            break 
if current_part:  
    parts.append(current_part)
    city_parts.append(current_city_part)
    value_parts.append(current_value_part)
x_label='City'
y_label='News Count'
title="News Count by City"
drawManyBar(city_parts,value_parts,x_label,y_label,title)

# time-news
x=[]
y=[]
for doc in db.time_results.find().sort("_id"):
    quarter_name=["春","夏","秋","冬"]
    x.append(doc['_id'][:-1]+quarter_name[int(doc['_id'][-1])-1])
    y.append(doc['value'])
print(x)
x_label='Quarter'
y_label='News Count'
title="News Count by Quarter"
drawBar(x,y,x_label,y_label,title)
    

