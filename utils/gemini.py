import google.generativeai as genai
import json
import re
import requests
class GeminiService:
    def __init__(self, api_key, model="openai/gpt-oss-120b"):
        self.api_key = api_key
        self.model = model
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"
        self.last_raw_response = None

    def generate_visualization_proposals(self, question, dataset_info, columns):
        
        # Identify numeric and categorical columns from dataset_info
        numeric_cols = list(dataset_info.get('statistics', {}).keys())
        categorical_cols = list(dataset_info.get('categorical_info', {}).keys())
        
        prompt = f"""
Tu es un expert en data visualisation. Analyse la question de l'utilisateur et propose 3 visualisations différentes et pertinentes.

QUESTION DE L'UTILISATEUR:
{question}

INFORMATIONS SUR LE DATASET:
Colonnes disponibles: {', '.join(columns)}
Nombre total de colonnes: {len(columns)}

Variables numériques ({len(numeric_cols)}): {', '.join(numeric_cols)}
Variables catégorielles ({len(categorical_cols)}): {', '.join(categorical_cols)}

Statistiques descriptives des variables numériques:
{json.dumps(dataset_info.get('statistics', {}), indent=2)}

Corrélations entre variables numériques:
{json.dumps(dataset_info.get('correlations', {}), indent=2)}

Informations sur les variables catégorielles:
{json.dumps(dataset_info.get('categorical_info', {}), indent=2)}

INSTRUCTIONS:
Analyse attentivement le dataset et la question pour proposer exactement 3 visualisations différentes qui répondent précisément à la question posée.

BONNES PRATIQUES DE VISUALISATION (OBLIGATOIRES):

1. PRINCIPE DE DATA-INK RATIO:
   - Maximiser le ratio data-ink: chaque élément visuel doit représenter des données
   - Minimiser le chartjunk: éviter les décorations inutiles
   - Supprimer tout élément redondant ou non informatif

2. CLARTÉ ET LISIBILITÉ:
   - Titres clairs et descriptifs
   - Axes toujours étiquetés avec unités si applicable
   - Légendes uniquement si nécessaire (pas de légende pour un seul dataset)
   - Police lisible, pas de texte trop petit

3. CHOIX DU TYPE DE GRAPHIQUE:
   - Bar chart: Comparaisons entre catégories (max 15 catégories)
   - Line chart: Évolutions temporelles ou séquentielles
   - Scatter plot: Relations entre 2 variables continues
   - Pie chart: Proportions d'un tout (max 5-7 catégories, éviter si possible)
   - Box plot: Distribution et comparaison de distributions
   - Correlation matrix: Relations multiples entre variables numériques
   
   ÉVITER:
   - Pie charts si > 7 catégories ou si bar chart plus clair
   - Graphiques trop chargés
   - Double axes Y

4. COULEURS:
   - Palette cohérente et accessible
   - Éviter trop de couleurs (max 5-7 couleurs distinctes)
   - Couleurs significatives (rouge pour négatif, vert pour positif si applicable)

5. ÉCHELLES:
   - Échelle Y commence à 0 pour bar charts (obligatoire)
   - Échelles appropriées pour line/scatter (peut ne pas commencer à 0)
   - Éviter les échelles tronquées qui exagèrent les différences
   - Pas d'échelles logarithmiques sauf si justifié

6. ORDRE ET ORGANISATION:
   - Catégories ordonnées de manière logique (alphabétique, par valeur, chronologique)
   - Pour bar charts: trier par valeur décroissante si pas d'ordre naturel
   - Grouper les éléments liés ensemble

RÈGLES IMPORTANTES:
1. Utilise UNIQUEMENT les colonnes qui existent dans le dataset
2. Adapte le type de visualisation au type de données (numériques vs catégorielles)
3. Les 3 visualisations doivent être COMPLÉMENTAIRES et apporter des perspectives différentes
4. Priorise les variables les plus pertinentes pour répondre à la question
5. JUSTIFIE chaque choix en expliquant pourquoi cette visualisation respecte les bonnes pratiques
NOTE: Si la question contient "répartition", privilégier un comptage (aggregation: "count") par variable catégorielle ou discrète.


Types de graphiques disponibles:
- "scatter": Pour relations entre 2 variables numériques (peut inclure color_by pour une catégorie)
- "bar": Pour comparer des moyennes/sommes par catégorie (vertical)
- "horizontalBar": Pour comparer des moyennes/sommes par catégorie (horizontal)
- "pie": Pour montrer la répartition en pourcentage de catégories
- "box": Pour voir la distribution d'une variable numérique par catégories
- "correlationMatrix": Pour matrice de corrélation complète entre variables numériques
- "heatmap": Pour visualiser une matrice de valeurs avec couleurs
- "line": Pour évolution temporelle (si données temporelles disponibles)
- "violin": Pour distribution détaillée par catégories

Pour chaque visualisation, fournis:
1. Un type de graphique adapté aux données
2. Un titre descriptif et précis
3. Une justification claire (2-3 phrases) expliquant comment cette visualisation répond à la question
4. La configuration technique avec les noms EXACTS des colonnes du dataset

IMPORTANT: Réponds UNIQUEMENT avec un JSON valide, sans texte avant ou après, au format suivant:

{{
  "propositions": [
    {{
      "id": 1,
      "type": "bar",
      "title": "Titre clair et descriptif",
      "justification": "Ce bar chart est optimal car: (1) il compare des catégories discrètes, (2) l'échelle Y part de 0 pour éviter les distorsions, (3) les barres sont ordonnées par valeur pour faciliter la lecture, (4) le ratio data-ink est maximisé en évitant les décorations inutiles.",
      "config": {{
        "x_axis": "nom_colonne",
        "y_axis": "nom_colonne_numerique",
        "aggregation": "mean",
        "sort_by": "value",
        "max_categories": 12
      }}
    }},
    {{
      "id": 2,
      "type": "scatter",
      "title": "Autre titre descriptif",
      "justification": "Le scatter plot est approprié pour: (1) visualiser la corrélation entre deux variables continues, (2) identifier des patterns ou outliers, (3) chaque point représente une observation réelle maximisant le data-ink ratio.",
      "config": {{
        "x_axis": "nom_colonne_numerique",
        "y_axis": "nom_colonne_numerique",
        "color_by": null
      }}
    }},
    {{
      "id": 3,
      "type": "horizontalBar",
      "title": "Troisième titre",
      "justification": "Le bar chart horizontal est préférable car: (1) les noms de catégories sont longs et plus lisibles horizontalement, (2) facilite la comparaison entre catégories, (3) l'ordre décroissant met en évidence le classement.",
      "config": {{
        "x_axis": "nom_colonne_categorielle",
        "y_axis": "nom_colonne_numerique",
        "aggregation": "sum",
        "sort_by": "value"
      }}
    }}
  ]
}}

EXEMPLES DE CONFIGURATIONS SELON LE TYPE:

1. Bar Chart pour COMPTER les occurrences:
   {{"type": "bar", "config": {{"x_axis": "bathrooms", "aggregation": "count"}}}}

2. Bar Chart pour MOYENNES:
   {{"type": "bar", "config": {{"x_axis": "bedrooms", "y_axis": "price", "aggregation": "mean"}}}}

3. Pie Chart pour RÉPARTITION:
   {{"type": "pie", "config": {{"category": "furnishingstatus"}}}}

4. Horizontal Bar pour COMPARAISON:
   {{"type": "horizontalBar", "config": {{"x_axis": "region", "y_axis": "sales", "aggregation": "sum"}}}}

5. Box Plot pour DISTRIBUTION:
   {{"type": "box", "config": {{"category": "bedrooms", "value": "price"}}}}

6. Correlation Matrix (pas de config nécessaire):
   {{"type": "correlationMatrix", "config": {{}}}}

RÈGLES IMPORTANTES:
- Pour BAR CHART avec comptage: SEULEMENT "x_axis" et "aggregation": "count"
- Pour BAR CHART avec agrégation: "x_axis" ET "y_axis" ET "aggregation"
- Pour PIE CHART comptage: SEULEMENT "category"
- Pour PIE CHART avec valeur: "category" ET "value" ET "aggregation"
- Pour SCATTER: TOUJOURS "x_axis" ET "y_axis" (colonnes numériques)
- Pour BOX: TOUJOURS "category" ET "value"

Assure-toi que:
- Les 3 visualisations sont DIFFÉRENTES (types et variables différents)
- Toutes les colonnes mentionnées existent EXACTEMENT dans le dataset (respecte la casse)
- Les types de graphiques correspondent aux types de données (numériques/catégorielles)
- Chaque visualisation apporte une réponse complémentaire à la question
- La réponse est un JSON valide et complet sans texte supplémentaire
"""
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Tu es un assistant expert en data visualisation."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(self.endpoint, headers=headers, json=payload, timeout=60)
            response.raise_for_status()

            data = response.json()

            response_text = data["choices"][0]["message"]["content"].strip()

            self.last_raw_response = response_text

            print("=" * 80)
            print("RAW GROQ RESPONSE")
            print("=" * 80)
            print(response_text)
            print("=" * 80)

            # Robust JSON extraction
            match = re.search(r"\{[\s\S]*\}", response_text)
            if not match:
                raise ValueError("No JSON found in response")

            json_str = match.group(0)
            proposals = json.loads(json_str)

            if "propositions" not in proposals:
                raise ValueError("Missing 'propositions'")

            return proposals["propositions"]

        except Exception as e:
            print("Groq error:", e)
            return self._get_default_proposals()

    def get_last_raw_response(self):
        return self.last_raw_response

    def _get_default_proposals(self):
        return [
            {
                "id": 1,
                "type": "scatter",
                "title": "Relation entre deux variables principales",
                "justification": "false",
                "config": {"x_axis": "auto", "y_axis": "auto"}
            },
            {
                "id": 2,
                "type": "bar",
                "title": "Comparaison par catégories",
                "justification": "false",
                "config": {"aggregation": "mean"}
            },
            {
                "id": 3,
                "type": "heatmap",
                "title": "Matrice de corrélation",
                "justification": "false",
                "config": {}
            }
        ]