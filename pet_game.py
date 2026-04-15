import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QFrame, 
                             QGraphicsDropShadowEffect, QScrollArea, QSizePolicy,
                             QGraphicsOpacityEffect)
from PyQt5.QtCore import (Qt, QSize, QPropertyAnimation, QEasingCurve, 
                         QTimer, pyqtSignal, QPoint, QByteArray)
from PyQt5.QtGui import QFont, QColor, QPixmap, QPainter


ASSETS_DIR = "assets"

def create_pet_images():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    from PIL import Image, ImageDraw, ImageFont
    
    def create_image(filename, emoji, bg_color):
        size = 200
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([5, 5, size-5, size-5], fill=bg_color, outline="#2C3E50", width=4)
        draw.ellipse([15, 15, size-15, size-15], fill=bg_color)
        try:
            emoji_font = ImageFont.truetype("seguiemj.ttf", 100)
        except:
            emoji_font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), emoji, font=emoji_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) // 2
        y = (size - text_height) // 2 - 15
        draw.text((x, y), emoji, font=emoji_font, embedded_color=True)
        img.save(filename)
        
        small = img.resize((80, 80), Image.Resampling.LANCZOS)
        small.save(filename.replace('.png', '_small.png'))
    
    pets = [("cat", "🐱", "#FFE4B5"), ("dog", "🐶", "#B0E0E6"), ("rabbit", "🐰", "#E6E6FA")]
    for name, emoji, color in pets:
        create_image(f"{ASSETS_DIR}/{name}.png", emoji, color)


class AnimatedButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(15)
        self._shadow.setColor(QColor(0, 0, 0, 80))
        self._shadow.setOffset(0, 4)
        self.setGraphicsEffect(self._shadow)
        
    def enterEvent(self, event):
        self._shadow.setBlurRadius(25)
        self._shadow.setOffset(0, 2)
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self._shadow.setBlurRadius(15)
        self._shadow.setOffset(0, 4)
        super().leaveEvent(event)


class ProgressBar(QFrame):
    def __init__(self, label, color):
        super().__init__()
        self.color = color
        self.setFixedHeight(30)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        
        self.name_label = QLabel(label)
        self.name_label.setFont(QFont("Arial", 11))
        self.name_label.setStyleSheet("color: white;")
        self.name_label.setMinimumWidth(100)
        layout.addWidget(self.name_label)
        
        self.bar_bg = QFrame()
        self.bar_bg.setStyleSheet("background: rgba(255,255,255,30); border-radius: 8px;")
        self.bar_bg.setMinimumHeight(16)
        layout.addWidget(self.bar_bg, 1)
        
        self.value_label = QLabel("50")
        self.value_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.value_label.setStyleSheet("color: white;")
        self.value_label.setMinimumWidth(35)
        layout.addWidget(self.value_label)
        
    def setValue(self, value):
        value = max(0, min(100, value))
        self.value_label.setText(str(value))
        
        if value >= 70:
            bar_color = "#4CAF50"
        elif value >= 40:
            bar_color = "#FFC107"
        else:
            bar_color = "#f44336"
        
        self.bar_bg.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {bar_color}, stop:1 {bar_color}88);
                border-radius: 8px;
            }}
        """)


class PetCard(QFrame):
    clicked = pyqtSignal(object)
    
    def __init__(self, pet):
        super().__init__()
        self.pet = pet
        self.setFixedHeight(80)
        self.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,15);
                border-radius: 12px;
            }
            QFrame:hover {
                background: rgba(255,255,255,25);
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        
        img_path = f"{ASSETS_DIR}/{pet.emoji}_small.png"
        if os.path.exists(img_path):
            self.img_label = QLabel()
            pixmap = QPixmap(img_path).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.img_label.setPixmap(pixmap)
        else:
            self.img_label = QLabel("🐾")
            self.img_label.setFont(QFont("", 25))
        self.img_label.setStyleSheet("background: transparent;")
        layout.addWidget(self.img_label)
        
        info = QVBoxLayout()
        info.setSpacing(2)
        
        name = QLabel(pet.name)
        name.setFont(QFont("Arial", 13, QFont.Bold))
        name.setStyleSheet("color: white; background: transparent;")
        info.addWidget(name)
        
        info2 = QLabel(f"{pet.pet_type}, {pet.age} лет")
        info2.setFont(QFont("Arial", 10))
        info2.setStyleSheet("color: rgba(255,255,255,150); background: transparent;")
        info.addWidget(info2)
        
        layout.addLayout(info)
        layout.addStretch()
        
        btn = AnimatedButton("Выбрать")
        btn.setFixedSize(90, 32)
        btn.setFont(QFont("Arial", 10))
        btn.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                border-radius: 16px;
                border: none;
            }
            QPushButton:hover {
                background: #2980b9;
            }
        """)
        btn.clicked.connect(lambda: self.clicked.emit(pet))
        layout.addWidget(btn)
        
    def set_selected(self, selected):
        if selected:
            self.setStyleSheet("""
                QFrame {
                    background: rgba(52,152,219,60);
                    border: 2px solid #3498db;
                    border-radius: 12px;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background: rgba(255,255,255,15);
                    border-radius: 12px;
                }
                QFrame:hover {
                    background: rgba(255,255,255,25);
                }
            """)


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
        return "Покормлен!"

    def play(self):
        self.mood = min(100, self.mood + 15)
        self.energy = max(0, self.energy - 10)
        self.hunger = min(100, self.hunger + 10)
        return "Поиграл!"

    def sleep(self):
        self.energy = min(100, self.energy + 30)
        self.health = min(100, self.health + 5)
        return "Отдохнул!"

    def walk(self):
        self.energy = max(0, self.energy - 15)
        self.mood = min(100, self.mood + 10)
        self.health = min(100, self.health + 5)
        return "Прогулялся!"

    def get_status(self):
        if self.health < 30: return "Болеет!", "#f44336"
        elif self.energy < 20: return "Устал", "#FFC107"
        elif self.hunger > 80: return "Голодный", "#FF9800"
        elif self.mood < 30: return "Грустный", "#9C27B0"
        return "Счастлив", "#4CAF50"


class PetGame(QMainWindow):
    def __init__(self):
        super().__init__()
        create_pet_images()
        
        self.setWindowTitle("Менеджер питомцев")
        self.resize(900, 600)
        self.setMinimumSize(800, 500)
        self.setStyleSheet("background: #1a1a2e;")
        
        self.pets = []
        self.selected_pet = None
        self.pet_cards = []
        
        self.setup_ui()
        self.create_pets()
        
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        left = self.create_left_panel()
        main_layout.addWidget(left, 1)
        
        right = self.create_right_panel()
        main_layout.addWidget(right, 2)
        
    def create_left_panel(self):
        panel = QFrame()
        panel.setStyleSheet("background: #16213e; border-radius: 15px;")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("Мои питомцы")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.pets_container = QScrollArea()
        self.pets_container.setWidgetResizable(True)
        self.pets_container.setStyleSheet("background: transparent; border: none;")
        self.pets_container.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        pets_widget = QWidget()
        self.pets_layout = QVBoxLayout(pets_widget)
        self.pets_layout.setSpacing(10)
        self.pets_layout.addStretch()
        
        self.pets_container.setWidget(pets_widget)
        layout.addWidget(self.pets_container)
        
        return panel
    
    def create_right_panel(self):
        panel = QFrame()
        panel.setStyleSheet("background: #16213e; border-radius: 15px;")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        self.pet_name_label = QLabel("Выберите питомца")
        self.pet_name_label.setFont(QFont("Arial", 22, QFont.Bold))
        self.pet_name_label.setStyleSheet("color: white;")
        self.pet_name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.pet_name_label)
        
        self.pet_image_label = QLabel()
        self.pet_image_label.setAlignment(Qt.AlignCenter)
        self.pet_image_label.setFixedHeight(150)
        self.pet_image_label.setStyleSheet("background: transparent;")
        layout.addWidget(self.pet_image_label)
        
        self.status_label = QLabel()
        self.status_label.setFont(QFont("Arial", 14))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #4CAF50;")
        layout.addWidget(self.status_label)
        
        stats = QFrame()
        stats.setStyleSheet("background: rgba(255,255,255,10); border-radius: 10px;")
        stats_layout = QVBoxLayout(stats)
        stats_layout.setSpacing(8)
        
        self.bars = {
            "hunger": ProgressBar("Голод", "#FF9800"),
            "mood": ProgressBar("Настроение", "#E91E63"),
            "energy": ProgressBar("Энергия", "#9C27B0"),
            "health": ProgressBar("Здоровье", "#f44336")
        }
        
        for bar in self.bars.values():
            stats_layout.addWidget(bar)
            
        layout.addWidget(stats)
        
        actions = QHBoxLayout()
        actions.setSpacing(10)
        
        self.action_btns = []
        acts = [("Покормить", "#4CAF50", "feed"), ("Поиграть", "#2196F3", "play"),
                ("Спать", "#9C27B0", "sleep"), ("Гулять", "#FF9800", "walk")]
        
        for text, color, action in acts:
            btn = self.make_btn(text, color, action)
            self.action_btns.append(btn)
            actions.addWidget(btn)
            
        layout.addLayout(actions)
        
        return panel
    
    def make_btn(self, text, color, action):
        btn = AnimatedButton(text)
        btn.setFixedHeight(50)
        btn.setFont(QFont("Arial", 11, QFont.Bold))
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {color};
                color: white;
                border-radius: 12px;
                border: none;
            }}
            QPushButton:hover {{
                background: {color}cc;
            }}
        """)
        btn.clicked.connect(lambda: self.do_action(action))
        return btn
    
    def create_pets(self):
        self.pets = [
            Pet("Барсик", "кот", 2, "cat"),
            Pet("Рекс", "пёс", 3, "dog"),
            Pet("Пушистик", "кролик", 1, "rabbit")
        ]
        
        for pet in self.pets:
            card = PetCard(pet)
            card.clicked.connect(self.select_pet)
            self.pets_layout.insertWidget(self.pets_layout.count() - 1, card)
            self.pet_cards.append(card)
            
        self.select_pet(self.pets[0])
    
    def select_pet(self, pet):
        self.selected_pet = pet
        
        for card in self.pet_cards:
            card.set_selected(card.pet == pet)
        
        self.pet_name_label.setText(f"{pet.name}")
        
        img_path = f"{ASSETS_DIR}/{pet.emoji}.png"
        if os.path.exists(img_path):
            pixmap = QPixmap(img_path).scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.pet_image_label.setPixmap(pixmap)
        
        status, color = pet.get_status()
        self.status_label.setText(status)
        self.status_label.setStyleSheet(f"color: {color};")
        
        self.bars["hunger"].setValue(pet.hunger)
        self.bars["mood"].setValue(pet.mood)
        self.bars["energy"].setValue(pet.energy)
        self.bars["health"].setValue(pet.health)
    
    def do_action(self, name):
        if not self.selected_pet:
            return
        action = getattr(self.selected_pet, name)
        action()
        self.select_pet(self.selected_pet)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = PetGame()
    window.show()
    sys.exit(app.exec_())