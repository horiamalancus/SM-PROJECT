import os

DEVICE = 'pi'

if DEVICE == 'pi':
    LED_PIN = 18
    LED_FREQ_HZ = 800000
    LED_DMA = 5
    BRIGHTNESS = 255
    LED_INVERT = False

USE_GUI = False
DISPLAY_FPS = True
N_PIXELS = 144

MIC_RATE = 44100

FPS = 50
_max_led_FPS = int(((N_PIXELS * 30e-6) + 50e-6)**-1.0)
assert FPS <= _max_led_FPS, 'FPS must be <= {}'.format(_max_led_FPS)

MIN_FREQUENCY = 200
MAX_FREQUENCY = 12000
N_FFT_BINS = 24

N_ROLLING_HISTORY = 2

MIN_VOLUME_THRESHOLD = 1e-7
