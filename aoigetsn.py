# 该脚本用于导出linename 与 sn
import psycopg2, os


def main():
    # 正式服务器连接数据库
    conn = psycopg2.connect( 
        dbname='aoiss',
        user='postgres',
        password='1234qwer!@#$QWER',
        host='10.41.242.38',
        # host='127.0.0.1',
        port='8301',
    )
    # 测试服务器连接数据库
    # conn = psycopg2.connect(
    #     dbname='aoiss',
    #     user='postgres',
    #     password='1234qwer!@#$QWER',
    #     host='10.41.95.85',
    #     port='8301',
    # )
    stagename = ["DIP_FINAL_AOI", "0"]
    cur = conn.cursor() #创建一个游标对象cur，用于执行数据库查询操作。
    cur.execute(
        '''select "LineName", "SerialNumber" from "AOIStorageRecord" where "StageName"=%s and "IsSubgraph"=%s ''',
        stagename,
    )
    raw = cur.fetchall() #将查询结果保存在变量raw中，以元组的形式存储。
    
    print(raw)
    # print(raw[1][0])
    savedir = os.getcwd() #获取当前工作目录
    savefile = "FinanAOI_SN.txt"
    savepath = os.path.join(savedir, savefile) #将savedir和savefile连接起来，形成保存文件的完整路径名，
    with open(savepath, 'a+', encoding="utf-8") as t:  # 创建或者续写记录文档
        with open(savepath, 'r') as fp:  # 读取记录文档的内容
            writed = fp.read().splitlines() #将fp文件中的内容读取出来，并使用splitlines()函数将其分割成行的列表形式
        for i in raw:
            # print(i)
            linename = i[0]
            sn = i[1]
            line = linename + " " + sn
            # print(line)
            if line in writed:
                print(line + "pass")
            else:
                t.writelines(line + "\n")


if __name__ == "__main__":
    main()
