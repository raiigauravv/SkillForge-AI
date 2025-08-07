"""
Interactive Data Visualization Dashboard using Plotly
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json

class VisualizationEngine:
    def __init__(self):
        self.color_palette = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
    
    def create_workflow_trends_chart(self, time_series_data: List[Dict]) -> str:
        """Create workflow trends over time chart"""
        try:
            df = pd.DataFrame(time_series_data)
            
            if df.empty:
                return self._create_empty_chart("No workflow data available")
            
            df['date'] = pd.to_datetime(df['date'])
            
            fig = go.Figure()
            
            # Add trend line
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['count'],
                mode='lines+markers',
                name='Daily Workflows',
                line=dict(color=self.color_palette[0], width=3),
                marker=dict(size=8)
            ))
            
            # Add moving average
            if len(df) >= 7:
                df['ma_7'] = df['count'].rolling(window=7).mean()
                fig.add_trace(go.Scatter(
                    x=df['date'],
                    y=df['ma_7'],
                    mode='lines',
                    name='7-Day Average',
                    line=dict(color=self.color_palette[1], width=2, dash='dash')
                ))
            
            fig.update_layout(
                title="📈 Workflow Creation Trends",
                xaxis_title="Date",
                yaxis_title="Number of Workflows",
                template="plotly_white",
                height=400,
                showlegend=True
            )
            
            return fig.to_html(include_plotlyjs=True, div_id="trends-chart")
            
        except Exception as e:
            return self._create_error_chart(f"Error creating trends chart: {e}")
    
    def create_success_distribution_chart(self, df: pd.DataFrame) -> str:
        """Create success score distribution chart"""
        try:
            if df.empty:
                return self._create_empty_chart("No success data available")
            
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Success Score Distribution', 'Success by Priority'),
                specs=[[{'type': 'histogram'}, {'type': 'box'}]]
            )
            
            # Histogram of success scores
            fig.add_trace(
                go.Histogram(
                    x=df['success_score'],
                    nbinsx=20,
                    name='Success Distribution',
                    marker_color=self.color_palette[2],
                    opacity=0.7
                ),
                row=1, col=1
            )
            
            # Box plot by priority
            priorities = df['priority'].unique()
            for i, priority in enumerate(priorities):
                priority_data = df[df['priority'] == priority]['success_score']
                fig.add_trace(
                    go.Box(
                        y=priority_data,
                        name=priority.title(),
                        marker_color=self.color_palette[i % len(self.color_palette)]
                    ),
                    row=1, col=2
                )
            
            fig.update_layout(
                title="🎯 Workflow Success Analytics",
                template="plotly_white",
                height=400,
                showlegend=False
            )
            
            return fig.to_html(include_plotlyjs=True, div_id="success-chart")
            
        except Exception as e:
            return self._create_error_chart(f"Error creating success chart: {e}")
    
    def create_clustering_visualization(self, clustering_data: Dict) -> str:
        """Create clustering analysis visualization"""
        try:
            if 'error' in clustering_data:
                return self._create_empty_chart(f"Clustering Error: {clustering_data['error']}")
            
            cluster_analysis = clustering_data.get('cluster_analysis', {})
            
            if not cluster_analysis:
                return self._create_empty_chart("No clustering data available")
            
            # Prepare data for visualization
            cluster_names = list(cluster_analysis.keys())
            sizes = [cluster_analysis[cluster]['size'] for cluster in cluster_names]
            success_scores = [cluster_analysis[cluster]['avg_success_score'] for cluster in cluster_names]
            
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Cluster Sizes', 'Avg Success by Cluster'),
                specs=[[{'type': 'pie'}, {'type': 'bar'}]]
            )
            
            # Pie chart for cluster sizes
            fig.add_trace(
                go.Pie(
                    labels=[f"Cluster {i}" for i in range(len(cluster_names))],
                    values=sizes,
                    name="Cluster Distribution"
                ),
                row=1, col=1
            )
            
            # Bar chart for success scores
            fig.add_trace(
                go.Bar(
                    x=[f"Cluster {i}" for i in range(len(cluster_names))],
                    y=success_scores,
                    name="Avg Success Score",
                    marker_color=self.color_palette[:len(cluster_names)]
                ),
                row=1, col=2
            )
            
            fig.update_layout(
                title="🔍 Workflow Pattern Clusters",
                template="plotly_white",
                height=400
            )
            
            return fig.to_html(include_plotlyjs=True, div_id="clustering-chart")
            
        except Exception as e:
            return self._create_error_chart(f"Error creating clustering chart: {e}")
    
    def create_hourly_heatmap(self, hourly_data: List[Dict]) -> str:
        """Create hourly workflow patterns heatmap"""
        try:
            df = pd.DataFrame(hourly_data)
            
            if df.empty:
                return self._create_empty_chart("No hourly data available")
            
            # Create a 24-hour heatmap
            hours = list(range(24))
            hour_counts = df.set_index('hour')['count'].reindex(hours, fill_value=0)
            
            # Create matrix for heatmap (7 days x 24 hours)
            heatmap_data = []
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            
            for day in range(7):
                row = []
                for hour in range(24):
                    # Simulate day-of-week variation (you can replace with real data)
                    base_count = hour_counts.iloc[hour]
                    variation = np.random.normal(1, 0.1)  # Add some variation
                    row.append(max(0, int(base_count * variation)))
                heatmap_data.append(row)
            
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data,
                x=[f"{h:02d}:00" for h in range(24)],
                y=days,
                colorscale='Blues',
                hoverongaps=False
            ))
            
            fig.update_layout(
                title="⏰ Workflow Activity Heatmap",
                xaxis_title="Hour of Day",
                yaxis_title="Day of Week",
                template="plotly_white",
                height=300
            )
            
            return fig.to_html(include_plotlyjs=True, div_id="heatmap-chart")
            
        except Exception as e:
            return self._create_error_chart(f"Error creating heatmap: {e}")
    
    def create_ml_performance_chart(self, ml_data: Dict) -> str:
        """Create ML model performance visualization"""
        try:
            if 'error' in ml_data:
                return self._create_empty_chart(f"ML Error: {ml_data['error']}")
            
            feature_importance = ml_data.get('feature_importance', {})
            accuracy = ml_data.get('accuracy', 0)
            
            if not feature_importance:
                return self._create_empty_chart("No ML performance data available")
            
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Feature Importance', 'Model Performance'),
                specs=[[{'type': 'bar'}, {'type': 'indicator'}]]
            )
            
            # Feature importance bar chart
            features = list(feature_importance.keys())
            importance = list(feature_importance.values())
            
            fig.add_trace(
                go.Bar(
                    x=importance,
                    y=features,
                    orientation='h',
                    name="Feature Importance",
                    marker_color=self.color_palette[3]
                ),
                row=1, col=1
            )
            
            # Accuracy gauge
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=accuracy * 100,
                    domain={'x': [0.6, 1], 'y': [0, 1]},
                    title={'text': "Accuracy %"},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': self.color_palette[4]},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 80], 'color': "yellow"},
                            {'range': [80, 100], 'color': "green"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ),
                row=1, col=2
            )
            
            fig.update_layout(
                title="🤖 ML Model Performance",
                template="plotly_white",
                height=400
            )
            
            return fig.to_html(include_plotlyjs=True, div_id="ml-chart")
            
        except Exception as e:
            return self._create_error_chart(f"Error creating ML chart: {e}")
    
    def create_comprehensive_dashboard(self, analytics_data: Dict) -> str:
        """Create a comprehensive dashboard with all visualizations"""
        try:
            # Extract data
            summary_stats = analytics_data.get('summary_stats', {})
            time_series = analytics_data.get('time_series', [])
            priority_analysis = analytics_data.get('priority_analysis', [])
            hourly_patterns = analytics_data.get('hourly_patterns', [])
            ml_predictions = analytics_data.get('ml_predictions', {})
            clustering_analysis = analytics_data.get('clustering_analysis', {})
            
            # Create individual charts
            trends_chart = self.create_workflow_trends_chart(time_series)
            hourly_heatmap = self.create_hourly_heatmap(hourly_patterns)
            clustering_viz = self.create_clustering_visualization(clustering_analysis)
            ml_performance = self.create_ml_performance_chart(ml_predictions)
            
            # Create summary cards HTML
            summary_html = f"""
            <div class="analytics-summary">
                <div class="summary-card">
                    <h3>📊 Total Workflows</h3>
                    <p class="metric">{summary_stats.get('total_workflows', 0)}</p>
                </div>
                <div class="summary-card">
                    <h3>🎯 Avg Success Score</h3>
                    <p class="metric">{summary_stats.get('avg_success_score', 0):.1f}%</p>
                </div>
                <div class="summary-card">
                    <h3>✅ Completion Rate</h3>
                    <p class="metric">{summary_stats.get('completion_rate', 0):.1f}%</p>
                </div>
                <div class="summary-card">
                    <h3>📅 Data Range</h3>
                    <p class="metric">{summary_stats.get('data_range_days', 0)} days</p>
                </div>
            </div>
            """
            
            # Combine all visualizations
            dashboard_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Workflow Analytics Dashboard</title>
                <style>
                    .analytics-summary {{
                        display: flex;
                        gap: 20px;
                        margin: 20px 0;
                        flex-wrap: wrap;
                    }}
                    .summary-card {{
                        background: #f8f9fa;
                        padding: 20px;
                        border-radius: 8px;
                        text-align: center;
                        min-width: 200px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                    .summary-card h3 {{
                        margin: 0 0 10px 0;
                        color: #333;
                        font-size: 14px;
                    }}
                    .metric {{
                        font-size: 24px;
                        font-weight: bold;
                        color: #1f77b4;
                        margin: 0;
                    }}
                    .chart-container {{
                        margin: 20px 0;
                        background: white;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                </style>
            </head>
            <body>
                <h1>🚀 Workflow Analytics Dashboard</h1>
                {summary_html}
                
                <div class="chart-container">
                    {trends_chart}
                </div>
                
                <div class="chart-container">
                    {hourly_heatmap}
                </div>
                
                <div class="chart-container">
                    {clustering_viz}
                </div>
                
                <div class="chart-container">
                    {ml_performance}
                </div>
                
                <p><em>Generated at: {analytics_data.get('generated_at', datetime.now().isoformat())}</em></p>
            </body>
            </html>
            """
            
            return dashboard_html
            
        except Exception as e:
            return f"<html><body><h1>Error creating dashboard: {e}</h1></body></html>"
    
    def _create_empty_chart(self, message: str) -> str:
        """Create an empty chart with a message"""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            template="plotly_white",
            height=300,
            xaxis={'visible': False},
            yaxis={'visible': False}
        )
        return fig.to_html(include_plotlyjs=True)
    
    def _create_error_chart(self, error_message: str) -> str:
        """Create an error chart"""
        return self._create_empty_chart(f"⚠️ {error_message}")

# Global visualization engine
viz_engine = VisualizationEngine()
