import pandas as pd
import datetime
from random import randrange
import traci
import time
import traci.constants as tc
import pytz


def getdatetime():
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    currentDT = utc_now.astimezone(pytz.timezone("Asia/Singapore"))
    DATIME = currentDT.strftime("%Y-%m-%d %H:%M:%S")
    return DATIME


sumoBinary = "C:/Users/LENOVO/Desktop/sumo-1.12.0/bin/sumo-gui.exe"
sumoCmd = [sumoBinary, "-c", "map.sumo.cfg"]
traci.start(sumoCmd)

packVehicleData = []
packTLSData = []
packBigData = []
i = 0
#while traci.simulation.getMinExpectedNumber() > 0:
while i<300:
    print(i)
    traci.simulationStep()

    vehicles = traci.vehicle.getIDList();
    trafficlights = traci.trafficlight.getIDList();
    # print(vehicles)
    # print(trafficlights)

    for i in range(0, len(vehicles)):
        vehid = vehicles[i]
        x, y = traci.vehicle.getPosition(vehicles[i])
        coord = [x, y]
        lon, lat = traci.simulation.convertGeo(x, y)
        gpscoord = [lon, lat]
        # x1, y1, z1 = traci.vehicle.getPosition3D(vehicles[i])
        # longitude, latitude, altitude = traci.simulation.convertGeo(x1, y1, z1)
        spd = round(traci.vehicle.getSpeed(vehicles[i]) * 3.6, 2)
        edge = traci.vehicle.getRoadID(vehicles[i])
        lane = traci.vehicle.getLaneID(vehicles[i])
        displacement = round(traci.vehicle.getDistance(vehicles[i]), 2)
        turnAngle = round(traci.vehicle.getAngle(vehicles[i]), 2)
        # nextTLS = traci.vehicle.getNextTLS(vehicles[i])
        Accel = traci.vehicle.getAccel(vehicles[i])
        t = getdatetime()
        print(t)
        t.replace('-', '').replace(':', '')
        print(t)
        # Packing of all the data for the creation of excel file
        vehList = [t, vehid, lat, lon, spd, edge, lane, displacement, turnAngle, Accel]
        # print(vehList)

        print("Vehicle: ", vehicles[i], " at datetime: ", getdatetime())
        print(vehicles[i], " >>> Position: ", coord, " | GPS Position: ", gpscoord, " |", \
              " Speed: ", round(traci.vehicle.getSpeed(vehicles[i]) * 3.6, 2), "km/h |", \
              # Returns the id of the edge the named vehicle was at within the last step.
              " EdgeID of veh: ", traci.vehicle.getRoadID(vehicles[i]), " |", \
              # Returns the id of the lane the named vehicle was at within the last step.
              " LaneID of veh: ", traci.vehicle.getLaneID(vehicles[i]), " |", \
              # Returns the distance to the starting point like an odometer.
              " Distance: ", round(traci.vehicle.getDistance(vehicles[i]), 2), "m |", \
              # Returns the angle in degrees of the named vehicle within the last step.
              " Vehicle orientation: ", round(traci.vehicle.getAngle(vehicles[i]), 2), "deg |", \
              # Return list of upcoming traffic lights [(tlsID, tlsIndex, distance, state), ...]
              " Upcoming traffic lights: ", traci.vehicle.getNextTLS(vehicles[i]), \
              )

        idd = traci.vehicle.getLaneID(vehicles[i])

        # Pack Simulated Data
        packBigData.append(vehList)
    i = i+1

traci.close()


columnnames = ['dateandtime', 'vehid', 'lon', 'lat', 'spd', 'edge', 'lane', 'displacement', 'turnAngle', 'Accel']
dataset = pd.DataFrame(packBigData, index=None, columns=columnnames)
dataset.to_excel("output.xlsx", index=False)
print("done!")


