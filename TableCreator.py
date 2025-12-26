import sqlite3
def create():
    conobj=sqlite3.connect(database="mybank.sqlite")
    curobj=conobj.cursor()
    query='''
create table if not exists accounts(
acn integer primary key autoincrement,
name text,
password text,
mob text,
email text,
adhar text,
bal float,
opndate datetime
)
'''
    curobj.execute(query)
    conobj.close()
