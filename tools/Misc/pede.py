import os
from io import BytesIO
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.graphics import Rectangle
from PIL import Image as PILImage, ImageDraw, ImageFont
from kivy.core.image import Image as CoreImage

# --- Config ---
BASE_DIR = os.getcwd()
page_files = sorted([f for f in os.listdir(BASE_DIR) if f.lower().endswith(".png")])
if not page_files:
    raise FileNotFoundError("No PNG pages found in current directory.")

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 36  # final PDF font size

# --- PDF Canvas ---
class PDFCanvas(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.overlays = []  # list of dicts: {"x", "y", "text", "width", "height"}
        self.original_size = (1,1)
        self.scale_x = 1
        self.scale_y = 1
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = None  # currently dragged annotation

    def update_scaling(self):
        if not self.texture:
            return
        img_w, img_h = self.texture.size
        self.scale_x = self.original_size[0] / img_w
        self.scale_y = self.original_size[1] / img_h
        self.offset_x = (self.width - img_w) / 2
        self.offset_y = (self.height - img_h) / 2

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)

        self.update_scaling()
        scale_factor = (self.scale_x + self.scale_y)/2

        # Check if touching an existing annotation (drag)
        for ann in reversed(self.overlays):
            x, y, w, h = ann["x"], ann["y"], ann["width"], ann["height"]
            display_x = x / self.scale_x + self.offset_x
            display_y = (self.original_size[1] - y) / self.scale_y + self.offset_y
            if display_x <= touch.x - self.x <= display_x + w and display_y <= touch.y - self.y <= display_y + h:
                self.dragging = ann
                self.drag_offset = (touch.x - self.x - display_x, touch.y - self.y - display_y)
                return True

        # Add new annotation
        app = App.get_running_app()
        text = app.text_input.text.strip()
        if text:
            img_x = (touch.x - self.x - self.offset_x) * self.scale_x
            img_y = self.original_size[1] - ((touch.y - self.y - self.offset_y) * self.scale_y)
            tex = app.label_to_texture(text, scale=scale_factor)
            ann = {"x": img_x, "y": img_y, "text": text, "width": tex.width, "height": tex.height}
            self.overlays.append(ann)
            self.draw_overlays()
            app.show_popup(f"Placed annotation at ({int(img_x)}, {int(img_y)})")
        return True

    def on_touch_move(self, touch):
        if self.dragging:
            self.update_scaling()
            dx, dy = self.drag_offset
            img_x = (touch.x - self.x - self.offset_x - dx) * self.scale_x
            img_y = self.original_size[1] - ((touch.y - self.y - self.offset_y - dy) * self.scale_y)
            self.dragging["x"] = img_x
            self.dragging["y"] = img_y
            self.draw_overlays()
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.dragging:
            self.dragging = None
            return True
        return super().on_touch_up(touch)

    def draw_overlays(self):
        self.canvas.after.clear()
        self.update_scaling()
        scale_factor = (self.scale_x + self.scale_y)/2
        with self.canvas.after:
            for ann in self.overlays:
                x, y, text = ann["x"], ann["y"], ann["text"]
                tex = App.get_running_app().label_to_texture(text, scale=scale_factor)
                ann["width"] = tex.width
                ann["height"] = tex.height
                display_x = x / self.scale_x + self.offset_x
                display_y = (self.original_size[1] - y) / self.scale_y + self.offset_y
                Rectangle(texture=tex, pos=(self.x + display_x, self.y + display_y), size=(tex.width, tex.height))

# --- PDF Editor App ---
class PDFEditorApp(App):
    def build(self):
        self.page_index = 0
        self.annotations = {}      # overlays per page
        self.page_textures = {}    # in-memory PIL images

        root = BoxLayout(orientation="vertical")

        # Controls
        ctrl = BoxLayout(size_hint=(1, 0.1))
        self.text_input = TextInput(hint_text="Type text and tap page", multiline=True)
        prev_btn = Button(text="Prev Page", on_release=self.prev_page)
        next_btn = Button(text="Next Page", on_release=self.next_page)
        save_btn = Button(text="Save PDF", on_release=self.save_pdf)
        ctrl.add_widget(self.text_input)
        ctrl.add_widget(prev_btn)
        ctrl.add_widget(next_btn)
        ctrl.add_widget(save_btn)

        # Canvas
        self.canvas_img = PDFCanvas()
        scroll = ScrollView(size_hint=(1, 0.9))
        scroll.add_widget(self.canvas_img)

        root.add_widget(ctrl)
        root.add_widget(scroll)

        self.load_pages()
        self.show_page()
        return root

    def load_pages(self):
        # Load all pages in-memory
        for path in page_files:
            pil_img = PILImage.open(path).convert("RGB")
            self.page_textures[path] = pil_img

    def show_page(self):
        img_path = page_files[self.page_index]
        pil_img = self.page_textures[img_path]
        self.canvas_img.original_size = pil_img.size

        # Resize for preview
        preview = pil_img.copy()
        preview.thumbnail((800, 1200), PILImage.LANCZOS)

        # Convert PIL to Kivy texture
        data = BytesIO()
        preview.save(data, format="png")
        data.seek(0)
        core_img = CoreImage(data, ext="png")
        self.canvas_img.texture = core_img.texture
        self.canvas_img.overlays = self.annotations.get(self.page_index, [])
        self.canvas_img.draw_overlays()

    def prev_page(self, *_):
        self.annotations[self.page_index] = self.canvas_img.overlays
        if self.page_index > 0:
            self.page_index -= 1
            self.show_page()

    def next_page(self, *_):
        self.annotations[self.page_index] = self.canvas_img.overlays
        if self.page_index < len(page_files)-1:
            self.page_index += 1
            self.show_page()

    def save_pdf(self, *_):
        self.annotations[self.page_index] = self.canvas_img.overlays
        output_pdf = os.path.join(BASE_DIR, "annotated.pdf")
        pil_pages = []

        for i, img_file in enumerate(page_files):
            pil_img = self.page_textures[img_file].copy()
            draw = ImageDraw.Draw(pil_img)
            for ann in self.annotations.get(i, []):
                try:
                    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
                except:
                    font = ImageFont.load_default()
                draw.multiline_text((ann["x"], ann["y"] - FONT_SIZE), ann["text"], font=font, fill="red")
            pil_pages.append(pil_img)

        pil_pages[0].save(output_pdf, save_all=True, append_images=pil_pages[1:])
        self.show_popup(f"PDF saved: {output_pdf}")

    def show_popup(self, message):
        popup = Popup(title="Info", content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

    def label_to_texture(self, text, scale=1.0):
        from kivy.core.text import Label as CoreLabel
        font_size = max(1, int(FONT_SIZE / scale))  # scaled for preview
        label = CoreLabel(text=text, font_size=font_size, color=(1,0,0,1))
        label.refresh()
        return label.texture

if __name__ == "__main__":
    PDFEditorApp().run()