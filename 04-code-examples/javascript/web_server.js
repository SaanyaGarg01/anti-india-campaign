#!/usr/bin/env node
/**
 * Web Server for GenAI JavaScript Examples
 * Provides REST API and interactive web interface
 */

const express = require('express');
const cors = require('cors');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

// Import our demo classes
const {
    GenAIProject,
    TextAnalysisDemo,
    RAGSystem,
    AIEthicsChecker,
    GenAIProjectManager
} = require('./genai_demo');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Initialize demo components
const textAnalysis = new TextAnalysisDemo();
const ragSystem = new RAGSystem();
const ethicsChecker = new AIEthicsChecker();
const projectManager = new GenAIProjectManager();

// In-memory storage
const projects = new Map();
const analytics = {
    totalRequests: 0,
    requestsByEndpoint: {},
    lastUpdated: new Date().toISOString()
};

// Helper function to track analytics
function trackRequest(endpoint) {
    analytics.totalRequests++;
    analytics.requestsByEndpoint[endpoint] = (analytics.requestsByEndpoint[endpoint] || 0) + 1;
    analytics.lastUpdated = new Date().toISOString();
}

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/api/health', (req, res) => {
    trackRequest('/api/health');
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        version: '1.0.0',
        services: {
            textAnalysis: 'operational',
            ragSystem: 'operational',
            ethicsChecker: 'operational',
            projectManager: 'operational'
        }
    });
});

// Text Analysis endpoints
app.post('/api/analyze-sentiment', (req, res) => {
    trackRequest('/api/analyze-sentiment');
    try {
        const { text } = req.body;
        if (!text) {
            return res.status(400).json({ error: 'Text is required' });
        }
        
        const result = textAnalysis.analyzeSentiment(text);
        res.json({
            success: true,
            ...result
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/extract-keywords', (req, res) => {
    trackRequest('/api/extract-keywords');
    try {
        const { text } = req.body;
        if (!text) {
            return res.status(400).json({ error: 'Text is required' });
        }
        
        const result = textAnalysis.extractKeywords(text);
        res.json({
            success: true,
            ...result
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/generate-text', (req, res) => {
    trackRequest('/api/generate-text');
    try {
        const { prompt, maxLength = 100 } = req.body;
        if (!prompt) {
            return res.status(400).json({ error: 'Prompt is required' });
        }
        
        const result = textAnalysis.generateText(prompt, maxLength);
        res.json({
            success: true,
            ...result
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// RAG System endpoints
app.post('/api/rag/add-documents', (req, res) => {
    trackRequest('/api/rag/add-documents');
    try {
        const { documents } = req.body;
        if (!documents || !Array.isArray(documents)) {
            return res.status(400).json({ error: 'Documents array is required' });
        }
        
        ragSystem.addDocuments(documents);
        res.json({
            success: true,
            message: `Added ${documents.length} documents`,
            totalDocuments: ragSystem.documents.length
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/rag/search', (req, res) => {
    trackRequest('/api/rag/search');
    try {
        const { query, topK = 3 } = req.body;
        if (!query) {
            return res.status(400).json({ error: 'Query is required' });
        }
        
        const results = ragSystem.searchDocuments(query, topK);
        res.json({
            success: true,
            query,
            results,
            totalDocuments: ragSystem.documents.length
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// AI Ethics endpoints
app.post('/api/ethics/detect-bias', (req, res) => {
    trackRequest('/api/ethics/detect-bias');
    try {
        const { text } = req.body;
        if (!text) {
            return res.status(400).json({ error: 'Text is required' });
        }
        
        const result = ethicsChecker.detectBias(text);
        res.json({
            success: true,
            ...result
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/ethics/suggest-mitigation', (req, res) => {
    trackRequest('/api/ethics/suggest-mitigation');
    try {
        const { biasResults } = req.body;
        if (!biasResults) {
            return res.status(400).json({ error: 'Bias results are required' });
        }
        
        const suggestions = ethicsChecker.suggestMitigation(biasResults);
        res.json({
            success: true,
            suggestions,
            count: suggestions.length
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Project Management endpoints
app.post('/api/projects', (req, res) => {
    trackRequest('/api/projects');
    try {
        const { name, description, modelType, useCase } = req.body;
        if (!name || !description || !modelType || !useCase) {
            return res.status(400).json({ error: 'All fields are required' });
        }
        
        const project = projectManager.createProject(name, description, modelType, useCase);
        projects.set(project.id, project);
        
        res.status(201).json({
            success: true,
            project: project.toJSON()
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/projects', (req, res) => {
    trackRequest('/api/projects');
    try {
        const allProjects = projectManager.getAllProjects();
        res.json({
            success: true,
            projects: allProjects.map(p => p.toJSON()),
            count: allProjects.length
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/projects/:id', (req, res) => {
    trackRequest('/api/projects/:id');
    try {
        const { id } = req.params;
        const project = projectManager.getProject(id);
        
        if (!project) {
            return res.status(404).json({ error: 'Project not found' });
        }
        
        res.json({
            success: true,
            project: project.toJSON()
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.put('/api/projects/:id/metrics', (req, res) => {
    trackRequest('/api/projects/:id/metrics');
    try {
        const { id } = req.params;
        const { accuracy, latency, userSatisfaction } = req.body;
        
        const success = projectManager.updateProjectMetrics(id, {
            accuracy: parseFloat(accuracy) || 0,
            latency: parseFloat(latency) || 0,
            userSatisfaction: parseFloat(userSatisfaction) || 0
        });
        
        if (!success) {
            return res.status(404).json({ error: 'Project not found' });
        }
        
        res.json({
            success: true,
            message: 'Metrics updated successfully'
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Analytics endpoint
app.get('/api/analytics', (req, res) => {
    trackRequest('/api/analytics');
    try {
        const summary = projectManager.getProjectSummary();
        res.json({
            success: true,
            analytics,
            projectSummary: summary,
            systemInfo: {
                totalDocuments: ragSystem.documents.length,
                availableTechniques: Object.keys(ethicsChecker.biasPatterns).length,
                timestamp: new Date().toISOString()
            }
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Demo data endpoint
app.post('/api/demo/initialize', (req, res) => {
    trackRequest('/api/demo/initialize');
    try {
        // Initialize with sample data
        const sampleDocuments = [
            "AI is transforming healthcare through improved diagnosis and treatment planning.",
            "Machine learning algorithms can predict equipment failures in manufacturing.",
            "AI-powered chatbots revolutionize customer service with 24/7 availability.",
            "Generative AI creates new opportunities in content creation and creative industries.",
            "Edge AI enables real-time processing and privacy-preserving applications."
        ];
        
        ragSystem.addDocuments(sampleDocuments);
        
        // Create sample projects
        const sampleProjects = [
            ['Healthcare AI', 'AI-powered diagnosis system', 'Deep Learning', 'Healthcare'],
            ['Customer Chatbot', 'Intelligent customer support', 'NLP', 'Customer Service'],
            ['Fraud Detection', 'AI fraud prevention system', 'Machine Learning', 'Finance']
        ];
        
        sampleProjects.forEach(([name, desc, modelType, useCase]) => {
            const project = projectManager.createProject(name, desc, modelType, useCase);
            projects.set(project.id, project);
            projectManager.updateProjectMetrics(project.id, {
                accuracy: Math.random() * 0.2 + 0.8,
                latency: Math.random() * 400 + 100,
                userSatisfaction: Math.random() * 0.2 + 0.7
            });
        });
        
        res.json({
            success: true,
            message: 'Demo data initialized successfully',
            documentsAdded: sampleDocuments.length,
            projectsCreated: sampleProjects.length
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something went wrong!' });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({ error: 'Endpoint not found' });
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 GenAI JavaScript Web Server running on port ${PORT}`);
    console.log(`📱 Open http://localhost:${PORT} in your browser`);
    console.log(`🔗 API available at http://localhost:${PORT}/api`);
    console.log(`📊 Health check: http://localhost:${PORT}/api/health`);
});

module.exports = app;
