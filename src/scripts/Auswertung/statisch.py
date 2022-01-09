#!/usr/bin/env python
import time
from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt
import rospy
from Sensorik_Team8_PKG.msg import auswertungsmessage

LENGTH = 0
data = []

def chatter_callback(message):
    global LENGTH, data
    values = [message.X, message.Y, message.Z]  # Werte anhaengen
    values.append(datetime.now())  # Zeitstempel hinzufuegen
    data.append(values)

    LENGTH = LENGTH + 1
    
rospy.init_node('Statisch', anonymous=True)

rospy.Subscriber("/Auswertung", auswertungsmessage, chatter_callback)

rospy.spin()


HEADERS = ["x", "y", "phiz", "Timestamp"]
CSV_FILE = "measurement.csv"
COLORS = ['b', 'g--', 'r:', 'k-.', 'c', 'm']


dataframe = pd.DataFrame(data, columns=HEADERS)
dataframe.set_index(['Timestamp'])

analysis = dataframe.describe()

print("")
print(analysis.iloc[[1, 2, 3, 7], 0:4])

x = dataframe[HEADERS[0]]

plt.figure(figsize=(15, 10))
plt.plot(dataframe['Timestamp'], x)
ax = plt.gca() # Zugriff auch Achsen des Diagramms
ax.set_xticks(ax.get_xticks()[::7]) # xticks Intervall auf 7 Tage
plt.xticks(rotation=90) # Datumsangabe um 90-Grad drehen
plt.ylabel("Die X-Koordenate in m")
plt.xlabel("Zeit")

y = dataframe[HEADERS[1]]

plt.figure(figsize=(15, 10))
plt.plot(dataframe['Timestamp'], y)
ax = plt.gca() # Zugriff auch Achsen des Diagramms
ax.set_xticks(ax.get_xticks()[::7]) # xticks Intervall auf 7 Tage
plt.xticks(rotation=90) # Datumsangabe um 90-Grad drehen
plt.ylabel("Die Y-Koordenate in m")
plt.xlabel("Zeit")

phiz = dataframe[HEADERS[2]]

plt.figure(figsize=(15, 10))
plt.plot(dataframe['Timestamp'], phiz)
ax = plt.gca() # Zugriff auch Achsen des Diagramms
ax.set_xticks(ax.get_xticks()[::7]) # xticks Intervall auf 7 Tage
plt.xticks(rotation=90) # Datumsangabe um 90-Grad drehen
plt.ylabel("winkel")
plt.xlabel("Zeit")


plt.figure(figsize=(15, 10))
plt.hist(dataframe['x'], bins=30, edgecolor='black')
plt.xlabel('Die x-Koordenate in m')
plt.ylabel('Werteverteilung')

plt.figure(figsize=(15, 10))
plt.hist(dataframe['y'], bins=30, edgecolor='black')
plt.xlabel('Die y-Koordenate in m')
plt.ylabel('Werteverteilung')

plt.figure(figsize=(15, 10))
plt.hist(dataframe['phiz'], bins=30, edgecolor='black')
plt.xlabel('winkel in °')
plt.ylabel('Werteverteilung')

plt.show()
