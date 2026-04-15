import tkinter as tk
from tkinter import font as tkfont
import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = "assets"

def create_pet_images():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    
    def create_image(filename, emoji, bg_color):
        size = 150
        img = Image.new('RGBA', (size, size), bg_color)
        draw = ImageDraw.Draw(img)
        try:
            emoji_font = ImageFont.truetype("seguiemj.ttf", 80)
        except:
            emoji_font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), emoji, font=emoji_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) // 2
        y = (size - text_height) // 2 - 10
        draw.text((x, y), emoji, font=emoji_font, embedded_color=True)
        img.save(filename)
    
    create_image(f"{ASSETS_DIR}/cat.png", "🐱", "#FFE4B5")
    create_image(f"{ASSETS_DIR}/dog.png", "🐶", "#B0E0E6")
    create_image(f"{ASSETS_DIR}/rabbit.png", "🐰", "#E6E6FA")
    create_image(f"{ASSETS_DIR}/hamster.png", "🐹", "#FFDAB9")
    create_image(f"{ASSETS_DIR}/bird.png", "🐦", "#98FB98")
    create_image(f"{ASSETS_DIR}/fish.png", "🐟", "#87CEEB")


class Pet:
    def __init__(self, name, pet_type, age, emoji):
        self.name = name
        self.pet_type = pet_type
        self.age = age
        self.emoji = emoji
        self.hunger = 50
        self.mood = 50
        self.energy = 50
        self.health = 100

    def feed(self):
        self.hunger = max(0, self.hunger - 15)
        self.health = min(100, self.health + 5)

    def play(self):
        self.mood = min(100, self.mood + 15)
        self.energy = max(0, self.energy - 10)
        self.hunger = min(100, self.hunger + 10)

    def sleep(self):
        self.energy = min(100, self.energy + 30)
        self.health = min(100, self.health + 5)

    def walk(self):
        self.energy = max(0, self.energy - 15)
        self.mood = min(100, self.mood + 10)
        self.health = min(100, self.health + 5)

    def get_status_color(self, value):
        if value >= 70:
            return "#4CAF50"
        elif value >= 40:
            return "#FFC107"
        else:
            return "#f44336"

    def get_status_text(self):
        if self.health < 30:
            return "😢 Болеет!"
        elif self.energy < 20:
            return "😴 Устал"
        elif self.hunger > 80:
            return "🍖 Голодный"
        elif self.mood < 30:
            return "😿 Грустный"
        else:
            return "😊 Счастлив"


class PetGame:
    def __init__(self):
        create_pet_images()
        
        self.root = tk.Tk()
        self.root.title("🏠 Менеджер питомцев")
        self.root.geometry("900x700")
        self.root.configure(bg="#2C3E50")
        self.root.resizable(False, False)
        
        self.pets = []
        self.selected_pet = None
        self.pet_buttons = []
        self.status_labels = []
        
        self.setup_ui()
        self.create_pets()
        self.update_ui()
        
    def setup_ui(self):
        title_font = tkfont.Font(family="Arial", size=24, weight="bold")
        btn_font = tkfont.Font(family="Arial", size=12, weight="bold")
        label_font = tkfont.Font(family="Arial", size=11)
        
        header = tk.Frame(self.root, bg="#34495E", height=80)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="🏠 Мой питомник", font=title_font, 
                        bg="#34495E", fg="white")
        title.pack(pady=20)
        
        main_frame = tk.Frame(self.root, bg="#2C3E50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        left_panel = tk.Frame(main_frame, bg="#34495E", width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        pets_label = tk.Label(left_panel, text="🐾 Мои питомцы", font=title_font,
                             bg="#34495E", fg="white")
        pets_label.pack(pady=15)
        
        self.pets_container = tk.Frame(left_panel, bg="#34495E")
        self.pets_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        right_panel = tk.Frame(main_frame, bg="#34495E")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.pet_display = tk.Label(right_panel, text="Выберите питомца", 
                                   font=title_font, bg="#34495E", fg="white")
        self.pet_display.pack(pady=10)
        
        self.pet_image_label = tk.Label(right_panel, bg="#2C3E50", width=15, height=8)
        self.pet_image_label.pack(pady=10)
        
        self.status_label = tk.Label(right_panel, text="", font=("Arial", 16),
                                    bg="#34495E", fg="#FFD700")
        self.status_label.pack()
        
        self.stats_frame = tk.Frame(right_panel, bg="#34495E")
        self.stats_frame.pack(pady=15, fill=tk.X, padx=20)
        
        self.stat_labels = {}
        stat_names = [("🍖 Голод", "hunger"), ("😊 Настроение", "mood"), 
                     ("⚡ Энергия", "energy"), ("❤️ Здоровье", "health")]
        
        for name, key in stat_names:
            frame = tk.Frame(self.stats_frame, bg="#34495E")
            frame.pack(fill=tk.X, pady=3)
            tk.Label(frame, text=name, font=label_font, bg="#34495E", 
                    fg="white", width=15, anchor='w').pack(side=tk.LEFT)
            bar_frame = tk.Frame(frame, bg="#1a1a1a", height=20, width=200)
            bar_frame.pack(side=tk.LEFT)
            bar_frame.pack_propagate(False)
            self.stat_labels[key] = tk.Frame(bar_frame, bg="#4CAF50", height=20)
            self.stat_labels[key].pack(side=tk.LEFT)
            self.stat_labels[f"{key}_label"] = tk.Label(bar_frame, text="50", 
                            bg="#1a1a1a", fg="white", width=5)
            self.stat_labels[f"{key}_label"].pack(side=tk.LEFT, padx=5)
        
        actions_frame = tk.Frame(right_panel, bg="#34495E")
        actions_frame.pack(pady=20)
        
        actions = [("🍖 Покормить", self.feed), ("🎮 Поиграть", self.play),
                  ("😴 Уложить спать", self.sleep), ("🚶 Выгулять", self.walk)]
        
        for i, (text, cmd) in enumerate(actions):
            btn = tk.Button(actions_frame, text=text, font=btn_font, 
                           bg="#27AE60", fg="white", width=12, height=2,
                           relief=tk.FLAT, cursor="hand2", command=cmd)
            btn.grid(row=0, column=i, padx=5, pady=5)
            
    def create_pets(self):
        self.pets = [
            Pet("Барсик", "кот 🐱", 2, "cat"),
            Pet("Рекс", "пёс 🐶", 3, "dog"),
            Pet("Пушистик", "кролик 🐰", 1, "rabbit")
        ]
        if self.selected_pet is None:
            self.selected_pet = self.pets[0]
            
    def load_pet_image(self, pet_type):
        img_path = f"{ASSETS_DIR}/{pet_type}.png"
        if os.path.exists(img_path):
            img = Image.open(img_path)
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            self.pet_photo = tk.PhotoImage(img)
            self.pet_image_label.config(image=self.pet_photo)
            
    def update_ui(self):
        for widget in self.pets_container.winfo_children():
            widget.destroy()
        self.pet_buttons = []
        
        for pet in self.pets:
            frame = tk.Frame(self.pets_container, bg="#3D566E", relief=tk.RAISED, bd=2)
            frame.pack(fill=tk.X, pady=5, padx=10)
            
            img_path = f"{ASSETS_DIR}/{pet.emoji}.png"
            if os.path.exists(img_path):
                img = Image.open(img_path)
                img = img.resize((50, 50), Image.Resampling.LANCZOS)
                photo = tk.PhotoImage(img)
                img_label = tk.Label(frame, image=photo, bg="#3D566E")
                img_label.image = photo
                img_label.pack(side=tk.LEFT, padx=10, pady=5)
            
            info_frame = tk.Frame(frame, bg="#3D566E")
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)
            
            tk.Label(info_frame, text=f"{pet.name}", font=("Arial", 12, "bold"),
                    bg="#3D566E", fg="white").pack(anchor='w')
            tk.Label(info_frame, text=f"{pet.pet_type}, {pet.age} лет", 
                    font=("Arial", 9), bg="#3D566E", fg="#BDC3C7").pack(anchor='w')
            
            btn = tk.Button(frame, text="Выбрать", bg="#3498DB", fg="white",
                          relief=tk.FLAT, cursor="hand2",
                          command=lambda p=pet: self.select_pet(p))
            btn.pack(side=tk.RIGHT, padx=10)
            self.pet_buttons.append(btn)
            
        self.update_pet_display()
        
    def select_pet(self, pet):
        self.selected_pet = pet
        self.update_pet_display()
        
    def update_pet_display(self):
        if not self.selected_pet:
            return
            
        pet = self.selected_pet
        self.pet_display.config(text=f"{pet.emoji} {pet.name}")
        self.status_label.config(text=pet.get_status_text())
        self.load_pet_image(pet.emoji)
        
        stats = [("hunger", pet.hunger), ("mood", pet.mood), 
                ("energy", pet.energy), ("health", pet.health)]
        
        for key, value in stats:
            color = pet.get_status_color(value)
            self.stat_labels[key].config(bg=color, width=int(value * 2 / 10))
            self.stat_labels[f"{key}_label"].config(text=str(value))
            
    def perform_action(self, action_name):
        if not self.selected_pet:
            self.status_label.config(text="Сначала выберите питомца!")
            return
            
        action = getattr(self.selected_pet, action_name)
        action()
        self.update_pet_display()
        
    def feed(self):
        self.perform_action("feed")
        
    def play(self):
        self.perform_action("play")
        
    def sleep(self):
        self.perform_action("sleep")
        
    def walk(self):
        self.perform_action("walk")
        
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = PetGame()
    game.run()
