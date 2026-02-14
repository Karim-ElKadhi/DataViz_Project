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

Pratiques Évitées : ❌ JAMAIS Utiliser
1. Charts 3D
Raison: Distorsion perspective, lecture difficile, chartjunk
2. Double Axes Y
Raison: Source majeure de confusion et manipulation
3. Pie Charts > 10 Catégories
Raison: Impossible de comparer précisément
4. Échelles Tronquées (sauf justification)
Raison: Exagère visuellement les différences

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

**Chart.js 4.4.0** est le framework de visualisation **officiellement spécifié** pour ce projet.

**Avantages confirmés:**
- ✅ Framework déclaré explicitement
- ✅ Best practices intégrées nativement
- ✅ Performance validée

**Impact sur le projet:**
- Visualisations conformes aux standards académiques
- Code maintenable et documenté
- Performance optimale
- Évolutivité assurée

**Documentation Principale:**
- API Reference: https://www.chartjs.org/docs/latest/api/
- Configuration: https://www.chartjs.org/docs/latest/configuration/
- Charts: https://www.chartjs.org/docs/latest/charts/

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


---

## 🚀 Déploiement sur Hugging Face Spaces

Ce projet est déployé sur Hugging Face Spaces. Voici les étapes complètes pour déployer votre propre version:

### Prérequis pour le Déploiement
- Compte Hugging Face (gratuit)
- Git installé
- Token d'accès Hugging Face avec permission "write"
- Clé API Google Gemini

### Étape 1: Créer un Compte Hugging Face

1. Allez sur https://huggingface.co/join
2. Créez un compte gratuit
3. Vérifiez votre email
4. Connectez-vous

### Étape 2: Obtenir un Token d'Accès

1. Allez sur https://huggingface.co/settings/tokens
2. Cliquez sur **"New token"**
3. Name: `spaces-deploy`
4. Role: **Write**
5. Copiez le token (vous en aurez besoin pour le push Git)

### Étape 3: Créer un Space sur Hugging Face

1. Allez sur https://huggingface.co/new-space
2. Remplissez le formulaire:
   - **Space name:** `DataViz-Project` (ou votre choix)
   - **License:** MIT
   - **Select SDK:** Docker
   - **Space hardware:** CPU basic (gratuit)
   - **Visibility:** Public
3. Cliquez sur **"Create Space"**

### Étape 4: Configurer le Repository Local

```bash
# 1. Cloner votre projet (si pas déjà fait)
git clone https://github.com/VOTRE_USERNAME/VOTRE_REPO.git
cd VOTRE_REPO

# 2. Ajouter Hugging Face comme remote
git remote add space https://huggingface.co/spaces/VOTRE_USERNAME/DataViz-Project

# 3. Vérifier les remotes
git remote -v
```

### Étape 5: Préparer les Fichiers pour le Déploiement

Assurez-vous d'avoir ces fichiers à la racine:

**Dockerfile** (port 7860 obligatoire):
```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

ENV PYTHONUNBUFFERED=1
ENV PORT=7860

CMD ["python", "app.py"]
```

**app.py** (modifier la dernière ligne):
```python
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 7860))
    app.run(debug=False, host='0.0.0.0', port=port)
```

**README.md** (header YAML obligatoire):
```yaml
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
```


### Étape 6: Commit et Push vers Hugging Face

```bash
# 1. Ajouter tous les fichiers
git add .

# 2. Commit
git commit -m "Deploy to Hugging Face Spaces"

# 3. Push vers Hugging Face
git push space main --force

# Lors du push, entrez:
# Username: votre_username_huggingface
# Password: votre_token_hf 
```

### Étape 7: Configurer les Secrets (IMPORTANT!)

1. Allez sur votre Space: `https://huggingface.co/spaces/VOTRE_USERNAME/DataViz-Project`
2. Cliquez sur l'onglet **"Settings"**
3. Section **"Repository secrets"**
4. Cliquez **"Add a secret"**
5. Configurez:
   - **Name:** `GEMINI_API_KEY`
   - **Value:** Votre clé API Google Gemini
6. Cliquez **"Add secret"**

### Étape 8: Vérifier le Build

1. Retournez à l'onglet **"App"** de votre Space
2. Le build Docker démarre automatiquement (2-5 minutes)
3. Surveillez les logs en temps réel dans l'onglet **"Logs"**
4. Attendez le message: `Running on http://0.0.0.0:7860`

### Étape 9: Tester l'Application

1. Une fois le build terminé, l'application s'affiche automatiquement
2. Testez:
   - Upload d'un fichier CSV
   - Génération de propositions (vérifie que Gemini fonctionne)
   - Visualisation des graphiques
   - Export PNG

### Étape 10: Partager l'Application

Votre application est maintenant publique à l'URL:
```
https://huggingface.co/spaces/VOTRE_USERNAME/DataViz-Project
```

---

## 🔄 Mettre à Jour l'Application Déployée

Pour mettre à jour votre application après des modifications:

```bash
# 1. Modifier vos fichiers localement
# 2. Tester localement
python app.py

# 3. Commit les changements
git add .
git commit -m "Update: description des changements"

# 4. Push vers Hugging Face
git push space main

```

---