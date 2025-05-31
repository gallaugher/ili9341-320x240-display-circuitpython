# ST7789-display-demo.py
# Fun demo cycling through image, colors, and animation
# Demo of ST7789 320x172 rounded corner display purchased from Aliexpress.
import board
import displayio, busio, terminalio
import digitalio
import time
from displayio import FourWire
from adafruit_st7789 import ST7789
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

# Release any resources currently in use for the displays
displayio.release_displays()

# Load custom font
try:
    custom_font = bitmap_font.load_font("/fonts/helvB08.bdf")
    print("✅ Custom font loaded")
except Exception as e:
    print(f"❌ Could not load custom font: {e}")
    custom_font = terminalio.FONT  # Fallback to built-in font

# SPI setup
SCL = board.GP18  # Clock (SCK)
SDA = board.GP19  # Data (MOSI)
MISO = board.GP16  # Required by CircuitPython but unused

spi = busio.SPI(SCL, SDA, MISO)
tft_cs = board.GP20
tft_dc = board.GP21
tft_rst = board.GP15

# Backlight control
backlight = digitalio.DigitalInOut(board.GP22)
backlight.direction = digitalio.Direction.OUTPUT
backlight.value = True  # Turn on backlight

print("Backlight turned ON")

display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)

display = ST7789(display_bus,
                 width=320,
                 height=172,
                 rotation=90,
                 colstart=33)

print("Display initialized")


def demo_image():
    """Display the awesome image"""
    print("🖼️ Image Display")

    splash = displayio.Group()

    try:
        bitmap = displayio.OnDiskBitmap("/images/make-something-awesome-small.bmp")
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
        splash.append(tile_grid)
        print("Image loaded successfully")
    except Exception as e:
        print(f"Error loading image: {e}")
        # Fallback - solid color if image fails
        color_bitmap = displayio.Bitmap(display.width, display.height, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFF0000  # Red to indicate error
        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        splash.append(bg_sprite)

    display.root_group = splash
    time.sleep(4)


def demo_color_bars():
    """Display color bars adapted for 320x172"""
    print("🌈 Color Spectrum Test")

    splash = displayio.Group()

    # Create vertical color bars
    colors = [
        0xFF0000,  # Red
        0xFF8000,  # Orange
        0xFFFF00,  # Yellow
        0x80FF00,  # Yellow-Green
        0x00FF00,  # Green
        0x00FF80,  # Green-Cyan
        0x00FFFF,  # Cyan
        0x0080FF,  # Blue-Cyan
        0x0000FF,  # Blue
        0x8000FF,  # Blue-Magenta
        0xFF00FF,  # Magenta
        0xFF0080,  # Red-Magenta
    ]

    bar_width = 320 // len(colors)

    for i, color in enumerate(colors):
        bar_bitmap = displayio.Bitmap(bar_width, 126, 1)  # Adjusted height for 172px display
        bar_palette = displayio.Palette(1)
        bar_palette[0] = color
        bar = displayio.TileGrid(bar_bitmap, pixel_shader=bar_palette,
                                 x=i * bar_width, y=24)
        splash.append(bar)

    # Title
    title = label.Label(
        custom_font,  # Use your custom font instead of terminalio.FONT
        text="Vivid Colors!",
        color=0xFFFF00,
        scale=2,  # You might want to adjust this since custom fonts have different sizes
        anchor_point=(0.5, 0.0),
        anchored_position=(display.width//2, 5)
    )
    splash.append(title)

    # Bottom text
    bottom_text = label.Label(
        terminalio.FONT,
        text="ST7789 • 320x172 • SPI",
        color=0xFFFFFF,
        scale=1,
        anchor_point=(0.5, 0.0),
        anchored_position=(160, 155)
    )
    splash.append(bottom_text)

    display.root_group = splash
    time.sleep(4)


def demo_running_character():
    """Fun animated character running across screen"""
    print("🏃 Animated Character Demo")

    # Character sprite data - simple 8x8 pixel art character
    # 1 = character color, 0 = transparent
    character_data = [
        [0, 0, 1, 1, 1, 1, 0, 0],  # Hat
        [0, 1, 1, 1, 1, 1, 1, 0],  # Head
        [0, 1, 0, 1, 1, 0, 1, 0],  # Eyes
        [0, 1, 1, 1, 1, 1, 1, 0],  # Face
        [0, 0, 1, 0, 0, 1, 0, 0],  # Mouth
        [1, 1, 1, 1, 1, 1, 1, 1],  # Body
        [0, 1, 1, 1, 1, 1, 1, 0],  # Body
        [0, 1, 0, 1, 1, 0, 1, 0],  # Legs
    ]

    char_width = 8
    char_height = 8
    char_scale = 6  # Bigger character! (48x48 pixels)

    # Bright light colors that pop against black background
    colors = [
        0xFFFF00,  # Bright Yellow
        0x00FFFF,  # Bright Cyan
        0xFF00FF,  # Bright Magenta
        0x80FF80,  # Light Green
        0xFF8080,  # Light Pink
        0xFFFFFF,  # White
        0xFF8000,  # Bright Orange
        0x8080FF,  # Light Blue
    ]
    color_index = 0

    # Animation loop
    for x_pos in range(-char_width * char_scale, 320 + char_width * char_scale, 6):
        splash = displayio.Group()

        # Black background
        bg_bitmap = displayio.Bitmap(320, 172, 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = 0x000000
        bg = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)
        splash.append(bg)

        # Create character sprite
        char_bitmap = displayio.Bitmap(char_width * char_scale, char_height * char_scale, 2)
        char_palette = displayio.Palette(2)
        char_palette[0] = 0x000000  # Transparent/background
        char_palette[1] = colors[color_index % len(colors)]  # Character color

        # Draw scaled character
        for y in range(char_height):
            for x in range(char_width):
                pixel_value = character_data[y][x]
                # Scale up the pixel
                for sy in range(char_scale):
                    for sx in range(char_scale):
                        char_bitmap[x * char_scale + sx, y * char_scale + sy] = pixel_value

        # Position character
        char_y = 172 // 2 - (char_height * char_scale) // 2  # Center vertically
        char_sprite = displayio.TileGrid(char_bitmap, pixel_shader=char_palette,
                                         x=x_pos, y=char_y)
        splash.append(char_sprite)

        # Add title
        title = label.Label(
            custom_font,
            text="Running Character!",
            color=0xFFFF00,
            scale=2,
            anchor_point=(0.5, 0.0),
            anchored_position=(160, 10)
        )
        splash.append(title)

        # Add ground line
        ground_bitmap = displayio.Bitmap(320, 2, 1)
        ground_palette = displayio.Palette(1)
        ground_palette[0] = 0x00FF00  # Green ground
        ground = displayio.TileGrid(ground_bitmap, pixel_shader=ground_palette,
                                    x=0, y=140)
        splash.append(ground)

        display.root_group = splash
        time.sleep(0.01)  # Animation speed

        # Change color occasionally
        if x_pos % 60 == 0:
            color_index += 1


def run_demo():
    """Run the complete demo cycle"""
    print("🚀 Starting ST7789 Fun Demo Cycle")

    demos = [
        demo_image,
        demo_color_bars,
        demo_running_character
    ]

    demo_index = 0

    while True:
        try:
            demos[demo_index]()
            demo_index = (demo_index + 1) % len(demos)
            time.sleep(1)  # Brief pause between demos
        except KeyboardInterrupt:
            print("Demo stopped")
            break
        except Exception as e:
            print(f"Error in demo: {e}")
            time.sleep(2)


# Start the demo
run_demo()