from connect_db import db_conn

#sql과 con을 받아 데이터 프레임만 출력하는 함수
def _fetch_res_from_oracle(**kwargs):
    
    res = None
    
    with db_conn.connect(kwargs['db_name']) as conn:
        with conn.connection() as con:
            cursor = con.cursor()
            
            if 'params' in kwargs.keys():
                cursor.execute(kwargs['query'], kwargs['params'])
            else:
                cursor.execute(kwargs['query'])
            
            if kwargs['crud'] == 'read':
                res = cursor.fetchall()
            
            con.commit()
            cursor.close()
            
    return res 

#sql과 con을 받아 데이터 프레임만 출력하는 함수
def _fetch_res_from_mysql(**kwargs):
    
    res = None
    
    with db_conn.connect(kwargs['db_name']) as conn:
        con = conn.connection()
        with con.cursor() as cursor:
            cursor.execute("USE " + kwargs['db'] + ";")
            
            if 'params' in kwargs.keys():
                cursor.execute(kwargs['query'], kwargs['params'])
            else:
                cursor.execute(kwargs['query'])
            
            if kwargs['crud'] == 'read':
                res = cursor.fetchall()
            
            con.commit()
            cursor.close()
            
    return res

#ORACLE 디비에 한번에 여러개 데이터를 넣을 경우
def _set_operation_df_in_db(df):
    
    df.sort_values(['정렬 컬럼'], ascending = [True])
    
    columns = list(df.columns)
    
    insert_num = 0
    insert_rows = []
    
    for idx, row in df.iterrows():
        insert_dict = {}
        
        for col in columns:
            if row[col] == row[col]:
                insert_dict[col] = row[col]
            else:
                insert_dict[col] = None
        
        if insert_num == 0:
            print(insert_dict)

        insert_num += 1
        insert_rows.append(insert_dict)        
        
        del insert_dict
    
    query = """
    INSERT INTO
        테이블_이름
        ({0})
    VALUES
        ({1})
    """.format(','.join(['"' + col + '"' for col in columns]), ','.join([' :' + col for col in columns]))
    
    del df
    
    with db_conn.connect('db_user') as conn:
        with conn.connection() as con:
            cursor = con.cursor()

            cursor.prepare(query)
            cursor.executemany(None, insert_rows)

            con.commit()
            cursor.close()
        con.close()
    
    del insert_rows
    
    return insert_num