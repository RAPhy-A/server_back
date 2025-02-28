import serial
import time

# Configuration du port série
arduino = serial.Serial(port='COM9', baudrate=2000000, timeout=0.1)

time.sleep(2)  # Attendre que la connexion série soit établie

# Envoi de la commande
arduino.write(b'0\n')
