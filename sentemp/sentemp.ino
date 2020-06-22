#include <ESP8266HTTPClient.h>
//#include <ESP_WiFiManager.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>

const char* ssid = "INFINITUM3894_2.4";
const char* password = "ckfDA5tfPy";
String web="http://192.168.1.73:8000/agregarTemperatura";
//WiFiClient espClient;


OneWire ourWire(4);

DallasTemperature sensors(&ourWire);
String no_co="15500683";


void setup() {
  // put your setup code here, to run once:
  
  delay(1000);
  Serial.begin(9600);
  sensors.begin();
  setup_wifi();
  

}

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

}

/*
 
void loop() {
  StaticJsonDocument<200> doc;
  HTTPClient cliente;
  cliente.begin(web);
  Serial.println(web);
  // put your main code here, to run repeatedly:
  sensors.requestTemperatures();
  float temp=sensors.getTempCByIndex(0);
  Serial.print("Temperatura= ");
  Serial.print(temp);
  Serial.println(" °C");
  doc["Temp"] = temp;
  doc["NoCo"] = no_co;
  String json;
  serializeJson(doc, json);
  //Para entrar al server
  //cliente.begin("144.202.34.148:8000/agregaTemperatura");
  //para entrar al localhost
  
  Serial.print(json);
  if(cliente.POST(json)){
   Serial.println("Se postea");
   delay(1000); 
   }
   else{
    Serial.print("No");
    delay(1000);
    }
  String resp=cliente.getString();
  Serial.print(resp);
  cliente.end();
}
*/
void loop(){
  sensors.requestTemperatures();
  float temp=sensors.getTempCByIndex(0);
  Serial.print("Temperatura= ");
  Serial.print(temp);
  Serial.println(" °C");
  post(temp,no_co);
  //Serial.print(post);
}
void post(int temp, String noco) {
  HTTPClient http;
  
  String json;
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& root = jsonBuffer.createObject();


  root["Temp"] = temp;
  root["NoCo"] = noco;
  root.printTo(json);

  http.begin(web);
  http.addHeader("Content-Type", "application/json");
  //http.println("POST/"+web+"");
  if(http.POST(json)){
  Serial.println("Funciona");  
  }
  http.writeToStream(&Serial);
  http.end();
  
}
