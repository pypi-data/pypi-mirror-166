#测试库token
from pyrda.dbms.rds import RdClient
def getcode(app2,param,tableName,param1,param2):
    '''
    通过传入的参数获得相应的编码
    :param app2 执行sql语句对象:
    :param param 需要查询的字段:
    :param tableName 表名:
    :param param1 查询条件字段:
    :param param2 条件:
    :return 将查询的到的结果返回:
    '''

    sql=f"select {param} from {tableName} where {param1}='{param2}'"

    res=app2.select(sql)

    return res[0][f'{param}']


if __name__ == '__main__':
    result=getcode(RdClient('0D9A668B-B136-4F0C-9A81-32E6477426A9'),"FNUMBER","rds_vw_unit","FNAME","箱")

    print(result)