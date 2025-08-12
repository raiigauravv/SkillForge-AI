// Analytics Dashboard JavaScript Functions

// Tab management
function showTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(button => button.classList.remove('active'));
    
    // Show selected tab
    const selectedTab = document.getElementById(tabName + '-tab');
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // Activate button
    const button = event.target;
    button.classList.add('active');
    
    // Load content based on tab
    switch(tabName) {
        case 'analytics':
            loadAnalyticsDashboard();
            break;
        case 'ml-insights':
            loadMLInsights();
            break;
        case 'workflows':
            loadWorkflows();
            break;
    }
}

// Analytics Dashboard Functions
async function loadAnalyticsDashboard() {
    const container = document.getElementById('analytics-dashboard-container');
    container.innerHTML = '<div class="loading">Loading analytics dashboard...</div>';
    
    try {
        const response = await fetch('/api/analytics/dashboard');
        
        if (response.ok) {
            const dashboardHTML = await response.text();
            container.innerHTML = dashboardHTML;
        } else {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
    } catch (error) {
        console.error('Error loading analytics dashboard:', error);
        container.innerHTML = `
            <div class="error-message">
                <h3>❌ Error Loading Analytics</h3>
                <p>${error.message}</p>
                <button onclick="loadAnalyticsDashboard()" class="refresh-btn">Try Again</button>
            </div>
        `;
    }
}

async function refreshAnalytics() {
    await loadAnalyticsDashboard();
    showSuccessMessage('Analytics dashboard refreshed successfully!');
}

async function exportAnalytics() {
    try {
        const response = await fetch('/api/analytics/data');
        const data = await response.json();
        
        // Convert to CSV or JSON download
        const dataStr = JSON.stringify(data, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `analytics_${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        
        showSuccessMessage('Analytics data exported successfully!');
    } catch (error) {
        console.error('Error exporting analytics:', error);
        showErrorMessage('Failed to export analytics data');
    }
}

// ML Insights Functions
async function loadMLInsights() {
    try {
        // Load ML insights data
        const response = await fetch('/api/analytics/ml-insights');
        const data = await response.json();
        
        // Update prediction metrics
        updatePredictionMetrics(data.predictions);
        
        // Update clustering analysis
        updateClusteringAnalysis(data.clustering);
        
        // Update recommendations
        updateMLRecommendations(data.recommendations);
        
        // Load performance metrics
        await loadPerformanceMetrics();
        
    } catch (error) {
        console.error('Error loading ML insights:', error);
        showErrorMessage('Failed to load ML insights');
    }
}

function updatePredictionMetrics(predictions) {
    const container = document.getElementById('prediction-metrics');
    
    if (predictions.error) {
        container.innerHTML = `<p class="error-message">${predictions.error}</p>`;
        return;
    }
    
    container.innerHTML = `
        <div class="metric">
            <span class="metric-label">Model Accuracy</span>
            <div class="metric-value">${(predictions.accuracy * 100).toFixed(1)}%</div>
        </div>
        <div class="metric">
            <span class="metric-label">Model Type</span>
            <div class="metric-value">${predictions.model_type || 'N/A'}</div>
        </div>
        <div class="metric">
            <span class="metric-label">Training Samples</span>
            <div class="metric-value">${predictions.training_samples || 0}</div>
        </div>
        <div class="feature-importance">
            <h4>Top Features:</h4>
            <ul>
                ${Object.entries(predictions.feature_importance || {})
                    .sort(([,a], [,b]) => b - a)
                    .slice(0, 3)
                    .map(([feature, importance]) => 
                        `<li>${feature}: ${(importance * 100).toFixed(1)}%</li>`
                    ).join('')}
            </ul>
        </div>
    `;
}

function updateClusteringAnalysis(clustering) {
    const container = document.getElementById('clustering-analysis');
    
    if (clustering.error) {
        container.innerHTML = `<p class="error-message">${clustering.error}</p>`;
        return;
    }
    
    const clusterInfo = clustering.cluster_analysis || {};
    const numClusters = clustering.n_clusters || 0;
    
    container.innerHTML = `
        <div class="metric">
            <span class="metric-label">Number of Clusters</span>
            <div class="metric-value">${numClusters}</div>
        </div>
        <div class="clusters-summary">
            <h4>Cluster Summary:</h4>
            ${Object.entries(clusterInfo).map(([cluster, info]) => `
                <div class="cluster-item">
                    <strong>${cluster}:</strong> ${info.size} workflows 
                    (${info.avg_success_score.toFixed(1)}% avg success)
                </div>
            `).join('')}
        </div>
    `;
}

function updateMLRecommendations(recommendations) {
    const container = document.getElementById('ml-recommendations');
    
    if (!recommendations || recommendations.length === 0) {
        container.innerHTML = '<p>No recommendations available yet. Create more workflows to get AI insights!</p>';
        return;
    }
    
    container.innerHTML = `
        <ul class="recommendations-list">
            ${recommendations.map(rec => `<li>${rec}</li>`).join('')}
        </ul>
    `;
}

async function loadPerformanceMetrics() {
    try {
        const response = await fetch('/api/analytics/performance-metrics');
        const data = await response.json();
        
        const container = document.getElementById('performance-metrics');
        
        if (data.error) {
            container.innerHTML = `<p class="error-message">${data.error}</p>`;
            return;
        }
        
        const metrics = data.metrics;
        
        container.innerHTML = `
            <div class="metric">
                <span class="metric-label">Total Workflows</span>
                <div class="metric-value">${metrics.workflow_volume?.total || 0}</div>
            </div>
            <div class="metric">
                <span class="metric-label">Daily Average</span>
                <div class="metric-value">${(metrics.workflow_volume?.daily_average || 0).toFixed(1)}</div>
            </div>
            <div class="metric">
                <span class="metric-label">Success Rate</span>
                <div class="metric-value">${(metrics.success_metrics?.success_rate || 0).toFixed(1)}%</div>
            </div>
            <div class="metric">
                <span class="metric-label">Avg Execution Time</span>
                <div class="metric-value">${(metrics.efficiency_metrics?.avg_execution_time || 0).toFixed(2)}s</div>
            </div>
        `;
        
    } catch (error) {
        console.error('Error loading performance metrics:', error);
    }
}

async function refreshMLInsights() {
    await loadMLInsights();
    showSuccessMessage('ML insights refreshed successfully!');
}

async function downloadMLReport() {
    try {
        const response = await fetch('/api/analytics/ml-insights');
        const data = await response.json();
        
        // Create a formatted report
        const report = {
            generated_at: new Date().toISOString(),
            predictions: data.predictions,
            clustering: data.clustering,
            recommendations: data.recommendations,
            data_summary: data.data_summary
        };
        
        const reportStr = JSON.stringify(report, null, 2);
        const reportBlob = new Blob([reportStr], {type: 'application/json'});
        
        const url = URL.createObjectURL(reportBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `ml_insights_${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        
        showSuccessMessage('ML report downloaded successfully!');
    } catch (error) {
        console.error('Error downloading ML report:', error);
        showErrorMessage('Failed to download ML report');
    }
}

// Enhanced workflow creation with analytics data collection
async function createWorkflowEnhanced(formData) {
    try {
        // Add analytics metadata
        const enhancedData = {
            ...formData,
            industry: document.getElementById('industry').value,
            created_by: 'user',
            user_session: generateSessionId(),
            device_info: {
                user_agent: navigator.userAgent,
                screen_resolution: `${screen.width}x${screen.height}`,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
            }
        };
        
        const response = await fetch('/api/workflows/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(enhancedData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            // Store analytics data
            await storeWorkflowAnalytics(result);
            
            // Show result and refresh analytics
            showWorkflowResult(result);
            
            // Refresh workflows list
            loadWorkflows();
            
            return result;
        } else {
            throw new Error(result.detail || 'Failed to create workflow');
        }
    } catch (error) {
        console.error('Error creating workflow:', error);
        showErrorMessage('Failed to create workflow: ' + error.message);
        throw error;
    }
}

async function storeWorkflowAnalytics(workflowData) {
    try {
        await fetch('/api/analytics/store-workflow-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(workflowData)
        });
    } catch (error) {
        console.error('Error storing workflow analytics:', error);
        // Don't throw - analytics storage failure shouldn't break workflow creation
    }
}

// Utility functions
function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function showSuccessMessage(message) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'success-message';
    msgDiv.innerHTML = `✅ ${message}`;
    
    document.body.appendChild(msgDiv);
    
    setTimeout(() => {
        msgDiv.remove();
    }, 3000);
}

function showErrorMessage(message) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'error-message';
    msgDiv.innerHTML = `❌ ${message}`;
    
    document.body.appendChild(msgDiv);
    
    setTimeout(() => {
        msgDiv.remove();
    }, 5000);
}

// Initialize analytics when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Load analytics dashboard by default if analytics tab is active
    const analyticsTab = document.getElementById('analytics-tab');
    if (analyticsTab && analyticsTab.classList.contains('active')) {
        loadAnalyticsDashboard();
    }
});

// Auto-refresh analytics every 5 minutes
setInterval(() => {
    const analyticsTab = document.getElementById('analytics-tab');
    if (analyticsTab && analyticsTab.classList.contains('active')) {
        loadAnalyticsDashboard();
    }
}, 300000); // 5 minutes
