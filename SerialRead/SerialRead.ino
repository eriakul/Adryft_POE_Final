String readString;
String radius1;
String theta1;
float radius2;
float theta2;

void setup()
{

  Serial.begin(9600);  // initialize serial communications at 9600 bps

}

void loop()
{
  while(!Serial.available()) {}
  // serial read section
  while (Serial.available())
  {
    if (Serial.available() >0)
    {
      readString = Serial.readString();
      int commaIndex = readString.indexOf(',');
      radius1 = readString.substring(0, commaIndex);
      theta1 = readString.substring(commaIndex + 1);
      radius2 = radius1.toFloat();
      theta2 = theta1.toFloat();
    }
  }

  if (readString.length() >0)
  {
    Serial.print("Arduino received: ");  
    String radius3 = String(radius2*2);
    String theta3 = String(theta2*2);
    Serial.print(radius3); //see what was received
    Serial.print(",");
    Serial.println(theta3);
  }

  delay(500);
  Serial.flush();
}
