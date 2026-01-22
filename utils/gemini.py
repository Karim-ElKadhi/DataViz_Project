from google import genai
import json

class GeminiService:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_visualization_proposals(self, question, dataset_info, columns):
        
        prompt = f"""
Tu es un expert en data visualisation. Analyse la question de l'utilisateur et propose 3 visualisations différentes et pertinentes.

QUESTION DE L'UTILISATEUR:
{question}

INFORMATIONS SUR LE DATASET (House Pricing):
Colonnes disponibles: {', '.join(columns)}

Statistiques descriptives:
{json.dumps(dataset_info.get('statistics', {}), indent=2)}

Corrélations importantes:
{json.dumps(dataset_info.get('correlations', {}), indent=2)}

Variables catégorielles: mainroad, guestroom, basement, hotwaterheating, airconditioning, prefarea, furnishingstatus
Variables numériques: price, area, bedrooms, bathrooms, stories, parking

INSTRUCTIONS:
Propose exactement 3 visualisations différentes qui répondent à la question.
Pour chaque visualisation, fournis:
1. Un type de graphique (scatter, bar, box, heatmap, violin, line)
2. Un titre descriptif
3. Une justification claire (2-3 phrases) expliquant pourquoi cette visualisation répond à la question
4. La configuration technique (axes, variables, groupements)

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
- Toutes les colonnes mentionnées existent dans le dataset
- La réponse est un JSON valide et complet
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
        """Fallback default proposals"""
        return [
            {
                "id": 1,
                "type": "scatter",
                "title": "Relation entre surface et prix",
                "justification": "Un nuage de points permet d'identifier la corrélation directe entre la surface du logement et son prix, tout en visualisant la dispersion des données.",
                "config": {
                    "x_axis": "area",
                    "y_axis": "price",
                    "color_by": "furnishingstatus"
                }
            },
            {
                "id": 2,
                "type": "bar",
                "title": "Prix moyen selon le nombre de chambres",
                "justification": "Un diagramme en barres compare efficacement les prix moyens pour différents nombres de chambres, révélant l'impact de cette variable sur le prix.",
                "config": {
                    "x_axis": "bedrooms",
                    "y_axis": "price",
                    "aggregation": "mean"
                }
            },
            {
                "id": 3,
                "type": "box",
                "title": "Distribution des prix par statut de meublage",
                "justification": "Les boîtes à moustaches montrent la distribution complète des prix selon le statut de meublage, incluant médiane, quartiles et valeurs extrêmes.",
                "config": {
                    "category": "furnishingstatus",
                    "value": "price"
                }
            }
        ]