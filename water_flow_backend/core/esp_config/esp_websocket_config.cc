// #include <ESP8266WiFi.h>
// #include <ArduinoWebsockets.h>
// #include <ArduinoJson.h>

// using namespace websockets;

// const char* ssid = "brisa-2090364";
// const char* password = "xzxcx5dt";
// const char* websockets_server_host = "192.168.0.105";
// const int websockets_server_port = 8000;

// WebsocketsClient client;

// #define FlowSensor_INPUT D1
// #define PERIOD 1000

// volatile unsigned long pulse_counter = 0;
// unsigned long old_time;

// void IRAM_ATTR interrupt_handler() {
//   pulse_counter++;
// }

// void setup() {
//   Serial.begin(115200);

//   pinMode(FlowSensor_INPUT, INPUT_PULLUP);
//   attachInterrupt(digitalPinToInterrupt(FlowSensor_INPUT), interrupt_handler, RISING);

//   WiFi.begin(ssid, password);
//   while (WiFi.status() != WL_CONNECTED) {
//     delay(500);
//     Serial.print(".");
//   }

//   Serial.println("\n✅ WiFi Conectado!");

//   // Conectar WebSocket
//   bool connected = client.connect(websockets_server_host, websockets_server_port, "/ws/flow-reading/");
//   if (connected) {
//     Serial.println("✅ WebSocket conectado!");
//   } else {
//     Serial.println("❌ Falha ao conectar WebSocket.");
//   }

//   client.onMessage([](WebsocketsMessage message) {
//     Serial.print("🔁 Resposta do servidor: ");
//     Serial.println(message.data());
//   });

//   configTime(0, 0, "pool.ntp.org", "time.nist.gov");
// }

// void loop() {
//   client.poll();
//   sendFlowRate();
//   delay(1000); // Intervalo de 1 segundo (igual ao BlynkTimer)
// }

// void sendFlowRate() {
//   unsigned long new_time = millis() - old_time;
//   if (new_time >= PERIOD) {
//     noInterrupts();
//     unsigned long pulse_count = pulse_counter;
//     pulse_counter = 0;
//     interrupts();

//     old_time = millis();

//     float pulse_rate = (pulse_count * 1000.0) / new_time;
//     float flow_rate = pulse_rate / 7.5;
//     flow_rate = round(flow_rate * 100) / 100.0;

//     Serial.print("FjsonStringluxo: ");
//     Serial.print(flow_rate, 2);
//     Serial.println(" L/min");

//     // Criar JSON com timestamp
//     time_t now = time(nullptr);
//     struct tm* timeinfo = localtime(&now);
//     char timestamp[30];
//     strftime(timestamp, sizeof(timestamp), "%Y-%m-%d %H:%M:%S", timeinfo);

//     StaticJsonDocument<200> jsonDoc;
//     jsonDoc["timestamp"] = timestamp;
//     jsonDoc["flow_rate"] = flow_rate;

//     String jsonString;
//     serializeJson(jsonDoc, jsonString);

//     client.send(jsonString);
//   }
// }
