// Blynk definitions
#define BLYNK_TEMPLATE_ID "TMPL29pJE2D4J"
#define BLYNK_TEMPLATE_NAME "ESP8266"
#define BLYNK_AUTH_TOKEN "_ul4sNrVwQ2OiuEuTt3-TO3BMs1ygzuz"

#include <ESP8266WiFi.h>          // Library for Wi-Fi connectivity
#include <BlynkSimpleEsp8266.h>   // Library for Blynk integration with ESP8266
#include <ESP8266HTTPClient.h>    // Library for making HTTP requests
#include <ArduinoJson.h>          // Library for handling JSON data
#include <time.h>                 // Library for handling time functions

#define FlowSensor_INPUT D1  // Flow sensor input pin (GPIO5 - D1 on NodeMCU)
#define PERIOD 1000          // Reading interval (1 second)

// Wi-Fi configuration
const char* ssid = "brisa-2090364";  // Wi-Fi network name
const char* pass = "xzxcx5dt";       // Wi-Fi password

const char* server_url = "http://192.168.0.105:8000/api/flow_reading/"; // API endpoint for sending data

BlynkTimer timer;  // Blynk timer for periodic tasks

volatile unsigned long pulse_counter = 0; // Variable to store pulse count
unsigned long old_time; // Variable to store previous timestamp

// Interrupt service routine for counting sensor pulses
void ICACHE_RAM_ATTR interrupt_handler() {
  pulse_counter++;  // Increment pulse count on each signal from the flow sensor
}

// Function to calculate and send flow rate to Blynk and backend server
void sendFlowRate() {
  unsigned long new_time = millis() - old_time;

  // Check if it's time to take a new reading
  if (new_time >= PERIOD) {
    noInterrupts(); // Disable interrupts temporarily
    unsigned long pulse_count = pulse_counter; // Store pulse count
    pulse_counter = 0; // Reset pulse counter
    interrupts(); // Re-enable interrupts

    old_time = millis(); // Update the last recorded time

    // Calculate flow rate in liters per minute
    float pulse_rate = (pulse_count * 1000.0) / new_time;
    float flow_rate = pulse_rate / 7.5;  // Conversion factor for sensors like YF-S201, YF-S402

    // Round the flow rate to 2 decimal places
    flow_rate = round(flow_rate * 100) / 100.0;

    Serial.print("Flow: ");
    Serial.print(flow_rate, 2);
    Serial.println(" L/min");

    // Send data to Blynk on Virtual Pin V2
    Blynk.virtualWrite(V2, flow_rate);

    // Send data to the Django backend server
    sendFlowDataToServer(flow_rate);
  }
}

// Function to send flow rate data to the backend server
void sendFlowDataToServer(float flow_rate) {
  if (WiFi.status() == WL_CONNECTED) {  // Check if Wi-Fi is connected
    WiFiClient client;
    HTTPClient http;

    http.begin(client, server_url);  // Initialize HTTP connection
    http.addHeader("Content-Type", "application/json"); // Set JSON content type

    // Get current date and time
    time_t now = time(nullptr);
    struct tm* timeinfo = localtime(&now);
    char timestamp[30];
    strftime(timestamp, sizeof(timestamp), "%Y-%m-%d %H:%M:%S", timeinfo); // Format timestamp

    StaticJsonDocument<200> jsonDoc; // JSON document for storing data
    jsonDoc["timestamp"] = timestamp; // Add timestamp to JSON object

    // Convert flow rate to string with 2 decimal places
    char flow_rate_str[10];
    dtostrf(flow_rate, 5, 2, flow_rate_str);
    jsonDoc["flow_rate"] = flow_rate;

    String jsonString;
    serializeJson(jsonDoc, jsonString); // Serialize JSON object to string

    int httpResponseCode = http.POST(jsonString); // Send POST request with JSON data

    Serial.print("HTTP Response Code: ");
    Serial.println(httpResponseCode);

    http.end(); // Close HTTP connection
  } else {
    Serial.println("ERROR: Wi-Fi Disconnected");
  }
}

void setup() {
  Serial.begin(115200); // Initialize serial communication

  pinMode(FlowSensor_INPUT, INPUT_PULLUP); // Set sensor pin as input with pull-up resistor
  attachInterrupt(digitalPinToInterrupt(FlowSensor_INPUT), interrupt_handler, RISING); // Attach interrupt to sensor

  // Connect to Wi-Fi
  WiFi.begin(ssid, pass);
  Serial.print("Connecting to Wi-Fi...");

  while (WiFi.status() != WL_CONNECTED) { // Wait for connection
    delay(1000);
    Serial.print(".");
  }

  Serial.println("\n✅ Wi-Fi Connected!");

  // Start Blynk service
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);

  // Configure Network Time Protocol (NTP) to get the correct time
  configTime(0, 0, "pool.ntp.org", "time.nist.gov");

  // Set up a timer to send flow rate data every 1 second
  timer.setInterval(1000L, sendFlowRate);
}

void loop() {
  Blynk.run();  // Keep Blynk running
  timer.run();  // Run Blynk timer for periodic tasks
}