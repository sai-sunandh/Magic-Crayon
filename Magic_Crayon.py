#using opencv
import cv2
import numpy as np

# Initialize drawing parameters
drawing = False
last_click_time = 0
current_color = (0, 0, 0)  # Default color: Black
eraser_size = 20
brush_size = 5
min_size = 1
max_size = 50
opacity = 255  # Default full opacity

# Create main canvas and control panel
canvas = np.ones((600, 800, 3), dtype=np.uint8) * 255  # White canvas
control_panel = np.ones((600, 100, 3), dtype=np.uint8) * 240  # Light gray control panel

# Combine canvas and control panel
window = np.hstack((canvas, control_panel))

def on_size_change(value):
    global brush_size, eraser_size
    if np.array_equal(current_color, colors['Eraser']):
        eraser_size = value
    else:
        brush_size = value

def on_opacity_change(value):
    global opacity

def draw(event, x, y, flags, param):
    global drawing, last_click_time, current_color, window

    # Adjust x coordinate for the main canvas
    if x >= 800:  # If clicking in control panel area
        return

    if event == cv2.EVENT_LBUTTONDOWN:
        button_clicked = check_button_click((x, y), buttons)
        if button_clicked:
            current_color = colors[button_clicked]
            drawing = False
            return
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        size = eraser_size if np.array_equal(current_color, colors['Eraser']) else brush_size
        if np.array_equal(current_color, colors['Eraser']):
            color = (255, 255, 255)
        else:
            # Apply opacity to the current color
            color = tuple(int(c * (opacity/255)) for c in current_color)
        cv2.circle(window[:, :800], (x, y), size, color, -1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

# Create color buttons
colors = {
    'Red': (0, 0, 255),
    'Green': (0, 255, 0),
    'Blue': (255, 0, 0),
    'Black': (0, 0, 0),
    'Eraser': (255, 255, 255)
}

def create_buttons():
    y = 20
    buttons = {}
    for name, color in colors.items():
        cv2.rectangle(window, (20, y), (70, y + 30), color, -1)
        cv2.rectangle(window, (20, y), (70, y + 30), (0, 0, 0), 1)
        buttons[name] = [(20, y), (70, y + 30)]
        y += 40
    return buttons

def check_button_click(pos, buttons):
    x, y = pos
    for name, coords in buttons.items():
        if (coords[0][0] <= x <= coords[1][0] and 
            coords[0][1] <= y <= coords[1][1]):
            return name
    return None

# Create window and set mouse callback
cv2.namedWindow('Drawing Board')
buttons = create_buttons()

# Create trackbars
cv2.createTrackbar('Size', 'Drawing Board', brush_size, max_size, on_size_change)
cv2.createTrackbar('Opacity', 'Drawing Board', opacity, 255, on_opacity_change)

cv2.setMouseCallback('Drawing Board', draw)

# ... existing code ...

# Modify the main loop
while True:
    # Get current trackbar values
    brush_size = cv2.getTrackbarPos('Size', 'Drawing Board')
    opacity = cv2.getTrackbarPos('Opacity', 'Drawing Board')
    
    # Show the window
    cv2.imshow('Drawing Board', window)
    
    # Check for window close button or 'q' key
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or cv2.getWindowProperty('Drawing Board', cv2.WND_PROP_VISIBLE) < 1:
        break

cv2.destroyAllWindows()
