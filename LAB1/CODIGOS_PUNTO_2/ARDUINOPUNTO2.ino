#include <DHT.h>
#define DHTPIN 2
#define DHTTYPE DHT11
#define LED_ROJO 8
#define LED_VERDE 9
DHT dht(DHTPIN, DHTTYPE);
void setup() {
 Serial.begin(9600);
 pinMode(LED_ROJO, OUTPUT);
 pinMode(LED_VERDE, OUTPUT);
 dht.begin();
}
void loop() {
 if (Serial.available()) {
   String comando = Serial.readStringUntil('\n');
   comando.trim();
   if (comando == "ROJO_ON") {
     digitalWrite(LED_ROJO, HIGH);
     Serial.println("Rojo encendido");
   }
   else if (comando == "ROJO_OFF") {
     digitalWrite(LED_ROJO, LOW);
     Serial.println("Rojo apagado");
   }
   else if (comando == "VERDE_ON") {
     digitalWrite(LED_VERDE, HIGH);
     Serial.println("Verde encendido");
   }
   else if (comando == "VERDE_OFF") {
     digitalWrite(LED_VERDE, LOW);
     Serial.println("Verde apagado");
   }
   else if (comando == "TEMP") {
     float t = dht.readTemperature();
     if (isnan(t)) {
       Serial.println("Error leyendo temperatura");
     } else {
       Serial.print("Temperatura:");
       Serial.println(t);
     }
   }
 }
}