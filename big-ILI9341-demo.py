# big-ILI9341-demo.py
"""
CircuitPython demo for ILI9341 320x240 display in landscape mode.
Optimized version with better resource management and reduced redundancy.
"""
import board
import busio
import time
import digitalio
import displayio
import pwmio
import terminalio
from adafruit_display_text import label
import adafruit_ili9341

# Import bitmap font support at startup to avoid delays
try:
    from adafruit_bitmap_font import bitmap_font

    BITMAP_FONT_AVAILABLE = True
    print("✅ Bitmap font support loaded")
except ImportError:
    BITMAP_FONT_AVAILABLE = False
    print("❌ Bitmap font support not available")

# --- Constants ---
DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240
DEMO_PAUSE = 1.0
FONT_PATHS = {
    "Collegiate-50": "/fonts/Collegiate-50.bdf",
    "helvB24": "/fonts/helvB24.bdf",
    "helvB18": "/fonts/helvB18.bdf",
    "helvB14": "/fonts/helvB14.bdf",
    "helvB12": "/fonts/helvB12.bdf",
    "helvB08": "/fonts/helvB08.bdf",
    "LeagueSpartan_Bold_16": "/fonts/LeagueSpartan_Bold_16.bdf",
    "forkawesome-42": "/fonts/forkawesome-42.pcf",
    "forkawesome-32": "/fonts/forkawesome-32.pcf",
    "forkawesome-24": "/fonts/forkawesome-24.pcf"
}

# Global font storage
FONTS = {}

# --- Display Setup ---
displayio.release_displays()

# SPI bus for display
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

# Initialize display in landscape mode
display = adafruit_ili9341.ILI9341(
    display_bus,
    width=DISPLAY_WIDTH,
    height=DISPLAY_HEIGHT,
    rotation=0,
    backlight_pin=None
)

print("✅ ILI9341 Display initialized (320x240 landscape)")


# --- Font Loading (Done Once) ---
def load_fonts():
    """Load all fonts once at startup"""
    if not BITMAP_FONT_AVAILABLE:
        print("❌ Skipping font loading - bitmap font support not available")
        return

    print("🔄 Loading all fonts (this may take a moment)...")
    start_time = time.monotonic()

    for font_name, font_path in FONT_PATHS.items():
        try:
            print(f"Loading {font_name}...")
            FONTS[font_name] = bitmap_font.load_font(font_path)
            print(f"✅ Loaded {font_name}")
        except Exception as e:
            print(f"❌ Could not load {font_name}: {e}")
            FONTS[font_name] = None

    end_time = time.monotonic()
    print(f"✅ Font loading complete ({end_time - start_time:.1f}s)")

    # Pre-warm the font fallback system by testing it
    print("🔄 Pre-warming font system...")
    for font_name in ["helvB24", "helvB18", "Collegiate-50"]:
        get_font_or_fallback(font_name)
    print("✅ Font system ready")

    # Preload glyphs used in the demo to avoid runtime delay
    preload_chars = "Font ShowcaseTerminalx0123456789ColorsSPIhelvB"
    for font in FONTS.values():
        if font is not None and hasattr(font, "load_glyphs"):
            try:
                font.load_glyphs(preload_chars)
            except Exception as e:
                print(f"⚠️ Could not preload glyphs for font: {e}")


# --- Helper Functions ---
def create_gradient_background(group, color_start, color_end):
    """Create a vertical gradient background"""
    for y in range(DISPLAY_HEIGHT):
        strip_bitmap = displayio.Bitmap(DISPLAY_WIDTH, 1, 1)
        strip_palette = displayio.Palette(1)

        # Linear interpolation between colors
        ratio = y / DISPLAY_HEIGHT
        r_start = (color_start >> 16) & 0xFF
        g_start = (color_start >> 8) & 0xFF
        b_start = color_start & 0xFF

        r_end = (color_end >> 16) & 0xFF
        g_end = (color_end >> 8) & 0xFF
        b_end = color_end & 0xFF

        r = int(r_start + (r_end - r_start) * ratio)
        g = int(g_start + (g_end - g_start) * ratio)
        b = int(b_start + (b_end - b_start) * ratio)

        color = (r << 16) | (g << 8) | b
        strip_palette[0] = color
        strip = displayio.TileGrid(strip_bitmap, pixel_shader=strip_palette, x=0, y=y)
        group.append(strip)


def create_solid_background(group, color):
    """Create a solid color background"""
    bg_bitmap = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, 1)
    bg_palette = displayio.Palette(1)
    bg_palette[0] = color
    bg = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)
    group.append(bg)


def get_font_or_fallback(font_name, scale=1):
    """Get a font or return terminal font with scaling"""
    if FONTS.get(font_name):
        return FONTS[font_name], 1
    else:
        return terminalio.FONT, scale


def cleanup_display():
    """Clean up display resources between demos"""
    # Clear the display
    display.root_group = displayio.Group()


# --- Demo Functions ---
def demo_splash_screen():
    """Display specification splash screen"""
    print("🚀 Splash Screen")

    group = displayio.Group()
    create_gradient_background(group, 0x000000, 0x404040)  # Black to gray

    # Title lines with fallback handling
    font_large, scale_large = get_font_or_fallback("Collegiate-50", 3)
    font_medium, scale_medium = get_font_or_fallback("helvB18", 2)

    title_line1 = label.Label(
        font_large, text="ILI9341", color=0xFFFF00, scale=scale_large,
        anchor_point=(0.5, 0.5), anchored_position=(160, 40)
    )
    group.append(title_line1)

    title_line2 = label.Label(
        font_large, text="2.2\" Display", color=0xFFFF00, scale=scale_large,
        anchor_point=(0.5, 0.5), anchored_position=(160, 90)
    )
    group.append(title_line2)

    resolution = label.Label(
        font_medium, text="320 x 240 Resolution", color=0x00FFFF, scale=scale_medium,
        anchor_point=(0.5, 0.5), anchored_position=(160, 140)
    )
    group.append(resolution)

    specs = label.Label(
        font_medium, text="65K Colors & SPI Interface", color=0xFFFFFF, scale=scale_medium,
        anchor_point=(0.5, 0.5), anchored_position=(160, 180)
    )
    group.append(specs)

    platform = label.Label(
        font_medium, text="CircuitPython", color=0xFFFFFF, scale=scale_medium,
        anchor_point=(0.5, 0.5), anchored_position=(160, 210)
    )
    group.append(platform)

    display.root_group = group
    time.sleep(3)


def demo_fonts_and_text():
    """Demonstrate different font sizes and text styles"""
    print("📝 Font Demo")

    print("Creating Group")
    group = displayio.Group()

    print("GRADIENT")
    create_gradient_background(group, 0x000020, 0x000060)  # Dark blue gradient

    y_pos = 10

    print("running get_font_or_fallback")
    # Title
    font_title, scale_title = get_font_or_fallback("helvB24", 3)

    print("Setting up labels")
    title = label.Label(
        font_title, text="Font Showcase", color=0xFFFF00, scale=scale_title,
        anchor_point=(0.5, 0.0), anchored_position=(160, y_pos)
    )

    print("appending title")
    group.append(title)
    y_pos += 35


    print("FONT_DEMOS created")
    # Font demonstrations
    font_demos = [
        ("Terminal Font", terminalio.FONT, 1, 0x00FFFF),
        ("Terminal x2", terminalio.FONT, 2, 0x00AAFF),
        ("helvB18", "helvB18", 1, 0xFFAAAA),
        ("helvB14", "helvB14", 1, 0xFF8888),
        ("helvB12", "helvB12", 1, 0xFFAAAA),
    ]

    print("for loop going through font_demos")
    for demo_text, font_key, scale, color in font_demos:
        if isinstance(font_key, str):
            font, actual_scale = get_font_or_fallback(font_key, scale)
        else:
            font, actual_scale = font_key, scale

        demo_label = label.Label(
            font, text=demo_text, color=color, scale=actual_scale,
            x=10, y=y_pos
        )

        print("apending demo_label")
        group.append(demo_label)
        y_pos += 22

    # Tech specs at bottom

    print("setting up scale_bottom from get_font_or_fallback")
    font_bottom, scale_bottom = get_font_or_fallback("helvB12", 1)
    bottom_info = label.Label(
        font_bottom, text="320x240 • 65K Colors • SPI", color=0x00FF00, scale=scale_bottom,
        anchor_point=(0.5, 0.0), anchored_position=(160, 215)
    )

    print("appending group bottom_info")
    group.append(bottom_info)


    print("displaying root_group")
    display.root_group = group
    time.sleep(4)


def demo_color_bars():
    """Display color bars to show color capability"""
    print("🌈 Color Test Pattern")

    group = displayio.Group()

    # Rainbow color palette
    colors = [
        0xFF0000, 0xFF8000, 0xFFFF00, 0x80FF00, 0x00FF00, 0x00FF80,
        0x00FFFF, 0x0080FF, 0x0000FF, 0x8000FF, 0xFF00FF, 0xFF0080
    ]

    bar_width = DISPLAY_WIDTH // len(colors)

    for i, color in enumerate(colors):
        bar_bitmap = displayio.Bitmap(bar_width, 180, 1)
        bar_palette = displayio.Palette(1)
        bar_palette[0] = color
        bar = displayio.TileGrid(bar_bitmap, pixel_shader=bar_palette,
                                 x=i * bar_width, y=30)
        group.append(bar)

    # Title and description
    title = label.Label(
        terminalio.FONT, text="65,536 Color Test Pattern", color=0xFFFFFF, scale=2,
        anchor_point=(0.5, 0.0), anchored_position=(160, 5)
    )
    group.append(title)

    description = label.Label(
        terminalio.FONT, text="Smooth gradients and vibrant colors", color=0xFFFFFF,
        anchor_point=(0.5, 0.0), anchored_position=(160, 220)
    )
    group.append(description)

    display.root_group = group
    time.sleep(4)


def demo_pong_animation():
    """Pong-style game with AI paddles"""
    print("🏓 Pong Animation Demo")

    # Game state - faster gameplay
    ball_x, ball_y = 160.0, 120.0
    ball_vel_x, ball_vel_y = 6.0, 4.5  # Faster ball
    ball_size = 8

    paddle_width, paddle_height = 8, 40
    paddle_speed = 6.0  # Faster paddle movement
    left_paddle_y = 100.0
    right_paddle_y = 100.0

    score_left, score_right = 0, 0

    for frame in range(50):  # ~0.85 seconds at ~60fps - half again
        group = displayio.Group()
        create_solid_background(group, 0x000000)  # Classic black

        # Center dashed line
        for i in range(0, DISPLAY_HEIGHT, 30):
            line_bitmap = displayio.Bitmap(2, 15, 1)
            line_palette = displayio.Palette(1)
            line_palette[0] = 0x666666
            line = displayio.TileGrid(line_bitmap, pixel_shader=line_palette,
                                      x=159, y=i)
            group.append(line)

        # Left paddle
        left_paddle_bitmap = displayio.Bitmap(paddle_width, paddle_height, 1)
        left_paddle_palette = displayio.Palette(1)
        left_paddle_palette[0] = 0xFFFFFF
        left_paddle = displayio.TileGrid(left_paddle_bitmap, pixel_shader=left_paddle_palette,
                                         x=15, y=int(left_paddle_y))
        group.append(left_paddle)

        # Right paddle
        right_paddle_bitmap = displayio.Bitmap(paddle_width, paddle_height, 1)
        right_paddle_palette = displayio.Palette(1)
        right_paddle_palette[0] = 0xFFFFFF
        right_paddle = displayio.TileGrid(right_paddle_bitmap, pixel_shader=right_paddle_palette,
                                          x=297, y=int(right_paddle_y))
        group.append(right_paddle)

        # Ball
        ball_bitmap = displayio.Bitmap(ball_size, ball_size, 1)
        ball_palette = displayio.Palette(1)
        ball_palette[0] = 0xFFFF00  # Yellow ball
        ball = displayio.TileGrid(ball_bitmap, pixel_shader=ball_palette,
                                  x=int(ball_x), y=int(ball_y))
        group.append(ball)

        # Score
        score_text = label.Label(
            terminalio.FONT, text=f"{score_left}    PONG DEMO    {score_right}",
            color=0x00FF00, scale=1,
            anchor_point=(0.5, 0.0), anchored_position=(160, 10)
        )
        group.append(score_text)

        display.root_group = group

        # AI paddle movement - more responsive
        ball_center_y = ball_y + ball_size // 2

        # Left paddle AI - faster reaction
        if ball_vel_x < 0:  # Ball moving toward left paddle
            left_center = left_paddle_y + paddle_height // 2
            if ball_center_y > left_center + 3:  # Smaller dead zone
                left_paddle_y += paddle_speed
            elif ball_center_y < left_center - 3:
                left_paddle_y -= paddle_speed

        # Right paddle AI - faster reaction
        if ball_vel_x > 0:  # Ball moving toward right paddle
            right_center = right_paddle_y + paddle_height // 2
            if ball_center_y > right_center + 3:  # Smaller dead zone
                right_paddle_y += paddle_speed
            elif ball_center_y < right_center - 3:
                right_paddle_y -= paddle_speed

        # Keep paddles on screen
        left_paddle_y = max(0, min(DISPLAY_HEIGHT - paddle_height, left_paddle_y))
        right_paddle_y = max(0, min(DISPLAY_HEIGHT - paddle_height, right_paddle_y))

        # Ball collision with left paddle
        if (ball_vel_x < 0 and ball_x <= 23 and ball_x >= 15 and
                ball_y + ball_size >= left_paddle_y and
                ball_y <= left_paddle_y + paddle_height):
            ball_vel_x = abs(ball_vel_x) * 1.05  # Slight speed increase
            ball_x = 24
            # Add spin based on paddle hit position
            hit_ratio = (ball_center_y - left_paddle_y) / paddle_height
            ball_vel_y += (hit_ratio - 0.5) * 3

        # Ball collision with right paddle
        if (ball_vel_x > 0 and ball_x + ball_size >= 297 and ball_x + ball_size <= 305 and
                ball_y + ball_size >= right_paddle_y and
                ball_y <= right_paddle_y + paddle_height):
            ball_vel_x = -abs(ball_vel_x) * 1.05  # Slight speed increase
            ball_x = 296 - ball_size
            # Add spin based on paddle hit position
            hit_ratio = (ball_center_y - right_paddle_y) / paddle_height
            ball_vel_y += (hit_ratio - 0.5) * 3

        # Update ball position
        ball_x += ball_vel_x
        ball_y += ball_vel_y

        # Ball collision with top/bottom walls
        if ball_y <= 25 or ball_y >= DISPLAY_HEIGHT - ball_size:
            ball_vel_y = -ball_vel_y
            ball_y = max(25, min(DISPLAY_HEIGHT - ball_size, ball_y))

        # Limit ball velocity - higher limits for faster gameplay
        ball_vel_y = max(-8, min(8, ball_vel_y))

        # Scoring - faster ball reset
        if ball_x < 0:
            score_right += 1
            ball_x, ball_y = 160, 120
            ball_vel_x, ball_vel_y = 6.0, 4.5
        elif ball_x > DISPLAY_WIDTH:
            score_left += 1
            ball_x, ball_y = 160, 120
            ball_vel_x, ball_vel_y = -6.0, 4.5

        time.sleep(0.017)  # ~60fps for smoother, faster gameplay


def demo_image_display():
    """Display image or fallback message"""
    print("🖼️ Image Display Demo")

    try:
        campus_bitmap = displayio.OnDiskBitmap("/campus.bmp")
        group = displayio.Group()

        image_grid = displayio.TileGrid(
            campus_bitmap, pixel_shader=campus_bitmap.pixel_shader
        )
        group.append(image_grid)

        title = label.Label(
            terminalio.FONT, text="Campus Image Display", color=0xFFFFFF, scale=2,
            anchor_point=(0.5, 0.0), anchored_position=(160, 10)
        )
        group.append(title)

        display.root_group = group
        time.sleep(5)

    except Exception as e:
        print(f"❌ Could not load image: {e}")

        group = displayio.Group()
        create_gradient_background(group, 0x000080, 0xFF8000)  # Blue to orange

        message = label.Label(
            terminalio.FONT, text="Image Demo", color=0xFFFFFF, scale=3,
            anchor_point=(0.5, 0.5), anchored_position=(160, 80)
        )
        group.append(message)

        instruction = label.Label(
            terminalio.FONT, text="Place 320x240 BMP as /campus.bmp", color=0xFFFFFF,
            anchor_point=(0.5, 0.5), anchored_position=(160, 140)
        )
        group.append(instruction)

        display.root_group = group
        time.sleep(4)


# --- Main Demo Loop ---
def run_demo():
    """Run the complete demo sequence"""
    print("🚀 Starting ILI9341 Display Demo")

    # Show loading screen while fonts load - make it persistent
    loading_group = displayio.Group()
    create_solid_background(loading_group, 0x000040)  # Dark blue

    loading_text = label.Label(
        terminalio.FONT, text="Loading Fonts & Resources", color=0xFFFFFF, scale=2,
        anchor_point=(0.5, 0.5), anchored_position=(160, 100)
    )
    loading_group.append(loading_text)

    progress_text = label.Label(
        terminalio.FONT, text="Please wait...", color=0x00FFFF, scale=1,
        anchor_point=(0.5, 0.5), anchored_position=(160, 140)
    )
    loading_group.append(progress_text)

    display.root_group = loading_group
    time.sleep(0.5)  # Ensure loading screen is visible

    # Load fonts once at startup
    load_fonts()

    # Update loading screen to show completion
    progress_text.text = "Ready! Starting demos..."
    progress_text.color = 0x00FF00
    time.sleep(1)  # Let user see the completion message

    demos = [
        demo_splash_screen,
        demo_fonts_and_text,
        demo_color_bars,
        demo_pong_animation,
        demo_image_display
    ]

    demo_index = 0

    while True:
        try:
            # Don't cleanup before first demo to avoid clearing loading screen prematurely
            if demo_index > 0:
                cleanup_display()
            demos[demo_index]()
            demo_index = (demo_index + 1) % len(demos)
            time.sleep(DEMO_PAUSE)
        except KeyboardInterrupt:
            print("Demo stopped")
            break
        except Exception as e:
            print(f"Error in demo: {e}")
            cleanup_display()
            time.sleep(2)


# Start the demo
if __name__ == "__main__":
    run_demo()