// Local Libraries
#include "Display_ST7789.h"
#include "LVGL_Driver.h"
#include "debug.h"
#include <small_bus.h>
#include <bus_icon.h>
#include <webserver.h>

// Arduino librarries
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>
#include <time.h>
#include <TimeLib.h>
#include <string.h>

#define debug true

#ifndef debug
#define debug false
#endif


// WiFi Credentials 
const char* ssid = "Stark Industries";
const char* password = "tony17071a0392";

// Default String
String routeNumber = "22";

unsigned long startAttemptTime = millis();
const unsigned long WIFI_TIMEOUT_MS = 150000; // 15 seconds timeout
const unsigned long poll_interval = 25000; // Request poll time is revery 25 seconds to avoid api call ehaustion

const char* host = "api-v3.mbta.com";
const int httpsPort = 443;
lv_obj_t* label;
lv_obj_t* img;
lv_obj_t* local_time;

int remaining_time[3] = {0,0,0};

// NTP server to request epoch time
const char* ntpServer = "pool.ntp.org";

// Variable to save current epoch time
unsigned long epochTime; 

// Function that gets current epoch time
unsigned long getTime() {
  time_t now;
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("Failed to obtain time");
    return(0);
  }
  char buffer[60];
  strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", &timeinfo);

  lv_label_set_text(local_time, buffer);
  
  DebugPrint("Debug :: ");
  DebugPrint(buffer);
  time(&now);
  return now;
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < WIFI_TIMEOUT_MS){
    delay(500);
    Serial.print(".");
  }

  if (WiFi.status() != WL_CONNECTED){
    Serial.println("\n WiFi NOT connected! Timed out"); 
    return;
  }

  if (WiFi.status() == WL_CONNECTED){
    Serial.println("\n✅ WiFi connected!");
  }
  
  configTime(0, 0, ntpServer);
  LCD_Init();
  Lvgl_Init();

  label = lv_label_create(lv_scr_act());
  lv_label_set_text(label, "Welcome!");
  lv_obj_align(label, LV_ALIGN_CENTER, 0, 0);
  
  img = lv_img_create(lv_scr_act());  // create image on active screen
  lv_img_set_src(img, &bus_icon);              // set your image source
  lv_obj_align(img, LV_ALIGN_TOP_MID, 0, 0);     // position image on screen


  local_time = lv_label_create(lv_scr_act());
  lv_label_set_text(local_time, "Time loading...");
  lv_obj_align(local_time, LV_ALIGN_CENTER, 0, -50);
  
  ServerBegin();

  }


// MBTA HHTPS Call//
void call_MBTA(){
    WiFiClientSecure client;
    client.setInsecure();  // WARNING: insecure



  String requestPath = "/predictions"
                          "?api_key=a7ce3bd86d3d4fb4ac2cfa39138c3396"
                          "&filter[latitude]=42.312322052258686"
                          "&filter[longitude]=-71.0934255584537"
                          "&filter[radius]=0.001"
                          "&filter[route]=" + routeNumber +
                          "&filter[direction_id]=1";
                          // "&filter[stop]: 1742"

    Serial.println("Connecting to MBTA API server...");
    if (!client.connect(host, httpsPort)) {
      Serial.println("❌ Connection failed!");
      return;
    }

    client.print(String("GET ") + requestPath + " HTTP/1.1\r\n" +
                "Host: " + host + "\r\n" +
                "User-Agent: ESP32Client/1.0\r\n" +
                "Connection: close\r\n\r\n");

    // Skip HTTP headers
    bool headersEnded = false;
    String response = "";
  while (client.connected() || client.available()) {
    if (client.available()) {
      char c = client.read();
      if (!headersEnded) {
        static String headerBuffer;
        headerBuffer += c;
        if (headerBuffer.endsWith("\r\n\r\n")) {
          headersEnded = true;
        }
      } else {
        response += c;
      }
    }
  }

    // Serial.println(" Raw JSON:");
    // Serial.println(response);
    
    // Parse JSON
    DynamicJsonDocument doc(24576);
    DeserializationError error = deserializeJson(doc, response);
    if (error) {
      Serial.print("❌ JSON parse error: ");
      Serial.println(error.f_str());
      return;
    }

    // Serial.println("✨ Pretty Printed JSON:");
    // serializeJsonPretty(doc, Serial);

    // Extract arrival times
    JsonArray data = doc["data"];
    Serial.println("🕐 Arrival times for Bus 22 to Ruggles:");
    int counter = 0;
    // Get the epoc time from the ntp server for the current time
    epochTime = getTime();

    for (JsonObject item : data) {
      if (counter > 2){
        break;
      }
      
      const char* time = item["attributes"]["arrival_time"];
      if (time && strlen(time)) {
          // Serial.println(time);
          // Input: ISO 8601 format string with timezone
          const char* iso8601 = time;

          char datetime[20];  // Only keep "2025-06-28T20:11:14"
          strncpy(datetime, iso8601, 19);
          datetime[19] = '\0';

          struct tm tm;
          memset(&tm, 0, sizeof(tm));
          strptime(datetime, "%Y-%m-%dT%H:%M:%S", &tm);

          time_t epoch = mktime(&tm);

          int timezone_offset_seconds = -4 * 3600;  // -4 hours
          epoch -= timezone_offset_seconds;

   
          // Substract the time to show the number of seconds left for the service to reach the desired stop
          int timeLeft = epoch - epochTime;
          // Serial.print("Time left : ");
          // Serial.println(timeLeft);

          // Converting time back to date time format
          // int hours = timeLeft % 3600;
          auto minutes = timeLeft / 60;
          if (minutes < 0){
            return;
          }
          remaining_time[counter] = minutes;
          Serial.print(minutes);
          Serial.println(" Minutes");
      } 
      else {
        Serial.println("No arrival_time");
      }
      counter++;
    }

    client.stop();  
    char buffer[80];
    snprintf(buffer, sizeof(buffer), "Route No : %s \nBus 1: %d min\nBus 2: %d min\nBus 3: %d min", routeNumber.c_str() ,remaining_time[0],remaining_time[1],remaining_time[2]);  // or whatever data
    lv_label_set_text(label, buffer);
}

unsigned long lastCallTime = 0;
unsigned long lastTimeUpdate = 0;
// First call Flag
bool firstCallFlag = false;


// Loop
void loop() {
  Timer_Loop();
  delay(5);
  handleRouteClient();
  if (firstCallFlag != true){
    getTime();
    call_MBTA();
    firstCallFlag = true;
    lastTimeUpdate = millis();
    lastCallTime = millis();
  }
  unsigned long now = millis();
  // Update local time label once every 1000 ms
  if (now - lastTimeUpdate >= 1000) {
    lastTimeUpdate = now;
    getTime();
  }
  if (now - lastCallTime >= poll_interval) {
    lastCallTime = now;
    call_MBTA();
  }
}

