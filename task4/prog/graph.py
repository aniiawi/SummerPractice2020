import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from influxdb import InfluxDBClient
import prog_constants as CNST

if __name__ == "__main__":
    client = InfluxDBClient(host='localhost', port=8086, database=CNST.INFLUXDB_DB_NAME)
    fields = {}
    time = {}

    def animate(i):
        qr = client.query('SELECT * FROM '+ CNST.INFLUXDB_MEAS_NAME +' GROUP BY "time()"', epoch='s')
        tm_ = qr.get_points()
        tm = [x for x in tm_]
        if len(tm) == 0:
            return

        for a in fields:
            fields[a].clear()
            time[a].clear()

        for a in tm:
            print(a)
            timen = a.pop("time")
            for b in a:
                if fields.get(b, None) is None:
                    time[b] = []
                    fields[b] = []
                if a[b] is None:
                    continue
                fields[b].append(a[b])
                time[b].append(timen)
        plt.cla()
        for b in fields:
            plt.plot(time[b], fields[b], label=b)
        plt.tight_layout()
        plt.legend(loc='lower right')


    ani = FuncAnimation(plt.gcf(), animate, interval=1000)
    plt.tight_layout()
    plt.show()