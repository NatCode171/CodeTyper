from moviepy import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token

# Paramètres
position = 0 # 1 = vidéo horizontale et 0 = verticale
file_path = "cop.py" # fichier qui contient le code à écrire
font_path = "seguiemj.ttf"
typing_sound_path = "sound.wav"

if position == 1:
    width, height = 1280, 720
    font_size = 20
else:
    width, height = 720, 1280
    font_size = 27

text_color = (255, 255, 255)
bg_color = (0, 0, 0)
fps = 30
typing_speed = 30  # caractères par seconde
char_duration = 1 / typing_speed  # durée d'apparition d'un caractère en secondes

# Lire le fichier
with open(file_path, encoding="utf-8") as f:
    code_lines = f.readlines()

# Police d'écriture
font = ImageFont.truetype(font_path, font_size)

pygments_colors = {
    Token.Keyword: (86, 156, 214),
    Token.Keyword.Constant: (86, 156, 214),
    Token.Keyword.Declaration: (86, 156, 214),
    Token.Keyword.Namespace: (86, 156, 214),
    Token.Keyword.Pseudo: (86, 156, 214),
    Token.Keyword.Reserved: (86, 156, 214),
    Token.Keyword.Type: (86, 156, 214),
    # etc...
}

def get_token_color(token_type):
    # Cherche la couleur la plus spécifique possible
    while token_type not in pygments_colors and token_type.parent:
        token_type = token_type.parent
    return pygments_colors.get(token_type, (212, 212, 212))  # Sinon gris clair par défaut

# Préparer son de frappe
typing_sound = AudioFileClip(typing_sound_path)

# Fusionner toutes les lignes en une seule string
full_text = "".join(code_lines)

# Durée totale de la vidéo en secondes
total_chars = len(full_text)
duration = total_chars * char_duration + 1  # 1 seconde de marge

# Fonction qui crée une image pour un nombre donné de caractères affichés
def make_frame(t):
    char_count = min(int(t / char_duration), total_chars)
    cursor_on = (int(t * 2) % 2 == 0)
    text_to_show = full_text[:char_count]
    if char_count < total_chars and cursor_on:
        text_to_show += "|"

    lines = text_to_show.split("\n")

    img_pil = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img_pil)

    line_height = font_size + 5
    total_text_height = len(lines) * line_height

    max_visible_height = int(height * 0.75)
    overflow = max(0, total_text_height - max_visible_height)
    scroll_y = overflow
    base_y = 20 - scroll_y

    max_width = width - 40
    scroll_trigger = max_width - 5
    scroll_speed = 100

    last_line = lines[-1] if lines else ""
    last_line_width = font.getlength(last_line)

    scroll_x = 0
    if last_line_width > scroll_trigger:
        scroll_amount = last_line_width - scroll_trigger
        scroll_x = min(scroll_amount, scroll_speed * t)

    y_text = base_y
    for line in lines:
        x_text = 20 - scroll_x

        # Coloration syntaxique ligne par ligne avec Pygments
        tokens = list(lex(line, PythonLexer()))
        for token_type, token_text in tokens:
            color = get_token_color(token_type)
            # Dessiner chaque caractère dans sa couleur
            draw.text((x_text, y_text), token_text, font=font, fill=color)
            x_text += font.getlength(token_text)

        y_text += line_height

    return np.array(img_pil)

# Créer une vidéo (en mode fonction)
video_clip = VideoClip(make_frame, duration=duration).with_fps(fps)

# Générer clip audio
sounds = []
sound_interval = typing_sound.duration
typing_end_time = total_chars * char_duration
current_time = 0

while current_time < typing_end_time:
    # Durée restante avant la fin de la frappe
    remaining = typing_end_time - current_time

    # Si le son dépasse la fin, on le coupe
    if remaining < sound_interval:
        sound_clip = typing_sound.subclipped(0, remaining).with_start(current_time)
    else:
        sound_clip = typing_sound.with_start(current_time)

    sounds.append(sound_clip)
    current_time += sound_interval

# Combiner les sons en un seul clip audio
if sounds:
    audio_clip = CompositeAudioClip(sounds)
else:
    audio_clip = None

# Ajouter l'audio à la vidéo
final_clip = video_clip.with_audio(audio_clip)

# Exporter
final_clip.write_videofile("terminal_typing_with_sound.mp4", codec="libx264", audio_codec="aac")

# Code source du programme qui créer ce genre
# de vidéo en description et en commentaire !