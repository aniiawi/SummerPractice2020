import time
from influxdb import InfluxDBClient


def select_from_database(
        db_addr='localhost',
        db_name='name',
        db_measure='mes',
        db_params=None,
        time_beg=0,
        time_last=None
):
    if db_params is None:
        db_params = ['*']
    q_s = "SELECT " + ''.join(db_params) + " FROM " + db_measure + " WHERE \"time\" > " + str(time_beg)

    if time_last is not None:
        q_s += " AND \"time\" < " + str(time_last)
    cli = InfluxDBClient(db_addr, database=db_name)
    timeb = time.time()
    qr = cli.query(q_s, epoch='s')
    pts = list(qr.get_points())
    timeb = time.time() - timeb
    return pts, timeb
