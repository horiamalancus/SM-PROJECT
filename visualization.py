import time
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
import config
import microphone
import led
import sys

visualization_type = sys.argv[1]
scroll_divisor_config = 4 if sys.argv[1] == "scroll_quad" else 2

_time_prev = time.time() * 1000.0

p = np.tile(1.0, (3, config.N_PIXELS // scroll_divisor_config))

def visualize_scroll(y):
    global p
    y = y**2.0
    y *= 255.0
    r = int(np.max(y[:len(y) // 3]))
    g = int(np.max(y[len(y) // 3: 2 * len(y) // 3]))
    b = int(np.max(y[2 * len(y) // 3:]))
    p[:, 1:] = p[:, :-1]
    p *= 0.98
    p = gaussian_filter1d(p, sigma=0.2)
    p[0, 0] = r
    p[1, 0] = g
    p[2, 0] = b
    return np.concatenate((p[:, ::-1], p), axis=1)

fft_window = np.hamming(int(config.MIC_RATE / config.FPS) * config.N_ROLLING_HISTORY)
prev_fps_update = time.time()


def microphone_update(audio_samples):
    global y_roll, prev_rms, prev_exp, prev_fps_update
    y = audio_samples / 2.0**15
    y_roll[:-1] = y_roll[1:]
    y_roll[-1, :] = np.copy(y)
    y_data = np.concatenate(y_roll, axis=0).astype(np.float32)
    
    vol = np.max(np.abs(y_data))
    if vol < config.MIN_VOLUME_THRESHOLD:
        print('No audio input. Volume below threshold. Volume:', vol)
        led.pixels = np.tile(0, (3, config.N_PIXELS))
        led.update()
    else:
        N = len(y_data)
        N_zeros = 2**int(np.ceil(np.log2(N))) - N
        y_data *= fft_window
        y_padded = np.pad(y_data, (0, N_zeros), mode='constant')
        YS = np.abs(np.fft.rfft(y_padded)[:N // 2])
        mel = np.atleast_2d(YS).T * dsp.mel_y.T
        mel = np.sum(mel, axis=0)
        mel = mel**2.0
        output = visualization_effect(mel)
        led.pixels = output
        
        ok = True
        if time.time() - 2.0 >prev_fps_update:
            f = open("/var/www/html/onoff.txt","r")
            if f.read() == "false":
                ok = False
        
        if ok == True:
            led.update()
        else:
            LED_COUNT = config.N_PIXELS
            LED_PIN = config.LED_PIN
            LED_FREQ_HZ = config.LED_FREQ_HZ
            LED_DMA = config.LED_DMA
            LED_BRIGHTNESS = config.BRIGHTNESS
            LED_INVERT = config.LED_INVERT
            LED_CHANNEL = 0

            def color_wipe(strip, color, wait_ms=50):
                for i in range(strip.numPixels()):
                    strip.setPixelColor(i, color)
                    strip.show()
                    time.sleep(wait_ms / 1000.0)

            parser = argparse.ArgumentParser()
            parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
            args = parser.parse_args()

            strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
            strip.begin()

            color_wipe(strip, Color(0, 0, 0), 10)

samples_per_frame = int(config.MIC_RATE / config.FPS)

y_roll = np.random.rand(config.N_ROLLING_HISTORY, samples_per_frame) / 1e16

if sys.argv[1] == "scroll":
        visualization_type = visualize_scroll

visualization_effect = visualization_type

if __name__ == '__main__':
    led.update()
    microphone.start_stream(microphone_update)