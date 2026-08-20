__version__ = "0.1.0"

from kivy.config import Config
Config.set("graphics", "width", "854")
Config.set("graphics", "height", "480")
Config.set("graphics", "resizable", "1")

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
import random, math, json, os

WORLD_W, WORLD_H = 2200, 1600
ROAD_W = 120
FPS = 45

class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.px, self.py = 420.0, 300.0
        self.in_car = False
        self.car = None
        self.angle = 0.0
        self.car_speed = 0.0
        self.score = 0
        self.money = 0
        self.best = 0
        self.keys = {"up":False,"down":False,"left":False,"right":False}
        self.vroads = [260, 720, 1180, 1640]
        self.hroads = [220, 620, 1020, 1420]
        self.cars = [
            {"x":260.0,"y":390.0,"angle":0.0,"speed":0.0,"color":(0.15,0.45,0.9)},
            {"x":720.0,"y":470.0,"angle":90.0,"speed":1.5,"color":(0.9,0.2,0.2)},
            {"x":1180.0,"y":850.0,"angle":0.0,"speed":1.5,"color":(0.95,0.75,0.1)},
            {"x":1640.0,"y":1250.0,"angle":90.0,"speed":1.5,"color":(0.2,0.75,0.55)},
        ]
        self.buildings = []
        for x in range(0, WORLD_W, 220):
            for y in range(0, WORLD_H, 200):
                cx, cy = x+100, y+90
                near = any(abs(cx-r) < ROAD_W for r in self.vroads) or any(abs(cy-r) < ROAD_W for r in self.hroads)
                if not near and random.random() < 0.7:
                    self.buildings.append((x+18,y+18,180,160))
        self.info = Label(text="City Drive Mobile  •  خفيفة", size_hint=(None,None),
                          size=(330,40), pos=(10,430), color=(1,1,1,1))
        self.add_widget(self.info)

        self.make_button("▲", 0.08, 0.18, "up")
        self.make_button("▼", 0.08, 0.04, "down")
        self.make_button("◀", 0.01, 0.11, "left")
        self.make_button("▶", 0.15, 0.11, "right")
        self.e_btn = Button(text="E", size_hint=(None,None), size=(72,72),
                            pos_hint={"right":0.96,"y":0.10})
        self.e_btn.bind(on_press=lambda *_: self.toggle_car())
        self.add_widget(self.e_btn)

        Clock.schedule_interval(self.update, 1/FPS)

    def make_button(self, text, x, y, key):
        b = Button(text=text, size_hint=(None,None), size=(70,70),
                   pos_hint={"x":x,"y":y})
        b.bind(on_press=lambda *_: self.set_key(key, True))
        b.bind(on_release=lambda *_: self.set_key(key, False))
        self.add_widget(b)

    def set_key(self, key, value):
        self.keys[key] = value

    def toggle_car(self):
        if self.in_car:
            self.in_car = False
            self.px += 48
            self.car = None
            self.car_speed = 0
            return
        nearest = min(self.cars, key=lambda c: math.hypot(c["x"]-self.px,c["y"]-self.py))
        if math.hypot(nearest["x"]-self.px, nearest["y"]-self.py) < 85:
            self.in_car = True
            self.car = nearest

    def on_touch_down(self, touch):
        return super().on_touch_down(touch)

    def is_road(self, x, y):
        return any(abs(x-r)<ROAD_W/2 for r in self.vroads) or any(abs(y-r)<ROAD_W/2 for r in self.hroads)

    def update(self, dt):
        if self.in_car:
            if self.keys["left"]: self.angle -= 3.2
            if self.keys["right"]: self.angle += 3.2
            if self.keys["up"]: self.car_speed = min(7.0, self.car_speed+0.22)
            elif self.keys["down"]: self.car_speed = max(-3.0, self.car_speed-0.22)
            else: self.car_speed *= 0.94
            r = math.radians(self.angle)
            self.car["x"] += math.sin(r)*self.car_speed
            self.car["y"] -= math.cos(r)*self.car_speed
            self.car["x"] = max(20,min(WORLD_W-20,self.car["x"]))
            self.car["y"] = max(20,min(WORLD_H-20,self.car["y"]))
            self.px, self.py = self.car["x"], self.car["y"]
            self.score += int(abs(self.car_speed)*dt*3)
        else:
            dx = (self.keys["right"]-self.keys["left"])*4
            dy = (self.keys["up"]-self.keys["down"])*4
            if dx and dy: dx *= .707; dy *= .707
            self.px = max(15,min(WORLD_W-15,self.px+dx))
            self.py = max(15,min(WORLD_H-15,self.py))

        for c in self.cars:
            if c is not self.car:
                r=math.radians(c["angle"])
                c["x"] += math.sin(r)*c["speed"]
                c["y"] -= math.cos(r)*c["speed"]
                if c["x"]<0: c["x"]=WORLD_W
                if c["x"]>WORLD_W: c["x"]=0
                if c["y"]<0: c["y"]=WORLD_H
                if c["y"]>WORLD_H: c["y"]=0

        self.info.text = f"City Drive Mobile   نقاط: {self.score}   💰 ${self.money}"
        self.draw()

    def draw(self):
        self.canvas.clear()
        camx=max(0,min(WORLD_W-self.width,self.px-self.width/2))
        camy=max(0,min(WORLD_H-self.height,self.py-self.height/2))
        with self.canvas:
            Color(.22,.55,.27); Rectangle(pos=(0,0),size=self.size)
            Color(.25,.26,.28)
            for r in self.vroads: Rectangle(pos=(r-ROAD_W/2-camx,-camy),size=(ROAD_W,WORLD_H))
            for r in self.hroads: Rectangle(pos=(-camx,r-ROAD_W/2-camy),size=(WORLD_W,ROAD_W))
            Color(.7,.7,.7)
            for r in self.vroads: Line(points=(r-ROAD_W/2-camx,0,r-ROAD_W/2-camx,self.height),width=1.2)
            for r in self.hroads: Line(points=(0,r-ROAD_W/2-camy,self.width,r-ROAD_W/2-camy),width=1.2)
            for x,y,w,h in self.buildings:
                Color(.65,.58,.5); Rectangle(pos=(x-camx,y-camy),size=(w,h))
                Color(.1,.1,.1); Line(rectangle=(x-camx,y-camy,w,h),width=1)

            for c in self.cars:
                Color(*c["color"]); Rectangle(pos=(c["x"]-18-camx,c["y"]-30-camy),size=(36,60))
                Color(.05,.05,.05); Line(rectangle=(c["x"]-18-camx,c["y"]-30-camy,36,60),width=1)

            if not self.in_car:
                Color(.95,.78,.62); Ellipse(pos=(self.px-12-camx,self.py-12-camy),size=(24,24))
                Color(.15,.35,.8); Ellipse(pos=(self.px-10-camx,self.py-2-camy),size=(20,20))

            # mini map
            mx,my= self.width-145, self.height-135
            Color(.08,.08,.08); Rectangle(pos=(mx,my),size=(130,120))
            sx,sy=130/WORLD_W,120/WORLD_H
            Color(.8,.15,.15); Ellipse(pos=(mx+self.px*sx-4,my+self.py*sy-4),size=(8,8))

class CityDriveApp(App):
    def build(self):
        Window.fullscreen = "auto"
        return Game()

if __name__ == "__main__":
    CityDriveApp().run()
