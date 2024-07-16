# 该脚本用于导出linename 与 sn
import psycopg2, os
import shutil
from datetime import datetime
from requests import Session
from zeep.transports import Transport
import logging
import http.client
import json
from zeep import Client


def main():
    # 正式服务器连接数据库
    session = Session()
    session.verify = False
    transport = Transport(session=session) 
    conn = psycopg2.connect( 
        dbname='aoiss',
        user='postgres',
        password='1234qwer!@#$QWER',
        host='10.41.242.38',
        port='8301',
    )
    # stagename = ["S1B","S1T","S7B","S7T","S12B","S12T","S18B","S18T","S19","S26B","S26T","D1","D2","D7","D11","D12","D18","D18F","D26"]
    stagename = ["D1"]
    # 获取S1B_log.txt的数据
    with open('S1B_log.txt','r') as file:
        lines = file.readlines()
        valid_stagenames = [line.strip() for line in lines]

    img_file = 'img.txt' # 记录已复制图片
    folder_path = 'hdd' #图片根目录
    os.makedirs(folder_path, exist_ok=True)
    cur = conn.cursor()

    # 获取已复制的图片列表
    copied_images = set()
    if os.path.isfile(img_file):
        with open(img_file, 'r') as f:
            for line in f:
                copied_images.add(line.strip())

    for stage in stagename:
        for valid_stage in valid_stagenames:
            if valid_stage in valid_stagenames:
                cur.execute(
                    'select "Path","DateTime" from "AOIStorageRecord" where "LineName" = %s and "SerialNumber" = %s',
                    (stage,valid_stage),
                )
                records = cur.fetchall()
                print('sn',valid_stage,records)
                for i,record in enumerate(records):
                    file_path = record[0]  # Path
                    datetimes = record[1]  # DateTime
                    year = datetimes.strftime("%Y")  # 提取年月部分，例 '2021'
                    month = datetimes.strftime("%m")  # 提取年月部分，例 '04'
                    year_month = year + "-" + month  # 年份和月份拼接 '2021-04'
                    datetime_dir = os.path.join(folder_path, year, month)  # 图片存储路径
                    # datetime_dir = os.path.join(folder_path, year_month) #图片存储路径                
                    file_name = os.path.basename(file_path)

                    # 创建年月文件夹
                    os.makedirs(datetime_dir, exist_ok=True)

                    # # 检查图片是否已复制过，如果是则跳过该图片
                    if file_name in copied_images:
                        continue

                    destination_path = os.path.join(datetime_dir, file_name)
                    if os.path.exists(destination_path): #判断文件夹中是否存在同名图片
                        dot_index = file_name.rfind(".")  # 获取最后一个点的位置
                        new_file_name = file_name[:dot_index] + "_" + str(i) + file_name[dot_index:] # 生成新的文件名
                        destination_path = os.path.join(datetime_dir, new_file_name)
                    shutil.copy2(file_path, destination_path)

                    # 记录已复制的图片
                    with open(img_file, 'a') as f:
                        f.write(file_name + '\n')

        conn.commit()


    conn.close()




if __name__ == "__main__":
    main()


