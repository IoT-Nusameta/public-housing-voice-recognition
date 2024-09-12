import asyncio
import aioserial
from dotenv import load_dotenv
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import serial

load_dotenv()

token = os.getenv('INFLUX_TOKEN')
org = os.getenv('INFLUX_ORG')
url = os.getenv('INFLUX_URL')
# url = "http://localhost:8086"
bucket= os.getenv('INFLUX_BUCKET')
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

parent_path = os.getenv('PARENT_PATH')
human_path = parent_path + '/temp/human.txt'

# class App:
#     async def read_serial(self, aioserial_instance: aioserial.AioSerial):
#         while True:
#             data: bytes = (await aioserial_instance.readline_async()).decode().strip()
#             print(data.split(";"))
#             received_data = data.split(";")
#             device_id = received_data[0]
#             data1 = received_data[1]
#             data2 = received_data[2]
#             data3 = received_data[3]

#             if device_id == "power-monitor":
#                 my_point = (
#                     Point("pv")
#                     .tag("device", "raspi")
#                     .field("current", int(data1))
#                     .field("voltage", int(data2))
#                 )
#                 try:
#                     write_api.write(bucket=bucket, org=org, record=my_point)
#                     print("[SUCCESS] Write data to influxdb")
#                 except Exception as e:
#                     print(e)
#             elif device_id == "distance-sensor":
#                 if int(data1) < 50:
#                     human_exist = 'true'
#                 else:
#                     human_exist = 'false'
#                 with open(human_path, 'w') as file:
#                     file.writelines(human_exist)
#                 print(f"[SUCCESS] Write {human_exist} data to {human_path}")

# if __name__ == "__main__":
#     app = App()
#     loop = asyncio.get_event_loop()
#     asyncio.ensure_future(app.read_serial(aioserial.AioSerial(port='/dev/ttyUSB0')))
#     time.sleep(1)
#     loop.run_forever()

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

while True:
    data = ser.readline().decode('utf-8')
    try:
        received_data = data.split(";")
        # print(received_data)
        device_id = received_data[0]
        data1 = received_data[1]
        data2 = received_data[2]
        data3 = received_data[3]
        
        if device_id == "power-monitor":
            my_point = (
                Point("pv")
                .tag("device", "raspi")
                .field("current", int(data1))
                .field("voltage", int(data2))
            )
            try:
                write_api.write(bucket=bucket, org=org, record=my_point)
                print("[SUCCESS] Write data to influxdb")
            except Exception as e:
                print(e)
        elif device_id == "distance-sensor":
            if int(data1) < 50:
                human_exist = 'true'
            else:
                human_exist = 'false'
            with open(human_path, 'w') as file:
                file.writelines(human_exist)
            print(f"[SUCCESS] Write {human_exist} data to {human_path}")

    except Exception as e:
        print(e)