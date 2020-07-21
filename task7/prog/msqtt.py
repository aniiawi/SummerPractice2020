from multiprocessing import Process

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import prog.prog_constants as CNST


class MQTTSetter:
    def __init__(self, host_influx, host_mqtt , var, topic):
        self._var = var
        self._topic = topic
        self._db_class = InfluxDBClient(host_influx, port=8086, database=CNST.INFLUXDB_DB_NAME)

        self._cli = mqtt.Client()

        def on_connect(client, userdata, flags, rc):
            client.subscribe(self._topic + "/" + self._var)

        def on_message(client, userdata, msg):
            self._db_class.write_points([
                    {
                        "measurement": CNST.INFLUXDB_MEAS_NAME,
                        "fields": {
                            self._var: float(msg.payload.decode('ascii'))
                        }
                    }
                ])

        self._cli.on_connect = on_connect
        self._cli.on_message = on_message
        self._cli.connect(host_mqtt, 1883, 60)
        self._cli.loop_forever()


def MqTTServerStart(host_influx, host_mqtt , var, topic):
    MQTTSetter(host_influx, host_mqtt, var, topic)


def StartMqtt(host_influx, host_mqtt , var, topic):
    pr = Process(target=MqTTServerStart, args=(host_influx, host_mqtt , var, topic))
    pr.start()
    return pr
