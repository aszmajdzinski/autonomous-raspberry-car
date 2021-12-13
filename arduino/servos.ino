void setupServos() {
  myServo1.attach(12, 580, 2500); // noname

}

void steeringServo(int pos) {
  if (pos <= 120 & pos >= 55) {
    myServo1.write(pos);  
  }  
}
