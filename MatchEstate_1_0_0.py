import pymysql
from pymysql.cursors import *

info = {'host': '172.16.8.160', 'user': 'root', 'password': '1qaz@WSX', 'database': 'mz', 'port': 3306}
with pymysql.connect(host=info['host'], user=info['user'], password=info['password'], port=info['port'],
                     database=info['database']) as conn:
    origin_cursor = conn.cursor(SSCursor)

    # 搜索没有小区的id
    find_null_estate_sql = """
        select id,地名 from result_full_origin
    """

    origin_cursor.execute(find_null_estate_sql)
    null_estate_id = origin_cursor.fetchall()

    for add_id, add_title in null_estate_id:
        fgj_cursor = conn.cursor()
        # 查找地名是否存在于房管局的小区名称中
        find_fgj_estate_sql = """
            select 小区名称 from fangguanju_address where 小区名称 like '{}'
        """.format(add_title)

        fgj_cursor.execute(find_fgj_estate_sql)
        fgj_estate_result = fgj_cursor.fetchone()
        if fgj_estate_result is not None:
            matched_fgj_estate = fgj_estate_result[0]

            # 更新原表的小区名称
            update_origin_estate_sql = """
                update result_full_origin set 小区='{}' where id='{}'
            """.format(matched_fgj_estate,add_id)

            fgj_cursor.execute(update_origin_estate_sql)
            conn.commit()