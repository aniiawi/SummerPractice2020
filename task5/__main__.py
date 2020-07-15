import argparse
from my_db import select_from_database

parser = argparse.ArgumentParser(description='Collect data from db and time that it needs')
parser.add_argument("--db", action="store", dest="db", help="database name")
parser.add_argument("--mn", action="store", dest="mn", help="measurment name")
parser.add_argument("--dbn", action="store", dest="dbn", help="database address")
parser.add_argument('--tb', action="store", dest="tb", help="begin time in seconds from epoch")
parser.add_argument('--tl', action="store", dest="tl", help="end time in seconds from epoch")
parser.add_argument('--vars', action="store", dest="vars", nargs="*", help="a, b, c or empty")

ps = parser.parse_args()

kwargs = {}
if ps.db is not None:
    kwargs["db_addr"] = ps.db
if ps.mn is not None:
    kwargs["db_measure"] = ps.mn
if ps.dbn is not None:
    kwargs["db_name"] = ps.dbn
if ps.vars is not None:
    kwargs["db_params"] = ps.vars
if ps.tb is not None:
    kwargs["time_beg"] = int(ps.tb) * 1000000000
if ps.tl is not None:
    kwargs["time_last"] = int(ps.tl) * 1000000000
ls, time_to_req = select_from_database(**kwargs)
print(ls)
print("=================")
print(time_to_req)
