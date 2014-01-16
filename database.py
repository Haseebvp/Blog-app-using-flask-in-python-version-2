import psycopg2
con=psycopg2.connect(database="has")
cur=con.cursor()
cur.execute("CREATE TABLE blog1(id serial,title text,post text,time text,date text)")
con.commit()
con.close()
