#!/usr/bin/env node
/**
 * GenAI JavaScript Demo - Future Opportunities & Skills
 * Demonstrates various GenAI capabilities using Node.js
 */

const natural = require('natural');
const { v4: uuidv4 } = require('uuid');

// Configure natural language processing
natural.PorterStemmer.attach();

class GenAIProject {
    constructor(name, description, modelType, useCase) {
        this.id = uuidv4();
        this.name = name;
        this.description = description;
        this.modelType = modelType;
        this.useCase = useCase;
        this.createdDate = new Date().toISOString();
        this.status = 'active';
        this.performanceMetrics = {
            accuracy: 0.0,
            latency: 0.0,
            userSatisfaction: 0.0,
            lastUpdated: new Date().toISOString()
        };
    }

    updateMetrics(metrics) {
        this.performanceMetrics = { ...this.performanceMetrics, ...metrics };
        this.performanceMetrics.lastUpdated = new Date().toISOString();
    }

    toJSON() {
        return {
            id: this.id,
            name: this.name,
            description: this.description,
            modelType: this.modelType,
            useCase: this.useCase,
            createdDate: this.createdDate,
            status: this.status,
            performanceMetrics: this.performanceMetrics
        };
    }
}

class TextAnalysisDemo {
    constructor() {
        this.tokenizer = new natural.WordTokenizer();
        this.tfidf = new natural.TfIdf();
        this.classifier = new natural.BayesClassifier();
        this.trainingData = this.initializeTrainingData();
        this.trainClassifier();
    }

    initializeTrainingData() {
        return {
            positive: [
                "I love this AI technology!",
                "This is amazing and helpful",
                "Great performance and results",
                "Excellent user experience",
                "Outstanding quality and features"
            ],
            negative: [
                "This is terrible and useless",
                "Poor performance and quality",
                "Disappointing results",
                "Bad user experience",
                "Awful and frustrating"
            ],
            neutral: [
                "The system works as expected",
                "It's okay, nothing special",
                "Average performance",
                "Standard functionality",
                "Meets basic requirements"
            ]
        };
    }

    trainClassifier() {
        this.trainingData.positive.forEach(text => {
            this.classifier.addDocument(text, 'positive');
        });
        this.trainingData.negative.forEach(text => {
            this.classifier.addDocument(text, 'negative');
        });
        this.trainingData.neutral.forEach(text => {
            this.classifier.addDocument(text, 'neutral');
        });
        this.classifier.train();
    }

    analyzeSentiment(text) {
        try {
            const classification = this.classifier.classify(text);
            const confidence = this.calculateConfidence(text, classification);
            
            return {
                text: text,
                sentiment: classification,
                confidence: confidence,
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            return {
                text: text,
                sentiment: 'unknown',
                confidence: 0.0,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    calculateConfidence(text, classification) {
        // Simple confidence calculation based on word overlap
        const words = this.tokenizer.tokenize(text.toLowerCase());
        const trainingExamples = this.trainingData[classification] || [];
        
        let maxOverlap = 0;
        trainingExamples.forEach(example => {
            const exampleWords = this.tokenizer.tokenize(example.toLowerCase());
            const overlap = words.filter(word => exampleWords.includes(word)).length;
            const overlapRatio = overlap / Math.max(words.length, exampleWords.length);
            maxOverlap = Math.max(maxOverlap, overlapRatio);
        });
        
        return Math.min(maxOverlap * 2, 1.0); // Scale to 0-1 range
    }

    extractKeywords(text) {
        try {
            const words = this.tokenizer.tokenize(text.toLowerCase());
            const stopWords = new Set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']);
            
            const filteredWords = words.filter(word => 
                word.length > 3 && !stopWords.has(word) && /^[a-zA-Z]+$/.test(word)
            );
            
            const wordFreq = {};
            filteredWords.forEach(word => {
                wordFreq[word] = (wordFreq[word] || 0) + 1;
            });
            
            const sortedWords = Object.entries(wordFreq)
                .sort(([,a], [,b]) => b - a)
                .slice(0, 10)
                .map(([word, freq]) => ({ word, frequency: freq }));
            
            return {
                text: text,
                keywords: sortedWords,
                totalWords: words.length,
                uniqueKeywords: sortedWords.length,
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            return {
                text: text,
                keywords: [],
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    generateText(prompt, maxLength = 100) {
        try {
            // Simple text generation using Markov chain approach
            const words = this.tokenizer.tokenize(prompt);
            if (words.length === 0) return prompt;
            
            let generatedText = prompt;
            const wordPairs = this.createWordPairs(prompt);
            
            while (generatedText.length < maxLength && wordPairs.length > 0) {
                const randomPair = wordPairs[Math.floor(Math.random() * wordPairs.length)];
                const nextWord = this.predictNextWord(randomPair);
                if (nextWord) {
                    generatedText += ' ' + nextWord;
                    wordPairs.push([randomPair[1], nextWord]);
                } else {
                    break;
                }
            }
            
            return {
                prompt: prompt,
                generatedText: generatedText,
                length: generatedText.length,
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            return {
                prompt: prompt,
                generatedText: prompt,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    createWordPairs(text) {
        const words = this.tokenizer.tokenize(text);
        const pairs = [];
        for (let i = 0; i < words.length - 1; i++) {
            pairs.push([words[i], words[i + 1]]);
        }
        return pairs;
    }

    predictNextWord(pair) {
        // Simple prediction - in a real implementation, this would use a trained model
        const commonWords = ['the', 'a', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'];
        return commonWords[Math.floor(Math.random() * commonWords.length)];
    }
}

class RAGSystem {
    constructor() {
        this.documents = [];
        this.tfidf = new natural.TfIdf();
        this.documentVectors = null;
    }

    addDocuments(documents) {
        this.documents = documents;
        this.tfidf = new natural.TfIdf();
        documents.forEach((doc, index) => {
            this.tfidf.addDocument(doc);
        });
    }

    searchDocuments(query, topK = 3) {
        if (this.documents.length === 0) return [];
        
        try {
            // Add query to TF-IDF for comparison
            const tempTfidf = new natural.TfIdf();
            tempTfidf.addDocument(query);
            
            const results = [];
            this.documents.forEach((doc, index) => {
                const similarity = this.calculateSimilarity(query, doc);
                results.push({
                    document: doc,
                    similarityScore: similarity,
                    rank: 0
                });
            });
            
            // Sort by similarity and assign ranks
            results.sort((a, b) => b.similarityScore - a.similarityScore);
            results.forEach((result, index) => {
                result.rank = index + 1;
            });
            
            return results.slice(0, topK);
        } catch (error) {
            console.error('Error in RAG search:', error);
            return [];
        }
    }

    calculateSimilarity(query, document) {
        try {
            const queryWords = new Set(query.toLowerCase().split(/\s+/));
            const docWords = new Set(document.toLowerCase().split(/\s+/));
            
            const intersection = new Set([...queryWords].filter(x => docWords.has(x)));
            const union = new Set([...queryWords, ...docWords]);
            
            return intersection.size / union.size;
        } catch (error) {
            return 0.0;
        }
    }
}

class AIEthicsChecker {
    constructor() {
        this.biasPatterns = {
            gender: ['he', 'she', 'man', 'woman', 'male', 'female', 'boy', 'girl'],
            age: ['young', 'old', 'elderly', 'youth', 'teenager', 'senior'],
            ethnicity: ['race', 'ethnic', 'nationality', 'cultural'],
            socioeconomic: ['rich', 'poor', 'wealthy', 'poverty', 'expensive', 'cheap']
        };
    }

    detectBias(text) {
        try {
            const textLower = text.toLowerCase();
            const biasResults = {};
            
            Object.entries(this.biasPatterns).forEach(([biasType, patterns]) => {
                const matches = patterns.filter(pattern => textLower.includes(pattern));
                biasResults[biasType] = {
                    detected: matches.length > 0,
                    patternsFound: matches,
                    count: matches.length
                };
            });
            
            const overallBiasScore = Object.values(biasResults)
                .reduce((sum, result) => sum + result.count, 0);
            
            return {
                text: text,
                biasAnalysis: biasResults,
                overallBiasScore: overallBiasScore,
                riskLevel: this.assessRiskLevel(overallBiasScore),
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            return {
                text: text,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    assessRiskLevel(biasScore) {
        if (biasScore === 0) return 'low';
        if (biasScore <= 2) return 'medium';
        if (biasScore <= 5) return 'high';
        return 'critical';
    }

    suggestMitigation(biasResults) {
        const suggestions = [];
        
        Object.entries(biasResults.biasAnalysis).forEach(([biasType, result]) => {
            if (result.detected) {
                switch (biasType) {
                    case 'gender':
                        suggestions.push('Consider using gender-neutral language');
                        break;
                    case 'age':
                        suggestions.push('Avoid age-related stereotypes');
                        break;
                    case 'ethnicity':
                        suggestions.push('Ensure diverse representation');
                        break;
                    case 'socioeconomic':
                        suggestions.push('Avoid socioeconomic assumptions');
                        break;
                }
            }
        });
        
        return suggestions;
    }
}

class GenAIProjectManager {
    constructor() {
        this.projects = new Map();
        this.performanceMetrics = new Map();
    }

    createProject(name, description, modelType, useCase) {
        const project = new GenAIProject(name, description, modelType, useCase);
        this.projects.set(project.id, project);
        this.performanceMetrics.set(project.id, {
            accuracy: 0.0,
            latency: 0.0,
            userSatisfaction: 0.0,
            lastUpdated: new Date().toISOString()
        });
        
        console.log(`Created project: ${project.id}`);
        return project;
    }

    getProject(projectId) {
        return this.projects.get(projectId);
    }

    getAllProjects() {
        return Array.from(this.projects.values());
    }

    updateProjectMetrics(projectId, metrics) {
        const project = this.projects.get(projectId);
        if (project) {
            project.updateMetrics(metrics);
            this.performanceMetrics.set(projectId, project.performanceMetrics);
            console.log(`Updated metrics for project: ${projectId}`);
            return true;
        }
        return false;
    }

    getProjectSummary() {
        const projects = Array.from(this.projects.values());
        const metrics = Array.from(this.performanceMetrics.values());
        
        return {
            totalProjects: projects.length,
            activeProjects: projects.filter(p => p.status === 'active').length,
            averageAccuracy: metrics.reduce((sum, m) => sum + m.accuracy, 0) / metrics.length || 0,
            projectsByType: this.groupProjectsByType(projects),
            lastUpdated: new Date().toISOString()
        };
    }

    groupProjectsByType(projects) {
        const grouped = {};
        projects.forEach(project => {
            grouped[project.modelType] = (grouped[project.modelType] || 0) + 1;
        });
        return grouped;
    }
}

// Main demonstration function
async function main() {
    console.log('🚀 GenAI JavaScript Demo - Future Opportunities & Skills');
    console.log('=' .repeat(60));
    
    // Initialize components
    const textAnalysis = new TextAnalysisDemo();
    const ragSystem = new RAGSystem();
    const ethicsChecker = new AIEthicsChecker();
    const projectManager = new GenAIProjectManager();
    
    // Demo 1: Text Analysis
    console.log('\n📝 Text Analysis Demo');
    console.log('-'.repeat(30));
    
    const sampleTexts = [
        "I absolutely love this new AI technology!",
        "This AI system is terrible and unreliable.",
        "The AI performance is acceptable but could be better."
    ];
    
    sampleTexts.forEach(text => {
        const sentiment = textAnalysis.analyzeSentiment(text);
        console.log(`Text: "${text}"`);
        console.log(`Sentiment: ${sentiment.sentiment} (confidence: ${sentiment.confidence.toFixed(2)})`);
        
        const keywords = textAnalysis.extractKeywords(text);
        console.log(`Keywords: ${keywords.keywords.map(k => k.word).join(', ')}`);
        console.log('');
    });
    
    // Demo 2: Text Generation
    console.log('\n🔮 Text Generation Demo');
    console.log('-'.repeat(30));
    
    const prompt = "The future of artificial intelligence will";
    const generated = textAnalysis.generateText(prompt, 80);
    console.log(`Prompt: "${prompt}"`);
    console.log(`Generated: "${generated.generatedText}"`);
    console.log(`Length: ${generated.length} characters`);
    
    // Demo 3: RAG System
    console.log('\n🔍 RAG System Demo');
    console.log('-'.repeat(30));
    
    const documents = [
        "AI is transforming healthcare through improved diagnosis and treatment planning.",
        "Machine learning algorithms can predict equipment failures in manufacturing.",
        "AI-powered chatbots revolutionize customer service with 24/7 availability.",
        "Generative AI creates new opportunities in content creation and creative industries."
    ];
    
    ragSystem.addDocuments(documents);
    
    const query = "How is AI improving healthcare?";
    const searchResults = ragSystem.searchDocuments(query, 3);
    
    console.log(`Query: "${query}"`);
    searchResults.forEach(result => {
        console.log(`Rank ${result.rank}: ${result.document}`);
        console.log(`Similarity Score: ${result.similarityScore.toFixed(3)}`);
    });
    
    // Demo 4: AI Ethics
    console.log('\n⚖️ AI Ethics & Bias Detection Demo');
    console.log('-'.repeat(30));
    
    const testTexts = [
        "The doctor and nurse worked together to help the patient.",
        "Only young people can understand new technology.",
        "The wealthy businessman hired the poor worker."
    ];
    
    testTexts.forEach(text => {
        const biasAnalysis = ethicsChecker.detectBias(text);
        console.log(`Text: "${text}"`);
        console.log(`Bias Score: ${biasAnalysis.overallBiasScore}`);
        console.log(`Risk Level: ${biasAnalysis.riskLevel}`);
        
        const suggestions = ethicsChecker.suggestMitigation(biasAnalysis);
        if (suggestions.length > 0) {
            console.log('Suggestions:');
            suggestions.forEach(suggestion => console.log(`  - ${suggestion}`));
        }
        console.log('');
    });
    
    // Demo 5: Project Management
    console.log('\n📊 GenAI Project Management Demo');
    console.log('-'.repeat(30));
    
    const projects = [
        ['Healthcare AI', 'AI-powered diagnosis system', 'Deep Learning', 'Healthcare'],
        ['Customer Chatbot', 'Intelligent customer support', 'NLP', 'Customer Service'],
        ['Fraud Detection', 'AI fraud prevention system', 'Machine Learning', 'Finance']
    ];
    
    projects.forEach(([name, desc, modelType, useCase]) => {
        const project = projectManager.createProject(name, desc, modelType, useCase);
        projectManager.updateProjectMetrics(project.id, {
            accuracy: Math.random() * 0.2 + 0.8,
            latency: Math.random() * 400 + 100,
            userSatisfaction: Math.random() * 0.2 + 0.7
        });
    });
    
    const summary = projectManager.getProjectSummary();
    console.log(`Total Projects: ${summary.totalProjects}`);
    console.log(`Active Projects: ${summary.activeProjects}`);
    console.log(`Average Accuracy: ${summary.averageAccuracy.toFixed(3)}`);
    console.log(`Projects by Type:`, summary.projectsByType);
    
    console.log('\n✅ JavaScript demo completed successfully!');
    console.log('\n💡 Key Takeaways:');
    console.log('- JavaScript provides powerful NLP capabilities for GenAI');
    console.log('- RAG systems can be implemented efficiently in Node.js');
    console.log('- Ethics and bias detection are crucial for responsible AI');
    console.log('- Project management ensures AI implementation success');
}

// Run the demo if this file is executed directly
if (require.main === module) {
    main().catch(console.error);
}

// Export classes for use in other modules
module.exports = {
    GenAIProject,
    TextAnalysisDemo,
    RAGSystem,
    AIEthicsChecker,
    GenAIProjectManager
};
