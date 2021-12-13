const byte charsNumber = 8;
const byte commandLength = 3;
char receivedChars[charsNumber];
boolean newData = false;

void setupSerial() {
  Serial.begin(115200);
}

void getCommand() {
  receiveCommand();
  parseCommand();
}

void receiveCommand() {
  static byte i = 0;
  char rc;
  
  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();
    if (rc != '\n') {
      receivedChars[i] = rc;
      i++;
      if (i >= charsNumber) {
        i = charsNumber - 1;
      }
    }
    else {
      receivedChars[i] = '\0';
      i = 0;
      newData = true;
    }
  }
}

void parseCommand() {
  if (newData == true) {
    command = String(receivedChars).substring(0,commandLength);
    value = atoi(String(receivedChars).substring(commandLength,charsNumber-1).c_str());
    newCommand = true;
    newData = false;
  }
}

void sendData(String data) {
  Serial.print(String(data));
  Serial.write('\n');
}
