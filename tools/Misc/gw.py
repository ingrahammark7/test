from PIL import Image, ImageDraw, ImageFilter, ImageChops
from math import cos, sin, pi
import random

# ======== Settings ========
width, height = 400, 400
num_key_shapes = 6
num_interpolated_frames = 20
polygon_resolution = 20
frame_duration = 80
max_shapes_per_frame = 4
num_particles = 100
trail_length = 4

# ======== Helper functions ========
def random_shape_points(shape_type, resolution):
    if shape_type=="circle":
        x0,y0=random.randint(30,120),random.randint(30,120)
        x1,y1=random.randint(280,370),random.randint(280,370)
        cx,cy=(x0+x1)/2,(y0+y1)/2
        rx,ry=(x1-x0)/2,(y1-y0)/2
        return [(cx+rx*cos(2*pi*i/resolution), cy+ry*sin(2*pi*i/resolution)) for i in range(resolution)]
    elif shape_type=="rectangle":
        x0,y0=random.randint(20,100),random.randint(20,100)
        x1,y1=random.randint(280,380),random.randint(280,380)
        corners=[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
        return [corners[i%4] for i in range(resolution)]
    elif shape_type=="triangle":
        p1=(random.randint(50,150),random.randint(20,100))
        p2=(random.randint(20,150),random.randint(280,380))
        p3=(random.randint(150,380),random.randint(280,380))
        return [ [p1,p2,p3][i%3] for i in range(resolution)]
    elif shape_type=="star":
        cx,cy=random.randint(100,300),random.randint(100,300)
        r=random.randint(20,80)
        points=[]
        for i in range(resolution):
            angle=2*pi*i/resolution
            radius=r*(1+0.3*(i%2))
            points.append((cx+cos(angle)*radius,cy+sin(angle)*radius))
        return points
    else:  # polygon
        return [(random.randint(0,width),random.randint(0,height)) for _ in range(resolution)]

def random_shape():
    stype=random.choice(["circle","rectangle","triangle","polygon","star"])
    return {
        "points": random_shape_points(stype, polygon_resolution),
        "color": (random.randint(0,255),random.randint(0,255),random.randint(0,255)),
        "alpha": random.randint(80,255),
        "rotation": random.randint(0,360),
        "scale": random.uniform(0.5,1.5),
        "stroke": random.choice([0,2,3]),
        "mirror": random.choice([True,False]),
        "distort": random.uniform(0,0.05),  # per-point distortion
    }

def lerp(a,b,t): return a+(b-a)*t
def lerp_points(a,b,t): return [(lerp(a[i][0],b[i][0],t),lerp(a[i][1],b[i][1],t)) for i in range(len(a))]
def lerp_color(c1,c2,t): return tuple(int(lerp(c1[i],c2[i],t)) for i in range(3))
def rotate_points(points,angle_deg,center):
    angle_rad=pi*angle_deg/180
    cx,cy=center
    return [(cx+(x-cx)*cos(angle_rad)-(y-cy)*sin(angle_rad),
             cy+(x-cx)*sin(angle_rad)+(y-cy)*cos(angle_rad)) for x,y in points]
def scale_points(points,scale,center):
    cx,cy=center
    return [(cx+(x-cx)*scale, cy+(y-cy)*scale) for x,y in points]
def jitter_points(points,max_jitter=3):
    return [(x+random.uniform(-max_jitter,max_jitter),y+random.uniform(-max_jitter,max_jitter)) for x,y in points]
def distort_points(points, factor=0.05):
    return [(x*(1+random.uniform(-factor,factor)),y*(1+random.uniform(-factor,factor))) for x,y in points]

# ======== Particle system ========
class Particle:
    def __init__(self):
        self.x=random.uniform(0,width)
        self.y=random.uniform(0,height)
        self.vx=random.uniform(-2,2)
        self.vy=random.uniform(-2,2)
        self.color=(random.randint(100,255),random.randint(100,255),random.randint(100,255))
        self.alpha=random.randint(50,150)
        self.size=random.randint(2,5)
    def update(self):
        self.x+=self.vx
        self.y+=self.vy
        if self.x<0 or self.x>width:self.vx*=-1
        if self.y<0 or self.y>height:self.vy*=-1
    def draw(self,draw):
        draw.ellipse([self.x-self.size,self.y-self.size,self.x+self.size,self.y+self.size],
                     fill=self.color+(self.alpha,))

particles=[Particle() for _ in range(num_particles)]

# ======== Generate key shapes ========
key_shapes=[]
for _ in range(num_key_shapes):
    frame_shapes=[random_shape() for _ in range(random.randint(1,max_shapes_per_frame))]
    key_shapes.append(frame_shapes)

# ======== Generate frames ========
frames=[]
prev_imgs=[]
total_frames=len(key_shapes)
for k in range(total_frames):
    start_shapes=key_shapes[k]
    end_shapes=key_shapes[(k+1)%total_frames]
    max_shapes=max(len(start_shapes),len(end_shapes))
    while len(start_shapes)<max_shapes:start_shapes.append(random_shape())
    while len(end_shapes)<max_shapes:end_shapes.append(random_shape())
    for i in range(num_interpolated_frames):
        t=i/num_interpolated_frames
        img=Image.new("RGBA",(width,height),(255,255,255,255))
        draw=ImageDraw.Draw(img)
        # Background gradient/noise
        bg_color=(random.randint(200,255),random.randint(200,255),random.randint(200,255))
        ImageDraw.Draw(img).rectangle([0,0,width,height],fill=bg_color)
        # Shapes
        for s in range(max_shapes):
            pts=lerp_points(start_shapes[s]["points"],end_shapes[s]["points"],t)
            pts=distort_points(pts,lerp(0,end_shapes[s]["distort"],t))
            pts=scale_points(pts,lerp(start_shapes[s]["scale"],end_shapes[s]["scale"],t),(width/2,height/2))
            pts=rotate_points(pts,lerp(start_shapes[s]["rotation"],end_shapes[s]["rotation"],t),(width/2,height/2))
            pts=jitter_points(pts,max_jitter=2)
            if random.random()<0.5: pts=[(width-x,y) for x,y in pts]
            color=lerp_color(start_shapes[s]["color"],end_shapes[s]["color"],t)
            alpha=int(lerp(start_shapes[s]["alpha"],end_shapes[s]["alpha"],t))
            draw.polygon(pts,fill=color+(alpha,),outline=(0,0,0,alpha) if start_shapes[s]["stroke"]>0 else None)
        # Particles
        for p in particles:
            p.update()
            p.draw(draw)
        # Trails
        for prev in prev_imgs[-trail_length:]:
            img=Image.alpha_composite(prev,img)
        # Glow/blur overlay
        glow=img.filter(ImageFilter.GaussianBlur(radius=3))
        img=Image.alpha_composite(glow,img)
        frames.append(img)
        prev_imgs.append(img)

# ======== Save GIF ========
frames[0].save(
    "ultimate_exhaustive_generative_art.gif",
    save_all=True,
    append_images=frames[1:],
    duration=frame_duration,
    loop=0,
    disposal=2
)
print("Saved ultimate_exhaustive_generative_art.gif")