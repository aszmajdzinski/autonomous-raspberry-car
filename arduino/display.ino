void setupDisplay(){
  pinMode(LED_BUILTIN, OUTPUT);
}

void ledOn() {
  digitalWrite(LED_BUILTIN, HIGH);
}

void ledOff() {
  digitalWrite(LED_BUILTIN, LOW);
}
