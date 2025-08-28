📟 ESP32 MBTA Display
An ESP32-C6 powered LCD display that shows real-time information (e.g., MBTA predictions, system stats) using LVGL GUI on a ST7789 TFT screen.
The project integrates Wi-Fi, Bluetooth, SD card storage, and LVGL graphics into one neat embedded system.

✨ Features
🖥️ 1.47" ST7789 LCD (172×320) display driver (custom SPI implementation).
🎨 LVGL GUI integration for clean, modern graphics.
🔦 Backlight control (PWM dimming).
📊 Live updates on the display using LVGL timers.

🛠️ Hardware Used
ESP32-C6 DevKit (or similar ESP32 board).
1.47" 172×320 ST7789 TFT LCD.
MicroSD card module (SPI).
Supporting components (wires, breadboard, power supply).


📂 Software Architecture

1. Display Driver (Display_ST7789.cpp/.h)
Handles SPI communication with ST7789 LCD.
Provides functions for initialization, drawing windows, and backlight control.

2. LVGL Driver (LVGL_Driver.cpp/.h)
Connects LVGL with the display via flush callback.
Initializes display buffers.
Creates a periodic tick for LVGL tasks.

3. LVGL Example (LVGL_Example.cpp/.h)
Builds the Onboard Parameters Dashboard:
SD card size.
Flash size.
Wireless scan results.
Uses LVGL tabview and grid layouts for UI.

4. Wireless (Wireless.cpp/.h)
Scans for Wi-Fi and BLE devices.
Updates global variables for GUI display.
Supports both blocking and FreeRTOS task-based scans.

5. SD Card (SD_Card.cpp/.h)
Initializes and checks SD card.
Retrieves file lists by extension.
Provides total/used/free space info.

⚙️ Setup
🔹 Prerequisites
ESP-IDF or Arduino-ESP32 framework installed.
LVGL library installed.
TFT_eSPI or SPI library enabled.

🔹 Wiring (example ESP32-C6 → ST7789)
ST7789 Pin	ESP32-C6 Pin
MOSI	GPIO6
SCLK	GPIO7
CS	GPIO14
DC	GPIO15
RST	GPIO21
BLK	GPIO22

SD card uses GPIO4 as CS.

🚀 How It Works
On boot:
LCD initializes with ST7789 commands.
LVGL GUI is created.
SD card and flash memory are checked.

Wireless scan:
Wi-Fi & BLE scan results are updated.
Display shows W: <wifi_count> B: <ble_count> OK.

Dashboard updates:
LVGL timer (example1_increase_lvgl_tick) refreshes SD size, flash size, and wireless results.
📸 Screenshots

📌 Future Improvements
✅ Integrate MBTA API (real-time train/bus predictions).
✅ Show arrival times & line information on the display.
⏳ Add touch support or button input for navigation.
⏳ Improve UI themes with LVGL widgets.
