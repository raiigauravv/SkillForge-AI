"""
Analytics API Routes - Data Science Endpoints
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from typing import Dict, Any, List
import logging
from datetime import datetime

from src.analytics.data_science_engine import analytics_engine
from src.analytics.visualization_engine import viz_engine
from database.mongodb_config import db_manager

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/analytics/dashboard", response_class=HTMLResponse)
async def get_analytics_dashboard():
    """
    Generate comprehensive analytics dashboard with visualizations
    """
    try:
        # Ensure database connection
        if not db_manager.db:
            await db_manager.connect()
        
        # Generate analytics data
        analytics_data = await analytics_engine.generate_analytics_dashboard_data()
        
        if "error" in analytics_data:
            # Return a simple dashboard with error message
            error_html = f"""
            <!DOCTYPE html>
            <html>
            <head><title>Analytics Dashboard</title></head>
            <body>
                <h1>📊 Analytics Dashboard</h1>
                <div style="padding: 20px; background: #f8f9fa; border-radius: 8px; margin: 20px;">
                    <h3>⚠️ {analytics_data['error']}</h3>
                    <p>Create some workflows to see analytics data!</p>
                </div>
            </body>
            </html>
            """
            return HTMLResponse(content=error_html)
        
        # Generate comprehensive dashboard
        dashboard_html = viz_engine.create_comprehensive_dashboard(analytics_data)
        
        return HTMLResponse(content=dashboard_html)
        
    except Exception as e:
        logger.error(f"Error generating analytics dashboard: {e}")
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Analytics Dashboard - Error</title></head>
        <body>
            <h1>📊 Analytics Dashboard</h1>
            <div style="padding: 20px; background: #ffe6e6; border-radius: 8px; margin: 20px;">
                <h3>❌ Error generating dashboard</h3>
                <p>{str(e)}</p>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=error_html)

@router.get("/analytics/data")
async def get_analytics_data():
    """
    Get raw analytics data as JSON
    """
    try:
        # Ensure database connection
        if not db_manager.db:
            await db_manager.connect()
        
        analytics_data = await analytics_engine.generate_analytics_dashboard_data()
        return analytics_data
        
    except Exception as e:
        logger.error(f"Error getting analytics data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/ml-insights")
async def get_ml_insights():
    """
    Get machine learning insights and predictions
    """
    try:
        # Ensure database connection
        if not db_manager.db:
            await db_manager.connect()
        
        # Collect workflow data
        df = await analytics_engine.collect_workflow_data(days_back=30)
        
        if df.empty:
            return {
                "message": "No data available for ML analysis",
                "predictions": {},
                "clustering": {},
                "recommendations": []
            }
        
        # Generate ML predictions
        prediction_results = await analytics_engine.predict_workflow_success(df)
        clustering_results = await analytics_engine.cluster_workflow_patterns(df)
        
        # Generate recommendations based on ML results
        recommendations = _generate_ml_recommendations(prediction_results, clustering_results)
        
        return {
            "predictions": prediction_results,
            "clustering": clustering_results,
            "recommendations": recommendations,
            "data_summary": {
                "total_samples": len(df),
                "date_range": f"{df['created_at'].min()} to {df['created_at'].max()}" if 'created_at' in df.columns else "N/A",
                "avg_success_score": df['success_score'].mean() if 'success_score' in df.columns else 0
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting ML insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/performance-metrics")
async def get_performance_metrics():
    """
    Get detailed performance metrics and KPIs
    """
    try:
        # Ensure database connection
        if not db_manager.db:
            await db_manager.connect()
        
        df = await analytics_engine.collect_workflow_data(days_back=30)
        
        if df.empty:
            return {
                "error": "No workflow data available",
                "metrics": {}
            }
        
        # Calculate detailed metrics
        metrics = {
            "workflow_volume": {
                "total": len(df),
                "daily_average": len(df) / 30,
                "peak_day": df.groupby(df['created_at'].dt.date).size().max() if 'created_at' in df.columns else 0
            },
            "success_metrics": {
                "average_score": df['success_score'].mean() if 'success_score' in df.columns else 0,
                "success_rate": (df['success_score'] > 75).mean() * 100 if 'success_score' in df.columns else 0,
                "completion_rate": (df['status'] == 'completed').mean() * 100 if 'status' in df.columns else 0
            },
            "efficiency_metrics": {
                "avg_execution_time": df['execution_time'].mean() if 'execution_time' in df.columns else 0,
                "avg_tokens_used": df['total_tokens'].mean() if 'total_tokens' in df.columns else 0,
                "cost_per_workflow": (df['total_tokens'].mean() * 0.00015) if 'total_tokens' in df.columns else 0  # Approximate cost
            },
            "priority_analysis": df['priority'].value_counts().to_dict() if 'priority' in df.columns else {},
            "time_patterns": {
                "peak_hour": df['hour'].mode().iloc[0] if 'hour' in df.columns and not df['hour'].mode().empty else 0,
                "busiest_day": df['day_of_week'].mode().iloc[0] if 'day_of_week' in df.columns and not df['day_of_week'].mode().empty else 0
            }
        }
        
        return {
            "metrics": metrics,
            "generated_at": datetime.now().isoformat(),
            "data_period": "Last 30 days"
        }
        
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analytics/store-workflow-data")
async def store_workflow_data(workflow_data: Dict[str, Any]):
    """
    Store workflow execution data for analytics
    """
    try:
        # Ensure database connection
        if not db_manager.db:
            await db_manager.connect()
        
        # Add analytics metadata
        analytics_record = {
            **workflow_data,
            "stored_at": datetime.now(),
            "analytics_version": "1.0"
        }
        
        # Store in MongoDB
        result = await db_manager.db.workflows.insert_one(analytics_record)
        
        return {
            "message": "Workflow data stored successfully",
            "document_id": str(result.inserted_id),
            "workflow_id": workflow_data.get("workflow_id")
        }
        
    except Exception as e:
        logger.error(f"Error storing workflow data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def _generate_ml_recommendations(prediction_results: Dict, clustering_results: Dict) -> List[str]:
    """
    Generate actionable recommendations based on ML analysis
    """
    recommendations = []
    
    try:
        # Recommendations based on prediction model
        if "feature_importance" in prediction_results:
            top_feature = max(prediction_results["feature_importance"], 
                            key=prediction_results["feature_importance"].get)
            recommendations.append(
                f"🎯 Focus on optimizing '{top_feature}' - it's the strongest predictor of workflow success"
            )
        
        if "accuracy" in prediction_results:
            accuracy = prediction_results["accuracy"]
            if accuracy > 0.8:
                recommendations.append("✅ High prediction accuracy - the model can reliably forecast workflow outcomes")
            elif accuracy > 0.6:
                recommendations.append("⚠️ Moderate prediction accuracy - consider collecting more diverse training data")
            else:
                recommendations.append("❌ Low prediction accuracy - review feature selection and data quality")
        
        # Recommendations based on clustering
        if "cluster_analysis" in clustering_results:
            cluster_analysis = clustering_results["cluster_analysis"]
            if len(cluster_analysis) > 1:
                # Find best performing cluster
                best_cluster = max(cluster_analysis.items(), 
                                 key=lambda x: x[1].get('avg_success_score', 0))
                recommendations.append(
                    f"🌟 {best_cluster[0]} shows highest success rate - replicate their patterns across other workflows"
                )
        
        # General recommendations
        recommendations.extend([
            "📊 Monitor workflow metrics daily to identify trends early",
            "🔄 Use A/B testing to validate workflow improvements",
            "📈 Set up automated alerts for performance anomalies"
        ])
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        recommendations.append("⚠️ Error generating personalized recommendations")
    
    return recommendations[:5]  # Return top 5 recommendations
