from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
import os
import board
import time
import asyncio 
import aioserial
import json
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from gpiozero import LED
from dotenv import load_dotenv

load_dotenv()

relay1 = LED(4)
relay2 = LED(10)
relay3 = LED(5)

bucket = "distanceMonitor"
org = os.getenv('ORG')
token = os.getenv('TOKEN')
# Store the URL of your InfluxDB instance
url= os.getenv('URL')

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)
USB_port = '/dev/ttyUSB0'
class Hat:
    async def read_cmd(self):
        while True:
            with open("light.json", "r+") as json_data:
                relays = json.load(json_data)
                (lambda: relay1.off(), lambda: relay1.on())[relays["relay1"] == 1]() #1 for on 0 for off"
                (lambda: relay2.off(), lambda: relay2.on())[relays["relay2"] == 1]()
                (lambda: relay3.off(), lambda: relay3.on())[relays["relay3"] == 1]()
            # with open("command.txt", "r+") as relay_txt:
            #     read_str = relay_txt.read().lower()
            #     parse_txt = read_str.split(';')
            #     # print(parse_txt[0])
            #     # print(parse_txt[1])
            #     # print(parse_txt[2])

            # (lambda: relay1.off(), lambda: relay1.on())[parse_txt[0] == '1']() #1 for on 0 for off"
            # (lambda: relay2.off(), lambda: relay2.on())[parse_txt[1] == '1']()
            # (lambda: relay3.off(), lambda: relay3.on())[parse_txt[2] == '1']()

            await asyncio.sleep(1)

    async def influx_query(self):
        while True:
            query_api = client.query_api()
            query = 'from(bucket:"distanceMonitor")\
            |> range(start: -10m)\
            |> filter(fn:(r) => r.location == "backyard")\
            |> filter(fn:(r) => r._field == "humanExist")\
            |> last()'

            result = query_api.query(org=org, query=query)
            results = []
            for table in result:
                for record in table.records:
                    results.append(record.get_value())

            print(results[0])
            await asyncio.sleep(1)
            with open('humanExist.txt', 'w+') as file:
                file.writelines(str(results[0]))

        
    async def read_serial(self, aioserial_instance: aioserial.AioSerial):
        while True:
            data: bytes = (await aioserial_instance.readline_async()).decode().strip()
            print(data.split(";"))
            received_data = data.split(";")
            location = received_data[0]
            distance = received_data[1]
            human_exist = received_data[2] # Maling Detection
            
            # print(location)
            # print(distance)
            # print(human_exist)

            with open('distance.txt', 'w+') as file:
                file.writelines(f"{received_data}")
            
            await asyncio.sleep(0.5)
        
    
loop = asyncio.get_event_loop()
app = Hat()
asyncio.ensure_future(app.read_cmd())
# asyncio.ensure_future(app.influx_query())
loop.run_forever()


