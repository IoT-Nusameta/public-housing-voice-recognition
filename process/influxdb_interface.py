import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from gpiozero import LED, CPUTemperature
from datetime import datetime
import random

token = "3_WZQh5jGY4hLAloOKCsSGDPrL21QrV135fPoeRUGrTxQwMfDAlVoj8kLfX7E1DLVeGGd_42cSQNpuTfLmGa6A=="
org = "photobooth"
url = "http://192.168.99.147:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket="power-monitor"
write_api = client.write_api(write_options=SYNCHRONOUS)
   
def log_temp():
    cpu = CPUTemperature()
    point = (
        Point("chip")
        .tag("device", "raspi")
        .field("cpu_temp", cpu.temperature)
    )
    print(point)
    write_api.write(bucket=bucket, org="photobooth", record=point)

def log_power(voltage, current):
    point = (
        Point("pv")
        .tag("device", "raspi")
        .field("voltage", voltage)
        .field("current", current)
    )
    write_api.write(bucket=bucket, org="photobooth", record=point)

def query_influx():
    query_api = client.query_api()
    # query = 'from(bucket: "power-monitor")\
    # |> range(start: -12h)\
    # |> filter(fn: (r) => r["_measurement"] == "chip" or r["_measurement"] == "pv")\
    # |> filter(fn: (r) => r["_field"] == "cpu_temp" or r["_field"] == "current" or r["_field"] == "voltage")\
    # |> filter(fn: (r) => r["device"] == "raspi")'
    
    query = 'from(bucket: "power-monitor")\
    |> range(start: -5m)\
    |> filter(fn: (r) => r["_measurement"] == "distance" or r["_measurement"] == "pv")\
    |> filter(fn: (r) => r["_field"] == "distance" or r["_field"] == "current" or r["_field"] == "voltage")\
    |> filter(fn: (r) => r["device"] == "raspi")'

    result = query_api.query(org=org, query=query)
    timestamp = []
    voltage_data = []
    current_data = []
    distance_data = []
    for table in result:
        for record in table.records:
            if record.get_field() == 'voltage':
                timestamp.append((record.get_time().isoformat()))
                voltage_data.append((record.get_value()))
            elif record.get_field() == 'current':
                current_data.append((record.get_value()))
            elif record.get_field() == 'cpu_temp':
                distance_data.append((record.get_value()))

    return timestamp, voltage_data, current_data, distance_data

while True:
    log_temp()
    log_power(random.randint(1, 6), random.randint(50, 100))
    time.sleep(5)

# query_power()
