"""
🎯 CAREER INTELLIGENCE ENGINE - Level 1 & Level 2 Integration
Advanced Data Science Engine for Career Analytics, Predictive Modeling, and Business Intelligence
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split, cross_val_score
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import asyncio
from typing import Dict, List, Any, Tuple, Optional
import json
import logging
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

@dataclass
class CareerMetrics:
    """Career analytics data structure"""
    job_market_score: float
    skill_gap_score: float
    salary_prediction: float
    job_match_probability: float
    career_growth_index: float
    portfolio_strength: float

class CareerIntelligenceEngine:
    """
    🚀 ADVANCED CAREER DATA SCIENCE ENGINE
    
    Level 1 - Core Data Science Problem Solving:
    ✅ Career trajectory prediction
    ✅ Salary forecasting models
    ✅ Skill gap analysis
    ✅ Job market segmentation
    
    Level 2 - Advanced Analytics & Visualization:
    ✅ Interactive dashboards
    ✅ Statistical modeling
    ✅ Predictive analytics
    ✅ Portfolio optimization
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.models = {
            'salary_predictor': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'job_matcher': RandomForestClassifier(n_estimators=100, random_state=42),
            'career_classifier': RandomForestClassifier(n_estimators=100, random_state=42)
        }
        self.is_trained = False
        
        # North American job market data (realistic synthetic data for modeling)
        self.canadian_job_market = self._initialize_market_data()
        
        # 🚀 PRE-TRAIN MODELS ON STARTUP FOR SPEED
        logger.info("🤖 Pre-training Career Intelligence models for optimal performance...")
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If already in an event loop, schedule training
                asyncio.create_task(self._auto_train_models())
            else:
                # If no event loop, create one
                asyncio.run(self._auto_train_models())
        except Exception as e:
            logger.warning(f"Auto-training failed, will train on first use: {e}")
    
    async def _auto_train_models(self):
        """Auto-train models on startup"""
        try:
            await self.train_models()
            logger.info("✅ Career Intelligence models pre-trained successfully!")
        except Exception as e:
            logger.warning(f"Auto-training failed: {e}")
        
    def _initialize_market_data(self) -> pd.DataFrame:
        """Initialize realistic North American job market dataset (Canada + US)"""
        np.random.seed(42)
        n_samples = 3000  # Increased for more markets
        
        # 🇨🇦🇺🇸 NORTH AMERICAN MARKET DATA
        # Canadian cities (CAD salaries)
        canadian_cities = ['Toronto', 'Vancouver', 'Montreal', 'Ottawa', 'Calgary', 'Edmonton']
        # US cities (USD salaries) 
        us_cities = ['New York', 'San Francisco', 'Seattle', 'Austin', 'Boston', 'Chicago', 'Los Angeles', 'Denver']
        
        industries = ['Tech', 'Finance', 'Healthcare', 'Government', 'Consulting', 'Retail']
        experience_levels = ['Junior', 'Intermediate', 'Senior', 'Principal', 'Director']
        education_levels = ['Bachelor', 'Master', 'PhD', 'Bootcamp', 'Certificate']
        
        # Create synthetic North American data
        data = []
        for i in range(n_samples):
            # Select country (60% Canada, 40% US for balanced representation)
            is_canada = np.random.random() < 0.6
            
            if is_canada:
                city = np.random.choice(canadian_cities)
                country = 'Canada'
                currency = 'CAD'
            else:
                city = np.random.choice(us_cities)
                country = 'USA'
                currency = 'USD'
                
            industry = np.random.choice(industries)
            experience = np.random.choice(experience_levels)
            education = np.random.choice(education_levels)
            
            # Base salary in local currency
            if is_canada:
                base_salary = 55000  # CAD base
                # Canadian city multipliers (Toronto baseline)
                city_multipliers = {
                    'Toronto': 1.2, 'Vancouver': 1.15, 'Montreal': 1.0,
                    'Ottawa': 1.1, 'Calgary': 1.08, 'Edmonton': 1.05
                }
            else:
                base_salary = 60000  # USD base (higher cost of living)
                # US city multipliers (adjusted for US market)
                city_multipliers = {
                    'San Francisco': 1.8, 'New York': 1.6, 'Seattle': 1.4,
                    'Boston': 1.3, 'Los Angeles': 1.25, 'Austin': 1.2,
                    'Chicago': 1.15, 'Denver': 1.1
                }
            
            # Industry and experience multipliers (similar across countries)
            exp_multiplier = {'Junior': 1.0, 'Intermediate': 1.4, 'Senior': 1.8, 
                            'Principal': 2.5, 'Director': 3.2}[experience]
            
            industry_multiplier = {'Tech': 1.3, 'Finance': 1.25, 'Healthcare': 1.1, 
                                 'Government': 1.05, 'Consulting': 1.35, 'Retail': 0.9}[industry]
            
            education_multiplier = {'PhD': 1.2, 'Master': 1.1, 'Bachelor': 1.0, 
                                  'Bootcamp': 0.95, 'Certificate': 0.9}[education]
            
            salary = base_salary * city_multipliers[city] * exp_multiplier * industry_multiplier * education_multiplier
            salary += np.random.normal(0, 8000)  # Add realistic variance
            salary = max(45000, min(350000, salary))  # Realistic bounds (higher for US markets)
            
            # Generate correlated skills and metrics
            python_skill = np.random.beta(2, 5) * 10
            sql_skill = np.random.beta(2, 4) * 10
            ml_skill = np.random.beta(1.5, 6) * 10
            communication = np.random.beta(3, 3) * 10
            
            portfolio_projects = np.random.poisson(3)
            github_commits = np.random.poisson(150)
            years_experience = {'Junior': np.random.uniform(0, 2), 
                              'Intermediate': np.random.uniform(2, 5),
                              'Senior': np.random.uniform(5, 10), 
                              'Principal': np.random.uniform(8, 15),
                              'Director': np.random.uniform(10, 20)}[experience]
            
            job_satisfaction = np.random.beta(3, 2) * 10
            career_growth = np.random.beta(2, 3) * 10
            
            data.append({
                'city': city,
                'country': country,
                'currency': currency,
                'industry': industry,
                'experience_level': experience,
                'education': education,
                'salary_cad': salary if is_canada else int(salary * 1.35),  # Convert USD to CAD for compatibility
                'salary_local': salary,  # Keep original currency
                'python_skill': python_skill,
                'sql_skill': sql_skill,
                'ml_skill': ml_skill,
                'communication_skill': communication,
                'portfolio_projects': portfolio_projects,
                'github_commits': github_commits,
                'years_experience': years_experience,
                'job_satisfaction': job_satisfaction,
                'career_growth_potential': career_growth,
                'remote_work_available': np.random.choice([0, 1], p=[0.3, 0.7]),
                'hired': np.random.choice([0, 1], p=[0.25, 0.75])
            })
        
        df = pd.DataFrame(data)
        
        # Create derived features
        df['skill_score'] = (df['python_skill'] + df['sql_skill'] + df['ml_skill'] + df['communication_skill']) / 4
        df['portfolio_strength'] = np.log1p(df['portfolio_projects']) + np.log1p(df['github_commits']) / 100
        df['experience_salary_ratio'] = df['salary_cad'] / (df['years_experience'] + 1)
        
        return df
    
    async def train_models(self) -> Dict[str, float]:
        """Train all ML models with career data"""
        try:
            logger.info("🤖 Training Career Intelligence Models...")
            
            df = self.canadian_job_market.copy()
            
            # Prepare features
            categorical_features = ['city', 'industry', 'experience_level', 'education']
            numerical_features = ['python_skill', 'sql_skill', 'ml_skill', 'communication_skill',
                                'portfolio_projects', 'github_commits', 'years_experience']
            
            # Encode categorical variables
            df_encoded = df.copy()
            for feature in categorical_features:
                df_encoded[feature] = LabelEncoder().fit_transform(df[feature])
            
            X = df_encoded[categorical_features + numerical_features]
            X_scaled = self.scaler.fit_transform(X)
            
            # 1. Salary Prediction Model
            y_salary = df['salary_cad']
            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_salary, test_size=0.2, random_state=42)
            
            self.models['salary_predictor'].fit(X_train, y_train)
            salary_score = self.models['salary_predictor'].score(X_test, y_test)
            
            # 2. Job Match Prediction Model
            y_hired = df['hired']
            X_train_job, X_test_job, y_train_job, y_test_job = train_test_split(X_scaled, y_hired, test_size=0.2, random_state=42)
            self.models['job_matcher'].fit(X_train_job, y_train_job)
            job_match_score = self.models['job_matcher'].score(X_test_job, y_test_job)
            
            # 3. Career Level Classification
            y_career = df_encoded['experience_level']
            X_train_career, X_test_career, y_train_career, y_test_career = train_test_split(X_scaled, y_career, test_size=0.2, random_state=42)
            self.models['career_classifier'].fit(X_train_career, y_train_career)
            career_score = self.models['career_classifier'].score(X_test_career, y_test_career)
            
            self.is_trained = True
            
            scores = {
                'salary_predictor_r2': round(salary_score, 3),
                'job_matcher_accuracy': round(job_match_score, 3),
                'career_classifier_accuracy': round(career_score, 3),
                'training_samples': len(df)
            }
            
            logger.info(f"✅ Models trained successfully: {scores}")
            return scores
            
        except Exception as e:
            logger.error(f"❌ Error training models: {e}")
            raise
    
    async def predict_career_metrics(self, profile: Dict[str, Any]) -> CareerMetrics:
        """
        🎯 CORE PREDICTION ENGINE
        Predict comprehensive career metrics for a given profile
        """
        try:
            # 🚀 FAST PATH: Check if models are already trained
            if not self.is_trained:
                logger.info("🤖 Training models on first use...")
                await self.train_models()
            
            # Prepare input features
            features = self._prepare_features(profile)
            features_scaled = self.scaler.transform([features])
            
            # Predictions
            salary_pred = self.models['salary_predictor'].predict(features_scaled)[0]
            job_match_prob = self.models['job_matcher'].predict_proba(features_scaled)[0][1]
            career_level_pred = self.models['career_classifier'].predict(features_scaled)[0]
            
            # Calculate composite metrics
            skill_gap_score = self._calculate_skill_gap(profile)
            job_market_score = self._calculate_market_score(profile)
            career_growth_index = self._calculate_growth_index(profile)
            portfolio_strength = self._calculate_portfolio_strength(profile)
            
            return CareerMetrics(
                job_market_score=round(job_market_score, 2),
                skill_gap_score=round(skill_gap_score, 2),
                salary_prediction=round(salary_pred, 0),
                job_match_probability=round(job_match_prob * 100, 1),
                career_growth_index=round(career_growth_index, 2),
                portfolio_strength=round(portfolio_strength, 2)
            )
            
        except Exception as e:
            logger.error(f"Error in career prediction: {e}")
            raise
    
    def _prepare_features(self, profile: Dict[str, Any]) -> List[float]:
        """Prepare features from user profile"""
        city_map = {'Toronto': 0, 'Vancouver': 1, 'Montreal': 2, 'Ottawa': 3, 'Calgary': 4, 'Edmonton': 5}
        industry_map = {'Tech': 0, 'Finance': 1, 'Healthcare': 2, 'Government': 3, 'Consulting': 4, 'Retail': 5}
        exp_map = {'Junior': 0, 'Intermediate': 1, 'Senior': 2, 'Principal': 3, 'Director': 4}
        edu_map = {'Bachelor': 0, 'Master': 1, 'PhD': 2, 'Bootcamp': 3, 'Certificate': 4}
        
        return [
            city_map.get(profile.get('city', 'Toronto'), 0),
            industry_map.get(profile.get('industry', 'Tech'), 0),
            exp_map.get(profile.get('experience_level', 'Junior'), 0),
            edu_map.get(profile.get('education', 'Bachelor'), 0),
            profile.get('python_skill', 5.0),
            profile.get('sql_skill', 5.0),
            profile.get('ml_skill', 3.0),
            profile.get('communication_skill', 6.0),
            profile.get('portfolio_projects', 2),
            profile.get('github_commits', 50),
            profile.get('years_experience', 2.0)
        ]
    
    def _calculate_skill_gap(self, profile: Dict[str, Any]) -> float:
        """Calculate skill gap score (0-10, higher is better)"""
        required_skills = {'python_skill': 8, 'sql_skill': 7, 'ml_skill': 6, 'communication_skill': 8}
        
        gaps = []
        for skill, required_level in required_skills.items():
            current_level = profile.get(skill, 0)
            gap = max(0, required_level - current_level)
            gaps.append(gap)
        
        avg_gap = np.mean(gaps)
        return max(0, 10 - avg_gap)
    
    def _calculate_market_score(self, profile: Dict[str, Any]) -> float:
        """Calculate job market competitiveness score"""
        city_scores = {'Toronto': 9, 'Vancouver': 8, 'Montreal': 7, 'Ottawa': 7, 'Calgary': 6, 'Edmonton': 6}
        industry_scores = {'Tech': 9, 'Finance': 8, 'Consulting': 8, 'Healthcare': 7, 'Government': 6, 'Retail': 5}
        
        city_score = city_scores.get(profile.get('city', 'Toronto'), 7)
        industry_score = industry_scores.get(profile.get('industry', 'Tech'), 7)
        
        return (city_score + industry_score) / 2
    
    def _calculate_growth_index(self, profile: Dict[str, Any]) -> float:
        """Calculate career growth potential index"""
        education_weight = {'PhD': 10, 'Master': 8, 'Bachelor': 6, 'Bootcamp': 7, 'Certificate': 5}
        portfolio_weight = min(10, profile.get('portfolio_projects', 0) * 2)
        experience_weight = min(10, profile.get('years_experience', 0))
        
        education_score = education_weight.get(profile.get('education', 'Bachelor'), 6)
        
        return (education_score * 0.4 + portfolio_weight * 0.3 + experience_weight * 0.3)
    
    def _calculate_portfolio_strength(self, profile: Dict[str, Any]) -> float:
        """Calculate portfolio strength score"""
        projects = profile.get('portfolio_projects', 0)
        commits = profile.get('github_commits', 0)
        
        project_score = min(10, projects * 2.5)
        commit_score = min(10, commits / 20)
        
        return (project_score + commit_score) / 2
    
    async def generate_career_insights(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        📊 COMPREHENSIVE CAREER ANALYSIS
        Generate detailed insights and recommendations
        """
        try:
            metrics = await self.predict_career_metrics(profile)
            
            # Salary benchmarking
            similar_profiles = self.canadian_job_market[
                (self.canadian_job_market['city'] == profile.get('city', 'Toronto')) &
                (self.canadian_job_market['industry'] == profile.get('industry', 'Tech'))
            ]
            
            salary_percentile = (similar_profiles['salary_cad'] < metrics.salary_prediction).mean() * 100
            
            # Skill recommendations
            skill_recommendations = self._generate_skill_recommendations(profile, metrics)
            
            # Career pathway
            career_pathway = self._generate_career_pathway(profile, metrics)
            
            # Market analysis
            market_analysis = self._generate_market_analysis(profile)
            
            return {
                'predictions': {
                    'salary_cad': metrics.salary_prediction,
                    'job_match_probability': metrics.job_match_probability,
                    'salary_percentile': round(salary_percentile, 1),
                    'career_growth_index': metrics.career_growth_index
                },
                'scores': {
                    'skill_gap_score': metrics.skill_gap_score,
                    'job_market_score': metrics.job_market_score,
                    'portfolio_strength': metrics.portfolio_strength
                },
                'recommendations': skill_recommendations,
                'career_pathway': career_pathway,
                'market_analysis': market_analysis,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating career insights: {e}")
            raise
    
    def _generate_skill_recommendations(self, profile: Dict[str, Any], metrics: CareerMetrics) -> List[Dict]:
        """Generate personalized skill recommendations"""
        recommendations = []
        
        skills = {
            'python_skill': {'name': 'Python Programming', 'target': 8, 'priority': 'high'},
            'sql_skill': {'name': 'SQL & Databases', 'target': 7, 'priority': 'high'},
            'ml_skill': {'name': 'Machine Learning', 'target': 6, 'priority': 'medium'},
            'communication_skill': {'name': 'Communication', 'target': 8, 'priority': 'high'}
        }
        
        for skill_key, skill_info in skills.items():
            current_level = profile.get(skill_key, 0)
            gap = skill_info['target'] - current_level
            
            if gap > 1:
                recommendations.append({
                    'skill': skill_info['name'],
                    'current_level': current_level,
                    'target_level': skill_info['target'],
                    'gap': round(gap, 1),
                    'priority': skill_info['priority'],
                    'estimated_improvement_months': max(1, int(gap * 2))
                })
        
        return sorted(recommendations, key=lambda x: x['gap'], reverse=True)
    
    def _generate_career_pathway(self, profile: Dict[str, Any], metrics: CareerMetrics) -> Dict[str, Any]:
        """Generate career progression pathway"""
        current_level = profile.get('experience_level', 'Junior')
        
        pathways = {
            'Junior': {
                'next_level': 'Intermediate',
                'timeline_months': 24,
                'requirements': ['2+ portfolio projects', 'Python proficiency', '1-2 years experience']
            },
            'Intermediate': {
                'next_level': 'Senior',
                'timeline_months': 36,
                'requirements': ['Technical leadership', 'ML project experience', '4+ years experience']
            },
            'Senior': {
                'next_level': 'Principal',
                'timeline_months': 48,
                'requirements': ['System design', 'Team mentoring', 'Business impact']
            }
        }
        
        return pathways.get(current_level, {
            'next_level': 'Senior+',
            'timeline_months': 24,
            'requirements': ['Continued excellence', 'Leadership', 'Innovation']
        })
    
    def _generate_market_analysis(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive North American market analysis"""
        city = profile.get('city', 'Toronto')
        industry = profile.get('industry', 'Tech')
        
        city_data = self.canadian_job_market[self.canadian_job_market['city'] == city]
        industry_data = self.canadian_job_market[self.canadian_job_market['industry'] == industry]
        
        # Determine if US or Canadian city for proper currency display
        us_cities = ['New York', 'San Francisco', 'Seattle', 'Austin', 'Boston', 'Chicago', 'Los Angeles', 'Denver']
        is_us_city = city in us_cities
        
        # Get market context
        if is_us_city:
            country = 'USA'
            currency = 'USD'
            # Use local salary for US cities
            avg_salary = round(city_data['salary_local'].mean(), 0) if not city_data.empty else 75000
            high_comp_threshold = 250000
        else:
            country = 'Canada'  
            currency = 'CAD'
            avg_salary = round(city_data['salary_cad'].mean(), 0) if not city_data.empty else 65000
            high_comp_threshold = 200000
        
        # Market competitiveness based on city
        competition_level = 'High' if city in ['Toronto', 'Vancouver', 'San Francisco', 'New York', 'Seattle'] else 'Medium'
        
        return {
            'city_analysis': {
                'city': city,
                'country': country,
                'currency': currency,
                'avg_salary': avg_salary,
                'job_opportunities': 'High' if len(city_data) > 200 else 'Medium',
                'remote_work_rate': round(city_data['remote_work_available'].mean() * 100, 1) if not city_data.empty else 65.0,
                'competition_level': competition_level,
                'market_context': f"{'Tech hub with high salaries' if is_us_city and city in ['San Francisco', 'Seattle'] else 'Growing tech market'}"
            },
            'industry_analysis': {
                'avg_salary': round(industry_data['salary_cad'].mean(), 0) if not industry_data.empty else 70000,
                'growth_trend': 'Growing' if industry in ['Tech', 'Finance'] else 'Stable',
                'skill_demand': ['Python', 'SQL', 'Machine Learning', 'Communication'],
                'hiring_rate': round(industry_data['hired'].mean() * 100, 1) if not industry_data.empty else 75.0
            },
            'recommendations': [
                f'Target {currency} {avg_salary:,}+ salary range for {city}',
                'Focus on high-demand skills for North American market',
                'Build a strong portfolio showcasing practical projects',
                f'Network in {city} tech community',
                'Consider remote opportunities across US/Canada border'
            ]
        }
    
    async def create_career_dashboard(self, profile: Dict[str, Any]) -> str:
        """
        📊 LEVEL 2: ADVANCED VISUALIZATION ENGINE
        Create comprehensive interactive career analytics dashboard
        """
        try:
            insights = await self.generate_career_insights(profile)
            
            # Create a beautiful, simple HTML dashboard
            dashboard_html = f"""
            <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 1000px; margin: 0 auto; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; padding: 30px; color: white;">
                
                <!-- Header -->
                <div style="text-align: center; margin-bottom: 40px;">
                    <h1 style="font-size: 2.5em; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🎯 Career Intelligence Dashboard</h1>
                    <p style="font-size: 1.1em; opacity: 0.9; margin: 10px 0;">Powered by Advanced Machine Learning</p>
                </div>
                
                <!-- Key Metrics Cards -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 40px;">
                    
                    <div style="background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); border-radius: 15px; padding: 25px; text-align: center; border: 1px solid rgba(255,255,255,0.2);">
                        <div style="font-size: 2.5em; margin-bottom: 10px;">💰</div>
                        <h3 style="margin: 0; font-size: 1.1em; opacity: 0.9;">Predicted Salary</h3>
                        <div style="font-size: 2em; font-weight: bold; margin: 10px 0;">CAD ${insights['predictions']['salary_cad']:,.0f}</div>
                        <div style="font-size: 0.9em; opacity: 0.8;">{insights['predictions']['salary_percentile']}th percentile</div>
                    </div>
                    
                    <div style="background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); border-radius: 15px; padding: 25px; text-align: center; border: 1px solid rgba(255,255,255,0.2);">
                        <div style="font-size: 2.5em; margin-bottom: 10px;">🎯</div>
                        <h3 style="margin: 0; font-size: 1.1em; opacity: 0.9;">Job Match</h3>
                        <div style="font-size: 2em; font-weight: bold; margin: 10px 0;">{insights['predictions']['job_match_probability']}%</div>
                        <div style="font-size: 0.9em; opacity: 0.8;">Match Probability</div>
                    </div>
                    
                    <div style="background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); border-radius: 15px; padding: 25px; text-align: center; border: 1px solid rgba(255,255,255,0.2);">
                        <div style="font-size: 2.5em; margin-bottom: 10px;">📈</div>
                        <h3 style="margin: 0; font-size: 1.1em; opacity: 0.9;">Growth Index</h3>
                        <div style="font-size: 2em; font-weight: bold; margin: 10px 0;">{insights['predictions']['career_growth_index']}/10</div>
                        <div style="font-size: 0.9em; opacity: 0.8;">Career Potential</div>
                    </div>
                    
                    <div style="background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); border-radius: 15px; padding: 25px; text-align: center; border: 1px solid rgba(255,255,255,0.2);">
                        <div style="font-size: 2.5em; margin-bottom: 10px;">🏆</div>
                        <h3 style="margin: 0; font-size: 1.1em; opacity: 0.9;">Portfolio</h3>
                        <div style="font-size: 2em; font-weight: bold; margin: 10px 0;">{insights['scores']['portfolio_strength']}/10</div>
                        <div style="font-size: 0.9em; opacity: 0.8;">Strength Score</div>
                    </div>
                
                </div>
                
                <!-- Skills Analysis -->
                <div style="background: rgba(255,255,255,0.95); border-radius: 15px; padding: 30px; margin-bottom: 30px; color: #333;">
                    <h2 style="margin: 0 0 25px 0; color: #667eea; display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 1.5em;">🚀</span> Skills Analysis
                    </h2>
                    
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                        <div style="text-align: center; padding: 15px;">
                            <h4 style="margin: 0 0 10px 0; color: #667eea;">Python</h4>
                            <div style="background: #e9ecef; border-radius: 10px; height: 20px; overflow: hidden;">
                                <div style="background: linear-gradient(90deg, #667eea, #764ba2); height: 100%; width: {profile.get('python_skill', 5) * 10}%; border-radius: 10px; transition: width 0.5s ease;"></div>
                            </div>
                            <div style="margin-top: 5px; font-size: 0.9em; color: #666;">{profile.get('python_skill', 5)}/10</div>
                        </div>
                        
                        <div style="text-align: center; padding: 15px;">
                            <h4 style="margin: 0 0 10px 0; color: #667eea;">SQL</h4>
                            <div style="background: #e9ecef; border-radius: 10px; height: 20px; overflow: hidden;">
                                <div style="background: linear-gradient(90deg, #11998e, #38ef7d); height: 100%; width: {profile.get('sql_skill', 5) * 10}%; border-radius: 10px; transition: width 0.5s ease;"></div>
                            </div>
                            <div style="margin-top: 5px; font-size: 0.9em; color: #666;">{profile.get('sql_skill', 5)}/10</div>
                        </div>
                        
                        <div style="text-align: center; padding: 15px;">
                            <h4 style="margin: 0 0 10px 0; color: #667eea;">Machine Learning</h4>
                            <div style="background: #e9ecef; border-radius: 10px; height: 20px; overflow: hidden;">
                                <div style="background: linear-gradient(90deg, #f093fb, #f5576c); height: 100%; width: {profile.get('ml_skill', 3) * 10}%; border-radius: 10px; transition: width 0.5s ease;"></div>
                            </div>
                            <div style="margin-top: 5px; font-size: 0.9em; color: #666;">{profile.get('ml_skill', 3)}/10</div>
                        </div>
                        
                        <div style="text-align: center; padding: 15px;">
                            <h4 style="margin: 0 0 10px 0; color: #667eea;">Communication</h4>
                            <div style="background: #e9ecef; border-radius: 10px; height: 20px; overflow: hidden;">
                                <div style="background: linear-gradient(90deg, #ffecd2, #fcb69f); height: 100%; width: {profile.get('communication_skill', 6) * 10}%; border-radius: 10px; transition: width 0.5s ease;"></div>
                            </div>
                            <div style="margin-top: 5px; font-size: 0.9em; color: #666;">{profile.get('communication_skill', 6)}/10</div>
                        </div>
                    </div>
                </div>
                
                <!-- Market Analysis -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 30px;">
                    
                    <div style="background: rgba(255,255,255,0.95); border-radius: 15px; padding: 25px; color: #333;">
                        <h3 style="margin: 0 0 20px 0; color: #667eea; display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 1.3em;">🏙️</span> {profile.get('city', 'Toronto')} Market ({insights['market_analysis']['city_analysis']['country']})
                        </h3>
                        <div style="display: grid; gap: 12px;">
                            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                                <span>Average Salary:</span>
                                <strong>{insights['market_analysis']['city_analysis']['currency']} ${insights['market_analysis']['city_analysis']['avg_salary']:,.0f}</strong>
                            </div>
                            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                                <span>Job Opportunities:</span>
                                <strong style="color: #28a745;">{insights['market_analysis']['city_analysis']['job_opportunities']}</strong>
                            </div>
                            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                                <span>Remote Work Rate:</span>
                                <strong>{insights['market_analysis']['city_analysis']['remote_work_rate']}%</strong>
                            </div>
                            <div style="display: flex; justify-content: space-between; padding: 8px 0;">
                                <span>Competition Level:</span>
                                <strong style="color: #dc3545;">{insights['market_analysis']['city_analysis']['competition_level']}</strong>
                            </div>
                        </div>
                    </div>
                    
                    <div style="background: rgba(255,255,255,0.95); border-radius: 15px; padding: 25px; color: #333;">
                        <h3 style="margin: 0 0 20px 0; color: #667eea; display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 1.3em;">🏢</span> {profile.get('industry', 'Tech')} Industry
                        </h3>
                        <div style="display: grid; gap: 12px;">
                            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                                <span>Average Salary:</span>
                                <strong>CAD ${insights['market_analysis']['industry_analysis']['avg_salary']:,.0f}</strong>
                            </div>
                            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                                <span>Growth Trend:</span>
                                <strong style="color: #28a745;">{insights['market_analysis']['industry_analysis']['growth_trend']}</strong>
                            </div>
                            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                                <span>Hiring Rate:</span>
                                <strong>{insights['market_analysis']['industry_analysis']['hiring_rate']}%</strong>
                            </div>
                            <div style="display: flex; justify-content: space-between; padding: 8px 0;">
                                <span>Top Skills:</span>
                                <strong style="font-size: 0.85em;">Python, SQL, ML</strong>
                            </div>
                        </div>
                    </div>
                
                </div>
                
                <!-- Career Pathway -->
                <div style="background: rgba(255,255,255,0.95); border-radius: 15px; padding: 30px; margin-bottom: 30px; color: #333;">
                    <h2 style="margin: 0 0 25px 0; color: #667eea; display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 1.5em;">🛤️</span> Career Pathway
                    </h2>
                    
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 25px;">
                        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 12px; color: white;">
                            <div style="font-size: 1.8em; margin-bottom: 10px;">📍</div>
                            <h4 style="margin: 0 0 10px 0;">Current Level</h4>
                            <div style="font-size: 1.3em; font-weight: bold;">{profile.get('experience_level', 'Junior')}</div>
                        </div>
                        
                        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #11998e, #38ef7d); border-radius: 12px; color: white;">
                            <div style="font-size: 1.8em; margin-bottom: 10px;">🎯</div>
                            <h4 style="margin: 0 0 10px 0;">Next Level</h4>
                            <div style="font-size: 1.3em; font-weight: bold;">{insights['career_pathway']['next_level']}</div>
                        </div>
                        
                        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #f093fb, #f5576c); border-radius: 12px; color: white;">
                            <div style="font-size: 1.8em; margin-bottom: 10px;">⏱️</div>
                            <h4 style="margin: 0 0 10px 0;">Timeline</h4>
                            <div style="font-size: 1.3em; font-weight: bold;">{insights['career_pathway']['timeline_months']} months</div>
                        </div>
                    </div>
                </div>
                
                <!-- Recommendations -->
                <div style="background: rgba(255,255,255,0.95); border-radius: 15px; padding: 30px; color: #333;">
                    <h2 style="margin: 0 0 25px 0; color: #667eea; display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 1.5em;">�</span> Action Recommendations
                    </h2>
                    
                    <div style="display: grid; gap: 15px;">
                        {''.join(f'''
                        <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 12px; display: flex; align-items: center; gap: 15px;">
                            <span style="font-size: 1.5em; min-width: 40px;">✨</span>
                            <span style="font-size: 1.1em; line-height: 1.4;">{rec}</span>
                        </div>
                        ''' for rec in insights['market_analysis']['recommendations'])}
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 30px; opacity: 0.8;">
                    <p style="margin: 0; font-size: 0.9em;">Generated by Career Intelligence Engine • {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                </div>
            
            </div>
            """
            
            return dashboard_html
            
        except Exception as e:
            logger.error(f"Error creating career dashboard: {e}")
            return f"<div>Error creating dashboard: {e}</div>"

# Global instance
career_engine = CareerIntelligenceEngine()
