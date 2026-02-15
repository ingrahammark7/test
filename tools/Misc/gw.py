from PIL import Image, ImageDraw
from math import cos, sin, pi

width, height = 200, 200
num_interpolated_frames = 20  # frames between shapes
polygon_resolution = 20  # number of points to approximate circle/rectangle

# Define key shapes as points and colors
key_shapes = []

# Circle (approximated as polygon)
circle_bbox = (50, 50, 150, 150)
circle_points = []
cx, cy = (circle_bbox[0]+circle_bbox[2])/2, (circle_bbox[1]+circle_bbox[3])/2
rx, ry = (circle_bbox[2]-circle_bbox[0])/2, (circle_bbox[3]-circle_bbox[1])/2
for i in range(polygon_resolution):
    angle = 2 * pi * i / polygon_resolution
    x = cx + rx * cos(angle)
    y = cy + ry * sin(angle)
    circle_points.append((x, y))
key_shapes.append({"points": circle_points, "color": (255, 0, 0)})

# Rectangle (approximated as polygon with same number of points)
rect_bbox = (30, 30, 170, 170)
rect_corners = [(rect_bbox[0], rect_bbox[1]), (rect_bbox[2], rect_bbox[1]),
                (rect_bbox[2], rect_bbox[3]), (rect_bbox[0], rect_bbox[3])]
# Repeat corners to match polygon_resolution
rect_points = []
for i in range(polygon_resolution):
    rect_points.append(rect_corners[i % 4])
key_shapes.append({"points": rect_points, "color": (0, 255, 0)})

# Triangle (3 points, repeat to match polygon_resolution)
tri_points = [(100, 30), (30, 170), (170, 170)]
triangle_points = []
for i in range(polygon_resolution):
    triangle_points.append(tri_points[i % 3])
key_shapes.append({"points": triangle_points, "color": (0, 0, 255)})

# Linear interpolation
def lerp_points(a, b, t):
    return [(a[i][0] + (b[i][0]-a[i][0])*t,
             a[i][1] + (b[i][1]-a[i][1])*t) for i in range(len(a))]

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i]-c1[i])*t) for i in range(3))

frames = []

for k in range(len(key_shapes)-1):
    start = key_shapes[k]
    end = key_shapes[k+1]
    for i in range(num_interpolated_frames):
        t = i / num_interpolated_frames
        points = lerp_points(start["points"], end["points"], t)
        color = lerp_color(start["color"], end["color"], t)
        img = Image.new("RGB", (width, height), "white")
        ImageDraw.Draw(img).polygon(points, fill=color)
        frames.append(img)

# Add final key shape
img = Image.new("RGB", (width, height), "white")
ImageDraw.Draw(img).polygon(key_shapes[-1]["points"], fill=key_shapes[-1]["color"])
frames.append(img)

# Save GIF
frames[0].save("morphing_shapes.gif",
               save_all=True,
               append_images=frames[1:],
               duration=100,
               loop=0)
print("Saved morphing_shapes.gif")