# big-ILI9341-demo.py# code.py - ILI9341 Display CircuitPython Demo (Improved version)

import board
import busio
import time
import displayio
import pwmio
import terminalio
from adafruit_display_text import label  # Import bitmap font support
import adafruit_ili9341

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

# Color constants for readability
BLACK = 0x000000
WHITE = 0xFFFFFF
YELLOW = 0xFFFF00
CYAN = 0x00FFFF
GRAY = 0x404040
DARK_BLUE = 0x000040

FONT_PATHS = {
    "Collegiate-50": "/fonts/Collegiate-50.bdf",
    "helvB24": "/fonts/helvB24.bdf",
    "helvB18": "/fonts/helvB18.bdf",
    "helvB14": "/fonts/helvB14.bdf",
    "helvB12": "/fonts/helvB12.bdf",
    "LeagueSpartan_Bold_16": "/fonts/LeagueSpartan_Bold_16.bdf",
    "forkawesome-42": "/fonts/forkawesome-42.pcf",
    "forkawesome-32": "/fonts/forkawesome-32.pcf",
    "forkawesome-24": "/fonts/forkawesome-24.pcf"
}
FONTS = {}

# --- Display Setup ---
displayio.release_displays()
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP16)
tft_cs = board.GP20
tft_dc = board.GP21
tft_reset = board.GP15
backlight = pwmio.PWMOut(board.GP22, frequency=5000, duty_cycle=65535)

display_bus = displayio.FourWire(
    spi,
    command=tft_dc,
    chip_select=tft_cs,
    reset=tft_reset
)

display = adafruit_ili9341.ILI9341(
    display_bus,
    width=DISPLAY_WIDTH,
    height=DISPLAY_HEIGHT,
    rotation=0,
    backlight_pin=None
)
print("✅ ILI9341 Display initialized (320x240 landscape)")


# --- Font Loading ---
def load_fonts():
    """Load all fonts once at startup; called before any demo runs."""
    if not BITMAP_FONT_AVAILABLE:
        print("❌ Skipping font loading - bitmap font support not available.")
        return
    print("🔄 Loading all fonts (may take a moment)")
    start_time = time.monotonic()

    for font_name, font_path in FONT_PATHS.items():
        try:
            print(f"Loading {font_name} ...")
            FONTS[font_name] = bitmap_font.load_font(font_path)
            print(f"✅ Loaded {font_name}")
        except (OSError, ValueError) as e:
            print(f"❌ Could not load {font_name}: {e}")
            FONTS[font_name] = None
        except Exception as e:
            print(f"❌ Unknown error loading {font_name}: {e}")
            FONTS[font_name] = None

    print(f"✅ Font loading complete ({time.monotonic() - start_time:.1f}s)")
    print("🔄 Pre-warming font fallback system...")
    for font_name in ["helvB24", "helvB18", "helvB14", "helvB12", "Collegiate-50"]:
        get_font_or_fallback(font_name)

    # Pre-warm display system to avoid delays on first demo
    print("🔄 Pre-warming display system...")
    prewarm_start = time.monotonic()

    # Create the same type of gradient used in demo_fonts_and_text to trigger initialization
    temp_group = displayio.Group()
    create_font_demo_background(temp_group)
    # Don't display it, just create it to warm up the system
    del temp_group

    print(f"✅ Display system pre-warmed ({time.monotonic() - prewarm_start:.1f}s)")

    # Pre-warm label system - this is the key fix!
    print("🔄 Pre-warming label system...")
    label_start = time.monotonic()

    # Create dummy labels with different fonts to trigger label initialization
    test_labels = []

    # Test with custom fonts
    for font_name in ["helvB24", "helvB18", "helvB14", "helvB12", "Collegiate-50"]:
        if FONTS.get(font_name):
            test_label = label.Label(
                FONTS[font_name],
                text="Test",
                color=WHITE,
                x=0,
                y=20
            )
            test_labels.append(test_label)

    # Test with terminal font at different scales
    for scale in [1, 2, 3]:
        test_label = label.Label(
            terminalio.FONT,
            text="Test",
            color=WHITE,
            scale=scale,
            x=0,
            y=20
        )
        test_labels.append(test_label)

    # Test with anchor points (different code path)
    test_label = label.Label(
        terminalio.FONT,
        text="Test",
        color=WHITE,
        anchor_point=(0.5, 0.0),
        anchored_position=(160, 100)
    )
    test_labels.append(test_label)

    # Clean up the test labels
    del test_labels

    print(f"✅ Label system pre-warmed ({time.monotonic() - label_start:.1f}s)")
    print("✅ Font system ready")


# --- Helper Functions ---
def create_gradient_background(group, color_start, color_end):
    """Create a vertical gradient background."""
    for y in range(DISPLAY_HEIGHT):
        strip_bitmap = displayio.Bitmap(DISPLAY_WIDTH, 1, 1)
        strip_palette = displayio.Palette(1)
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


def create_font_demo_background(group):
    """Create the specific dark blue gradient used in font demo."""
    for y in range(240):
        strip_bitmap = displayio.Bitmap(320, 1, 1)
        strip_palette = displayio.Palette(1)
        # Dark blue gradient
        blue_val = 0x000020 + (y // 8)
        strip_palette[0] = blue_val
        strip = displayio.TileGrid(strip_bitmap, pixel_shader=strip_palette, x=0, y=y)
        group.append(strip)


def create_solid_background(group, color):
    """Create a solid color background."""
    bg_bitmap = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, 1)
    bg_palette = displayio.Palette(1)
    bg_palette[0] = color
    bg = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)
    group.append(bg)


def get_font_or_fallback(font_name, scale=1):
    """Fetch font from global cache or fall back to terminalio.FONT with scaling."""
    if FONTS.get(font_name):
        return FONTS[font_name], 1
    else:
        return terminalio.FONT, scale


def cleanup_display():
    """Quickly clear display for next demo."""
    display.root_group = displayio.Group()


# --- Demo Functions ---
def demo_splash_screen():
    """Spec splash screen."""
    print("🚀 Splash Screen")
    group = displayio.Group()
    create_gradient_background(group, BLACK, GRAY)
    font_large, scale_large = get_font_or_fallback("Collegiate-50", 3)
    font_medium, scale_medium = get_font_or_fallback("helvB18", 2)

    group.append(label.Label(
        font_large, text="ILI9341", color=YELLOW, scale=scale_large,
        anchor_point=(0.5, 0.5), anchored_position=(160, 40)
    ))
    group.append(label.Label(
        font_large, text="2.2\" Display", color=YELLOW, scale=scale_large,
        anchor_point=(0.5, 0.5), anchored_position=(160, 90)
    ))
    group.append(label.Label(
        font_medium, text="320 x 240 Resolution", color=CYAN, scale=scale_medium,
        anchor_point=(0.5, 0.5), anchored_position=(160, 140)
    ))
    group.append(label.Label(
        font_medium, text="65K Colors & SPI Interface", color=WHITE, scale=scale_medium,
        anchor_point=(0.5, 0.5), anchored_position=(160, 180)
    ))
    group.append(label.Label(
        font_medium, text="CircuitPython", color=WHITE, scale=scale_medium,
        anchor_point=(0.5, 0.5), anchored_position=(160, 210)
    ))
    display.root_group = group
    time.sleep(3)


def demo_fonts_and_text():
    """Demonstrate different font sizes and text styles"""
    print("📝 Font Demo")
    group = displayio.Group()

    # Create the dark blue gradient background (now pre-warmed)
    print("creating font demo background group")
    create_font_demo_background(group)

    y_pos = 10

    # Title using largest available font
    print("if FONTS[helvB24]:")
    title = label.Label(
        FONTS["helvB24"],
        text="Font Showcase",
        color=0xFFFF00,
        anchor_point=(0.5, 0.0),
        anchored_position=(160, y_pos)
    )
    y_pos += 35
    group.append(title)
    display.root_group = group

    # Built-in terminal font demonstration
    terminal_demo = label.Label(
        terminalio.FONT,
        text="Built-in Terminal Font",
        color=0x00FFFF,
        scale=1,
        x=10,
        y=y_pos
    )
    group.append(terminal_demo)
    display.root_group = group
    y_pos += 18

    # Terminal font scaled up
    print("terminal_scaled = label.Label(")
    terminal_scaled = label.Label(
        terminalio.FONT,
        text="Terminal x2 Scale",
        color=0x00FFFF,
        scale=2,
        x=10,
        y=y_pos
    )
    print("group.append(terminal_scaled)")
    group.append(terminal_scaled)
    display.root_group = group
    y_pos += 28

    # helvB24
    print("helv24_label = label.Label(")
    helv24_label = label.Label(
        FONTS["helvB24"],
        text="helvB24",
        color=0xFFFFFF,
        x=10,
        y=y_pos
    )
    group.append(helv24_label)
    display.root_group = group
    y_pos += 30

    # Custom font demonstrations with better spacing
    font_demos = [
        ("helvB18", "helvB18", 0xFFAAAA),
        ("helvB14", "helvB14", 0xFF8888),
        ("Collegiate-50", "Collegiate-50", 0x88FF88),
    ]

    print("About to enumerate font_demos")
    for i, (font_key, demo_text, color) in enumerate(font_demos):
        # Add extra spacing before helvB14 to separate from helvB18
        if font_key == "helvB14":
            y_pos += 5

        # Nudge Collegiate down by 3 pixels
        label_y = y_pos + 3 if font_key == "Collegiate-50" else y_pos

        font_label = label.Label(
            FONTS[font_key],
            text=demo_text,
            color=color,
            x=10,
            y=label_y
        )
        group.append(font_label)
        display.root_group = group
        # Give more space for the large Collegiate font
        spacing = 50 if font_key == "Collegiate-50" else 22
        y_pos += spacing

    # Bottom technical info
    bottom_info = label.Label(
        FONTS["helvB12"],
        text="320x240 • 65K Colors • SPI",
        color=0x00FF00,
        anchor_point=(0.5, 0.0),
        anchored_position=(160, 215)
    )
    group.append(bottom_info)

    print("about to display.root_group")
    display.root_group = group
    print("and now sleeping for 4")
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


def demo_forkawesome_icons():
    """Showcase ForkAwesome icons (uses preloaded FONTS)."""
    print("🎨 ForkAwesome Icons Demo")
    font_sizes = ["42", "32", "24"]
    forkawesome_font = None
    for size in font_sizes:
        font_obj = FONTS.get(f"forkawesome-{size}")
        if font_obj:
            forkawesome_font = font_obj
            break
    if not forkawesome_font:
        print("❌ No ForkAwesome fonts available, skipping icon demo")
        return

    group = displayio.Group()
    create_solid_background(group, WHITE)
    group.append(label.Label(
        terminalio.FONT, text="ForkAwesome Icon Library", color=0xFF1493, scale=2,
        anchor_point=(0.5, 0.0), anchored_position=(160, 0)
    ))

    icons_to_show = [
        ("\uf193", "wheelchair", 0xFF1493),
        ("\uf164", "thumbs_up", 0x32CD32),
        ("\uf062", "arrow_up", 0x4169E1),
        ("\uf063", "arrow_down", 0x4169E1),
        ("\uf060", "arrow_left", 0x4169E1),
        ("\uf061", "arrow_right", 0x4169E1),
        ("\uf004", "heart", 0xFF0000),
        ("\uf35f", "bunny", 0xFF69B4),
        ("\uf1b9", "car", 0xFF0000),
        ("\uf118", "smile", 0x9932CC),
        ("\uf005", "star", 0xFFD700),
        ("\uf329", "sun", 0xFF8C00),
        ("\uf0c2", "cloud", 0x4682B4),
        ("\uf017", "clock", 0x8B4513),
        ("\uf001", "music", 0xFF1493),
        ("\uf06c", "leaf", 0x228B22)
    ]
    x_start = 20
    y_start = 48
    icon_spacing_x = 75
    icon_spacing_y = 47
    icons_per_row = 4
    row = 0
    col = 0

    for icon_char, icon_name, color in icons_to_show:
        x_pos = x_start + (col * icon_spacing_x)
        y_pos = y_start + (row * icon_spacing_y)
        if row > 0:
            y_pos += 6 * row
        try:
            group.append(label.Label(
                forkawesome_font, text=icon_char, color=color,
                x=x_pos, y=y_pos
            ))
        except Exception as e:
            print(f"❌ Failed to display {icon_name}: {e}")
        col += 1
        if col >= icons_per_row:
            col = 0
            row += 1

    display.root_group = group
    time.sleep(4)


def demo_turtle_graphics():
    """Optional turtle graphics; falls back gracefully if lib missing."""
    print("🐢 Turtle Graphics Demo")
    try:
        from adafruit_turtle import turtle, Color
    except ImportError:
        print("❌ adafruit_turtle not available, skipping")
        group = displayio.Group()
        create_solid_background(group, BLACK)
        group.append(label.Label(
            terminalio.FONT, text="Turtle Graphics Not Available", color=YELLOW, scale=2,
            anchor_point=(0.5, 0.5), anchored_position=(160, 100)
        ))
        group.append(label.Label(
            terminalio.FONT, text="Install adafruit_turtle library", color=WHITE, scale=1,
            anchor_point=(0.5, 0.5), anchored_position=(160, 130)
        ))
        display.root_group = group
        time.sleep(4)
        return
    try:
        my_turtle = turtle(display)
        my_turtle.bgcolor(Color.BLACK)
        my_turtle.speed(0)
        my_turtle.pensize(1)
        colors = [Color.RED, Color.ORANGE, Color.YELLOW, Color.GREEN,
                  Color.BLUE, Color.PURPLE, Color.PINK]
        patterns = [
            (0, 0, 50),
            (-80, -50, 30),
            (80, 50, 40),
            (0, -80, 25),
        ]
        for pattern_x, pattern_y, pattern_size in patterns:
            my_turtle.penup()
            my_turtle.goto(pattern_x, pattern_y)
            my_turtle.pendown()
            for i in range(21):
                my_turtle.pencolor(colors[i % len(colors)])
                for _ in range(6):
                    my_turtle.forward(pattern_size)
                    my_turtle.right(61)
                my_turtle.right(11.1111)
            time.sleep(0.5)
        time.sleep(2)
    except Exception as e:
        print(f"❌ Turtle graphics error: {e}")
        group = displayio.Group()
        create_solid_background(group, BLACK)
        group.append(label.Label(
            terminalio.FONT, text="Turtle Graphics Error", color=0xFF0000, scale=2,
            anchor_point=(0.5, 0.5), anchored_position=(160, 100)
        ))
        group.append(label.Label(
            terminalio.FONT, text="Skipping turtle demo", color=WHITE, scale=1,
            anchor_point=(0.5, 0.5), anchored_position=(160, 130)
        ))
        display.root_group = group
        time.sleep(1)


def demo_pong_animation():
    """Simple AI Pong animation."""
    print("🏓 Pong Animation Demo")
    ball_x, ball_y = 160.0, 120.0
    ball_vel_x, ball_vel_y = 6.0, 4.5
    ball_size = 8
    paddle_width, paddle_height = 8, 40
    paddle_speed = 6.0
    left_paddle_y = 100.0
    right_paddle_y = 100.0
    score_left, score_right = 0, 0
    for frame in range(50):
        group = displayio.Group()
        create_solid_background(group, BLACK)
        for i in range(0, DISPLAY_HEIGHT, 30):
            line_bitmap = displayio.Bitmap(2, 15, 1)
            line_palette = displayio.Palette(1)
            line_palette[0] = 0x666666
            line = displayio.TileGrid(line_bitmap, pixel_shader=line_palette, x=159, y=i)
            group.append(line)
        left_paddle_bitmap = displayio.Bitmap(paddle_width, paddle_height, 1)
        left_paddle_palette = displayio.Palette(1)
        left_paddle_palette[0] = WHITE
        group.append(displayio.TileGrid(left_paddle_bitmap, pixel_shader=left_paddle_palette,
                                        x=15, y=int(left_paddle_y)))
        right_paddle_bitmap = displayio.Bitmap(paddle_width, paddle_height, 1)
        right_paddle_palette = displayio.Palette(1)
        right_paddle_palette[0] = WHITE
        group.append(displayio.TileGrid(right_paddle_bitmap, pixel_shader=right_paddle_palette,
                                        x=297, y=int(right_paddle_y)))
        ball_bitmap = displayio.Bitmap(ball_size, ball_size, 1)
        ball_palette = displayio.Palette(1)
        ball_palette[0] = YELLOW
        group.append(displayio.TileGrid(ball_bitmap, pixel_shader=ball_palette,
                                        x=int(ball_x), y=int(ball_y)))
        group.append(label.Label(
            terminalio.FONT, text=f"{score_left}    PONG DEMO    {score_right}",
            color=0x00FF00, scale=1,
            anchor_point=(0.5, 0.0), anchored_position=(160, 10)
        ))
        display.root_group = group

        # Paddle AI
        ball_center_y = ball_y + ball_size // 2
        if ball_vel_x < 0:
            left_center = left_paddle_y + paddle_height // 2
            if ball_center_y > left_center + 3:
                left_paddle_y += paddle_speed
            elif ball_center_y < left_center - 3:
                left_paddle_y -= paddle_speed
        if ball_vel_x > 0:
            right_center = right_paddle_y + paddle_height // 2
            if ball_center_y > right_center + 3:
                right_paddle_y += paddle_speed
            elif ball_center_y < right_center - 3:
                right_paddle_y -= paddle_speed
        left_paddle_y = max(0, min(DISPLAY_HEIGHT - paddle_height, left_paddle_y))
        right_paddle_y = max(0, min(DISPLAY_HEIGHT - paddle_height, right_paddle_y))

        # Ball collision
        if (ball_vel_x < 0 and ball_x <= 23 and ball_x >= 15 and
                ball_y + ball_size >= left_paddle_y and
                ball_y <= left_paddle_y + paddle_height):
            ball_vel_x = abs(ball_vel_x) * 1.05
            ball_x = 24
            hit_ratio = (ball_center_y - left_paddle_y) / paddle_height
            ball_vel_y += (hit_ratio - 0.5) * 3
        if (ball_vel_x > 0 and ball_x + ball_size >= 297 and ball_x + ball_size <= 305 and
                ball_y + ball_size >= right_paddle_y and
                ball_y <= right_paddle_y + paddle_height):
            ball_vel_x = -abs(ball_vel_x) * 1.05
            ball_x = 296 - ball_size
            hit_ratio = (ball_center_y - right_paddle_y) / paddle_height
            ball_vel_y += (hit_ratio - 0.5) * 3
        ball_x += ball_vel_x
        ball_y += ball_vel_y
        if ball_y <= 25 or ball_y >= DISPLAY_HEIGHT - ball_size:
            ball_vel_y = -ball_vel_y
            ball_y = max(25, min(DISPLAY_HEIGHT - ball_size, ball_y))
        ball_vel_y = max(-8, min(8, ball_vel_y))
        if ball_x < 0:
            score_right += 1
            ball_x, ball_y = 160, 120
            ball_vel_x, ball_vel_y = 6.0, 4.5
        elif ball_x > DISPLAY_WIDTH:
            score_left += 1
            ball_x, ball_y = 160, 120
            ball_vel_x, ball_vel_y = -6.0, 4.5
        time.sleep(0.017)  # ~60fps


def demo_image_display():
    """Display BMP or a help message if not found."""
    print("🖼️ Image Display Demo")
    try:
        campus_bitmap = displayio.OnDiskBitmap("/campus.bmp")
        group = displayio.Group()
        group.append(displayio.TileGrid(campus_bitmap, pixel_shader=campus_bitmap.pixel_shader))
        group.append(label.Label(
            terminalio.FONT, text="Campus Image Display", color=WHITE, scale=2,
            anchor_point=(0.5, 0.0), anchored_position=(160, 10)
        ))
        display.root_group = group
        time.sleep(5)
    except (OSError, ValueError) as e:
        print(f"❌ Could not load image: {e}")
        group = displayio.Group()
        create_gradient_background(group, 0x000080, 0xFF8000)
        group.append(label.Label(
            terminalio.FONT, text="Image Demo", color=WHITE, scale=3,
            anchor_point=(0.5, 0.5), anchored_position=(160, 80)
        ))
        group.append(label.Label(
            terminalio.FONT, text="Place 320x240 BMP as /campus.bmp", color=WHITE,
            anchor_point=(0.5, 0.5), anchored_position=(160, 140)
        ))
        display.root_group = group
        time.sleep(4)


# --- Main Demo Loop ---
def run_demo():
    print("🚀 Starting ILI9341 Display Demo")

    # Persistent loading screen while fonts/resources load
    loading_group = displayio.Group()
    create_solid_background(loading_group, DARK_BLUE)
    loading_group.append(label.Label(
        terminalio.FONT, text="Loading Fonts & Resources", color=WHITE, scale=2,
        anchor_point=(0.5, 0.5), anchored_position=(160, 100)
    ))
    progress_text = label.Label(
        terminalio.FONT, text="Please wait", color=CYAN, scale=1,
        anchor_point=(0.5, 0.5), anchored_position=(160, 140)
    )
    loading_group.append(progress_text)
    display.root_group = loading_group
    time.sleep(0.5)
    load_fonts()
    progress_text.text = "Ready! Starting demos"
    progress_text.color = 0x00FF00
    time.sleep(1)

    demos = [
        demo_splash_screen,
        demo_fonts_and_text,
        demo_forkawesome_icons,
        demo_color_bars,
        demo_turtle_graphics,
        demo_pong_animation,
        demo_image_display
    ]
    demo_index = 0
    while True:
        try:
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


if __name__ == "__main__":
    run_demo()
