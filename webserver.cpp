#include <WiFi.h>
#include "WiFiClient.h"
#include <webserver.h>

WiFiServer server(80);

void ServerBegin() {
  server.begin();
  Serial.println("Webserver has Started!!");
  Serial.println("The IP Address of the server is >> ");
  Serial.println(WiFi.localIP());
}

void handleRouteClient() {
  WiFiClient client = server.available();
  if (!client) return;

  Serial.println("A client has connected!!");
  String request = "";
  bool headersEnded = false;

  while (client.connected()) {
    if (client.available()) {
      char c = client.read();
      request += c;
      Serial.write(c);  // Print entire HTTP request

      if (!headersEnded && request.endsWith("\r\n\r\n")) {
        headersEnded = true;
        Serial.println("\n--- End of headers ---");
      }

      if (headersEnded && client.available() == 0) break;
    }
  }

  // Look for POST form data
  if (request.indexOf("POST") >= 0 && request.indexOf("route=") >= 0) {
    int idx = request.indexOf("route=");
    String routeValue = request.substring(idx + 6);
    routeValue.trim();
    routeValue.replace("+", " ");
    routeValue.replace("\r", "");
    routeValue.replace("\n", "");
    routeNumber = routeValue;
    Serial.print("✅ Extracted Route: ");
    Serial.println(routeNumber);
  }

  // Send response HTML with dialog-style form
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println();
  client.println(R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <title>Set Route Number</title>
  <style>
    body {
      font-family: Arial;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background-color: #f0f0f0;
    }
    .dialog-box {
      background: white;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(0,0,0,0.3);
    }
    input[type="text"] {
      padding: 10px;
      width: 200px;
      font-size: 16px;
    }
    input[type="submit"] {
      padding: 10px 20px;
      font-size: 16px;
      margin-top: 10px;
    }
  </style>
</head>
<body>
  <div class="dialog-box">
    <h2>Enter Route Number</h2>
    <form method="POST" action="/">
      <input type="text" name="route" placeholder="e.g. 22">
      <br><br>
      <input type="submit" value="Submit">
    </form>
  </div>
</body>
</html>
)rawliteral");

  delay(1);
  client.stop();
  Serial.println("Client disconnected.");
}


