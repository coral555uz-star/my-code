import json
import pymysql


#1、读取json文件
with open('result.json','r',encoding='utf-8') as f:
    data=json.load(f)

#2、连接mysql
conn=pymysql.connect(
    host='127.0.0.1',
    user='root',
    passwd='123456',
    database='chip',
    charset='utf8mb4'
)
cursor = conn.cursor()



for key,value in data.items():
    print(f"正在导入：{key} - {value}")
    sql=f"INSERT INTO chip_info (chip_name, guo_chan, car_type, score, shipment, intro, chip_application, summary) VALUES ('{key}', '空', '空', 10, 0, '{value}', 0, '空')"
    cursor.execute(sql) 
conn.commit()
cursor.close()
conn.close()
print("导入完成")
