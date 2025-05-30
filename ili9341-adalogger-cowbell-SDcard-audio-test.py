# ili9341-adalogger-cowbell-SDcard-audio-test.py
"""
CircuitPython test for ILI9341 SPI display + Adalogger Cowbell (SD card) + audio.
- Displays a message with a styled frame
- Mounts SD card with MP3s in /sd/robot_sounds/
- Plays 3 MP3s using audiomp3 and AudioOut
"""
import board
import busio
import sdcardio
import storage
import time
import digitalio
import displayio
import pwmio
import terminalio
from audiomp3 import MP3Decoder
from adafruit_display_text import label
import adafruit_ili9341

# --- Display Setup ---
displayio.release_displays()

# Shared SPI bus for display and SD card
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP16)

# Display control pins
tft_cs = board.GP20
tft_dc = board.GP21
tft_reset = board.GP15

# PWM backlight
backlight = pwmio.PWMOut(board.GP22, frequency=5000, duty_cycle=65535)

# Display bus
display_bus = displayio.FourWire(
    spi,
    command=tft_dc,
    chip_select=tft_cs,
    reset=tft_reset
)

# Initialize display
display = adafruit_ili9341.ILI9341(
    display_bus,
    width=320,
    height=240,
    rotation=0,
    backlight_pin=None  # we control it manually
)

# Create display group
splash = displayio.Group()
display.root_group = splash

# Frame (purple)
frame_bitmap = displayio.Bitmap(320, 240, 1)
frame_palette = displayio.Palette(1)
frame_palette[0] = 0x800080  # Purple
frame = displayio.TileGrid(frame_bitmap, pixel_shader=frame_palette)
splash.append(frame)

# Background (blue inset)
bg_bitmap = displayio.Bitmap(290, 210, 1)
bg_palette = displayio.Palette(1)
bg_palette[0] = 0x0033FF  # Blue
bg = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette, x=15, y=15)
splash.append(bg)

# Centered label
text = label.Label(
    terminalio.FONT,
    text="ILI9341 Makes Awesome!",
    color=0xFFFF00,
    scale=2,
    anchor_point=(0.5, 0.5),
    anchored_position=(display.width // 2, display.height // 2)
)
splash.append(text)

print("✅ ILI9341 Display initialized")

# --- SD Card Setup ---
SD_CS = board.GP17

try:
    sdcard = sdcardio.SDCard(spi, SD_CS)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    print("😎 SD card mounted")
except Exception as e:
    print("❌ SD card mount failed:", e)
    while True:
        pass

# --- Audio Setup ---
try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        print("❌ This board does not support audio")
        while True:
            pass

audio = AudioOut(board.GP3)  # Speaker on GP3

# --- MP3 Playback ---
path = "/sd/robot_sounds/"
filename = "0.mp3"
try:
    mp3_file = open(path + filename, "rb")
    decoder = MP3Decoder(mp3_file)
except Exception as e:
    print("❌ Failed to open initial MP3 file:", e)
    while True:
        pass

def play_mp3(filename):
    try:
        decoder.file = open(path + filename, "rb")
        audio.play(decoder)
        print(f"🎵 Playing {filename}")
        while audio.playing:
            pass
    except Exception as e:
        print(f"❌ Error playing {filename}:", e)

print("🐮 Cowbell Adalogger SD Test")
play_mp3("0.mp3")
play_mp3("1.mp3")
play_mp3("2.mp3")

while True:
    pass
