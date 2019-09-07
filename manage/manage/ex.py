# import xlrd
import pymysql



# data = xlrd.open_workbook('excel.xlsx')
# table = data.sheets()[2]          #通过索引顺序获取

# table = data.sheet_by_index(0) #通过索引顺序获取
# sheet = data.sheet_by_name(u'Sheet3')#通过名称获取


client=pymysql.connect(
    host='rm-uf6h7mn2i76j190dw9o.mysql.rds.aliyuncs.com',
    port=3306,
    user='zhaoli',
    password='Ab58576145',
    database='manage',
    charset='utf8'
)
cursor1=client.cursor() # cursor是游标，执行结果默认返回元组
# for i in range(858):
#     t = table.row_values(i)
depart_list = "1,2,3"
func_list = "1,2,3,4,5,6"
sql = """insert into `group` (id,name,`describe`,depart_list,func_list) values (1,'研发','研发人员','%s','%s');""" %(depart_list,func_list)
# sql = """insert into users (id,name,join_time,department_id,user_id,status,password,role,deleted) values('%s','%s','%s','%s','%s','%s','%s','%s','%s');""" %(t[0],t[1],t[3],int(t[6]),str(t[7]).replace('.0',''),1,'123456',3 , 0)
res = cursor1.execute(sql)
# print(333)
client.commit()
cursor1.close()
client.close()