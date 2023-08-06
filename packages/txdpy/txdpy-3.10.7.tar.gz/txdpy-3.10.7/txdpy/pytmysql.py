# coding:utf-8
import re,pymysql
from pymysql.converters import escape_string
from loguru import logger

class PyMySQL:
    #初始化
    def __init__(self,host='localhost', user='root', password='', database=''):
        self.db = pymysql.connect(host=host, user=user, password=password, database=database)
        logger.info(f'已连接数据库：host={host}, user={user}, password={password}, database={database}')
        self.cursor = self.db.cursor()

    #插入数据库
    def insert_into(self,database=None,fields=[],values=[],update_fields={},SQL=False):
        """
        :param database: 数据表名
        :param fields: 字段名列表
        :param values: 值列表
        :param update_fields: 更新字段字典
        :param SQL: 输出mysql插入语句
        :return: 插入数据库
        """
        fields_format=','.join([f'`{field}`' for field in fields])
        values_format='","'.join([str(value) for value in values])
        fields_update_format=','.join([f'{key}="{value}"' for key, value in update_fields.items()])
        sql=f"""
            INSERT INTO {database}
            ({fields_format})
            VALUES ("{values_format}")
            """
        if update_fields:
            sql = f"""
                INSERT INTO {database}
                ({fields_format})
                VALUES ("{values_format}")
                ON DUPLICATE KEY UPDATE
                {fields_update_format}
                """
        if SQL:
            logger.info(sql)
        VALUES=re.search('VALUES \((.*)\)',sql).group(1)[:250]
        try:
            self.cursor.execute(sql)
            self.db.commit()
            logger.info(VALUES+'\t成功加入数据库！')
        except Exception as e:
            if str(e).startswith('(1062, "Duplicate entry'):
                logger.info(VALUES+'\t数据重复!')
            else:
                logger.error(e)
            self.db.rollback()

    #自定义sql语句
    def custom_sql(self,sql):
        """
        :param sql: 自定义sql语句
        :return: 执行自定义sql语句
        """
        try:
            self.cursor.execute(sql)
            self.db.commit()
            logger.info(sql)
        except Exception as e:
            logger.error(e,sql)
            self.db.rollback()

    #查询数据
    def select(self,sql,fetch='all'):
        """
        :param sql: 查询数据sql
        :return: 查询结果
        """
        self.cursor.execute(sql)
        if fetch=='one':
            return self.cursor.fetchone()
        return self.cursor.fetchall()

    #转义字符格式化
    def escape_string(self,character_string):
        """
        :param character_string: 部分文本中字符影响SQL语句，需要做字符串处理
        :return: 处理好的字符串
        """
        return escape_string(character_string)

    #获取表头
    def getdatah(self):
        """
        :return: 获取表头
        """
        return [a[0] for a in self.cursor.description]

    #关闭数据库
    def close(self):
        """
        :return: 关闭数据库的所有操作
        """
        self.cursor.close()
        self.db.close()
        logger.info('数据库连接已断开！')