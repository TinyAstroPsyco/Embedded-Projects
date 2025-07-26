#pragma once

#include <WiFi.h>

extern String routeNumber;

void ServerBegin();  // Call this once in setup()
void handleRouteClient();    // Call this repeatedly in loop()