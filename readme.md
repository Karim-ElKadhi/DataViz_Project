---
title: Intelligent Data Visualization
emoji: 📊
colorFrom: blue
colorTo: purple
sdk: docker
sdk_version: "4.36.1"
python_version: "3.10"
app_file: app.py
pinned: false
---

# 📊 Data Visualization System

Application web intelligente de visualisation de données. Ce système analyse automatiquement n'importe quel dataset CSV et génère des propositions de visualisations pertinentes basées sur les meilleures pratiques académiques en data visualization.

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Karim-Elkadhi/DATAVIZ)
---

## 🌐 Application Déployée

**🔗 Accéder à l'application:** [https://huggingface.co/spaces/Karim-Elkadhi/DATAVIZ](https://huggingface.co/spaces/Karim-Elkadhi/DATAVIZ)

L'application est déployée sur **Hugging Face Spaces** et accessible publiquement. Aucune installation requise pour l'utiliser en ligne!

---

## 📖 Description du Projet

### Contexte
Ce projet a été développé dans le cadre d'un cours de data visualization, avec pour objectif de créer un système intelligent capable de:
- Analyser automatiquement la structure de n'importe quel dataset CSV
- Générer des visualisations pertinentes en fonction d'une question analytique
- Respecter les bonnes pratiques académiques (Edward Tufte, Cleveland & McGill)
- Fournir des justifications claires pour chaque proposition

### Fonctionnalités Principales

#### 🤖 Intelligence Artificielle
- **Analyse contextuelle** du dataset et de la question
- **Génération de 3 propositions** de visualisations différentes
- **Justifications détaillées** basées sur les best practices
- **Support des requêtes complexes** (top N, classements, corrélations)

#### 📊 Types de Visualisations (9 types)
1. **Bar Chart** (vertical/horizontal) - Comparaisons entre catégories
2. **Scatter Plot** - Relations entre variables continues
3. **Pie Chart** - Proportions d'un tout
4. **Box Plot** - Distributions par catégories
5. **Correlation Matrix** - Relations multiples entre variables
6. **Heatmap** - Carte de chaleur des corrélations
7. **Line Chart** - Évolutions temporelles
8. **Violin Plot** - Distributions détaillées

#### 🎨 Bonnes Pratiques Implémentées
- **Data-ink ratio maximisé** 
  - Suppression du chartjunk (bordures, effets inutiles)
  - Grilles minimales et subtiles
  - Légendes uniquement si nécessaires

- **Échelles appropriées**
  - Échelles adaptées pour scatter/line charts
  - Pas d'échelles tronquées ou trompeuses



#### Fonctionnalités UX
- **Navigation fluide** entre les étapes
- **Retour aux propositions** sans re-générer
- **Changement de dataset** sans recharger la page
- **Export PNG** haute qualité

---

## 🛠️ Technologies Utilisées

### Backend
- **Flask** - Framework web Python
- **Pandas 2.1.4** - Manipulation et analyse de données
- **NumPy 1.26.2** - Calculs scientifiques
- **OpenAi Oss** - Groq API

### Frontend
- **HTML5** - Structure sémantique
- **CSS3** - Design moderne avec gradients et animations
- **JavaScript** - Aucune dépendance externe

### Déploiement
- **Docker** - Containerisation
- **Hugging Face Spaces** - Hébergement cloud

---

## 📥 Installation Locale

### Prérequis
- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)
- Git
- Clé API Groq

### Étapes d'Installation

#### 1. Cloner le Repository

```bash
# Via HTTPS
git clone https://huggingface.co/spaces/Karim-Elkadhi/DATAVIZ
cd DataViz
```

#### 2. Créer un Environnement Virtuel (Recommandé)

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
# Sur Windows:
venv\Scripts\activate

# Sur Mac/Linux:
source venv/bin/activate
```

#### 3. Installer les Dépendances

```bash
pip install -r requirements.txt
```

#### 4. Configurer les Variables d'Environnement

```bash
# Créer le fichier .env
export "yourkey" > .env

```

#### 5. Vérifier la Structure des Dossiers

Assurez-vous d'avoir cette structure:

```
DataViz-Project/
├── app.py
├── requirements.txt
├── .env
├── utils/
│   ├── __init__.py
│   ├── data_analyzer.py
│   └── gemini_service.py
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

---

## 🚀 Instructions de Lancement

### Lancement en Local

```bash
# 1. Activer l'environnement virtuel (si pas déjà fait)
source venv/bin/activate  # Mac

# 2. Lancer l'application Flask
python app.py

# 3. Ouvrir dans le navigateur
# L'application sera accessible sur: le localhost
```

Vous devriez voir dans le terminal:
```
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

---

## 📚 Guide d'Utilisation

### 1. Upload du Dataset

1. Cliquez sur **"Choisir un fichier"**
2. Sélectionnez votre fichier CSV
3. Le système analyse automatiquement:
   - Types de colonnes (numériques/catégorielles)
   - Statistiques descriptives
   - Corrélations entre variables
   - Valeurs manquantes

**Format CSV requis:**
- Séparateur: virgule (`,`)
- Première ligne: noms des colonnes
- Encodage: UTF-8 recommandé
- Taille: jusqu'à 50K lignes testées

### 2. Poser une Question

Exemples de questions supportées:

**Questions exploratoires:**
- "Quels sont les facteurs les plus corrélés?"
- "Y a-t-il des patterns intéressants dans les données?"
- "Montrer une vue d'ensemble du dataset"

**Questions de classement:**
- "Top 10 des meilleures ventes"
- "Les 5 produits les plus chers"
- "Classement des régions par revenus"

**Questions comparatives:**
- "Comparer les prix par catégorie"
- "Différence entre groupes A et B"

**Questions relationnelles:**
- "Relation entre prix et surface"
- "Comment X influence-t-elle Y?"
- "Matrice de corrélation complète"

### 3. Choisir une Visualisation

- Gemini génère **3 propositions** différentes
- Chaque proposition inclut:
  - **Type de graphique** approprié
  - **Titre** descriptif
  - **Justification** détaillée expliquant pourquoi cette visualisation répond à votre question

### 4. Explorer et Exporter

- Visualisez le graphique interactif
- Utilisez **"Retour aux propositions"** pour essayer une autre visualisation
- Cliquez **"Télécharger PNG"** pour exporter
- Ou **"Nouvelle question"** pour analyser différemment

---

## 🎓 Principes Académiques Appliqués

### Edward Tufte - "The Visual Display of Quantitative Information"
- ✅ Maximisation du data-ink ratio
- ✅ Minimisation du chartjunk
- ✅ Intégrité graphique (échelles honnêtes)
- ✅ Pas de distorsions visuelles
