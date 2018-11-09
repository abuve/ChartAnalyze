#!/usr/bin/env python
# _*_coding:utf-8_*_

try:
    import pymysql
except ImportError:
    import MySQLdb


def ExecuteSQL(conn, sql, parameter=[], _type="select", is_batch=False, is_pd=False):
    """
    执行sql并返回结果
    :param conn:  mysql链接信息 类型{}
    :param sql:  执行的sql
    :param parameter:  传入的参数
    :param _type:  sql 的类型，select,delete,update,insert
    :param is_batch:  是否处理多行数据
    :param is_pd:  是否处理多行数据
    :return:
    """
    try:
        conn = pymysql.connect(**conn)
        sql = sql

        def execute():
            """
            返回数据
            :return:
            """
            cur = conn.cursor()
            if _type == "insert" and is_batch:
                rst = cur.executemany(sql, parameter)
            else:
                if parameter:
                    rst = cur.execute(sql, parameter)
                else:
                    rst = cur.execute(sql)
            if _type in ["insert", "update"]:
                conn.commit()
            # print(rst)
            #logger.info("{0}".format(rst))
            return cur.fetchall()

        def pd_execute():
            if _type == "select":
                # sql = sql % (tuple(parameter))
                df = pd.read_sql(sql, con=conn, params=parameter)
            return [df]

        if is_pd:
            data = pd_execute()
        else:
            data = execute()
        if data:
            # print(data)
            # logger.info("影响行数{0}".format(data))
            # print(execute()[0])
            return data
    except pymysql.err.OperationalError as e:
        print(conn,e)
        #logger.error(e.args)
        # print("")
    except pymysql.err.IntegrityError as e:
        print(conn,e)
        #logger.error(e.args)
    except Exception as e:
        print(conn,e)
        #logger.error(e.args)
        # except "timeout" as e:
        #     print(e)
    else:
        print("执行成功")
        #logger.info("执行成功")


if __name__ == "__main__":
    conn_dict = dict(host='rm-2ze4sz06v886yg0wg.mysql.rds.aliyuncs.com', user='aranya', passwd='aranya890@)!*', db='data_control', port=3306, charset='utf8')
    sql = """
        select id, mobile from member_base limit 10;
    """
    # df = ExecuteSQL(conn_dict, sql, parameter=[start_datetime,end_datetime], is_pd=True)
    # df = df[0]
    # print(df["ip"].count())
    result = ExecuteSQL(conn_dict, sql)
    print(result)

