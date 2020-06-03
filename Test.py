import comm_arduino
import serial
port = 'COM3'





def send(arduino, message_sent):
    print(message_sent)
    arduino.write(message_sent.encode('utf-8'))

arduino = comm_arduino.connect(port)
comm_arduino.send(arduino,'Test')