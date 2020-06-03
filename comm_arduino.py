import serial


def connect(port):
    try:
        arduino = serial.Serial(port, 115200)
        wait_for_arduino(arduino)
        return arduino
    except:
        print("Not able to connect on this port")
        return None

def wait_for_arduino(arduino):
    msg = ""
    while msg.find("Connected") == -1:  #string.find() return -1 if value not found
        while arduino.inWaiting() == 0:  #inWaiting() return number of bytes in buffer, equivalent of Serial.available in arduino
            pass
        msg = receive(arduino) #return decoded serial data
        print(msg)  # python3 requires parenthesis

def receive(arduino):
    message_received = "" #message received start as an empty string
    x = "z"  #next char read from serial . need to start as any value that is not an end- or startMarker
    byteCount = -1  #to allow for the fact that the last increment will be one too many

    # wait for the start character
    while ord(x) != 60:  # ord() return utf-8 for a char(1 length string)  ex: return 60 for char <
        x = arduino.read()  # loop until start marker found
    # save data until the end marker is found
    while ord(x) != 62:  # loop until end marker found
        if ord(x) != 60:  # if not start marker
            message_received = message_received + x.decode("utf-8")  # add decoded char to string
            byteCount += 1  # WHY IS BYTECOUNT FOR?
        x = arduino.read()  # read next char
    #print(message_received)
    return (message_received)


def send(arduino, message_sent):
    #print(message_sent)
    arduino.write(message_sent.encode('utf-8')) 
    

    

        
