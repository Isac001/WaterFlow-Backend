// #include <ESP8266WiFi.h>
// #include <ArduinoWebsockets.h>
// #include <ArduinoJson.h>
// #include <time.h>

// using namespace websockets;

// const char* ssid = "brisa-2090364";
// const char* password = "xzxcx5dt";
// const char* websockets_server_host = "192.168.0.105";
// const int websockets_server_port = 8000;

// #define FlowSensor_INPUT D1
// #define PERIOD 1000

// WebsocketsClient client;

// volatile unsigned long pulse_counter = 0;
// unsigned long old_time = 0;

// void IRAM_ATTR interrupt_handler() {
//   pulse_counter++;
// }

// // Adicionando a declaração da função antes do setup()
// void waitForNTP() {
//   Serial.print("⌛ Aguardando NTP");
//   time_t now = time(nullptr);
//   int attempts = 0;
//   while (now < 8 * 3600 * 2) {
//     delay(500);
//     Serial.print(".");
//     now = time(nullptr);
//     attempts++;
//     if (attempts > 30) {
//       Serial.println("\n❌ Erro: NTP não respondeu. Reiniciando...");
//       ESP.restart();
//     }
//   }
//   Serial.println("\n✅ Horário sincronizado com sucesso!");
//   Serial.print("🕒 Horário atual: ");
//   Serial.println(ctime(&now));
// }

// void setup() {
//   Serial.begin(115200);
//   delay(1000);
//   Serial.println("🚀 Inicializando...");

//   // Lista redes WiFi disponíveis
//   Serial.println("🔍 Scan de redes WiFi disponíveis:");
//   int n = WiFi.scanNetworks();
//   if (n == 0) {
//     Serial.println("Nenhuma rede encontrada");
//   } else {
//     Serial.print(n);
//     Serial.println(" redes encontradas:");
//     for (int i = 0; i < n; ++i) {
//       Serial.print(i + 1);
//       Serial.print(": ");
//       Serial.print(WiFi.SSID(i));
//       Serial.print(" (");
//       Serial.print(WiFi.RSSI(i));
//       Serial.print(" dBm)");
//       Serial.println((WiFi.encryptionType(i) == ENC_TYPE_NONE) ? " " : "*");
//       delay(10);
//     }
//   }
//   Serial.println("========================");

//   pinMode(FlowSensor_INPUT, INPUT_PULLUP);
//   attachInterrupt(digitalPinToInterrupt(FlowSensor_INPUT), interrupt_handler, RISING);
//   Serial.println("✅ Sensor de fluxo configurado.");

//   Serial.println("🧹 Limpando configurações WiFi antigas...");
//   WiFi.disconnect(true);
//   delay(1000);
//   WiFi.mode(WIFI_STA);

//   Serial.print("📶 Conectando-se à rede WiFi: ");
//   Serial.println(ssid);
//   WiFi.begin(ssid, password);

//   int wifi_attempts = 0;
//   while (WiFi.status() != WL_CONNECTED) {
//     delay(500);
//     Serial.print(".");
//     wifi_attempts++;
//     if (wifi_attempts > 30) {
//       Serial.print("\n❌ Falha ao conectar ao WiFi. Status: ");
//       Serial.println(WiFi.status());
//       Serial.println("🔄 Reiniciando...");
//       ESP.restart();
//     }
//   }

//   Serial.println("\n✅ WiFi conectado com sucesso!");
//   Serial.print("🔗 IP: ");
//   Serial.println(WiFi.localIP());

//   Serial.print("🌐 Conectando ao WebSocket: ");
//   Serial.print(websockets_server_host);
//   Serial.print(":");
//   Serial.println(websockets_server_port);

//   bool connected = client.connect(websockets_server_host, websockets_server_port, "/ws/flow-reading/");
//   if (connected) {
//     Serial.println("✅ WebSocket conectado com sucesso!");
//   } else {
//     Serial.println("❌ Falha ao conectar WebSocket.");
//   }

//   client.onMessage([](WebsocketsMessage message) {
//     Serial.print("📩 Mensagem recebida do servidor: ");
//     Serial.println(message.data());
//   });

//   Serial.println("⏱️ Configurando sincronização NTP...");
//   configTime(-3 * 3600, 0, "pool.ntp.org", "time.nist.gov");
//   waitForNTP();
// }

// void loop() {
//   client.poll();
//   sendFlowRate();
//   delay(1000);
// }

// void sendFlowRate() {
//   unsigned long current_time = millis();
//   unsigned long delta_time = current_time - old_time;

//   if (delta_time >= PERIOD) {
//     old_time = current_time;

//     noInterrupts();
//     unsigned long pulse_count = pulse_counter;
//     pulse_counter = 0;
//     interrupts();

//     float pulse_rate = (pulse_count * 1000.0) / delta_time;
//     float flow_rate = pulse_rate / 7.5;
//     flow_rate = round(flow_rate * 100) / 100.0;

//     Serial.print("💧 Vazão: ");
//     Serial.print(flow_rate, 2);
//     Serial.println(" L/min");

//     time_t now = time(nullptr);
//     if (now < 8 * 3600 * 2) {
//       Serial.println("❌ Horário inválido, descartando leitura.");
//       return;
//     }

//     struct tm* timeinfo = localtime(&now);
//     char times_tamp[30];
//     strftime(times_tamp, sizeof(times_tamp), "%d/%m/%Y %H:%M:%S", timeinfo);

//     StaticJsonDocument<200> jsonDoc;
//     jsonDoc["times_tamp"] = times_tamp;
//     jsonDoc["flow_rate"] = flow_rate;

//     String jsonString;
//     serializeJson(jsonDoc, jsonString);

//     Serial.print("📤 Enviando para servidor: ");
//     Serial.println(jsonString);

//     bool ok = client.send(jsonString);
//     if (!ok) {
//       Serial.println("❌ Falha no envio do WebSocket.");
//     }
//   }
// }