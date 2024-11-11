import pandas as pd
from sqlalchemy import create_engine

def load_csv_to_db(file_path, table_name, columns ,db_url):
    df = pd.read_csv(file_path, header=None)
    print(f"file loaded {file_path} ")
    print(df.size)
    df = df.dropna(how='any',axis=0)
    print(df.size)
    engine = create_engine(db_url, echo=True)
    print(f"conected {db_url}")
    df.columns = columns
    df.to_sql(table_name, engine, if_exists='append', index=False)
    print('data loaded')


db_path = 'sqlite:///../../db.sqlite3'
load_csv_to_db('departments.csv', 'challenge1_department', ["id","department"],db_path)
load_csv_to_db('jobs.csv', 'challenge1_job', ["id","job"] ,db_path)
load_csv_to_db('hired_employees.csv', 'challenge1_hiredemployee',["id","name","datetime","department_id","job_id"], db_path)
