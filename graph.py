import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from influxdb import InfluxDBClient
import constants as CS


if __name__ == "__main__":
    client = InfluxDBClient(host='localhost', port=8086, database="name")
    fields = {x: [] for x in CS.VARS_LIST}
    time = []

    def animate(i):
        qr = client.query('SELECT * FROM "mes" GROUP BY "time()"', epoch='s')
        tm_ = qr.get_points()
        tm = [x for x in tm_]
        if len(tm) == 0:
            return

        time.clear()
        for a in fields:
            fields[a].clear()
        for a in tm:
            time.append(int(a["time"]))
            for b in CS.VARS_LIST:
                fields[b].append(int(a[b]))
        plt.cla()
        for b in CS.VARS_LIST:
            plt.plot(time, fields[b], label=b)
        plt.tight_layout()
        plt.legend(loc='lower right')


    ani = FuncAnimation(plt.gcf(), animate, interval=1000)
    plt.tight_layout()
    plt.show()
