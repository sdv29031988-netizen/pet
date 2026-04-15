import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QFrame, 
                             QGraphicsDropShadowEffect, QScrollArea, QSizePolicy,
                             QGraphicsOpacityEffect)
from PyQt5.QtCore import (Qt, QSize, QPropertyAnimation, QRect, QEasingCurve, 
                         QParallelAnimationGroup, QSequentialAnimationGroup, 
                         QTimer, pyqtSignal, QObject, QPoint)
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QPixmap, QPainter, QPen
from PIL import Image, ImageDraw, ImageQt, ImageFont


ASSETS_DIR = "assets"

class Animator(QObject):
    pulse = pyqtSignal()
    
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.opacity = QGraphicsOpacityEffect(self)
        self.widget.setGraphicsEffect(self.opacity)
        self.opacity.setOpacity(1.0)
        
    def fade_in(self, duration=300):
        anim = QPropertyAnimation(self.opacity, b"opacity")
        anim.setDuration(duration)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.start()
        return anim
        
    def fade_out(self, duration=300):
        anim = QPropertyAnimation(self.opacity, b"opacity")
        anim.setDuration(duration)
        anim.setStartValue(1)
        anim.setEndValue(0)
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.start()
        return anim


def create_pet_images():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    
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
    
    pets = [
        ("cat", "🐱", "#FFE4B5"),
        ("dog", "🐶", "#B0E0E6"),
        ("rabbit", "🐰", "#E6E6FA"),
        ("hamster", "🐹", "#FFDAB9"),
        ("bird", "🐦", "#98FB98"),
        ("fish", "🐟", "#87CEEB")
    ]
    for name, emoji, color in pets:
        create_image(f"{ASSETS_DIR}/{name}.png", emoji, color)


class AnimatedButton(QPushButton):
    def __init__(self, text="", icon=None, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(15)
        self._shadow.setColor(QColor(0, 0, 0, 80))
        self._shadow.setOffset(0, 4)
        self.setGraphicsEffect(self._shadow)
        
    def enterEvent(self, event):
        self.animateShadow(0, 2, 20)
        self.setStyleSheet(self.styleSheet() + "transform: scale(1.05);")
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.animateShadow(0, 4, 15)
        self.setStyleSheet(self.styleSheet().replace("transform: scale(1.05);", ""))
        super().leaveEvent(event)
        
    def animateShadow(self, x, y, blur):
        self.anim_x = QPropertyAnimation(self._shadow, b"offset")
        self.anim_x.setDuration(200)
        self.anim_x.setStartValue(self._shadow.offset())
        self.anim_x.setEndValue(QPoint(x, y))
        self.anim_x.setEasingCurve(QEasingCurve.OutCubic)
        
        self.anim_b = QPropertyAnimation(self._shadow, b"blurRadius")
        self.anim_b.setDuration(200)
        self.anim_b.setStartValue(self._shadow.blurRadius())
        self.anim_b.setEndValue(blur)
        self.anim_b.setEasingCurve(QEasingCurve.OutCubic)
        
        group = QParallelAnimationGroup(self)
        group.addAnimation(self.anim_x)
        group.addAnimation(self.anim_b)
        group.start()


class ProgressBar(QFrame):
    def __init__(self, label, color, max_val=100):
        super().__init__()
        self.max_val = max_val
        self.current_val = 50
        self.color = color
        self.label_text = label
        
        self.setMinimumHeight(35)
        self.setMaximumHeight(35)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)
        
        self.name_label = QLabel(label)
        self.name_label.setFont(QFont("Segoe UI", 10, QFont.Medium))
        self.name_label.setMinimumWidth(120)
        self.name_label.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(self.name_label)
        
        self.bar_container = QFrame()
        self.bar_container.setFixedHeight(16)
        self.bar_container.setStyleSheet(f"""
            QFrame {{
                background: rgba(255,255,255,30);
                border-radius: 8px;
                border: 1px solid rgba(255,255,255,50);
            }}
        """)
        bar_layout = QVBoxLayout(self.bar_container)
        bar_layout.setContentsMargins(2, 2, 2, 2)
        
        self.bar = QFrame()
        self.bar.setFixedHeight(12)
        self.bar.setStyleSheet(f"""
            background: {color};
            border-radius: 6px;
        """)
        self.bar_layout = QHBoxLayout(self.bar)
        self.bar_layout.setContentsMargins(0, 0, 0, 0)
        self.bar_layout.addStretch()
        bar_layout.addWidget(self.bar)
        
        layout.addWidget(self.bar_container)
        
        self.value_label = QLabel("50")
        self.value_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.value_label.setMinimumWidth(40)
        self.value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.value_label.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(self.value_label)
        
    def setValue(self, value, animate=True):
        self.current_val = max(0, min(self.max_val, value))
        width = int((self.current_val / self.max_val) * (self.bar_container.width() - 4))
        
        if animate:
            self.anim = QPropertyAnimation(self.bar, b"minimumWidth")
            self.anim.setDuration(500)
            self.anim.setStartValue(self.bar.width())
            self.anim.setEndValue(max(20, width))
            self.anim.setEasingCurve(QEasingCurve.OutCubic)
            self.anim.start()
        
        color = self.get_color_for_value(self.current_val)
        self.bar.setStyleSheet(f"background: {color}; border-radius: 6px;")
        self.value_label.setText(str(self.current_val))
        
    def get_color_for_value(self, value):
        if value >= 70:
            return "#4CAF50"
        elif value >= 40:
            return "#FFC107"
        else:
            return "#f44336"
            
    def resizeEvent(self, event):
        self.setValue(self.current_val, animate=False)
        super().resizeEvent(event)


class PetCard(QFrame):
    clicked = pyqtSignal(object)
    
    def __init__(self, pet):
        super().__init__()
        self.pet = pet
        self.animator = Animator(self)
        self.setup_ui()
        
    def setup_ui(self):
        self.setFixedHeight(90)
        self.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,10);
                border-radius: 15px;
                border: 2px solid transparent;
            }
            QFrame:hover {
                background: rgba(255,255,255,20);
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        
        img_path = f"{ASSETS_DIR}/{self.pet.emoji}_small.png"
        if os.path.exists(img_path):
            self.img_label = QLabel()
            pixmap = QPixmap(img_path).scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.img_label.setPixmap(pixmap)
        else:
            self.img_label = QLabel("🐾")
            self.img_label.setFont(QFont("Segoe UI Emoji", 30))
        self.img_label.setFixedWidth(80)
        layout.addWidget(self.img_label)
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(3)
        
        self.name_label = QLabel(self.pet.name)
        self.name_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.name_label.setStyleSheet("color: white; background: transparent;")
        info_layout.addWidget(self.name_label)
        
        self.type_label = QLabel(self.pet.pet_type)
        self.type_label.setFont(QFont("Segoe UI", 11))
        self.type_label.setStyleSheet("color: rgba(255,255,255,150); background: transparent;")
        info_layout.addWidget(self.type_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        self.select_btn = AnimatedButton("Выбрать")
        self.select_btn.setFixedSize(100, 35)
        self.select_btn.setFont(QFont("Segoe UI", 10, QFont.Medium))
        self.select_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border-radius: 17px;
                border: none;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2980b9, stop:1 #3498db);
            }
        """)
        self.select_btn.clicked.connect(lambda: self.clicked.emit(self.pet))
        layout.addWidget(self.select_btn)
        
    def set_selected(self, selected):
        if selected:
            self.setStyleSheet("""
                QFrame {
                    background: rgba(52,152,219,50);
                    border-radius: 15px;
                    border: 2px solid #3498db;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background: rgba(255,255,255,10);
                    border-radius: 15px;
                    border: 2px solid transparent;
                }
                QFrame:hover {
                    background: rgba(255,255,255,20);
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
        return "🍼 Покормлен!"

    def play(self):
        self.mood = min(100, self.mood + 15)
        self.energy = max(0, self.energy - 10)
        self.hunger = min(100, self.hunger + 10)
        return "🎾 Поиграл!"

    def sleep(self):
        self.energy = min(100, self.energy + 30)
        self.health = min(100, self.health + 5)
        return "😴 Отдохнул!"

    def walk(self):
        self.energy = max(0, self.energy - 15)
        self.mood = min(100, self.mood + 10)
        self.health = min(100, self.health + 5)
        return "🚶 Прогулялся!"

    def get_status(self):
        if self.health < 30:
            return "😢 Болеет!", "#f44336"
        elif self.energy < 20:
            return "😴 Устал", "#FFC107"
        elif self.hunger > 80:
            return "🍖 Голодный", "#FF9800"
        elif self.mood < 30:
            return "😿 Грустный", "#9C27B0"
        return "😊 Счастлив", "#4CAF50"


class PetGame(QMainWindow):
    def __init__(self):
        super().__init__()
        create_pet_images()
        
        self.setWindowTitle("🏠 Менеджер питомцев")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet("background: #1a1a2e;")
        
        self.pets = []
        self.selected_pet = None
        self.pet_cards = []
        self.action_animations = []
        
        self.setup_ui()
        self.create_pets()
        self.update_pet_list()
        self.select_pet(self.pets[0])
        
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, stretch=1)
        
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, stretch=2)
        
    def create_left_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #16213e, stop:1 #1a1a2e);
                border-radius: 20px;
                border: 1px solid rgba(255,255,255,20);
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 25, 20, 20)
        
        title = QLabel("🐾 Мои питомцы")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: rgba(255,255,255,20);
                border-radius: 10px;
                width: 8px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255,255,25550);
                border-radius: 4px;
            }
        """)
        
        self.pets_container = QWidget()
        self.pets_layout = QVBoxLayout(self.pets_container)
        self.pets_layout.setSpacing(10)
        self.pets_layout.addStretch()
        
        scroll.setWidget(self.pets_container)
        layout.addWidget(scroll)
        
        return panel
    
    def create_right_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #16213e, stop:1 #1a1a2e);
                border-radius: 20px;
                border: 1px solid rgba(255,255,255,20);
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(30, 25, 30, 20)
        layout.setSpacing(15)
        
        self.pet_name_label = QLabel("Выберите питомца")
        self.pet_name_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
        self.pet_name_label.setStyleSheet("color: white; background: transparent;")
        self.pet_name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.pet_name_label)
        
        self.pet_image_label = QLabel()
        self.pet_image_label.setAlignment(Qt.AlignCenter)
        self.pet_image_label.setFixedSize(200, 200)
        self.pet_image_label.setStyleSheet("background: transparent;")
        layout.addWidget(self.pet_image_label)
        
        self.status_label = QLabel()
        self.status_label.setFont(QFont("Segoe UI", 16, QFont.Medium))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #4CAF50; background: transparent;")
        layout.addWidget(self.status_label)
        
        self.message_label = QLabel()
        self.message_label.setFont(QFont("Segoe UI", 14))
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("color: #FFD700; background: transparent;")
        self.message_label.setFixedHeight(30)
        layout.addWidget(self.message_label)
        
        stats_frame = QFrame()
        stats_frame.setStyleSheet("background: rgba(255,255,255,5); border-radius: 15px; padding: 10px;")
        stats_layout = QVBoxLayout(stats_frame)
        stats_layout.setSpacing(8)
        
        self.progress_bars = {
            "hunger": ProgressBar("🍖 Голод", "#FF9800"),
            "mood": ProgressBar("😊 Настроение", "#E91E63"),
            "energy": ProgressBar("⚡ Энергия", "#9C27B0"),
            "health": ProgressBar("❤️ Здоровье", "#f44336")
        }
        
        for bar in self.progress_bars.values():
            stats_layout.addWidget(bar)
            
        layout.addWidget(stats_frame)
        
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)
        
        self.action_buttons = []
        actions = [
            ("🍖", "Покормить", "#4CAF50", "feed"),
            ("🎮", "Поиграть", "#2196F3", "play"),
            ("😴", "Спать", "#9C27B0", "sleep"),
            ("🚶", "Гулять", "#FF9800", "walk")
        ]
        
        for icon, text, color, action in actions:
            btn = self.create_action_button(icon, text, color, action)
            self.action_buttons.append(btn)
            actions_layout.addWidget(btn)
            
        layout.addLayout(actions_layout)
        
        return panel
    
    def create_action_button(self, icon, text, color, action):
        btn = AnimatedButton()
        btn.setFixedHeight(60)
        btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn.setText(f"{icon}\n{text}")
        btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {color}, stop:1 {self.darken_color(color)});
                color: white;
                border-radius: 15px;
                border: none;
            }}
        """)
        btn.clicked.connect(lambda _, a=action: self.perform_action(a))
        return btn
    
    def darken_color(self, color):
        if color == "#4CAF50": return "#388E3C"
        if color == "#2196F3": return "#1976D2"
        if color == "#9C27B0": return "#7B1FA2"
        if color == "#FF9800": return "#F57C00"
        return color
    
    def create_pets(self):
        self.pets = [
            Pet("Барсик", "кот 🐱", 2, "cat"),
            Pet("Рекс", "пёс 🐶", 3, "dog"),
            Pet("Пушистик", "кролик 🐰", 1, "rabbit")
        ]
        
    def update_pet_list(self):
        while self.pets_layout.count() > 1:
            item = self.pets_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.pet_cards = []
        for pet in self.pets:
            card = PetCard(pet)
            card.clicked.connect(self.select_pet)
            self.pets_layout.insertWidget(self.pets_layout.count() - 1, card)
            self.pet_cards.append(card)
    
    def select_pet(self, pet):
        self.selected_pet = pet
        
        for card in self.pet_cards:
            card.set_selected(card.pet == pet)
        
        self.pet_name_label.setText(f"{self.get_pet_emoji(pet)} {pet.name}")
        
        img_path = f"{ASSETS_DIR}/{pet.emoji}.png"
        if os.path.exists(img_path):
            pixmap = QPixmap(img_path).scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.pet_image_label.setPixmap(pixmap)
        
        status, color = pet.get_status()
        self.status_label.setText(status)
        self.status_label.setStyleSheet(f"color: {color}; background: transparent; font-size: 18px;")
        
        self.update_stats()
        
    def get_pet_emoji(self, pet):
        emoji_map = {"cat": "🐱", "dog": "🐶", "rabbit": "🐰", "hamster": "🐹", "bird": "🐦", "fish": "🐟"}
        return emoji_map.get(pet.emoji, "🐾")
    
    def update_stats(self):
        if not self.selected_pet:
            return
        
        pet = self.selected_pet
        self.progress_bars["hunger"].setValue(pet.hunger)
        self.progress_bars["mood"].setValue(pet.mood)
        self.progress_bars["energy"].setValue(pet.energy)
        self.progress_bars["health"].setValue(pet.health)
        
    def perform_action(self, action_name):
        if not self.selected_pet:
            return
            
        action = getattr(self.selected_pet, action_name)
        message = action()
        
        self.message_label.setText(message)
        self.message_label.adjustSize()
        
        self.animate_message()
        self.update_stats()
        
        status, color = self.selected_pet.get_status()
        self.status_label.setText(status)
        self.status_label.setStyleSheet(f"color: {color}; background: transparent; font-size: 18px;")
        
    def animate_message(self):
        self.msg_anim = QPropertyAnimation(self.message_label, b"opacity")
        self.msg_anim.setDuration(2000)
        self.msg_anim.setStartValue(1.0)
        self.msg_anim.setKeyValueAt(0.5, 1.0)
        self.msg_anim.setEndValue(0.0)
        self.msg_anim.setEasingCurve(QEasingCurve.InQuad)
        self.msg_anim.start()
        
        self.msg_timer = QTimer()
        self.msg_timer.singleShot(2500, lambda: self.message_label.setText(""))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(26, 26, 46))
    app.setPalette(palette)
    
    window = PetGame()
    window.show()
    sys.exit(app.exec_())
