from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
import random

# --- 1. DONNÉES COMPLÈTES (Identiques à la version PC) ---
COLLECTIONS_DATA = {
    "Défis Fantastiques": {"type": "classic_df", "stats": ["HABILETÉ", "ENDURANCE", "CHANCE"],
                           "currency": "Pièces d'Or", "dice": "2d6"},
    "Sorcellerie!": {"type": "classic_df", "stats": ["HABILETÉ", "ENDURANCE", "CHANCE"], "currency": "Pièces d'Or",
                     "dice": "2d6", "extra": "Livre des Sorts"},
    "Loup Solitaire": {"type": "lone_wolf", "stats": ["HABILETÉ", "ENDURANCE"], "currency": "Couronnes", "dice": "d10"},
    "Astre d'Or": {"type": "lone_wolf", "stats": ["VOLONTÉ", "ENDURANCE"], "currency": "Lunes", "dice": "d10",
                   "extra_title": "Pouvoirs Magiques"},
    "La Voie du Tigre": {"type": "generic", "stats": ["Endurance", "Force Int.", "Destin"], "currency": "Or",
                         "dice": "2d6", "special": "Techniques"},
    "L'épée de Légende": {"type": "generic", "stats": ["Habileté", "Endurance", "Chance"], "currency": "Pièces d'Or",
                          "dice": "2d6", "special": "Classe"},
    "Le Maitre du Destin": {"type": "generic", "stats": ["Habileté", "Endurance", "Indices"], "currency": "Livres",
                            "dice": "2d6"},
    "Destin": {"type": "generic", "stats": ["Force", "Agilité", "Mental", "Vie"], "currency": "Crédits", "dice": "2d6",
               "special": "Comp. Info"},
    "Métamorphoses": {"type": "generic", "stats": ["Physique", "Mental", "Chance"], "currency": "Troc", "dice": "2d6"},
    "Loup*Ardent": {"type": "generic",
                    "stats": ["Force", "Rapidité", "Endurance", "Courage", "Chance", "Charme", "Habileté", "Pouvoir"],
                    "currency": "Or", "dice": "2d6"},
    "Quête du Graal": {"type": "generic", "stats": ["Points de Vie"], "currency": "Pièces d'Or", "dice": "2d6",
                       "special": "Sortilèges/Excalibur"},
    "Les messagers du Temps": {"type": "classic_df", "stats": ["HABILETÉ", "ENDURANCE", "TEMPS"], "currency": "Or",
                               "dice": "2d6"},
    "Défis et Sortilèges": {"type": "generic", "stats": ["Vie", "Magie", "Argent"], "currency": "Pièces",
                            "dice": "2d6"},
    "Les Portes Interdites": {"type": "generic", "stats": ["Physique", "Mental"], "currency": "Dollars", "dice": "2d6",
                              "special": "Santé Mentale"},
    "Epouvante!": {"type": "classic_df", "stats": ["HABILETÉ", "ENDURANCE", "PEUR"], "currency": "Or", "dice": "2d6"},
    "Histoire / Défis": {"type": "generic", "stats": ["Habileté", "Endurance"], "currency": "Deniers", "dice": "2d6"},
    "Double Jeu": {"type": "generic", "stats": ["Habileté", "Endurance", "Force"], "currency": "Or", "dice": "2d6",
                   "special": "Code Secret"}
}


class AdventureApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Brown"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.theme_style = "Light"  # Fond clair

        # Structure principale
        self.screen = MDScreen()

        # Layout vertical principal
        root_layout = MDBoxLayout(orientation='vertical')

        # 1. Barre du haut (Toolbar)
        self.toolbar = MDTopAppBar(title="Feuille d'Aventure")
        self.toolbar.right_action_items = [["bookshelf", lambda x: self.menu.open()]]
        self.toolbar.elevation = 4
        root_layout.add_widget(self.toolbar)

        # 2. Zone de contenu Scrollable
        self.scroll = MDScrollView()
        self.content_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            adaptive_height=True
        )
        self.scroll.add_widget(self.content_layout)
        root_layout.add_widget(self.scroll)

        self.screen.add_widget(root_layout)

        # Création du menu déroulant pour les collections
        menu_items = [
            {
                "text": name,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=name: self.set_collection(x),
            } for name in sorted(COLLECTIONS_DATA.keys())
        ]
        self.menu = MDDropdownMenu(
            caller=self.toolbar,
            items=menu_items,
            width_mult=4,
        )

        # Charger la première collection par défaut
        self.set_collection("Défis Fantastiques")

        return self.screen

    def set_collection(self, name):
        self.menu.dismiss()
        self.toolbar.title = name
        self.content_layout.clear_widgets()  # Nettoyage complet

        data = COLLECTIONS_DATA[name]

        # --- Construction dynamique ---

        # 1. Section STATS
        self.build_section_title("Caractéristiques")
        stats_grid = MDGridLayout(cols=2, spacing=dp(10), adaptive_height=True)

        for stat in data["stats"]:
            # Une petite carte pour chaque stat
            card = MDCard(orientation='vertical', padding=dp(10), spacing=dp(5), size_hint_y=None, height=dp(100),
                          elevation=2)
            card.add_widget(MDLabel(text=stat, halign="center", bold=True, theme_text_color="Primary"))

            input_box = MDBoxLayout(orientation='horizontal', spacing=dp(10))
            input_box.add_widget(MDTextField(hint_text="Init", input_filter="int", mode="rectangle"))
            input_box.add_widget(MDTextField(hint_text="Actuel", input_filter="int", mode="rectangle"))

            card.add_widget(input_box)
            stats_grid.add_widget(card)

        self.content_layout.add_widget(stats_grid)

        # 2. Section SPÉCIALE (Loup Solitaire / Magie)
        if data["type"] == "lone_wolf" or "extra" in data or "special" in data:
            title = data.get("extra_title", data.get("extra", data.get("special", "Spécial")))
            self.build_section_title(title)
            self.content_layout.add_widget(
                MDTextField(
                    hint_text="Liste ( Disciplines / Sorts / Codes )",
                    mode="rectangle",
                    multiline=True,
                    size_hint_y=None,
                    height=dp(100)
                )
            )

        # 3. ÉQUIPEMENT & ARGENT
        self.build_section_title("Inventaire")

        # Argent
        currency_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10), adaptive_height=True)
        currency_layout.add_widget(MDTextField(hint_text=f"{data['currency']}", input_filter="int", mode="fill"))
        self.content_layout.add_widget(currency_layout)

        # Liste objets (Loup Solitaire a une grille, les autres une liste)
        if data["type"] == "lone_wolf":
            self.content_layout.add_widget(MDLabel(text="Armes (Max 2)", theme_text_color="Secondary"))
            self.content_layout.add_widget(MDTextField(hint_text="Arme 1"))
            self.content_layout.add_widget(MDTextField(hint_text="Arme 2"))
            self.content_layout.add_widget(MDLabel(text="Sac à dos (Max 8)", theme_text_color="Secondary"))
            grid_sac = MDGridLayout(cols=2, spacing=dp(10), adaptive_height=True)
            for i in range(8):
                grid_sac.add_widget(MDTextField(hint_text=f"Objet {i + 1}"))
            self.content_layout.add_widget(grid_sac)
        else:
            self.content_layout.add_widget(
                MDTextField(
                    hint_text="Votre équipement...",
                    mode="rectangle",
                    multiline=True,
                    size_hint_y=None,
                    height=dp(150)
                )
            )

        # 4. DÉS
        self.build_section_title("Zone de Hasard")
        dice_type = data.get("dice", "2d6")
        btn_text = "Lancer 2 dés (2d6)"
        if dice_type == "d10": btn_text = "Table de Hasard (0-9)"

        btn = MDFillRoundFlatButton(
            text=btn_text,
            pos_hint={"center_x": 0.5},
            font_size=dp(18)
        )
        btn.bind(on_release=lambda x: self.roll_dice(dice_type))
        self.content_layout.add_widget(btn)

        # Espace vide en bas pour le scroll
        self.content_layout.add_widget(MDBoxLayout(size_hint_y=None, height=dp(50)))

    def build_section_title(self, text):
        lbl = MDLabel(text=text.upper(), font_style="H6", theme_text_color="Primary", adaptive_height=True)
        self.content_layout.add_widget(lbl)

    def roll_dice(self, dice_type):
        if dice_type == "d10":
            res = random.randint(0, 9)
            msg = f"Table de Hasard : {res}"
        else:
            d1 = random.randint(1, 6)
            d2 = random.randint(1, 6)
            msg = f"Résultat : {d1 + d2} ({d1} + {d2})"

        Snackbar(text=msg, bg_color=get_color_from_hex("#5c4a3d")).open()


if __name__ == "__main__":
    AdventureApp().run()
