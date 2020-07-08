import time
import random
from multiprocessing import Manager, Process

from influxdb import InfluxDBClient
import prog.prog_constants as CNST


class Var:
    def __init__(self, name, begin_value, change_range):
        self.name = name
        self.value: float = float(begin_value)
        self.change_rate: float = float(change_range)
        print(self.value, self.change_rate)


class PublisherClass:
    def __init__(self):
        self._client = InfluxDBClient(host=CNST.INFLUXDB_ADDR, port=8086, database=CNST.INFLUXDB_DB_NAME)
        self.manager = Manager()
        self._lc = Manager().Lock()
        self._var_list = self.manager.list()
        self.wrk = None

    def add_field(self, variable: Var):
        self._lc.acquire(blocking=True)
        self._var_list.append(variable)
        self._lc.release()

    def start_work(self):
        if self.wrk is not None:
            return False
        self.wrk = Process(target=PublisherClass.work_f, args=(self, ))
        self.wrk.start()
        return True

    def del_field(self, nm):
        index = -1
        self._lc.acquire(blocking=True)
        for a in range(len(self._var_list)):
            if self._var_list[a].name == nm:
                index = a
                break
        rv = True
        if index != -1:
            self._var_list.pop(index)
        else:
            rv = False
        self._lc.release()
        return rv

    def stop_work(self):
        if self.wrk is None:
            return False
        self._lc.acquire(blocking=True)
        self.wrk.terminate()
        self.wrk.join()
        self.wrk = None
        self._lc.release()
        return True

    def work_f(self):
        while True:
            if len(self._var_list) != 0:
                self._lc.acquire(blocking=True)
                tm = {}
                for a in self._var_list:
                    tm[a.name] = a.value
                self._client.write_points([
                    {
                        "measurement": CNST.INFLUXDB_MEAS_NAME,
                        "fields": tm
                    }
                ])

                for a in range(len(self._var_list)):
                    rr = self._var_list[a]
                    rr.value = -1 + 2 * random.randint(0, 1) + rr.change_rate * random.random()
                    self._var_list[a] = rr
                self._lc.release()
            time.sleep(1)

    def get_var_list(self):
        self._lc.acquire(blocking=True)
        r_m = {}
        for a in self._var_list:
           r_m[a.name] = a.value
        self._lc.release()
        return r_m



