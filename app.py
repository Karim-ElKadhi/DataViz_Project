from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import pandas as pd
import json
import os
from utils.analyse import DataAnalyzer
from utils.prompt import GeminiService
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize services
data_analyzer = DataAnalyzer()
gemini_service = GeminiService(api_key=os.getenv('GROQ_API_KEY'))

# Store uploaded data in memory
current_dataset = None

# Routes for HTML pages
@app.route('/')
def index():
    return render_template('index.html')

# API Routes
@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload and analyze CSV file"""
    global current_dataset
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Read CSV
        df = pd.read_csv(file)
        current_dataset = df
        
        # Analyze dataset
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
    """Generate 3 visualization proposals using Gemini"""
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
        
        # Get the raw response for debugging
        raw_response = gemini_service.get_last_raw_response()
        
        return jsonify({
            'success': True,
            'proposals': proposals,
            'raw_response': raw_response  # Include raw response in API response
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-raw-response', methods=['GET'])
def get_raw_response():
    """Get the last raw response from Gemini for debugging"""
    raw_response = gemini_service.get_last_raw_response()
    
    if raw_response is None:
        return jsonify({
            'success': False,
            'message': 'No response available yet'
        }), 404
    
    return jsonify({
        'success': True,
        'raw_response': raw_response
    })

@app.route('/api/prepare-visualization', methods=['POST'])
def prepare_visualization():
    """Prepare data for selected visualization"""
    global current_dataset
    
    if current_dataset is None:
        return jsonify({'error': 'No dataset uploaded'}), 400
    
    data = request.json
    viz_config = data.get('config', {})
    viz_type = data.get('type', '')
    
    try:
        # Prepare data based on visualization type
        prepared_data = data_analyzer.prepare_visualization_data(
            current_dataset, 
            viz_type, 
            viz_config
        )
        
        # Check if there's an error in the prepared data
        if 'error' in prepared_data:
            return jsonify({
                'success': False,
                'error': prepared_data['error']
            }), 400
        
        return jsonify({
            'success': True,
            'data': prepared_data,
            'config': viz_config
        })
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error preparing visualization: {error_details}")
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7860))
    app.run(debug=False, host='0.0.0.0', port=port)