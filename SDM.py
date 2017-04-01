import psycopg2
import psycopg2.extras


def sdm_from_db():
    total_years_data = 0  # keeps count of number of years data for formation of pooling group
    pooling_group = {}

    conn = psycopg2.connect(dbname='feh1', user='jem', host='localhost', )
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    dict_cur.execute(
        "SELECT catchment_name, cd3_data.stationnum,"
        "sqrt((3.2::DOUBLE PRECISION * (((ln(user_ungauged_catchment.areai::DOUBLE PRECISION) - ln(cd3_data.dtmarea::DOUBLE PRECISION)) / 1.28::DOUBLE PRECISION) ^ 2::DOUBLE PRECISION))"
        "+(0.5::DOUBLE PRECISION * (((ln(user_ungauged_catchment.saari::DOUBLE PRECISION) - ln(cd3_data.saar::DOUBLE PRECISION)) / 0.37::DOUBLE PRECISION) ^ 2::DOUBLE PRECISION))"
        "+(0.1::DOUBLE PRECISION * (((user_ungauged_catchment.farli - cd3_data.farl) / 0.05::DOUBLE PRECISION) ^ 2::DOUBLE PRECISION))"
        "+(0.2::DOUBLE PRECISION * (((user_ungauged_catchment.fpexti - cd3_data.fpext) / 0.04::DOUBLE PRECISION) ^ 2::DOUBLE PRECISION)))"
        " AS SDM FROM user_ungauged_catchment, cd3_data WHERE user_ungauged_catchment.catchment_name::TEXT = '37017'::TEXT AND cd3_data.suitpooling = TRUE ORDER BY SDM")

    rows = dict_cur.fetchall()

    for row in rows:
        if total_years_data <= 500:
            rd_cur = conn.cursor()
            st = row['stationnum']
            rd_cur.execute('SELECT flow FROM amaxdata WHERE stationnum=%s', (st,))

            amaxdata = rd_cur.fetchall()

            amaxdata = [flow[0] for flow in amaxdata]  # changes list of tuples in tuple
            row['amaxdata'] = amaxdata
            row['amaxcount'] = len(amaxdata)
            pooling_group[row['stationnum']] = row
            del(row['stationnum'])
            total_years_data += len(amaxdata)

        else:
            break

    return pooling_group
