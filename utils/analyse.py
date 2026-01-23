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
        # Correlations between all numeric columns
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            # Get top correlations
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
            # Sort by absolute correlation value
            correlations_list.sort(key=lambda x: abs(x['correlation']), reverse=True)
            analysis['correlations'] = correlations_list[:10]  # Top 10 correlations
        
        # Categorical info with limits
        for col in categorical_cols:
            unique_vals = df[col].dropna().unique()
            value_counts = df[col].value_counts()
            
            # Limit to top 20 categories to avoid overwhelming Gemini
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
        """Prepare data for specific visualization type"""
        
        if viz_type == 'scatter':
            return self._prepare_scatter(df, config)
        elif viz_type == 'bar':
            return self._prepare_bar(df, config)
        elif viz_type == 'horizontalBar':
            return self._prepare_horizontal_bar(df, config)
        elif viz_type == 'pie':
            return self._prepare_pie(df, config)
        elif viz_type == 'box':
            return self._prepare_box(df, config)
        elif viz_type == 'correlationMatrix':
            return self._prepare_correlation_matrix(df, config)
        elif viz_type == 'heatmap':
            return self._prepare_heatmap(df, config)
        elif viz_type == 'violin':
            return self._prepare_violin(df, config)
        elif viz_type == 'line':
            return self._prepare_line(df, config)
        else:
            return {'error': f'Unknown visualization type: {viz_type}'}
    
    def _prepare_scatter(self, df, config):
        """Prepare scatter plot data"""
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
        """Prepare bar chart data"""
        x_axis = config.get('x_axis')
        y_axis = config.get('y_axis')
        aggregation = config.get('aggregation', 'count')  # Default to count
        
        # Validation x_axis
        if not x_axis or x_axis not in df.columns:
            return {'error': f'Column {x_axis} not found in dataset'}
        
        # If no y_axis specified, use count aggregation
        if not y_axis or y_axis not in df.columns:
            if aggregation == 'count' or not y_axis:
                # Count mode - just count occurrences
                try:
                    df_clean = df[x_axis].dropna()
                    if len(df_clean) == 0:
                        return {'error': 'No valid data after removing NaN values'}
                    
                    grouped = df_clean.value_counts()
                    data = [
                        {'category': str(cat), 'value': int(val)}
                        for cat, val in grouped.items()
                    ]
                    
                    return {
                        'data': sorted(data, key=lambda x: x['category']),
                        'x_label': x_axis,
                        'y_label': 'Count'
                    }
                except Exception as e:
                    return {'error': f'Error preparing bar chart: {str(e)}'}
            else:
                # Need numeric column for aggregation
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                if numeric_cols:
                    y_axis = numeric_cols[0]
                else:
                    return {'error': 'No numeric column found for aggregation'}
        
        try:
            # Drop NaN values before grouping
            df_clean = df[[x_axis, y_axis]].dropna()
            
            if len(df_clean) == 0:
                return {'error': 'No valid data after removing NaN values'}
            
            if aggregation == 'mean':
                grouped = df_clean.groupby(x_axis)[y_axis].mean()
            elif aggregation == 'sum':
                grouped = df_clean.groupby(x_axis)[y_axis].sum()
            elif aggregation == 'count':
                grouped = df_clean.groupby(x_axis)[y_axis].count()
            else:
                grouped = df_clean.groupby(x_axis)[y_axis].mean()
            
            data = [
                {'category': str(cat), 'value': float(val)}
                for cat, val in grouped.items()
            ]
            
            return {
                'data': sorted(data, key=lambda x: x['category']),
                'x_label': x_axis,
                'y_label': f'{aggregation.capitalize()} of {y_axis}'
            }
        except Exception as e:
            return {'error': f'Error preparing bar chart: {str(e)}'}
    
    def _prepare_horizontal_bar(self, df, config):
        """Prepare horizontal bar chart data"""
        # Same as bar but return flag for horizontal rendering
        result = self._prepare_bar(df, config)
        if 'error' not in result:
            result['horizontal'] = True
        return result
    
    def _prepare_pie(self, df, config):
        """Prepare pie chart data"""
        category = config.get('category')
        value = config.get('value', None)
        aggregation = config.get('aggregation', 'count')
        
        # Validation
        if not category or category not in df.columns:
            return {'error': f'Column {category} not found in dataset'}
        
        try:
            # If no value specified or aggregation is count, just count occurrences
            if not value or aggregation == 'count':
                # Count occurrences
                grouped = df[category].value_counts()
            elif value in df.columns:
                # Aggregate a specific value column
                df_clean = df[[category, value]].dropna()
                
                if len(df_clean) == 0:
                    return {'error': 'No valid data after removing NaN values'}
                
                if aggregation == 'sum':
                    grouped = df_clean.groupby(category)[value].sum()
                elif aggregation == 'mean':
                    grouped = df_clean.groupby(category)[value].mean()
                else:
                    grouped = df_clean.groupby(category)[value].sum()
            else:
                return {'error': f'Column {value} not found in dataset'}
            
            data = [
                {'label': str(cat), 'value': float(val)}
                for cat, val in grouped.items()
            ]
            
            # Limit to top 10 for readability
            data = sorted(data, key=lambda x: x['value'], reverse=True)[:10]
            
            return {
                'data': data,
                'category_label': category,
                'value_label': value if value else 'Count'
            }
        except Exception as e:
            return {'error': f'Error preparing pie chart: {str(e)}'}
    
    def _prepare_box(self, df, config):
        """Prepare box plot data"""
        category = config.get('category')
        value = config.get('value')
        
        # Validation
        if not category or category not in df.columns:
            return {'error': f'Column {category} not found'}
        
        if not value or value not in df.columns:
            # Try to find first numeric column
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                value = numeric_cols[0]
            else:
                return {'error': 'No numeric column found'}
        
        try:
            data = []
            for cat in df[category].unique():
                if pd.isna(cat):
                    continue
                    
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
            
            if not data:
                return {'error': 'No valid data for box plot'}
            
            return {
                'data': data,
                'x_label': category,
                'y_label': value
            }
        except Exception as e:
            return {'error': f'Error preparing box plot: {str(e)}'}
    
    def _prepare_heatmap(self, df, config):
        """Prepare correlation heatmap data"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Limit to specified columns or top correlations
        if 'columns' in config and config['columns']:
            cols_to_use = [c for c in config['columns'] if c in numeric_cols]
        else:
            cols_to_use = numeric_cols[:10]  # Limit to 10 for readability
        
        if len(cols_to_use) < 2:
            return {'error': 'Need at least 2 numeric columns for heatmap'}
        
        corr_matrix = df[cols_to_use].corr()
        
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
            'variables': cols_to_use,
            'x_label': 'Variables',
            'y_label': 'Variables'
        }
    
    def _prepare_correlation_matrix(self, df, config):
        """Prepare full correlation matrix"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) < 2:
            return {'error': 'Need at least 2 numeric columns for correlation matrix'}
        
        # Limit to 12 columns max for readability
        cols_to_use = numeric_cols[:12]
        
        corr_matrix = df[cols_to_use].corr()
        
        # Convert to format suitable for heatmap
        data = []
        for i, row_name in enumerate(corr_matrix.index):
            row_data = []
            for j, col_name in enumerate(corr_matrix.columns):
                row_data.append({
                    'x': j,
                    'y': i,
                    'value': float(corr_matrix.iloc[i, j]),
                    'xLabel': col_name,
                    'yLabel': row_name
                })
            data.append(row_data)
        
        return {
            'data': data,
            'variables': cols_to_use,
            'x_labels': cols_to_use,
            'y_labels': cols_to_use,
            'type': 'correlationMatrix'
        }
    
    def _prepare_line(self, df, config):
        """Prepare line chart data"""
        x_axis = config.get('x_axis')
        y_axis = config.get('y_axis')
        
        # Sort by x_axis for proper line chart
        df_sorted = df.sort_values(by=x_axis)
        
        data = []
        for _, row in df_sorted.iterrows():
            if pd.notna(row[x_axis]) and pd.notna(row[y_axis]):
                data.append({
                    'x': str(row[x_axis]),
                    'y': float(row[y_axis])
                })
        
        return {
            'data': data,
            'x_label': x_axis,
            'y_label': y_axis
        }
    
    def _prepare_violin(self, df, config):
        """Prepare violin plot data"""
        # Similar to box plot but return all values for violin rendering
        return self._prepare_box(df, config)