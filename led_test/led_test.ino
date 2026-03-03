void setup() {
  Serial.begin(9600);    // Must match the Python baud rate
  pinMode(13, OUTPUT);   // Built-in LED
}

void loop() {
  if (Serial.available() > 0) {
    char signal = Serial.read();
    
    if (signal == '1') {        // '1' means discoloration detected
      digitalWrite(13, HIGH);
    } 
    else if (signal == '0') {   // '0' means clear/normal
      digitalWrite(13, LOW);
    }
  }
}