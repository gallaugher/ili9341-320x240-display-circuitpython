# ili9341-display-demo.py
"""
CircuitPython demo for ILI9341 320x240 display in landscape mode.
Demonstrates fonts, colors, graphics, turtle graphics, and image display.
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
    width=320,
    height=240,
    rotation=0,  # Landscape mode
    backlight_pin=None
)

print("✅ ILI9341 Display initialized (320x240 landscape)")


# --- Demo Functions ---

def demo_splash_screen():
    """Display specification splash screen with different fonts"""
    print("🚀 Splash Screen")

    # Import bitmap font support
    from adafruit_bitmap_font import bitmap_font

    group = displayio.Group()

    # Subtle black to gray gradient background
    for y in range(240):
        strip_bitmap = displayio.Bitmap(320, 1, 1)
        strip_palette = displayio.Palette(1)
        # Black to gray gradient - subtle and professional
        gray_val = min(64, y // 4)  # Gradual increase to dark gray
        color = gray_val | (gray_val << 8) | (gray_val << 16)  # RGB same value = gray
        strip_palette[0] = color
        strip = displayio.TileGrid(strip_bitmap, pixel_shader=strip_palette, x=0, y=y)
        group.append(strip)

    # Load fonts
    fonts = {}
    font_files = [
        ("Collegiate-50", "/fonts/Collegiate-50.bdf"),
        ("helvB18", "/fonts/helvB18.bdf")
    ]

    for font_name, font_path in font_files:
        try:
            fonts[font_name] = bitmap_font.load_font(font_path)
            print(f"✅ Loaded {font_name} for splash screen")
        except Exception as e:
            print(f"❌ Could not load {font_name}: {e}")
            fonts[font_name] = None

    # Line 1: "ILI9341" - Collegiate-50
    if fonts["Collegiate-50"]:
        title_line1 = label.Label(
            fonts["Collegiate-50"],
            text="ILI9341",
            color=0xFFFF00,
            anchor_point=(0.5, 0.5),
            anchored_position=(160, 40)
        )
    else:
        title_line1 = label.Label(
            terminalio.FONT,
            text="ILI9341",
            color=0xFFFF00,
            scale=3,
            anchor_point=(0.5, 0.5),
            anchored_position=(160, 40)
        )
    group.append(title_line1)

    # Line 2: "2.2\" Display" - Collegiate-50
    if fonts["Collegiate-50"]:
        title_line2 = label.Label(
            fonts["Collegiate-50"],
            text="2.2\" Display",
            color=0xFFFF00,
            anchor_point=(0.5, 0.5),
            anchored_position=(160, 90)
        )
    else:
        title_line2 = label.Label(
            terminalio.FONT,
            text="2.2\" Display",
            color=0xFFFF00,
            scale=3,
            anchor_point=(0.5, 0.5),
            anchored_position=(160, 90)
        )
    group.append(title_line2)

    # Line 3: "320 x 240 Resolution" - helvB18
    if fonts["helvB18"]:
        resolution = label.Label(
            fonts["helvB18"],
            text="320 x 240 Resolution",
            color=0x00FFFF,
            anchor_point=(0.5, 0.5),
            anchored_position=(160, 140)
        )
    else:
        resolution = label.Label(
            terminalio.FONT,
            text="320 x 240 Resolution",
            color=0x00FFFF,
            scale=2,
            anchor_point=(0.5, 0.5),
            anchored_position=(160, 140)
        )
    group.append(resolution)

    # Line 4: "65K Colors & SPI Interface" - helvB18
    if fonts["helvB18"]:
        specs_line1 = label.Label(
            fonts["helvB18"],
            text="65K Colors & SPI Interface",
            color=0xFFFFFF,
            anchor_point=(0.5, 0.5),
            anchored_position=(160, 180)
        )
    else:
        specs_line1 = label.Label(
            terminalio.FONT,
            text="65K Colors & SPI Interface",
            color=0xFFFFFF,
            scale=1,
            anchor_point=(0.5, 0.5),
            anchored_position=(160, 180)
        )
    group.append(specs_line1)

    # Line 5: "CircuitPython" - helvB18
    if fonts["helvB18"]:
        specs_line2 = label.Label(
            fonts["helvB18"],
            text="CircuitPython",
            color=0xFFFFFF,
            anchor_point=(0.5, 0.5),
            anchored_position=(160, 210)
        )
    else:
        specs_line2 = label.Label(
            terminalio.FONT,
            text="CircuitPython",
            color=0xFFFFFF,
            scale=1,
            anchor_point=(0.5, 0.5),
            anchored_position=(160, 210)
        )
    group.append(specs_line2)

    display.root_group = group
    time.sleep(1)

def demo_fonts_and_text():
    """Demonstrate different font sizes and text styles"""
    print("📝 Font Demo")

    # Import bitmap font support
    from adafruit_bitmap_font import bitmap_font

    group = displayio.Group()

    # Clean background - dark blue gradient
    for y in range(240):
        strip_bitmap = displayio.Bitmap(320, 1, 1)
        strip_palette = displayio.Palette(1)
        # Dark blue gradient
        blue_val = 0x000020 + (y // 8)
        strip_palette[0] = blue_val
        strip = displayio.TileGrid(strip_bitmap, pixel_shader=strip_palette, x=0, y=y)
        group.append(strip)

    # Try to load custom fonts, fall back to terminal font if not available
    fonts = {}
    font_files = [
        ("helvB24", "/fonts/helvB24.bdf"),
        ("Collegiate-50", "/fonts/Collegiate-50.bdf"),
        ("LeagueSpartan_Bold_16", "/fonts/LeagueSpartan_Bold_16.bdf"),
        ("helvB18", "/fonts/helvB18.bdf"),
        ("helvB14", "/fonts/helvB14.bdf"),
        ("helvB12", "/fonts/helvB12.bdf"),
        ("helvB08", "/fonts/helvB08.bdf")
    ]

    for font_name, font_path in font_files:
        try:
            fonts[font_name] = bitmap_font.load_font(font_path)
            print(f"✅ Loaded {font_name}")
        except Exception as e:
            print(f"❌ Could not load {font_name}: {e}")
            fonts[font_name] = None

    y_pos = 10

    # Title using largest available font
    if fonts["helvB24"]:
        title = label.Label(
            fonts["helvB24"],
            text="Font Showcase",
            color=0xFFFF00,
            anchor_point=(0.5, 0.0),
            anchored_position=(160, y_pos)
        )
        y_pos += 35
    else:
        title = label.Label(
            terminalio.FONT,
            text="Font Showcase",
            color=0xFFFF00,
            scale=3,
            anchor_point=(0.5, 0.0),
            anchored_position=(160, y_pos)
        )
        y_pos += 30
    group.append(title)

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
    y_pos += 18

    # Terminal font scaled up
    terminal_scaled = label.Label(
        terminalio.FONT,
        text="Terminal x2 Scale",
        color=0x00FFFF,
        scale=2,
        x=10,
        y=y_pos
    )
    group.append(terminal_scaled)
    y_pos += 28

    # helvB24
    if fonts["helvB24"]:
        helv24_label = label.Label(
            fonts["helvB24"],
            text="helvB24",
            color=0xFFFFFF,
            x=10,
            y=y_pos
        )
        group.append(helv24_label)
        y_pos += 30

    # Custom font demonstrations with better spacing
    font_demos = [
        ("helvB18", "helvB18", 0xFFAAAA),
        ("helvB14", "helvB14", 0xFF8888),
        ("Collegiate-50", "Collegiate-50", 0x88FF88),
        ("helvB12", "helvB12", 0xFFAAAA),
        ("helvB08", "helvB08", 0x8888FF)
    ]

    for i, (font_key, demo_text, color) in enumerate(font_demos):
        # Add extra spacing before helvB14 to separate from helvB18
        if font_key == "helvB14":
            y_pos += 5

        if fonts[font_key] and y_pos < 180:
            # Nudge Collegiate down by 3 pixels
            label_y = y_pos + 3 if font_key == "Collegiate-50" else y_pos

            font_label = label.Label(
                fonts[font_key],
                text=demo_text,
                color=color,
                x=10,
                y=label_y
            )
            group.append(font_label)
            # Give more space for the large Collegiate font
            spacing = 50 if font_key == "Collegiate-50" else 22
            y_pos += spacing
        elif font_key == "Collegiate-50" and not fonts[font_key]:
            # Try LeagueSpartan at 2x scale as fallback
            if fonts["LeagueSpartan_Bold_16"]:
                spartan_2x = label.Label(
                    fonts["LeagueSpartan_Bold_16"],
                    text="League Spartan x2 Scale",
                    color=0x88FF88,
                    scale=2,
                    x=10,
                    y=y_pos
                )
                group.append(spartan_2x)
                y_pos += 35
        elif y_pos < 180:
            # Fallback if font didn't load
            fallback_label = label.Label(
                terminalio.FONT,
                text=f"{font_key}: (not loaded)",
                color=0x666666,
                scale=1,
                x=10,
                y=y_pos
            )
            group.append(fallback_label)
            y_pos += 15

    # Bottom technical info
    if fonts["helvB12"]:
        bottom_info = label.Label(
            fonts["helvB12"],
            text="320x240 • 65K Colors • SPI",
            color=0x00FF00,
            anchor_point=(0.5, 0.0),
            anchored_position=(160, 215)
        )
        group.append(bottom_info)

    display.root_group = group
    time.sleep(4)

def demo_forkawesome_icons():
    """ForkAwesome Icons showcase on colorful backgrounds"""
    print("ForkAwesome Icons Demo")

    # Import bitmap font support
    from adafruit_bitmap_font import bitmap_font

    # Load ForkAwesome fonts
    forkawesome_fonts = {}
    for size in ["42", "32", "24"]:
        try:
            forkawesome_fonts[size] = bitmap_font.load_font(f"/fonts/forkawesome-{size}.pcf")
            print(f"✅ Loaded ForkAwesome-{size}")
        except Exception as e:
            print(f"❌ Could not load ForkAwesome-{size}: {e}")
            forkawesome_fonts[size] = None

    # If no fonts loaded, skip this demo
    if not any(forkawesome_fonts.values()):
        print("❌ No ForkAwesome fonts available, skipping icon demo")
        return

    group = displayio.Group()

    # White background
    bg_bitmap = displayio.Bitmap(320, 240, 1)
    bg_palette = displayio.Palette(1)
    bg_palette[0] = 0xFFFFFF  # White
    bg = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)
    group.append(bg)

    # Title
    title = label.Label(
        terminalio.FONT,
        text="ForkAwesome Icon Library",
        color=0xFF1493,  # Hot pink
        scale=2,
        anchor_point=(0.5, 0.0),
        anchored_position=(160, 0)
    )
    group.append(title)

    # Icons to display with their Unicode and names
    icons_to_show = [
        ("\uf193", "wheelchair", 0xFF1493),  # Hot pink
        ("\uf164", "thumbs_up", 0x32CD32),  # Lime green
        ("\uf062", "arrow_up", 0x4169E1),  # Royal blue
        ("\uf063", "arrow_down", 0x4169E1),  # Royal blue
        ("\uf060", "arrow_left", 0x4169E1),  # Royal blue
        ("\uf061", "arrow_right", 0x4169E1),  # Royal blue
        ("\uf004", "heart", 0xFF0000),  # Red
        ("\uf35f", "bunny", 0xFF69B4),  # Hot pink
        ("\uf1b9", "car", 0xFF0000),  # Red
        ("\uf118", "smile", 0x9932CC),  # Dark orchid
        ("\uf005", "star", 0xFFD700),  # Gold
        ("\uf329", "sun", 0xFF8C00),  # Dark orange
        ("\uf0c2", "cloud", 0x4682B4),  # Steel blue
        ("\uf017", "clock", 0x8B4513),  # Saddle brown
        ("\uf001", "music", 0xFF1493),  # Hot pink - musical note
        ("\uf06c", "leaf", 0x228B22)  # Forest green - nature/flower
    ]

    # Display icons in a grid
    x_start = 20
    y_start = 48
    icon_spacing_x = 75
    icon_spacing_y = 47
    icons_per_row = 4

    # Use the largest available font
    icon_font = None
    for size in ["42", "32", "24"]:
        if forkawesome_fonts[size]:
            icon_font = forkawesome_fonts[size]
            icon_size = int(size)
            break

    if icon_font:
        row = 0
        col = 0
        displayed_count = 0

        for icon_char, icon_name, color in icons_to_show:
            if displayed_count >= 16:  # Show 16 icons (4 complete rows)
                break

            x_pos = x_start + (col * icon_spacing_x)
            y_pos = y_start + (row * icon_spacing_y)
            # Add 6 pixels per row for even spacing between all rows
            if row > 0:
                y_pos += 6 * row

            try:
                icon_label = label.Label(
                    icon_font,
                    text=icon_char,
                    color=color,
                    x=x_pos,
                    y=y_pos
                )
                group.append(icon_label)
                displayed_count += 1
                print(f"✅ Row {row + 1}: {icon_name} at ({x_pos}, {y_pos})")
            except Exception as e:
                print(f"❌ Failed to display {icon_name}: {e}")

            # Move to next position
            col += 1
            if col >= icons_per_row:
                col = 0
                row += 1

    display.root_group = group
    time.sleep(4)

def demo_color_bars():
    """Display color bars to show color capability"""
    print("🌈 Color Test Pattern")
    group = displayio.Group()

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
        bar_bitmap = displayio.Bitmap(bar_width, 180, 1)
        bar_palette = displayio.Palette(1)
        bar_palette[0] = color
        bar = displayio.TileGrid(bar_bitmap, pixel_shader=bar_palette,
                                 x=i * bar_width, y=30)
        group.append(bar)

    # Title
    title = label.Label(
        terminalio.FONT,
        text="65,536 Color Test Pattern",
        color=0xFFFFFF,
        scale=2,
        anchor_point=(0.5, 0.0),
        anchored_position=(160, 5)
    )
    group.append(title)

    # Bottom text
    bottom_text = label.Label(
        terminalio.FONT,
        text="Smooth gradients and vibrant colors",
        color=0xFFFFFF,
        scale=1,
        anchor_point=(0.5, 0.0),
        anchored_position=(160, 220)
    )
    group.append(bottom_text)

    display.root_group = group
    time.sleep(4)


def demo_turtle_graphics():
    """Turtle graphics demo - continuous animated flower patterns"""
    print("🐢 Turtle Graphics Demo")

    try:
        from adafruit_turtle import turtle, Color
    except ImportError:
        print("❌ adafruit_turtle library not available, skipping turtle demo")
        # Show fallback message
        group = displayio.Group()

        # Black background
        bg_bitmap = displayio.Bitmap(320, 240, 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = 0x000000
        bg = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)
        group.append(bg)

        # Message
        message = label.Label(
            terminalio.FONT,
            text="Turtle Graphics Not Available",
            color=0xFFFF00,
            scale=2,
            anchor_point=(0.5, 0.5),
            anchored_position=(160, 100)
        )
        group.append(message)

        sub_message = label.Label(
            terminalio.FONT,
            text="Install adafruit_turtle library",
            color=0xFFFFFF,
            scale=1,
            anchor_point=(0.5, 0.5),
            anchored_position=(160, 130)
        )
        group.append(sub_message)

        display.root_group = group
        time.sleep(4)
        return

    try:
        # Initialize turtle
        my_turtle = turtle(display)
        my_turtle.bgcolor(Color.BLACK)
        my_turtle.speed(0)  # Fastest
        my_turtle.pensize(1)

        # Color palette for the flower pattern
        colors = [Color.RED, Color.ORANGE, Color.YELLOW, Color.GREEN,
                  Color.BLUE, Color.PURPLE, Color.PINK]

        # Draw multiple flower patterns for continuous animation
        patterns = [
            (0, 0, 50),  # Center, normal size
            (-80, -50, 30),  # Left, smaller
            (80, 50, 40),  # Right, medium
            (0, -80, 25),  # Bottom, small
        ]

        for pattern_x, pattern_y, pattern_size in patterns:
            # Position turtle for this pattern
            my_turtle.penup()
            my_turtle.goto(pattern_x, pattern_y)
            my_turtle.pendown()

            # Beautiful geometric flower pattern with colors
            for i in range(21):
                # Change color every few petals for rainbow effect
                my_turtle.pencolor(colors[i % len(colors)])

                # Draw one petal/section
                for _ in range(6):
                    my_turtle.forward(pattern_size)
                    my_turtle.right(61)

                # Rotate to next position
                my_turtle.right(11.1111)

            # Small pause between patterns
            time.sleep(0.5)

        time.sleep(2)  # Hold final result

    except Exception as e:
        print(f"❌ Turtle graphics error: {e}")
        # Show error message instead of crashing
        group = displayio.Group()

        # Black background
        bg_bitmap = displayio.Bitmap(320, 240, 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = 0x000000
        bg = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)
        group.append(bg)

        # Error message
        message = label.Label(
            terminalio.FONT,
            text="Turtle Graphics Error",
            color=0xFF0000,
            scale=2,
            anchor_point=(0.5, 0.5),
            anchored_position=(160, 100)
        )
        group.append(message)

        error_msg = label.Label(
            terminalio.FONT,
            text="Skipping turtle demo",
            color=0xFFFFFF,
            scale=1,
            anchor_point=(0.5, 0.5),
            anchored_position=(160, 130)
        )
        group.append(error_msg)

        display.root_group = group
        time.sleep(1)

def demo_pong_game():
    """Classic Pong game demo with smarter paddle AI and actual gameplay"""
    print("🏓 Pong Game Demo")

    # Game parameters - optimized for reliable collision detection
    ball_x = 160.0
    ball_y = 120.0
    ball_vel_x = 5.0  # Slightly slower for better collision detection
    ball_vel_y = 4.0
    ball_size = 8

    paddle_width = 8  # Slightly wider paddles
    paddle_height = 40
    paddle_speed = 5.0  # Fast but reliable

    left_paddle_y = 100.0
    right_paddle_y = 100.0

    score_left = 0
    score_right = 0

    # Run game for about 4 seconds with smarter AI
    # for frame in range(160):  # More frames for better gameplay
    for frame in range(80):  # More frames for better gameplay
        group = displayio.Group()

        # Black background (classic Pong)
        bg_bitmap = displayio.Bitmap(320, 240, 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = 0x000000
        bg = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)
        group.append(bg)

        # Center line (dashed) - simplified for speed
        for i in range(0, 240, 40):
            line_bitmap = displayio.Bitmap(2, 20, 1)
            line_palette = displayio.Palette(1)
            line_palette[0] = 0x888888
            line = displayio.TileGrid(line_bitmap, pixel_shader=line_palette,
                                      x=159, y=i)
            group.append(line)

        # Left paddle
        left_paddle_bitmap = displayio.Bitmap(paddle_width, paddle_height, 1)
        left_paddle_palette = displayio.Palette(1)
        left_paddle_palette[0] = 0xFFFFFF
        left_paddle = displayio.TileGrid(left_paddle_bitmap, pixel_shader=left_paddle_palette,
                                         x=10, y=int(left_paddle_y))
        group.append(left_paddle)

        # Right paddle
        right_paddle_bitmap = displayio.Bitmap(paddle_width, paddle_height, 1)
        right_paddle_palette = displayio.Palette(1)
        right_paddle_palette[0] = 0xFFFFFF
        right_paddle = displayio.TileGrid(right_paddle_bitmap, pixel_shader=right_paddle_palette,
                                          x=302, y=int(right_paddle_y))  # Moved slightly left
        group.append(right_paddle)

        # Ball
        ball_bitmap = displayio.Bitmap(ball_size, ball_size, 1)
        ball_palette = displayio.Palette(1)
        ball_palette[0] = 0xFFFF00  # Yellow ball
        ball = displayio.TileGrid(ball_bitmap, pixel_shader=ball_palette,
                                  x=int(ball_x), y=int(ball_y))
        group.append(ball)

        # Score display
        score_text = label.Label(
            terminalio.FONT,
            text=f"{score_left}    SMART PONG    {score_right}",
            color=0x00FF00,
            scale=1,
            anchor_point=(0.5, 0.0),
            anchored_position=(160, 10)
        )
        group.append(score_text)

        display.root_group = group

        # Smart paddle AI - track the ball but with some imperfection
        ball_center_y = ball_y + ball_size // 2

        # Left paddle AI - moves toward ball when ball is coming toward it
        if ball_vel_x < 0:  # Ball moving left
            left_paddle_center = left_paddle_y + paddle_height // 2
            if ball_center_y > left_paddle_center + 8:
                left_paddle_y += paddle_speed
            elif ball_center_y < left_paddle_center - 8:
                left_paddle_y -= paddle_speed

        # Right paddle AI - moves toward ball when ball is coming toward it
        if ball_vel_x > 0:  # Ball moving right
            right_paddle_center = right_paddle_y + paddle_height // 2
            if ball_center_y > right_paddle_center + 8:
                right_paddle_y += paddle_speed
            elif ball_center_y < right_paddle_center - 8:
                right_paddle_y -= paddle_speed

        # Keep paddles on screen
        left_paddle_y = max(0, min(240 - paddle_height, left_paddle_y))
        right_paddle_y = max(0, min(240 - paddle_height, right_paddle_y))

        # IMPROVED Ball collision with left paddle - more forgiving
        if (ball_vel_x < 0 and  # Ball moving toward left paddle
                ball_x <= 18 and ball_x >= 8 and  # Wider collision zone
                ball_y + ball_size >= left_paddle_y - 2 and  # Slightly extended
                ball_y <= left_paddle_y + paddle_height + 2):
            ball_vel_x = abs(ball_vel_x) * 1.02  # Small speed increase
            ball_x = 19  # Move ball away from paddle
            # Add some angle based on where it hit the paddle
            hit_pos = (ball_y + ball_size // 2 - left_paddle_y) / paddle_height
            ball_vel_y += (hit_pos - 0.5) * 2

        # IMPROVED Ball collision with right paddle - more forgiving
        if (ball_vel_x > 0 and  # Ball moving toward right paddle
                ball_x + ball_size >= 302 and ball_x + ball_size <= 312 and  # Wider collision zone
                ball_y + ball_size >= right_paddle_y - 2 and  # Slightly extended
                ball_y <= right_paddle_y + paddle_height + 2):
            ball_vel_x = -abs(ball_vel_x) * 1.02  # Small speed increase
            ball_x = 301 - ball_size  # Move ball away from paddle
            # Add some angle based on where it hit the paddle
            hit_pos = (ball_y + ball_size // 2 - right_paddle_y) / paddle_height
            ball_vel_y += (hit_pos - 0.5) * 2

        # Update ball position AFTER collision detection
        ball_x += ball_vel_x
        ball_y += ball_vel_y

        # Ball collision with top/bottom walls
        if ball_y <= 0 or ball_y >= 240 - ball_size:
            ball_vel_y = -ball_vel_y
            ball_y = max(0, min(240 - ball_size, ball_y))  # Keep on screen

        # Limit ball speed
        ball_vel_y = max(-7, min(7, ball_vel_y))
        ball_vel_x = max(-8, min(8, ball_vel_x))

        # Ball goes off left side (right player scores)
        if ball_x < -ball_size:
            score_right += 1
            ball_x = 160
            ball_y = 120
            ball_vel_x = 5.0
            ball_vel_y = 4.0 if frame % 2 else -4.0

        # Ball goes off right side (left player scores)
        if ball_x > 320:
            score_left += 1
            ball_x = 160
            ball_y = 120
            ball_vel_x = -5.0
            ball_vel_y = 4.0 if frame % 2 else -4.0

        # Good refresh rate
        # time.sleep(0.025)  # ~40fps

    # time.sleep(1)  # Hold final score


def demo_image_display():
    """Display the campus image"""
    print("🖼️ Image Display Demo")

    try:
        # Try to load the campus image
        # Note: Image should be converted to 320x240 BMP format and placed in root directory
        campus_bitmap = displayio.OnDiskBitmap("/campus.bmp")

        group = displayio.Group()

        # Display the image
        image_grid = displayio.TileGrid(
            campus_bitmap,
            pixel_shader=campus_bitmap.pixel_shader
        )
        group.append(image_grid)

        # Add title overlay
        title = label.Label(
            terminalio.FONT,
            text="Beautiful Campus View",
            color=0xFFFFFF,
            scale=2,
            anchor_point=(0.5, 0.0),
            anchored_position=(160, 10)
        )
        group.append(title)

        display.root_group = group
        time.sleep(5)

    except Exception as e:
        print(f"❌ Could not load campus image: {e}")
        print("💡 Convert your image to 320x240 BMP and save as /campus.bmp")

        # Show fallback message
        group = displayio.Group()

        # Gradient background
        for y in range(240):
            strip_bitmap = displayio.Bitmap(320, 1, 1)
            strip_palette = displayio.Palette(1)
            # Blue to orange gradient (like sky)
            blue_component = max(0, 255 - (y * 2))
            red_component = min(255, y * 2)
            green_component = min(255, y)
            color = (red_component << 16) | (green_component << 8) | blue_component
            strip_palette[0] = color
            strip = displayio.TileGrid(strip_bitmap, pixel_shader=strip_palette, x=0, y=y)
            group.append(strip)

        # Message
        message = label.Label(
            terminalio.FONT,
            text="Image Not Found",
            color=0xFFFFFF,
            scale=3,
            anchor_point=(0.5, 0.5),
            anchored_position=(160, 100)
        )
        group.append(message)

        instruction = label.Label(
            terminalio.FONT,
            text="Convert image to 320x240 BMP",
            color=0xFFFFFF,
            scale=1,
            anchor_point=(0.5, 0.5),
            anchored_position=(160, 130)
        )
        group.append(instruction)

        filename = label.Label(
            terminalio.FONT,
            text="Save as /campus.bmp",
            color=0xFFFFFF,
            scale=1,
            anchor_point=(0.5, 0.5),
            anchored_position=(160, 150)
        )
        group.append(filename)

        display.root_group = group
        time.sleep(4)


# --- Main Demo Loop ---
def run_demo():
    """Run the complete demo sequence"""
    print("🚀 Starting ILI9341 Complete Display Demo")

    demos = [
        demo_splash_screen,  # Display specifications
        demo_fonts_and_text,  # Font showcase
        demo_forkawesome_icons,  # Icon library
        demo_color_bars,  # Color test pattern
        demo_turtle_graphics,  # Turtle graphics (now with continuous animation)
        demo_pong_game,  # Classic Pong game demo
        demo_image_display  # Campus image
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
if __name__ == "__main__":
    run_demo()