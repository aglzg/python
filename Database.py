'Python连接到 MySQL 数据库及相关操作(基于Python3)'
import pymysql.cursors
class Database:    
    connected = False
    __conn = None
    conf = {}
    # 构造函数，初始化时直接连接数据库
    def __init__(self,host='',port=3306,db='',user='',passwd='',charset='utf8'):
        self.conf['host'] = host
        self.conf['port'] = port
        self.conf['db'] = db
        self.conf['user'] = user
        self.conf['passwd'] = passwd
        self.conf['charset'] = charset
        try:
            self.__conn = pymysql.connect(
                host=self.conf['host'],
                port=self.conf['port'],
                user=self.conf['user'],
                passwd=self.conf['passwd'],
                db=self.conf['db'],
                charset=self.conf['charset'],
                cursorclass=pymysql.cursors.DictCursor)
            self.connected = True
        except pymysql.Error as e:
            print('数据库连接失败:', end='')
    def where(self,where_obj):        
        if type(where_obj) != dict : 
            return where_obj

        strWhere = ''
        for k,v in where_obj.items():
            strWhere += "`" + str(k) + "`='" + str(v) + "' and " 
        strWhere = strWhere[:-4]
        return strWhere
    def set_update_data(self,var_obj):
        str_update = ''
        for k,v in var_obj.items():
            str_update += "`" + str(k) + "`='" + str(v) + "'," 
        str_update = str_update[:-1]
        return str_update
    # 插入数据到数据表
    def insert(self, table, val_obj):              
        try:
            strKey = ''
            strVal = ''
            for v,k in val_obj.items():
                strKey += str(v)+"`,`"
                strVal += str(k)+"','"
            strKey = "`"+strKey
            strVal = "'"+strVal
            strKey = strKey[:-2]
            strVal = strVal[:-2]
            sql = "INSERT INTO `%s`(%s)VALUES(%s)"%(table,strKey,strVal)
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return self.__conn.insert_id()
        except pymysql.Error as e:
            self.__conn.rollback()
            return False
    
    # 更新数据到数据表
    def update(self, table, val_obj, where_obj):
        try:
            set_update = self.set_update_data(val_obj)
            where = self.where(where_obj)
            sql = "UPDATE `%s` SET %s where %s"%(table,set_update,where)
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.rowcount
        except pymysql.Error as e:
            self.__conn.rollback()
            return False

    # 删除数据在数据表中
    def delete(self, table, where_obj):
        try:            
            where = self.where(where_obj)
            sql = "DELETE FROM  `%s` where %s"%(table,where)
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.rowcount
        except pymysql.Error as e:
            self.__conn.rollback()
            return False

    # 查询唯一数据在数据表中
    def selectOne(self, table, where_obj, field='*'):
        where = self.where(where_obj)
        sql = "SELECT %s FROM  `%s` where %s"%(field,table,where)
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.fetchone()
        except pymysql.Error as e:
            return False

    # 查询多条数据在数据表中
    def selectMore(self, table, where_obj, field='*'):
        where = self.where(where_obj)
        sql = "SELECT %s FROM  `%s` where %s"%(field,table,where)
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.fetchall()
        except pymysql.Error as e:
            return False

    # 统计某表某条件下的总行数
    def count(self, table, where_obj='1'):
        where = self.where(where_obj)
        sql = "SELECT count(*)res FROM  `%s` where %s"%(table,where_obj)
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.fetchall()[0]['res']
        except pymysql.Error as e:
            return False

    # 销毁对象时关闭数据库连接
    def __del__(self):
        try:
            self.__conn.close()
        except pymysql.Error as e:
            pass

    # 关闭数据库连接
    def close(self):
        self.__del__()
 