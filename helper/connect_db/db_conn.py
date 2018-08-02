#ORACLE과 MY-sql에 디비를 연결할 때 사용
import MySQLdb
import cx_Oracle
import socket
import yaml
import os

#현재 파일 상대경로 받아오기 아이파이썬에서
#path=os.getcwd()

#현재 파일의 경로를 받아옵 크론잡에서 사용할 경우
path = os.path.realpath(os.path.dirname(__file__))

certification_path = os.path.join(path, 'db_config_파일_폴더_경로')

stream = open(os.path.join(certification_path, 'db_config_파일'), 'r')
db_config = yaml.load(stream)

#로컬 컴퓨터(리눅스)의 경우 ip를 127.0.1.1로 뱉음
my_ip = socket.gethostbyname(socket.gethostname())
my = 'cloud_service'

print(my_ip)
if my_ip == '127.0.1.1':
    my = 'local'
else :
    pass 

class DbConn:
    def __init__(self, db_table):
        self._conn = None
        
        self._db_type = db_config[db_table]['db_type']
        self._db_user = db_config[db_table]['db_user']
        self._db_password = db_config[db_table]['db_password']
        self._db_name = db_config[db_table]['db_name']
        
        if self._db_type == 'oracle':
            self._db_host = db_config[db_table][my]['db_host']
            self._db_port = db_config[db_table]['db_port']
        else:
            self._db_host = db_config[db_table][my]['db_host']
            self._db_port = db_config[db_table][my]['db_port']
            
            
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, *exec_info):
        del exec_info
        
    def connect(self):
        if self._db_type == 'oracle':
            #if sid
            dsn = cx_Oracle.makedsn(self._db_host, self._db_port, sid = self._db_name)
            #elseif service_name
            #dsn = cx_Oracle.makedsn(self._db_host, self._db_port, service_name = self._db_name)
                
            self._conn = cx_Oracle.connect(self._db_user, self._db_password, dsn, encoding = "UTF-8", nencoding = "UTF-16")
            self._conn.autocommit =  True
        elif self._db_type == 'mysql':
            self._conn = MySQLdb.Connect(host = self._db_host, port = self._db_port, user = self._db_user, passwd = self._db_password, use_unicode=True, charset="utf8" )
        
    def commit(self):
        self._conn.commit()
        
    def close(self):
        if self._conn:
            self._conn.close()
            
    def connection(self):
        return self._conn
    
    
def connect(db_table):
    return DbConn(db_table) 