import google.generativeai as genai
import json

class GeminiService:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
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

RÈGLES IMPORTANTES:
1. Utilise UNIQUEMENT les colonnes qui existent dans le dataset
2. Adapte le type de visualisation au type de données (numériques vs catégorielles)
3. Les 3 visualisations doivent être COMPLÉMENTAIRES et apporter des perspectives différentes
4. Priorise les variables les plus pertinentes pour répondre à la question

Types de graphiques disponibles:
- "scatter": Pour relations entre 2 variables numériques (peut inclure color_by pour une catégorie)
- "bar": Pour comparer des moyennes/sommes par catégorie
- "box": Pour voir la distribution d'une variable numérique par catégories
- "heatmap": Pour matrice de corrélation entre variables numériques
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
      "type": "scatter",
      "title": "Titre de la visualisation",
      "justification": "Explication de pourquoi cette visualisation est pertinente...",
      "config": {{
        "x_axis": "nom_colonne",
        "y_axis": "nom_colonne",
        "color_by": "nom_colonne_optionnel",
        "size_by": "nom_colonne_optionnel"
      }}
    }},
    {{
      "id": 2,
      "type": "bar",
      "title": "Autre titre",
      "justification": "Autre explication...",
      "config": {{
        "x_axis": "nom_colonne",
        "y_axis": "price",
        "aggregation": "mean"
      }}
    }},
    {{
      "id": 3,
      "type": "box",
      "title": "Troisième titre",
      "justification": "Troisième explication...",
      "config": {{
        "category": "nom_colonne",
        "value": "price"
      }}
    }}
  ]
}}

Assure-toi que:
- Les 3 visualisations sont DIFFÉRENTES (types et variables différents)
- Toutes les colonnes mentionnées existent EXACTEMENT dans le dataset (respecte la casse)
- Les types de graphiques correspondent aux types de données (numériques/catégorielles)
- Chaque visualisation apporte une réponse complémentaire à la question
- La réponse est un JSON valide et complet sans texte supplémentaire
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
            
            # Parse JSON
            proposals = json.loads(response_text)
            
            # Validate structure
            if 'propositions' not in proposals:
                raise ValueError("Invalid response structure")
            
            return proposals['propositions']
        
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response text: {response_text}")
            # Return default proposals as fallback
            return self._get_default_proposals()
        except Exception as e:
            print(f"Error generating proposals: {e}")
            return self._get_default_proposals()
    
    def _get_default_proposals(self):
        """Fallback generic proposals based on data types"""
        return [
            {
                "id": 1,
                "type": "scatter",
                "title": "Relation entre deux variables principales",
                "justification": "Un nuage de points permet d'identifier les corrélations et patterns entre les principales variables du dataset.",
                "config": {
                    "x_axis": "auto",
                    "y_axis": "auto",
                    "color_by": None
                }
            },
            {
                "id": 2,
                "type": "bar",
                "title": "Comparaison par catégories",
                "justification": "Un diagramme en barres compare efficacement les valeurs moyennes entre différentes catégories du dataset.",
                "config": {
                    "x_axis": "auto",
                    "y_axis": "auto",
                    "aggregation": "mean"
                }
            },
            {
                "id": 3,
                "type": "heatmap",
                "title": "Matrice de corrélation complète",
                "justification": "Une heatmap révèle toutes les corrélations entre variables numériques, offrant une vue d'ensemble des relations dans les données.",
                "config": {}
            }
        ]