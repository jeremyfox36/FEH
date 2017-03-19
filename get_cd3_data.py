import psycopg2.extras

conn = psycopg2.connect(dbname='feh1', user='jem', host='localhost',)
nt_cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
nt_cur.execute('SELECT stationNum, dTMArea, saar, farl, fPExt FROM cd3_data WHERE suitPooling=TRUE')

rows = nt_cur.fetchall()

for row in rows:
    row['SDM'] = '1'  # todo: call the SDM function from here
    # todo: make sure to typecast the values before running SDM on each of them
    print('{}  {}  {}'.format(row['stationnum'], row['farl'], type(int(row['SDM']))))
