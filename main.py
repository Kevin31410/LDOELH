import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QLabel, QLineEdit,
                             QPushButton, QTextEdit, QGroupBox, QSpinBox,
                             QScrollArea, QFrame, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QPainter

import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# --- 1. CONFIGURATION COMPLÈTE DES COLLECTIONS ---
# type: "classic_df" (3 cases haut), "lone_wolf" (Action Chart), "generic" (Liste)
COLLECTIONS_DATA = {
    "Défis Fantastiques": {
        "type": "classic_df",  "stats": ["HABILETÉ", "ENDURANCE", "CHANCE"],
        "currency": "Pièces d'Or", "dice": "2d6"
    },
    "Sorcellerie!": {
        "type": "classic_df", "stats": ["HABILETÉ", "ENDURANCE", "CHANCE"],
        "currency": "Pièces d'Or", "dice": "2d6", "extra": "Livre des Sorts"
    },
    "Loup Solitaire": {
        "type": "lone_wolf", "stats": ["HABILETÉ", "ENDURANCE"],
        "currency": "Couronnes", "dice": "d10"
    },
    "Astre d'Or": {
        "type": "lone_wolf", "stats": ["VOLONTÉ", "ENDURANCE"],
        "currency": "Lunes", "dice": "d10", "extra_title": "Pouvoirs Magiques"
    },
    "La Voie du Tigre": {
        "type": "generic", "stats": ["Endurance", "Force Intérieure", "Destin"],
        "currency": "Or", "dice": "2d6", "special": "Techniques (Poing, Pied...)"
    },
    "L'épée de Légende": {
        "type": "generic", "stats": ["Habileté", "Endurance", "Chance"],
        "currency": "Pièces d'Or", "dice": "2d6", "special": "Classe (Guerrier, Voleur...)"
    },
    "Le Maitre du Destin": {
        "type": "generic", "stats": ["Habileté", "Endurance", "Indices"],
        "currency": "Livres Sterling", "dice": "2d6"
    },
    "Destin": {
        "type": "generic", "stats": ["Force", "Agilité", "Mental", "Vie"],
        "currency": "Crédits", "dice": "2d6", "special": "Compétences Informatiques"
    },
    "Métamorphoses": {
        "type": "generic", "stats": ["Physique", "Mental", "Chance"],
        "currency": "Troc", "dice": "2d6"
    },
    "Loup*Ardent": {
        "type": "generic",
        # Loup Ardent a beaucoup de stats, le mode "generic" va gérer les colonnes
        "stats": ["Force", "Rapidité", "Endurance", "Courage", "Chance", "Charme", "Habileté", "Pouvoir"],
        "currency": "Or", "dice": "2d6"
    },
    "Quête du Graal": {
        "type": "generic", "stats": ["Points de Vie"],
        "currency": "Pièces d'Or", "dice": "2d6", "special": "Sortilèges / Excalibur Jr."
    },
    "Les messagers du Temps": {
        "type": "classic_df", "stats": ["HABILETÉ", "ENDURANCE", "TEMPS"],
        "currency": "Or", "dice": "2d6"
    },
    "Défis et Sortilèges": {
        "type": "generic", "stats": ["Vie", "Magie", "Argent"],
        "currency": "Pièces", "dice": "2d6"
    },
    "Les Portes Interdites": {
        "type": "generic", "stats": ["Physique", "Mental"],
        "currency": "Dollars", "dice": "2d6", "special": "Santé Mentale / Indices"
    },
    "Epouvante!": {
        "type": "classic_df", "stats": ["HABILETÉ", "ENDURANCE", "PEUR"],
        "currency": "Or", "dice": "2d6"
    },
    "Histoire / Défis de l'Histoire": {
        "type": "generic", "stats": ["Habileté", "Endurance"],
        "currency": "Deniers", "dice": "2d6"
    },
    "Double Jeu": {
        "type": "generic", "stats": ["Habileté", "Endurance", "Force"],
        "currency": "Or", "dice": "2d6", "special": "Code Secret / Lien Partenaire"
    }
}


class AventureSheetFinal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bibliothèque des Héros - Complète")
        # On met une taille par défaut raisonnable, le script l'ajustera tout de suite après
        self.resize(650, 600)

        # Fond Parchemin
        self.background_pixmap = QPixmap(resource_path("parchemin.jpg"))
        self.use_bg = not self.background_pixmap.isNull()

        # --- STYLE VISUEL ---
        self.setStyleSheet("""
            QMainWindow { background: transparent; }
            QScrollArea, QWidget#Container, QWidget#SheetWidget { background: transparent; border: none; }

            QGroupBox {
                font-family: "Garamond", serif; font-size: 15px; font-weight: bold;
                text-transform: uppercase;
                border: 3px double #3d2b1f; border-radius: 4px; margin-top: 20px;
                background-color: rgba(255, 250, 240, 150); padding: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin; subcontrol-position: top center;
                background-color: #fdf5e6; padding: 0 10px; color: #2b1d15; border: 1px solid #3d2b1f;
            }
            QLabel { color: #1a110d; font-family: "Georgia", serif; font-size: 12px; font-weight: bold; }

            QLineEdit {
                background: transparent; border: none; border-bottom: 2px solid #5c4a3d;
                font-family: "Courier New", monospace; font-size: 13px; font-weight: bold; color: #000080;
            }
            QLineEdit:focus { border-bottom: 2px solid #b22222; }

            QSpinBox { background: rgba(255,255,255,0.4); border: 1px solid #5c4a3d; font-weight: bold; }

            QPushButton {
                background-color: #4a3c31; color: #f5deb3;
                border: 2px outset #6b5b4e; border-radius: 4px;
                font-weight: bold; padding: 6px;
            }
            QPushButton:pressed { border-style: inset; }
        """)

        # Main Container
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.setCentralWidget(self.scroll)

        self.container = QWidget()
        self.container.setObjectName("Container")
        self.main_layout = QVBoxLayout(self.container)
        self.scroll.setWidget(self.container)

        # Top Bar
        self.create_top_bar()

        # Placeholder pour la feuille active
        self.current_sheet_widget = None

        # Lancement par défaut
        self.load_interface("Défis Fantastiques")

    def adjust_window_size(self):
        """Redimensionne la fenêtre principale selon le contenu, sans dépasser l'écran."""
        # 1. On force la mise à jour de la géométrie pour avoir les bonnes mesures
        self.current_sheet_widget.adjustSize()
        self.container.adjustSize()

        # 2. On récupère la hauteur souhaitée par le contenu
        # Hauteur du contenu + Hauteur de la barre du haut (approx 70px) + Marges (approx 40px)
        content_height = self.current_sheet_widget.sizeHint().height()
        target_height = content_height + 120

        # 3. On récupère la taille disponible de l'écran de l'utilisateur
        screen_geometry = self.screen().availableGeometry()
        max_height = screen_geometry.height() - 100  # On laisse une marge de sécurité (barre des tâches)

        # 4. On choisit la plus petite valeur entre "Taille Idéale" et "Taille Max Écran"
        final_height = min(target_height, max_height)

        # 5. On applique le redimensionnement (on garde la largeur actuelle)
        self.resize(self.width(), final_height)

    def paintEvent(self, event):
        if self.use_bg:
            p = QPainter(self)
            p.drawPixmap(self.rect(), self.background_pixmap)

    def create_top_bar(self):
        bar = QFrame()
        # Ajout de la hauteur fixe pour empêcher l'agrandissement intempestif
        bar.setFixedHeight(60)

        bar.setStyleSheet("""
            background-color: rgba(255,255,255,0.4); 
            border-bottom: 2px solid #5c4a3d;
            border-radius: 5px;
        """)

        l = QHBoxLayout(bar)
        l.setContentsMargins(10, 5, 10, 5)  # Marges intérieures (Gauche, Haut, Droite, Bas)

        lbl = QLabel("COLLECTION :")
        # On force le label à ne pas prendre tout l'espace horizontal
        lbl.setFixedWidth(120)

        self.combo = QComboBox()
        self.combo.addItems(sorted(COLLECTIONS_DATA.keys()))
        self.combo.currentTextChanged.connect(self.load_interface)

        # Style spécifique pour la ComboBox pour qu'elle soit bien visible
        self.combo.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                padding: 5px;
            }
        """)

        l.addWidget(lbl)
        l.addWidget(self.combo)

        # Important : On ajoute le widget, mais on s'assure qu'il reste en haut
        self.main_layout.addWidget(bar)

    def load_interface(self, name):
        # --- 1. NETTOYAGE ABSOLU (Méthode Kärcher) ---
        # On regarde le layout principal. Tant qu'il y a plus d'1 élément (la barre du haut),
        # on supprime tout ce qui suit.
        while self.main_layout.count() > 1:
            item = self.main_layout.takeAt(1)  # On prend toujours l'élément n°1 (juste après la barre)
            widget = item.widget()
            if widget:
                widget.deleteLater()  # On le détruit

        # Une petite pause pour laisser le temps à Qt de supprimer les objets
        QApplication.processEvents()

        # --- 2. CRÉATION DE LA NOUVELLE FEUILLE ---
        self.current_sheet_widget = QWidget()
        self.current_sheet_widget.setObjectName("SheetWidget")
        self.sheet_layout = QVBoxLayout(self.current_sheet_widget)
        self.sheet_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.current_sheet_widget)

        # Vérification de sécurité
        if name not in COLLECTIONS_DATA:
            return  # Si la collection n'existe pas, on arrête là

        data = COLLECTIONS_DATA[name]

        # Construction selon le type
        if data["type"] == "classic_df":
            self.build_classic_df(data)
        elif data["type"] == "lone_wolf":
            self.build_lone_wolf(data)
        else:
            self.build_generic(data)

        self.add_dice_roller(data.get("dice", "2d6"))

        # Ressort vers le bas + Redimensionnement
        self.sheet_layout.addStretch()
        self.adjust_window_size()

    # --- ARCHITECTURE 1 : STYLE DÉFIS FANTASTIQUES ---
    def build_classic_df(self, data):
        # Stats en haut (3 cases)
        stats_box = QGroupBox("Caractéristiques")
        grid = QGridLayout()
        stats = data.get("stats", [])

        for i, stat in enumerate(stats):
            frame = QFrame()
            frame.setStyleSheet("border: 2px solid #2b1d15; background-color: rgba(255,255,255,0.3);")
            vbox = QVBoxLayout(frame)
            lbl = QLabel(stat)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

            row = QHBoxLayout()
            s_init = QSpinBox();
            s_init.setPrefix("Init: ")
            s_curr = QSpinBox();
            s_curr.setPrefix("Act: ")
            s_init.setRange(0, 99);
            s_curr.setRange(0, 99)

            row.addWidget(s_init);
            row.addWidget(s_curr)
            vbox.addWidget(lbl);
            vbox.addLayout(row)
            grid.addWidget(frame, 0, i)
        stats_box.setLayout(grid)
        self.sheet_layout.addWidget(stats_box)

        # Corps
        body = QHBoxLayout()
        inv_box = QGroupBox("Équipement")
        v_inv = QVBoxLayout()
        for i in range(1, 11):
            v_inv.addWidget(QLineEdit(placeholderText=f"{i}. __________________"))
        inv_box.setLayout(v_inv)

        right_col = QVBoxLayout()
        gold_box = QGroupBox(data.get("currency", "Trésor"))
        v_gold = QVBoxLayout()
        v_gold.addWidget(QLabel("Quantité :"))
        v_gold.addWidget(QSpinBox())
        v_gold.addWidget(QLabel("Joyaux / Notes :"))
        v_gold.addWidget(QTextEdit())
        gold_box.setLayout(v_gold)

        # Section Extra (Provisions ou Sorts)
        extra_title = data.get("extra", "Provisions")
        prov_box = QGroupBox(extra_title)
        v_prov = QVBoxLayout()
        if "Sorts" in extra_title:
            v_prov.addWidget(QTextEdit(placeholderText="Listez vos sorts..."))
        else:
            v_prov.addWidget(QLabel("Restant :"))
            v_prov.addWidget(QSpinBox())
        prov_box.setLayout(v_prov)

        right_col.addWidget(gold_box)
        right_col.addWidget(prov_box)
        right_col.addStretch()

        body.addWidget(inv_box, 2)
        body.addLayout(right_col, 1)
        self.sheet_layout.addLayout(body)

    # --- ARCHITECTURE 2 : STYLE LOUP SOLITAIRE ---
    def build_lone_wolf(self, data):
        # Top : Disciplines
        top_box = QGroupBox("Disciplines & Statistiques")
        top_layout = QHBoxLayout()

        # Stats
        stats_frame = QFrame()
        stats_layout = QVBoxLayout(stats_frame)
        for stat in data.get("stats", []):
            stats_layout.addWidget(QLabel(stat))
            sb = QSpinBox();
            sb.setRange(0, 50)
            stats_layout.addWidget(sb)
        top_layout.addWidget(stats_frame)

        # Disciplines
        disc_frame = QFrame()
        disc_layout = QVBoxLayout(disc_frame)
        disc_title = data.get("extra_title", "Disciplines Kaï")
        disc_layout.addWidget(QLabel(f"{disc_title} :"))
        for i in range(1, 6):
            disc_layout.addWidget(QLineEdit(placeholderText=f"{i}. ..."))
        top_layout.addWidget(disc_frame)

        top_box.setLayout(top_layout)
        self.sheet_layout.addWidget(top_box)

        # Grille Armes / Sac
        mid_box = QGroupBox("Armes & Sac à Dos")
        mid_layout = QGridLayout()
        mid_layout.addWidget(QLabel("ARMES (Max 2)"), 0, 0)
        mid_layout.addWidget(QLineEdit(placeholderText="Main 1..."), 1, 0)
        mid_layout.addWidget(QLineEdit(placeholderText="Main 2..."), 2, 0)
        mid_layout.addWidget(QLabel("OBJETS DE SAC À DOS (Max 8)"), 0, 1)
        for i in range(8):
            mid_layout.addWidget(QLineEdit(placeholderText=f"Objet {i + 1}"), (i // 2) + 1, (i % 2) + 1)
        mid_box.setLayout(mid_layout)
        self.sheet_layout.addWidget(mid_box)

        # Bourse
        bot_box = QGroupBox("Bourse & Spécial")
        bl = QHBoxLayout()
        bl.addWidget(QLabel(f"{data.get('currency')} :"))
        bl.addWidget(QSpinBox())
        bl.addWidget(QLabel("Objets Spéciaux :"))
        bl.addWidget(QLineEdit())
        bot_box.setLayout(bl)
        self.sheet_layout.addWidget(bot_box)

    # --- ARCHITECTURE 3 : GÉNÉRIQUE ADAPTATIF ---
    def build_generic(self, data):
        gbox = QGroupBox("Feuille de Personnage")
        layout = QVBoxLayout()

        # Stats : Gestion dynamique (1 ou 2 colonnes selon le nombre)
        stats = data.get("stats", [])
        stats_layout = QGridLayout()

        num_cols = 2 if len(stats) > 4 else 1  # Double colonne pour Loup*Ardent

        for i, stat_name in enumerate(stats):
            row = i // num_cols
            col_base = (i % num_cols) * 3  # 3 sous-colonnes par stat (Label, Init, Act)

            stats_layout.addWidget(QLabel(stat_name), row, col_base)
            s1 = QSpinBox();
            s1.setPrefix("Init:")
            s2 = QSpinBox();
            s2.setPrefix("Act:")
            s1.setRange(0, 999);
            s2.setRange(0, 999)  # Large range

            stats_layout.addWidget(s1, row, col_base + 1)
            stats_layout.addWidget(s2, row, col_base + 2)

        layout.addLayout(stats_layout)

        # Section Spéciale si définie
        if "special" in data:
            layout.addWidget(QLabel(f"Notes Spéciales ({data['special']}) :"))
            layout.addWidget(QTextEdit())

        # Inventaire Standard
        layout.addWidget(QLabel("Inventaire & Équipement :"))
        layout.addWidget(QTextEdit())

        # Monnaie
        h_money = QHBoxLayout()
        h_money.addWidget(QLabel(f"{data.get('currency', 'Or')} :"))
        h_money.addWidget(QSpinBox())
        h_money.addStretch()
        layout.addLayout(h_money)

        gbox.setLayout(layout)
        self.sheet_layout.addWidget(gbox)

    def add_dice_roller(self, type_dice):
        box = QGroupBox("Zone de Hasard")
        l = QHBoxLayout()
        self.res_lbl = QLabel("Résultat : -")
        self.res_lbl.setStyleSheet("font-size: 18px; color: #8b0000;")

        btn = QPushButton()
        if type_dice == "d10":
            btn.setText("Table de Hasard (0-9)")
            btn.clicked.connect(lambda: self.res_lbl.setText(f"Résultat : {random.randint(0, 9)}"))
        elif type_dice == "1d6":
            btn.setText("1 dé (1d6)")
            btn.clicked.connect(lambda: self.res_lbl.setText(f"Résultat : {random.randint(1, 6)}"))
        else:
            btn.setText("Lancer 2 dés (2d6)")
            btn.clicked.connect(
                lambda: self.res_lbl.setText(f"Résultat : {random.randint(1, 6) + random.randint(1, 6)}"))

        l.addWidget(btn)
        l.addWidget(self.res_lbl)
        box.setLayout(l)
        self.sheet_layout.addWidget(box)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AventureSheetFinal()
    window.show()
    sys.exit(app.exec())
