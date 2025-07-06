# CodeTyper – Code Python pour créer une vidéo de saisie avec coloration

Transforme un fichier Python en une **vidéo animée stylisée** qui **simule la frappe en direct**, avec :
- Coloration syntaxique comme dans VS Code (via Pygments)
- Effet sonore de frappe réaliste
- Support vidéo verticale ou horizontale (YouTube Shorts, Reels, etc.)
- Défilement automatique du texte et gestion des longues lignes
- Export rapide en `.mp4`

---

## Fonctionnalités
- Lecture et rendu de code depuis un fichier `.py`
- Animation caractère par caractère avec curseur clignotant
- Coloration précise de chaque mot-clé, string, commentaire, etc.
- Sons synchronisés avec la vitesse de frappe
- Adapté aux formats *16:9* et *9:16*

---

## Utilisation

### 1. Cloner le projet
```bash
git clone https://github.com/NatCode171/CodeTyper.git
cd CodeTyper
```

### 2. Placer le fichier à animer
Modifie `file_path = "cop.py"` dans le script ou remplace le fichier `cop.py`.

### 3. Lancer le script
```bash
py main.py
```

---

## Dépendances

- `moviepy`
- `Pillow`
- `pygments`
- `numpy`

Installe-les avec :
```bash
pip install moviepy pillow pygments numpy
```

---

## Licence

MIT – Utilisation libre et open source.
