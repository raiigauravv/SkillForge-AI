"""
Data Science Analytics Engine for Workflow Performance Analysis
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, r2_score
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import asyncio
from typing import Dict, List, Any
import logging

from database.mongodb_config import db_manager

logger = logging.getLogger(__name__)

class DataScienceEngine:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.models = {}
        
    async def collect_workflow_data(self, days_back: int = 30) -> pd.DataFrame:
        """Collect workflow data for analysis"""
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Query workflows from MongoDB
            cursor = db_manager.db.workflows.find({
                "created_at": {"$gte": start_date, "$lte": end_date}
            })
            
            workflows = await cursor.to_list(length=None)
            
            if not workflows:
                logger.warning("No workflow data found")
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(workflows)
            
            # Data preprocessing
            df = self._preprocess_workflow_data(df)
            
            logger.info(f"Collected {len(df)} workflow records for analysis")
            return df
            
        except Exception as e:
            logger.error(f"Error collecting workflow data: {e}")
            return pd.DataFrame()
    
    def _preprocess_workflow_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess workflow data for analysis"""
        try:
            # Convert datetime columns
            if 'created_at' in df.columns:
                df['created_at'] = pd.to_datetime(df['created_at'])
                df['hour'] = df['created_at'].dt.hour
                df['day_of_week'] = df['created_at'].dt.dayofweek
                df['month'] = df['created_at'].dt.month
            
            # Extract numeric features from token_usage
            if 'token_usage' in df.columns:
                df['total_tokens'] = df['token_usage'].apply(
                    lambda x: x.get('total_tokens', 0) if isinstance(x, dict) else 0
                )
                df['completion_tokens'] = df['token_usage'].apply(
                    lambda x: x.get('completion_tokens', 0) if isinstance(x, dict) else 0
                )
            
            # Calculate success score based on execution time and user feedback
            df['success_score'] = self._calculate_success_score(df)
            
            # Add categorical features
            df['priority_numeric'] = df['priority'].map({
                'low': 1, 'medium': 2, 'high': 3, 'urgent': 4
            }).fillna(2)
            
            # Fill missing values
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())
            
            categorical_columns = df.select_dtypes(include=['object']).columns
            df[categorical_columns] = df[categorical_columns].fillna('unknown')
            
            return df
            
        except Exception as e:
            logger.error(f"Error preprocessing data: {e}")
            return df
    
    def _calculate_success_score(self, df: pd.DataFrame) -> pd.Series:
        """Calculate workflow success score"""
        try:
            # Base score from completion status
            base_score = df['status'].map({
                'completed': 100,
                'in_progress': 50,
                'failed': 0,
                'cancelled': 25
            }).fillna(50)
            
            # Adjust based on execution time (faster = better, up to reasonable limit)
            if 'execution_time' in df.columns:
                # Normalize execution time (lower is better)
                max_time = df['execution_time'].quantile(0.95)
                time_penalty = (df['execution_time'] / max_time * 30).clip(0, 30)
                base_score = base_score - time_penalty
            
            # Adjust based on user feedback if available
            if 'user_feedback' in df.columns:
                feedback_bonus = df['user_feedback'].apply(
                    lambda x: x.get('rating', 0) * 5 if isinstance(x, dict) else 0
                )
                base_score = base_score + feedback_bonus
            
            return base_score.clip(0, 100)
            
        except Exception as e:
            logger.error(f"Error calculating success score: {e}")
            return pd.Series([75] * len(df))
    
    async def predict_workflow_success(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Build ML model to predict workflow success"""
        try:
            if df.empty or len(df) < 10:
                return {"error": "Insufficient data for prediction model"}
            
            # Prepare features
            feature_columns = [
                'priority_numeric', 'hour', 'day_of_week', 'month',
                'total_tokens', 'completion_tokens'
            ]
            
            # Filter available columns
            available_features = [col for col in feature_columns if col in df.columns]
            
            if len(available_features) < 3:
                return {"error": "Insufficient features for prediction"}
            
            X = df[available_features].fillna(0)
            y = (df['success_score'] > 75).astype(int)  # Binary: successful or not
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train model
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Feature importance
            feature_importance = dict(zip(available_features, model.feature_importances_))
            
            # Store model
            self.models['success_prediction'] = model
            
            return {
                "model_type": "Random Forest Classifier",
                "accuracy": accuracy,
                "feature_importance": feature_importance,
                "training_samples": len(X_train),
                "test_samples": len(X_test),
                "features_used": available_features
            }
            
        except Exception as e:
            logger.error(f"Error building prediction model: {e}")
            return {"error": str(e)}
    
    async def cluster_workflow_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform clustering analysis on workflow patterns"""
        try:
            if df.empty or len(df) < 5:
                return {"error": "Insufficient data for clustering"}
            
            # Prepare features for clustering
            feature_columns = [
                'priority_numeric', 'hour', 'day_of_week',
                'total_tokens', 'execution_time', 'success_score'
            ]
            
            available_features = [col for col in feature_columns if col in df.columns]
            
            if len(available_features) < 3:
                return {"error": "Insufficient features for clustering"}
            
            X = df[available_features].fillna(df[available_features].median())
            
            # Standardize features
            X_scaled = self.scaler.fit_transform(X)
            
            # Determine optimal number of clusters
            optimal_k = min(5, len(df) // 2)
            
            # Perform clustering
            kmeans = KMeans(n_clusters=optimal_k, random_state=42)
            clusters = kmeans.fit_predict(X_scaled)
            
            # Add cluster labels to dataframe
            df_clustered = df.copy()
            df_clustered['cluster'] = clusters
            
            # Analyze clusters
            cluster_analysis = {}
            for i in range(optimal_k):
                cluster_data = df_clustered[df_clustered['cluster'] == i]
                cluster_analysis[f'cluster_{i}'] = {
                    'size': len(cluster_data),
                    'avg_success_score': cluster_data['success_score'].mean(),
                    'avg_execution_time': cluster_data.get('execution_time', pd.Series([0])).mean(),
                    'common_priority': cluster_data['priority'].mode().iloc[0] if not cluster_data['priority'].mode().empty else 'unknown',
                    'peak_hour': cluster_data['hour'].mode().iloc[0] if not cluster_data['hour'].mode().empty else 0
                }
            
            return {
                "n_clusters": optimal_k,
                "cluster_analysis": cluster_analysis,
                "features_used": available_features,
                "silhouette_score": "N/A"  # Could add silhouette analysis
            }
            
        except Exception as e:
            logger.error(f"Error performing clustering: {e}")
            return {"error": str(e)}
    
    async def generate_analytics_dashboard_data(self) -> Dict[str, Any]:
        """Generate comprehensive analytics data for dashboard"""
        try:
            # Collect data
            df = await self.collect_workflow_data(days_back=30)
            
            if df.empty:
                return {"error": "No data available for analytics"}
            
            # Basic statistics
            total_workflows = len(df)
            avg_success_score = df['success_score'].mean()
            completion_rate = (df['status'] == 'completed').mean() * 100
            
            # Time series data
            daily_counts = df.groupby(df['created_at'].dt.date).size().reset_index()
            daily_counts.columns = ['date', 'count']
            
            # Success by priority
            priority_success = df.groupby('priority')['success_score'].mean().reset_index()
            
            # Hourly patterns
            hourly_patterns = df.groupby('hour').size().reset_index()
            hourly_patterns.columns = ['hour', 'count']
            
            # Industry analysis if available
            industry_analysis = {}
            if 'industry' in df.columns:
                industry_analysis = df.groupby('industry')['success_score'].agg([
                    'mean', 'count', 'std'
                ]).round(2).to_dict()
            
            # ML predictions
            prediction_results = await self.predict_workflow_success(df)
            clustering_results = await self.cluster_workflow_patterns(df)
            
            return {
                "summary_stats": {
                    "total_workflows": total_workflows,
                    "avg_success_score": round(avg_success_score, 2),
                    "completion_rate": round(completion_rate, 2),
                    "data_range_days": 30
                },
                "time_series": daily_counts.to_dict('records'),
                "priority_analysis": priority_success.to_dict('records'),
                "hourly_patterns": hourly_patterns.to_dict('records'),
                "industry_analysis": industry_analysis,
                "ml_predictions": prediction_results,
                "clustering_analysis": clustering_results,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating analytics: {e}")
            return {"error": str(e)}

# Global analytics engine
analytics_engine = DataScienceEngine()
