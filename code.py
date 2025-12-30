import time
import board
import digitalio

# ==== PINS ====
PIR_PIN  = board.GP0      # OUT du HC-SR501
LED_A_PIN = board.GP1     # LED 1 (ex: rouge)
LED_B_PIN = board.GP2     # LED 2 (ex: bleue)

# ==== Réglages sirène ====
SWITCH_LED_PERIOD_S = 0.12   # 0.12s -> alternance rapide (sirène)

# ==== PIR ====
pir = digitalio.DigitalInOut(PIR_PIN)
pir.direction = digitalio.Direction.INPUT
pir.pull = digitalio.Pull.DOWN

# ==== LEDs ====
led_a = digitalio.DigitalInOut(LED_A_PIN)
led_a.direction = digitalio.Direction.OUTPUT

led_b = digitalio.DigitalInOut(LED_B_PIN)
led_b.direction = digitalio.Direction.OUTPUT

time.sleep(2)


while True:
    if pir.value:  # mouvement détecté
        phase = int(time.monotonic() / SWITCH_LED_PERIOD_S) % 2
        led_a.value = (phase == 0)
        led_b.value = (phase == 1)
    else:
        led_a.value = False
        led_b.value = False

    time.sleep(0.1)
