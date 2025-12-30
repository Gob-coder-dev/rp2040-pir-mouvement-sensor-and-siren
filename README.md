# RP2040 Zero motion detector siren (CircuitPython)

Prototype: PIR HC-SR501 on a Waveshare RP2040 Zero. When motion is detected, two LEDs flash in opposition to imitate a siren.

![image_1](https://github.com/user-attachments/assets/9fcfee10-47c9-4b81-8125-7ec6461bd75a)

## Hardware
- Waveshare RP2040 Zero
- PIR sensor HC-SR501
- 2 LEDs + 2 current-limit resistors (220 to 330 ohms)
- Breadboard, jumper wires, USB 5 V power
- Temporary GP15-to-GND jumper to re-enable the CIRCUITPY drive (see `boot.py`)

## Flash CircuitPython (one time)
1) Hold BOOT/BOOTSEL while plugging the board to USB to mount the `RPI-RP2` drive.
2) Copy `adafruit-circuitpython-waveshare_rp2040_zero-fr-10.0.3.uf2` to the root of that drive.
3) The board reboots and mounts `CIRCUITPY` (unless `boot.py` disables it; see below).

## Put the project files on the board
- Copy `code.py` and `boot.py` to the root of `CIRCUITPY`.
- `boot.py` disables the USB drive if GP15 is **not** tied to GND at boot. To edit files, connect GP15 to GND and press RESET (or comment out that protection).

## Wiring (see build photo)
- PIR VCC -> board 5 V / VSYS pin (or 3V3 if your module is set for 3.3 V)
- PIR GND -> common GND
- PIR OUT -> GP0
- LED A (e.g., red): GP1 -> 220-330 ohm resistor -> LED anode; LED cathode -> GND
- LED B (e.g., blue): GP2 -> 220-330 ohm resistor -> LED anode; LED cathode -> GND
- Common ground for every component.

Note: the HC-SR501 output is typically around 3.3 V (RP2040 safe). If your module outputs 5 V, add a resistor divider or a transistor to protect GP0.

### Breadboard wiring as in the photo (color callouts)
- Orange wire: PIR OUT (middle pin on HC-SR501) runs to GP0 on the RP2040 Zero (lower-right pin in the photo).
- Black wire: PIR VCC goes to the 5 V / VSYS pin on the RP2040 (upper-left pin area).
- White wire from PIR: PIR GND goes to the RP2040 GND (upper-right pin area); short black jumpers also tie the LED cathode row to the same ground.
- Purple jumper 1: GP1 from the RP2040 to the series resistor, then to the red LED anode (red LED cathode to ground).
- Purple jumper 2: GP2 from the RP2040 to the series resistor, then to the blue LED anode (blue LED cathode to ground).
- Two resistors on the right are the current limiters for the LEDs; each sits between its GPIO pin and the purple wire going to the matching LED.
- Keep a loose jumper for GP15->GND when you need the CIRCUITPY drive; remove it for normal locked operation.

![image_2](https://github.com/user-attachments/assets/7d0e0a17-218f-4f08-8817-c266f93dbbbe)
![image_3](https://github.com/user-attachments/assets/8dfbffeb-b8f5-4a81-bf05-a5b0420ddb38)

## Code behavior (`code.py`)
- Pins: PIR on GP0 with pull-down; LED A on GP1; LED B on GP2.
- `SWITCH_LED_PERIOD_S = 0.12` sets the alternation speed (~4.2 toggles/s).
- `time.sleep(2)` gives the PIR 2 s to settle at startup.
- Main loop: if `pir.value` is high, compute a phase from `time.monotonic()` and alternate the LEDs. Otherwise both LEDs stay off. Poll every 100 ms.

## Startup
1) Power the board via USB (or 5 V on VSYS).
2) Let the PIR warm up (often 30-60 s on HC-SR501, plus the 2 s in code).
3) Check GP15: leave it open to hide `CIRCUITPY`, tie it to GND if you need disk access.
4) Wave in front of the sensor: the LEDs alternate quickly on motion; both off when idle.

## Customize
- Pins: change `PIR_PIN`, `LED_A_PIN`, `LED_B_PIN` to match your wiring.
- Siren rate: adjust `SWITCH_LED_PERIOD_S` (smaller = faster).
- Buzzer: replace one LED with a buzzer (ideally driven via transistor) and reuse the same toggling logic.

## Troubleshooting
- No `CIRCUITPY` drive: tie GP15 to GND and reboot; otherwise edit/remove `boot.py`.
- No motion detected: check PIR power (5 V or 3.3 V per jumper), common ground, and sensor position.
- Dim or dead LEDs: check polarity and resistor values (220-330 ohms).
