import os
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from PIL import Image as PILImage, ImageDraw, ImageFont

BASE_DIR = os.getcwd()
page_files = sorted([f for f in os.listdir(BASE_DIR) if f.lower().endswith(".png")])
if not page_files:
    raise FileNotFoundError("No PNG pages found in current directory.")

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 36

class PDFCanvas(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.overlays = []
        self.original_size = (1,1)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            app = App.get_running_app()
            text = app.text_input.text.strip()
            if text:
                # Map touch to original image size with offset correction
                img_w, img_h = self.texture.size
                offset_x = (self.width - img_w) / 2
                offset_y = (self.height - img_h) / 2
                img_x = (touch.x - self.x - offset_x) * (self.original_size[0] / img_w)
                img_y = (touch.y - self.y - offset_y) * (self.original_size[1] / img_h)
                # Flip Y because Pillow has (0,0) at top-left
                img_y = self.original_size[1] - img_y
                self.overlays.append((img_x, img_y, text))
                self.draw_overlays()
                app.show_popup(f"Placed '{text}' at ({int(img_x)}, {int(img_y)})")
            return True
        return super().on_touch_down(touch)

    def draw_overlays(self):
        self.canvas.after.clear()
        with self.canvas.after:
            for x, y, text in self.overlays:
                scale_x = self.width / self.original_size[0]
                scale_y = self.height / self.original_size[1]
                display_x = x * scale_x
                display_y = (self.original_size[1] - y) * scale_y  # flip Y for display
                tex = App.get_running_app().label_to_texture(text)
                Rectangle(texture=tex, pos=(self.x + display_x, self.y + display_y), size=(tex.width, tex.height))

class PDFEditorApp(App):
    def build(self):
        self.page_index = 0
        self.annotations = {}  # overlays per page

        root = BoxLayout(orientation="vertical")

        # Controls
        ctrl = BoxLayout(size_hint=(1, 0.1))
        self.text_input = TextInput(hint_text="Type text and tap page", multiline=False)
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

        self.show_page()
        return root

    def show_page(self):
        img_path = page_files[self.page_index]
        pil_img = PILImage.open(img_path).convert("RGB")
        self.canvas_img.original_size = pil_img.size

        # Resize for preview
        pil_img.thumbnail((800,1200))
        pil_img.save("temp_preview.png")
        self.canvas_img.source = "temp_preview.png"
        self.canvas_img.reload()
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
            pil_img = PILImage.open(img_file).convert("RGB")
            draw = ImageDraw.Draw(pil_img)
            for x, y, text in self.annotations.get(i, []):
                try:
                    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
                except:
                    font = ImageFont.load_default()
                draw.text((x, y - FONT_SIZE), text, font=font, fill="red")  # adjust Y
            pil_pages.append(pil_img)

        pil_pages[0].save(output_pdf, save_all=True, append_images=pil_pages[1:])
        self.show_popup(f"PDF saved: {output_pdf}")

    def show_popup(self, message):
        popup = Popup(title="Info",
                      content=TextInput(text=message, readonly=True),
                      size_hint=(0.8, 0.4))
        popup.open()

    def label_to_texture(self, text):
        from kivy.core.text import Label as CoreLabel
        label = CoreLabel(text=text, font_size=20, color=(1,0,0,1))
        label.refresh()
        return label.texture

if __name__ == "__main__":
    PDFEditorApp().run()