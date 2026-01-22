from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import json
import os
from utils.analyse import DataAnalyzer
from utils.gemini import GeminiService

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

data_analyzer = DataAnalyzer()
gemini_service = GeminiService(api_key=os.getenv('GEMINI_API_KEY'))

current_dataset = None

@app.route('/api/upload', methods=['POST'])
def upload_file():
    global current_dataset
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        df = pd.read_csv(file)
        current_dataset = df
        
        analysis = data_analyzer.analyze_dataset(df)
        
        return jsonify({
            'success': True,
            'message': 'Dataset uploaded successfully',
            'rows': len(df),
            'columns': list(df.columns),
            'analysis': analysis
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-visualizations', methods=['POST'])
def generate_visualizations():
    global current_dataset
    
    if current_dataset is None:
        return jsonify({'error': 'No dataset uploaded'}), 400
    
    data = request.json
    user_question = data.get('question', '')
    
    if not user_question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        # Get dataset analysis
        analysis = data_analyzer.analyze_dataset(current_dataset)
        
        # Generate proposals with Gemini
        proposals = gemini_service.generate_visualization_proposals(
            question=user_question,
            dataset_info=analysis,
            columns=list(current_dataset.columns)
        )
        
        return jsonify({
            'success': True,
            'proposals': proposals
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/prepare-visualization', methods=['POST'])
def prepare_visualization():
    global current_dataset
    
    if current_dataset is None:
        return jsonify({'error': 'No dataset uploaded'}), 400
    
    data = request.json
    viz_config = data.get('config', {})
    viz_type = data.get('type', '')
    
    try:
        prepared_data = data_analyzer.prepare_visualization_data(
            current_dataset, 
            viz_type, 
            viz_config
        )
        
        return jsonify({
            'success': True,
            'data': prepared_data,
            'config': viz_config
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)