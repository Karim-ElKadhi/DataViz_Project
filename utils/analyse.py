import pandas as pd
import numpy as np

class DataAnalyzer:
    def analyze_dataset(self, df):
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
        
        for col in categorical_cols:
            if df[col].dtype == 'bool':
                df[col] = df[col].astype(str)
        
        analysis = {
            'statistics': {},
            'correlations': {},
            'categorical_info': {},
            'dataset_summary': {
                'total_rows': len(df),
                'total_columns': len(df.columns),
                'numeric_columns': len(numeric_cols),
                'categorical_columns': len(categorical_cols),
                'missing_values': df.isnull().sum().to_dict()
            }
        }
        
        # stats basiques
        for col in numeric_cols:
            analysis['statistics'][col] = {
                'mean': float(df[col].mean()) if not df[col].isnull().all() else None,
                'median': float(df[col].median()) if not df[col].isnull().all() else None,
                'min': float(df[col].min()) if not df[col].isnull().all() else None,
                'max': float(df[col].max()) if not df[col].isnull().all() else None,
                'std': float(df[col].std()) if not df[col].isnull().all() else None
            }
        
        # Correlations 
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            correlations_list = []
            for i in range(len(numeric_cols)):
                for j in range(i+1, len(numeric_cols)):
                    corr_value = corr_matrix.iloc[i, j]
                    if not np.isnan(corr_value):
                        correlations_list.append({
                            'var1': numeric_cols[i],
                            'var2': numeric_cols[j],
                            'correlation': float(corr_value)
                        })
            # tri
            correlations_list.sort(key=lambda x: abs(x['correlation']), reverse=True)
            analysis['correlations'] = correlations_list[:10]  # Top 10 correlations
        
        # Infos catégorielles
        for col in categorical_cols:
            unique_vals = df[col].dropna().unique()
            value_counts = df[col].value_counts()
            
            # Limite aux 20 premières catégories pour éviter de surcharger Gemini
            if len(unique_vals) > 20:
                top_values = value_counts.head(20).to_dict()
                analysis['categorical_info'][col] = {
                    'unique_count': len(unique_vals),
                    'top_20_values': {str(k): int(v) for k, v in top_values.items()},
                    'note': f'Showing top 20 out of {len(unique_vals)} unique values'
                }
            else:
                analysis['categorical_info'][col] = {
                    'unique_count': len(unique_vals),
                    'unique_values': [str(v) for v in unique_vals[:50]],  # Limit to 50
                    'value_counts': {str(k): int(v) for k, v in value_counts.to_dict().items()}
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