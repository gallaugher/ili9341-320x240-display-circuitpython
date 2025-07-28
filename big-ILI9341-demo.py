# big-ILI9341-demo.py# code.py
"""
CircuitPython demo for ILI9341 320x240 display in landscape mode.
Demonstrates fonts, icons, colors, turtle graphics, game-style animation, and image display.
"""
import board
import busio
import time
import displayio, fourwire
import pwmio
import terminalio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import adafruit_ili9341

# --- Display Setup ---
displayio.release_displays()

spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP16)
display_bus = fourwire.FourWire(spi, command=board.GP21, chip_select=board.GP20, reset=board.GP15)
backlight = pwmio.PWMOut(board.GP22, frequency=5000, duty_cycle=65535)

display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240, rotation=0, backlight_pin=None)
print("✅ ILI9341 Display initialized (320x240 landscape)")


# --- Helper Functions ---
def create_gradient(group, start_color, end_color, height=240):
    """Create a vertical gradient background"""
    for y in range(height):
        strip_bitmap = displayio.Bitmap(320, 1, 1)
        strip_palette = displayio.Palette(1)
        ratio = y / height
        r_start, g_start, b_start = (start_color >> 16) & 0xFF, (start_color >> 8) & 0xFF, start_color & 0xFF
        r_end, g_end, b_end = (end_color >> 16) & 0xFF, (end_color >> 8) & 0xFF, end_color & 0xFF
        r = int(r_start + (r_end - r_start) * ratio)
        g = int(g_start + (g_end - g_start) * ratio)
        b = int(b_start + (b_end - b_start) * ratio)
        strip_palette[0] = (r << 16) | (g << 8) | b
        group.append(displayio.TileGrid(strip_bitmap, pixel_shader=strip_palette, x=0, y=y))


def load_fonts(font_list):
    """Load fonts with simple error handling"""
    fonts = {}
    for font_name, font_path in font_list:
        try:
            fonts[font_name] = bitmap_font.load_font(font_path)
            print(f"✅ Loaded {font_name}")
        except:
            print(f"❌ Could not load {font_name}")
            fonts[font_name] = None
    return fonts


# --- Demo Functions ---
def demo_splash_screen():
    """Display specification splash screen"""
    print("🚀 Splash Screen")
    group = displayio.Group()

    # Black to gray gradient
    for y in range(240):
        strip_bitmap = displayio.Bitmap(320, 1, 1)
        strip_palette = displayio.Palette(1)
        gray_val = min(64, y // 4)
        color = gray_val | (gray_val << 8) | (gray_val << 16)
        strip_palette[0] = color
        group.append(displayio.TileGrid(strip_bitmap, pixel_shader=strip_palette, x=0, y=y))

    fonts = load_fonts([("Collegiate-50", "/fonts/Collegiate-50.bdf"), ("helvB18", "/fonts/helvB18.bdf")])

    # Title lines
    group.append(label.Label(fonts["Collegiate-50"] or terminalio.FONT, text="ILI9341", color=0xFFFF00,
                             scale=1 if fonts["Collegiate-50"] else 3, anchor_point=(0.5, 0.5),
                             anchored_position=(160, 40)))
    group.append(label.Label(fonts["Collegiate-50"] or terminalio.FONT, text="2.2\" Display", color=0xFFFF00,
                             scale=1 if fonts["Collegiate-50"] else 3, anchor_point=(0.5, 0.5),
                             anchored_position=(160, 90)))
    group.append(label.Label(fonts["helvB18"] or terminalio.FONT, text="320 x 240 Resolution", color=0x00FFFF,
                             scale=1 if fonts["helvB18"] else 2, anchor_point=(0.5, 0.5), anchored_position=(160, 140)))
    group.append(label.Label(fonts["helvB18"] or terminalio.FONT, text="65K Colors & SPI Interface", color=0xFFFFFF,
                             scale=1 if fonts["helvB18"] else 1, anchor_point=(0.5, 0.5), anchored_position=(160, 180)))
    group.append(label.Label(fonts["helvB18"] or terminalio.FONT, text="CircuitPython", color=0xFFFFFF,
                             scale=1 if fonts["helvB18"] else 1, anchor_point=(0.5, 0.5), anchored_position=(160, 210)))

    display.root_group = group
    time.sleep(1)


def demo_fonts_and_text():
    """Demonstrate different font sizes and text styles"""
    print("📝 Font Demo")
    group = displayio.Group()

    # Dark blue gradient background
    for y in range(240):
        strip_bitmap = displayio.Bitmap(320, 1, 1)
        strip_palette = displayio.Palette(1)
        strip_palette[0] = 0x000020 + (y // 8)
        group.append(displayio.TileGrid(strip_bitmap, pixel_shader=strip_palette, x=0, y=y))

    fonts = load_fonts([
        ("helvB24", "/fonts/helvB24.bdf"), ("Collegiate-50", "/fonts/Collegiate-50.bdf"),
        ("helvB18", "/fonts/helvB18.bdf"), ("helvB14", "/fonts/helvB14.bdf"),
        ("helvB12", "/fonts/helvB12.bdf"), ("helvB08", "/fonts/helvB08.bdf")
    ])

    y_pos = 10

    # Title
    group.append(label.Label(fonts["helvB24"] or terminalio.FONT, text="Font Showcase", color=0xFFFF00,
                             scale=1 if fonts["helvB24"] else 3, anchor_point=(0.5, 0.0),
                             anchored_position=(160, y_pos)))
    y_pos += 35 if fonts["helvB24"] else 30

    # Terminal font examples
    group.append(label.Label(terminalio.FONT, text="Built-in Terminal Font", color=0x00FFFF, scale=1, x=10, y=y_pos))
    y_pos += 18
    group.append(label.Label(terminalio.FONT, text="Terminal x2 Scale", color=0x00FFFF, scale=2, x=10, y=y_pos))
    y_pos += 28

    # Custom fonts
    if fonts["helvB24"]:
        group.append(label.Label(fonts["helvB24"], text="helvB24", color=0xFFFFFF, x=10, y=y_pos))
        y_pos += 30

    font_demos = [("helvB18", 0xFFAAAA), ("helvB14", 0xFF8888), ("Collegiate-50", 0x88FF88), ("helvB12", 0xFFAAAA),
                  ("helvB08", 0x8888FF)]

    for font_key, color in font_demos:
        if font_key == "helvB14": y_pos += 5
        if fonts[font_key] and y_pos < 180:
            label_y = y_pos + 3 if font_key == "Collegiate-50" else y_pos
            group.append(label.Label(fonts[font_key], text=font_key, color=color, x=10, y=label_y))
            y_pos += 50 if font_key == "Collegiate-50" else 22

    # Bottom info
    if fonts["helvB12"]:
        group.append(label.Label(fonts["helvB12"], text="320x240 • 65K Colors • SPI", color=0x00FF00,
                                 anchor_point=(0.5, 0.0), anchored_position=(160, 215)))

    display.root_group = group
    time.sleep(4)


def demo_forkawesome_icons():
    """ForkAwesome Icons showcase"""
    print("🎨 ForkAwesome Icons Demo")

    # Load ForkAwesome fonts
    forkawesome_fonts = {}
    for size in ["42", "32", "24"]:
        try:
            forkawesome_fonts[size] = bitmap_font.load_font(f"/fonts/forkawesome-{size}.pcf")
            print(f"✅ Loaded ForkAwesome-{size}")
        except:
            forkawesome_fonts[size] = None

    # Find the largest available font
    icon_font = None
    for size in ["42", "32", "24"]:
        if forkawesome_fonts[size]:
            icon_font = forkawesome_fonts[size]
            break

    if not icon_font:
        print("❌ No ForkAwesome fonts available, skipping")
        return

    group = displayio.Group()

    # White background
    bg_bitmap = displayio.Bitmap(320, 240, 1)
    bg_palette = displayio.Palette(1)
    bg_palette[0] = 0xFFFFFF
    group.append(displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette))

    group.append(label.Label(terminalio.FONT, text="ForkAwesome Icon Library", color=0xFF1493, scale=2,
                             anchor_point=(0.5, 0.0), anchored_position=(160, 0)))

    icons = [
        ("\uf193", 0xFF1493), ("\uf164", 0x32CD32), ("\uf062", 0x4169E1), ("\uf063", 0x4169E1),
        ("\uf060", 0x4169E1), ("\uf061", 0x4169E1), ("\uf004", 0xFF0000), ("\uf35f", 0xFF69B4),
        ("\uf1b9", 0xFF0000), ("\uf118", 0x9932CC), ("\uf005", 0xFFD700), ("\uf329", 0xFF8C00),
        ("\uf0c2", 0x4682B4), ("\uf017", 0x8B4513), ("\uf001", 0xFF1493), ("\uf06c", 0x228B22)
    ]

    for i, (icon_char, color) in enumerate(icons):
        row, col = i // 4, i % 4
        x_pos = 20 + (col * 75)
        y_pos = 48 + (row * 47) + (6 * row if row > 0 else 0)
        group.append(label.Label(icon_font, text=icon_char, color=color, x=x_pos, y=y_pos))

    display.root_group = group
    time.sleep(4)


def demo_color_bars():
    """Display color bars"""
    print("🌈 Color Test Pattern")
    group = displayio.Group()

    colors = [0xFF0000, 0xFF8000, 0xFFFF00, 0x80FF00, 0x00FF00, 0x00FF80,
              0x00FFFF, 0x0080FF, 0x0000FF, 0x8000FF, 0xFF00FF, 0xFF0080]
    bar_width = 320 // len(colors)

    for i, color in enumerate(colors):
        bar_bitmap = displayio.Bitmap(bar_width, 180, 1)
        bar_palette = displayio.Palette(1)
        bar_palette[0] = color
        group.append(displayio.TileGrid(bar_bitmap, pixel_shader=bar_palette, x=i * bar_width, y=30))

    group.append(label.Label(terminalio.FONT, text="65,536 Color Test Pattern", color=0xFFFFFF, scale=2,
                             anchor_point=(0.5, 0.0), anchored_position=(160, 5)))
    group.append(label.Label(terminalio.FONT, text="Smooth gradients and vibrant colors", color=0xFFFFFF, scale=1,
                             anchor_point=(0.5, 0.0), anchored_position=(160, 220)))

    display.root_group = group
    time.sleep(4)


def demo_turtle_graphics():
    """Turtle graphics demo"""
    print("🐢 Turtle Graphics Demo")

    try:
        from adafruit_turtle import turtle, Color

        my_turtle = turtle(display)
        my_turtle.bgcolor(Color.BLACK)
        my_turtle.speed(0)
        my_turtle.pensize(1)
 
        colors = [Color.RED, Color.ORANGE, Color.YELLOW, Color.GREEN, Color.BLUE, Color.PURPLE, Color.PINK]
        patterns = [(0, 0, 50), (-80, -50, 30), (80, 50, 40), (0, -80, 25)]

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
        # time.sleep(2)

    except ImportError:
        group = displayio.Group()
        bg_bitmap = displayio.Bitmap(320, 240, 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = 0x000000
        group.append(displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette))
        group.append(label.Label(terminalio.FONT, text="Turtle Graphics Not Available", color=0xFFFF00, scale=2,
                                 anchor_point=(0.5, 0.5), anchored_position=(160, 100)))
        group.append(label.Label(terminalio.FONT, text="Install adafruit_turtle library", color=0xFFFFFF, scale=1,
                                 anchor_point=(0.5, 0.5), anchored_position=(160, 130)))
        display.root_group = group
        time.sleep(2)


def demo_pong_game():
    """Classic Pong game demo"""
    print("🏓 Pong Game Demo")

    ball_x, ball_y = 160.0, 120.0
    ball_vel_x, ball_vel_y = 5.0, 4.0
    ball_size = 8
    paddle_width, paddle_height = 8, 40
    paddle_speed = 5.0
    left_paddle_y, right_paddle_y = 100.0, 100.0
    score_left, score_right = 0, 0

    for frame in range(80):
        group = displayio.Group()

        # Black background
        bg_bitmap = displayio.Bitmap(320, 240, 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = 0x000000
        group.append(displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette))

        # Center line
        for i in range(0, 240, 40):
            line_bitmap = displayio.Bitmap(2, 20, 1)
            line_palette = displayio.Palette(1)
            line_palette[0] = 0x888888
            group.append(displayio.TileGrid(line_bitmap, pixel_shader=line_palette, x=159, y=i))

        # Paddles
        left_paddle_bitmap = displayio.Bitmap(paddle_width, paddle_height, 1)
        left_paddle_palette = displayio.Palette(1)
        left_paddle_palette[0] = 0xFFFFFF
        group.append(
            displayio.TileGrid(left_paddle_bitmap, pixel_shader=left_paddle_palette, x=10, y=int(left_paddle_y)))

        right_paddle_bitmap = displayio.Bitmap(paddle_width, paddle_height, 1)
        right_paddle_palette = displayio.Palette(1)
        right_paddle_palette[0] = 0xFFFFFF
        group.append(
            displayio.TileGrid(right_paddle_bitmap, pixel_shader=right_paddle_palette, x=302, y=int(right_paddle_y)))

        # Ball
        ball_bitmap = displayio.Bitmap(ball_size, ball_size, 1)
        ball_palette = displayio.Palette(1)
        ball_palette[0] = 0xFFFF00
        group.append(displayio.TileGrid(ball_bitmap, pixel_shader=ball_palette, x=int(ball_x), y=int(ball_y)))

        # Score
        group.append(
            label.Label(terminalio.FONT, text=f"{score_left}    SMART PONG    {score_right}", color=0x00FF00, scale=1,
                        anchor_point=(0.5, 0.0), anchored_position=(160, 10)))

        display.root_group = group

        # AI paddle movement
        ball_center_y = ball_y + ball_size // 2
        if ball_vel_x < 0:
            left_paddle_center = left_paddle_y + paddle_height // 2
            if ball_center_y > left_paddle_center + 8:
                left_paddle_y += paddle_speed
            elif ball_center_y < left_paddle_center - 8:
                left_paddle_y -= paddle_speed
        if ball_vel_x > 0:
            right_paddle_center = right_paddle_y + paddle_height // 2
            if ball_center_y > right_paddle_center + 8:
                right_paddle_y += paddle_speed
            elif ball_center_y < right_paddle_center - 8:
                right_paddle_y -= paddle_speed

        left_paddle_y = max(0, min(240 - paddle_height, left_paddle_y))
        right_paddle_y = max(0, min(240 - paddle_height, right_paddle_y))

        # Ball collision with paddles
        if (ball_vel_x < 0 and ball_x <= 18 and ball_x >= 8 and
                ball_y + ball_size >= left_paddle_y - 2 and ball_y <= left_paddle_y + paddle_height + 2):
            ball_vel_x = abs(ball_vel_x) * 1.02
            ball_x = 19
            hit_pos = (ball_y + ball_size // 2 - left_paddle_y) / paddle_height
            ball_vel_y += (hit_pos - 0.5) * 2

        if (ball_vel_x > 0 and ball_x + ball_size >= 302 and ball_x + ball_size <= 312 and
                ball_y + ball_size >= right_paddle_y - 2 and ball_y <= right_paddle_y + paddle_height + 2):
            ball_vel_x = -abs(ball_vel_x) * 1.02
            ball_x = 301 - ball_size
            hit_pos = (ball_y + ball_size // 2 - right_paddle_y) / paddle_height
            ball_vel_y += (hit_pos - 0.5) * 2

        ball_x += ball_vel_x
        ball_y += ball_vel_y

        # Ball collision with walls
        if ball_y <= 0 or ball_y >= 240 - ball_size:
            ball_vel_y = -ball_vel_y
            ball_y = max(0, min(240 - ball_size, ball_y))

        ball_vel_y = max(-7, min(7, ball_vel_y))
        ball_vel_x = max(-8, min(8, ball_vel_x))

        # Scoring
        if ball_x < -ball_size:
            score_right += 1
            ball_x, ball_y = 160, 120
            ball_vel_x, ball_vel_y = 5.0, 4.0 if frame % 2 else -4.0
        if ball_x > 320:
            score_left += 1
            ball_x, ball_y = 160, 120
            ball_vel_x, ball_vel_y = -5.0, 4.0 if frame % 2 else -4.0


def demo_image_display():
    """Display the campus image"""
    print("🖼️ Image Display Demo")

    try:
        campus_bitmap = displayio.OnDiskBitmap("/campus.bmp")
        group = displayio.Group()
        group.append(displayio.TileGrid(campus_bitmap, pixel_shader=campus_bitmap.pixel_shader))
        display.root_group = group
        time.sleep(5)
    except:
        group = displayio.Group()
        create_gradient(group, 0x000080, 0xFF8000)
        group.append(label.Label(terminalio.FONT, text="Image Not Found", color=0xFFFFFF, scale=3,
                                 anchor_point=(0.5, 0.5), anchored_position=(160, 100)))
        group.append(label.Label(terminalio.FONT, text="Convert image to 320x240 BMP", color=0xFFFFFF, scale=1,
                                 anchor_point=(0.5, 0.5), anchored_position=(160, 130)))
        group.append(label.Label(terminalio.FONT, text="Save as /campus.bmp", color=0xFFFFFF, scale=1,
                                 anchor_point=(0.5, 0.5), anchored_position=(160, 150)))
        display.root_group = group
        time.sleep(4)


# --- Main Demo Loop ---
def run_demo():
    """Run the complete demo sequence"""
    print("🚀 Starting ILI9341 Complete Display Demo")

    demos = [demo_splash_screen, demo_fonts_and_text, demo_forkawesome_icons, demo_color_bars,
             demo_turtle_graphics, demo_pong_game, demo_image_display]
    demo_index = 0

    while True:
        try:
            demos[demo_index]()
            demo_index = (demo_index + 1) % len(demos)
            time.sleep(1)
        except KeyboardInterrupt:
            print("Demo stopped")
            break
        except Exception as e:
            print(f"Error in demo: {e}")
            time.sleep(2)


if __name__ == "__main__":
    run_demo()
