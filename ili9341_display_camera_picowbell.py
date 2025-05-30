# ili9341_display_camera_picowbell.py

"""
Demo for Raspberry Pi Pico W + PiCowbell Camera + ILI9341 320x240 SPI Display
Shows a live feed from the OV5640 camera on the display.
Wiring of display should not conflict with either Adalogger Cowbell
or the Camerra Cowbell used here
"""

import time, board, busio, digitalio, displayio, pwmio
import adafruit_ov5640, adafruit_ili9341

displayio.release_displays()
# Shared SPI bus for display and SD card
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP16)

# Display control pins
tft_cs = board.GP20
tft_dc = board.GP21
tft_reset = board.GP15

# PWM backlight
backlight = pwmio.PWMOut(board.GP22, frequency=5000, duty_cycle=65535)
display_bus = displayio.FourWire(
    spi,
    command=tft_dc,
    chip_select=tft_cs,
    reset=tft_reset
)

display = adafruit_ili9341.ILI9341(display_bus,
                                   width=320,
                                   height=240,
                                   rotation=180,
                                   colstart=0,
                                   rowstart=0,
                                   backlight_pin=None  # we're using pwmio manually
                                   )

# === I2C + Camera Setup ===
i2c = busio.I2C(scl=board.GP5, sda=board.GP4)

reset = digitalio.DigitalInOut(board.GP14)

cam = adafruit_ov5640.OV5640(
    i2c,
    data_pins=(
        board.GP6,
        board.GP7,
        board.GP8,
        board.GP9,
        board.GP10,
        board.GP11,
        board.GP12,
        board.GP13,
    ),
    clock=board.GP3,      # XCLK / PCLK (external clock pin)
    vsync=board.GP0,
    href=board.GP2,
    mclk=None,
    shutdown=None,
    reset=reset,
    size=adafruit_ov5640.OV5640_SIZE_QVGA,  # 320x240
)

print("Camera ID:", cam.chip_id)

# === Camera Settings ===
cam.colorspace = adafruit_ov5640.OV5640_COLOR_RGB
cam.flip_y = True
cam.flip_x = False
cam.test_pattern = False

# === Create Bitmap Buffer to Hold Camera Output ===
try:
    bitmap = displayio.Bitmap(cam.width, cam.height, 65535)
except MemoryError:
    print("MemoryError: falling back to smaller camera size")
    cam.size = adafruit_ov5640.OV5640_SIZE_QCIF  # 176x144
    bitmap = displayio.Bitmap(cam.width, cam.height, 65535)

# === Prepare Display Group ===
g = displayio.Group(scale=1, x=(display.width - cam.width) // 2, y=(display.height - cam.height) // 2)
tg = displayio.TileGrid(
    bitmap,
    pixel_shader=displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565_SWAPPED)
)
g.append(tg)
display.root_group = g

# === Main Camera Loop ===
display.auto_refresh = False
t0 = time.monotonic_ns()

print("Camera code running!")

while True:
    cam.capture(bitmap)
    bitmap.dirty()
    display.refresh(minimum_frames_per_second=0)
    t1 = time.monotonic_ns()
    print("FPS:", round(1e9 / (t1 - t0), 2))
    t0 = t1
