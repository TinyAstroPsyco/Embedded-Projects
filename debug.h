#pragma once

#define debug false

#if debug
  #define DebugPrint(x) Serial.print(x)
  #define DebugPrintln(x) Serial.println(x)

#else 
  #define DebugPrint(x)
  #define DebugPrintln(x)

#endif
