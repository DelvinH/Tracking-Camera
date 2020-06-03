#include <Servo.h>

Servo panServo;
Servo tiltServo;

float panServoAngle = 90.0;
float tiltServoAngle = 120.0;

const byte buffSize = 40;
char inputBuffer[buffSize];
const char startMarker = '<';
const char endMarker = '>';
byte bytesRecvd = 0;
boolean readInProgress = false;

void setup() {
  Serial.begin(115200); 
  Serial.println("Starting");
  panServo.attach(9);
  tiltServo.attach(10);
  //startSequence();
  
  Serial.println("<Connected>"); //Let Python script know arduino is ready
}

void loop() {
  getDataFromPC();
  moveServo();
}


//Recieve data from Python script
void getDataFromPC() {
  if(Serial.available() > 0) {
    char x = Serial.read();              //read char from serial
      
    if (x == endMarker) {                //look for end marker
      readInProgress = false;            //if found, set read in progress to false (will stop adding new byte to buffer)
      inputBuffer[bytesRecvd] = 0;       //clear input buffer
      processData();                     //process data in buffer
    }
    
    if(readInProgress) {
      inputBuffer[bytesRecvd] = x;       //populate input buffer with bytes
      bytesRecvd ++;                     //increment index
      if (bytesRecvd == buffSize) {      //when buffer is full
        bytesRecvd = buffSize - 1;       //keep space for end marker
      }
    }

    if (x == startMarker) {              //look for start maker
      bytesRecvd = 0;                    //if found, set byte received to 0
      readInProgress = true;             //set read in progress true
    }
  }
}

//Unpack data from Python script
void processData() // for data type "<float, float, int>" 
{
  char * strtokIndx; // this is used by strtok() as an index

  strtokIndx = strtok(inputBuffer,",");      //get target pan angle
  panServoAngle = atof(strtokIndx);          //convert this part to a float

  strtokIndx = strtok(NULL,",");             //get target tilt angle)
  tiltServoAngle = atof(strtokIndx);         //convert this part to a float
}

void moveServo() 
{
  panServo.write(panServoAngle);
  tiltServo.write(tiltServoAngle);
}


void startSequence()
{
  panServo.write(panServoAngle - 10);
  delay(1000);
  panServo.write(panServoAngle + 10);
  delay(1000);
  panServo.write(panServoAngle);
  delay(1000);
  tiltServo.write(tiltServoAngle - 10);
  delay(1000);
  tiltServo.write(tiltServoAngle + 10);
  delay(1000);
  tiltServo.write(tiltServoAngle);
  delay(1000);
  
}
