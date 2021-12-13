#define in1 6
#define in2 11

byte acceleration = 0;
char direction = '0';

void setupMotorsHW() {
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
}

void frontMotor(int power) {
  power = checkPowerValue(power);
  if (power >= 0) {
    analogWrite(in1, abs(power));
    digitalWrite(in2, LOW);
  } else {
      digitalWrite(in1, LOW);
      analogWrite(in2, abs(power));
  }
  
}

void rearMotor(int power) {
  power = checkPowerValue(power);
}

void motorsStop() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
}

int checkPowerValue(int power) {
  if (power > 255) {
    return 255;
  } else {
    return power;
  }
}
