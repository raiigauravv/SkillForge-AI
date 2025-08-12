"""
MongoDB Configuration and Connection Management
"""
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import asyncio
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBManager:
    def __init__(self):
        # MongoDB connection string - using local MongoDB for development
        self.connection_string = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
        self.database_name = "workflow_analytics"
        self.client = None
        self.db = None
        
    async def connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(self.connection_string)
            self.db = self.client[self.database_name]
            # Test connection
            await self.client.admin.command('ping')
            logger.info(f"Successfully connected to MongoDB: {self.database_name}")
            
            # Create indexes for better performance
            await self.create_indexes()
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False
    
    async def create_indexes(self):
        """Create database indexes for optimal performance"""
        try:
            # Workflows collection indexes
            await self.db.workflows.create_index("workflow_id", unique=True)
            await self.db.workflows.create_index("created_at")
            await self.db.workflows.create_index("status")
            await self.db.workflows.create_index("priority")
            
            # Analytics collection indexes
            await self.db.analytics.create_index("workflow_id")
            await self.db.analytics.create_index("timestamp")
            await self.db.analytics.create_index("metric_type")
            
            # User behavior collection indexes
            await self.db.user_behavior.create_index("user_session")
            await self.db.user_behavior.create_index("timestamp")
            
            logger.info("Database indexes created successfully")
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")
    
    async def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

# Collections structure for data science analytics
COLLECTIONS = {
    "workflows": {
        "workflow_id": str,
        "name": str,
        "description": str,
        "industry": str,
        "problem_category": str,
        "priority": str,
        "status": str,
        "created_at": datetime,
        "updated_at": datetime,
        "execution_time": float,
        "token_usage": dict,
        "result": dict,
        "user_feedback": dict,
        "success_metrics": dict
    },
    "analytics": {
        "workflow_id": str,
        "metric_type": str,  # performance, usage, satisfaction, roi
        "metric_value": float,
        "timestamp": datetime,
        "metadata": dict
    },
    "user_behavior": {
        "user_session": str,
        "action_type": str,  # create, execute, view, feedback
        "workflow_id": str,
        "timestamp": datetime,
        "duration": float,
        "device_info": dict,
        "location": str
    },
    "ml_models": {
        "model_id": str,
        "model_type": str,  # prediction, classification, clustering
        "training_data": dict,
        "performance_metrics": dict,
        "created_at": datetime,
        "last_updated": datetime,
        "model_parameters": dict
    }
}

# Global database manager instance
db_manager = MongoDBManager()
