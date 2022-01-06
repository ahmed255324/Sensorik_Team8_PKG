#!/usr/bin/env python
import time
from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt
import rospy
from Sensorik_Team8_PKG.msg import auswertungsmessage

LENGTH = 0
data = []
time.sleep(1)

def chatter_callback(message):
    global LENGTH, data
    values = [message.x, message.Y, message.Z]  # Werte anhaengen
    values.append(datetime.now())  # Zeitstempel hinzufuegen
    data.append(values)

    LENGTH = LENGTH + 1
    
rospy.init_node('Statisch', anonymous=True)

rospy.Subscriber("/Auswertung", auswertungsmessage, chatter_callback)

rospy.spin()


HEADERS = ["x", "y", "phiz"]
CSV_FILE = "measurement.csv"
COLORS = ['b', 'g--', 'r:', 'k-.', 'c', 'm']


dataframe = pd.DataFrame(data, columns=HEADERS)
dataframe.set_index(['Timestamp'])

dataframe.to_csv(CSV_FILE)

dataframe = pd.read_csv(CSV_FILE)

x = dataframe[HEADERS[0]].to_list()

plt.figure(figsize=(15, 10))
plt.plot(dataframe['Timestamp'], x)
ax = plt.gca() # Zugriff auch Achsen des Diagramms
ax.set_xticks(ax.get_xticks()[::30]) # xticks Intervall auf 7 Tage
plt.xticks(rotation=90) # Datumsangabe um 90-Grad drehen
plt.xlabel("Zeit")
plt.legend()
plt.show()
