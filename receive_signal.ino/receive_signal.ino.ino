const int motorPin = ;

void setup() {
  Serial.begin(9600);
  pinMode(motorPin, OUTPUT);

}

void loop() {
  if (Serial.available() > 0){
    char data = Serial.read();
    
    if (data == '1'){
      digitalWrite(motorPin, HIGH);
    } 
    else if (data == '0) {
      digitalWrite(motorPin, LOW);
    }
  }
}
