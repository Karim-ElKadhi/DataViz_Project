import pandas as pd
import numpy as np

class DataAnalyzer:
    def analyze_dataset(self, df):
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        analysis = {
            'statistics': {},
            'correlations': {},
            'categorical_info': {}
        }
        
        # stats basiques
        for col in numeric_cols:
            analysis['statistics'][col] = {
                'mean': float(df[col].mean()),
                'median': float(df[col].median()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'std': float(df[col].std())
            }
        
        # Correlations 
        if 'price' in numeric_cols:
            correlations = df[numeric_cols].corr()['price'].to_dict()
            analysis['correlations'] = {
                k: float(v) for k, v in correlations.items() 
                if k != 'price' and not np.isnan(v)
            }
        
        # Info catégorielle
        for col in categorical_cols:
            analysis['categorical_info'][col] = {
                'unique_values': df[col].unique().tolist(),
                'value_counts': df[col].value_counts().to_dict()
            }
        
        return analysis
    
    def prepare_visualization_data(self, df, viz_type, config):
        
        if viz_type == 'scatter':
            return self._prepare_scatter(df, config)
        elif viz_type == 'bar':
            return self._prepare_bar(df, config)
        elif viz_type == 'box':
            return self._prepare_box(df, config)
        elif viz_type == 'heatmap':
            return self._prepare_heatmap(df, config)
        elif viz_type == 'violin':
            return self._prepare_violin(df, config)
        else:
            return {'error': f'Unknown visualization type: {viz_type}'}
    
    def _prepare_scatter(self, df, config):
        x_axis = config.get('x_axis')
        y_axis = config.get('y_axis')
        color_by = config.get('color_by')
        
        data = []
        for _, row in df.iterrows():
            point = {
                'x': float(row[x_axis]) if pd.notna(row[x_axis]) else None,
                'y': float(row[y_axis]) if pd.notna(row[y_axis]) else None
            }
            if color_by and color_by in df.columns:
                point['category'] = str(row[color_by])
            data.append(point)
        
        return {
            'data': data,
            'x_label': x_axis,
            'y_label': y_axis,
            'color_label': color_by
        }
    
    def _prepare_bar(self, df, config):
        x_axis = config.get('x_axis')
        y_axis = config.get('y_axis', 'price')
        aggregation = config.get('aggregation', 'mean')
        
        if aggregation == 'mean':
            grouped = df.groupby(x_axis)[y_axis].mean()
        elif aggregation == 'sum':
            grouped = df.groupby(x_axis)[y_axis].sum()
        elif aggregation == 'count':
            grouped = df.groupby(x_axis)[y_axis].count()
        else:
            grouped = df.groupby(x_axis)[y_axis].mean()
        
        data = [
            {'category': str(cat), 'value': float(val)}
            for cat, val in grouped.items()
        ]
        
        return {
            'data': sorted(data, key=lambda x: x['category']),
            'x_label': x_axis,
            'y_label': f'{aggregation.capitalize()} of {y_axis}'
        }
    
    def _prepare_box(self, df, config):
        category = config.get('category')
        value = config.get('value', 'price')
        
        data = []
        for cat in df[category].unique():
            values = df[df[category] == cat][value].dropna().tolist()
            if values:
                data.append({
                    'category': str(cat),
                    'values': values,
                    'min': float(np.min(values)),
                    'q1': float(np.percentile(values, 25)),
                    'median': float(np.median(values)),
                    'q3': float(np.percentile(values, 75)),
                    'max': float(np.max(values))
                })
        
        return {
            'data': data,
            'x_label': category,
            'y_label': value
        }
    
    def _prepare_heatmap(self, df, config):
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        corr_matrix = df[numeric_cols].corr()
        
        data = []
        for i, row_name in enumerate(corr_matrix.index):
            for j, col_name in enumerate(corr_matrix.columns):
                data.append({
                    'x': col_name,
                    'y': row_name,
                    'value': float(corr_matrix.iloc[i, j])
                })
        
        return {
            'data': data,
            'variables': numeric_cols
        }
    
    def _prepare_violin(self, df, config):
        return self._prepare_box(df, config)