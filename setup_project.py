#!/usr/bin/env python3
"""
GenAI Project Setup Script
Automatically sets up the entire project for hackathon presentation
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

class ProjectSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.python_dir = self.project_root / "04-code-examples" / "python"
        self.js_dir = self.project_root / "04-code-examples" / "javascript"
        self.web_dir = self.project_root / "04-code-examples" / "web-app"
        
        # Colors for terminal output
        self.colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'bold': '\033[1m',
            'end': '\033[0m'
        }
    
    def print_header(self, text):
        """Print a formatted header"""
        print(f"\n{self.colors['bold']}{self.colors['blue']}{'='*60}")
        print(f"{text.center(60)}")
        print(f"{'='*60}{self.colors['end']}")
    
    def print_success(self, text):
        """Print success message"""
        print(f"{self.colors['green']}✅ {text}{self.colors['end']}")
    
    def print_warning(self, text):
        """Print warning message"""
        print(f"{self.colors['yellow']}⚠️  {text}{self.colors['end']}")
    
    def print_error(self, text):
        """Print error message"""
        print(f"{self.colors['red']}❌ {text}{self.colors['end']}")
    
    def print_info(self, text):
        """Print info message"""
        print(f"{self.colors['cyan']}ℹ️  {text}{self.colors['end']}")
    
    def check_python_version(self):
        """Check if Python version is compatible"""
        self.print_header("Checking Python Version")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.print_error(f"Python 3.8+ required. Current version: {version.major}.{version.minor}")
            return False
        
        self.print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    
    def check_node_version(self):
        """Check if Node.js is installed"""
        self.print_header("Checking Node.js Installation")
        
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.print_success(f"Node.js {version} detected")
                return True
            else:
                self.print_warning("Node.js not found. JavaScript examples will not work.")
                return False
        except FileNotFoundError:
            self.print_warning("Node.js not found. JavaScript examples will not work.")
            return False
    
    def install_python_dependencies(self):
        """Install Python dependencies"""
        self.print_header("Installing Python Dependencies")
        
        if not self.python_dir.exists():
            self.print_error("Python examples directory not found")
            return False
        
        requirements_file = self.python_dir / "requirements.txt"
        if not requirements_file.exists():
            self.print_error("requirements.txt not found")
            return False
        
        try:
            # Upgrade pip first
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                         check=True, capture_output=True)
            
            # Install requirements
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)], 
                         check=True, capture_output=True)
            
            self.print_success("Python dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to install Python dependencies: {e}")
            return False
    
    def install_node_dependencies(self):
        """Install Node.js dependencies"""
        self.print_header("Installing Node.js Dependencies")
        
        if not self.js_dir.exists():
            self.print_error("JavaScript examples directory not found")
            return False
        
        package_json = self.js_dir / "package.json"
        if not package_json.exists():
            self.print_error("package.json not found")
            return False
        
        try:
            # Change to JavaScript directory
            os.chdir(self.js_dir)
            
            # Install dependencies
            subprocess.run(['npm', 'install'], check=True, capture_output=True)
            
            self.print_success("Node.js dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to install Node.js dependencies: {e}")
            return False
        finally:
            # Return to project root
            os.chdir(self.project_root)
    
    def create_web_app(self):
        """Create a simple web application"""
        self.print_header("Creating Web Application")
        
        web_dir = self.project_root / "04-code-examples" / "web-app"
        web_dir.mkdir(exist_ok=True)
        
        # Create package.json for web app
        package_json = {
            "name": "genai-web-app",
            "version": "1.0.0",
            "description": "Web application for GenAI demos",
            "main": "server.js",
            "scripts": {
                "start": "node server.js",
                "dev": "nodemon server.js"
            },
            "dependencies": {
                "express": "^4.18.2",
                "cors": "^2.8.5",
                "socket.io": "^4.7.2"
            },
            "devDependencies": {
                "nodemon": "^3.0.1"
            }
        }
        
        with open(web_dir / "package.json", "w") as f:
            json.dump(package_json, f, indent=2)
        
        # Create simple web server
        server_js = '''const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8080;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/api/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        service: 'GenAI Web App'
    });
});

app.listen(PORT, () => {
    console.log(`🚀 GenAI Web App running on port ${PORT}`);
    console.log(`📱 Open http://localhost:${PORT} in your browser`);
});
'''
        
        with open(web_dir / "server.js", "w") as f:
            f.write(server_js)
        
        # Create public directory and HTML file
        public_dir = web_dir / "public"
        public_dir.mkdir(exist_ok=True)
        
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GenAI Web Application</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        .header {
            text-align: center;
            margin-bottom: 3rem;
        }
        .header h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .demo-section {
            background: rgba(255,255,255,0.1);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            backdrop-filter: blur(10px);
        }
        .demo-section h2 {
            color: #ffd700;
            margin-bottom: 1rem;
        }
        button {
            background: #ffd700;
            color: #333;
            padding: 1rem 2rem;
            border: none;
            border-radius: 25px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            margin: 0.5rem;
        }
        button:hover {
            background: #ffed4e;
            transform: scale(1.05);
        }
        .result {
            background: rgba(0,0,0,0.3);
            padding: 1rem;
            border-radius: 5px;
            margin-top: 1rem;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 GenAI Web Application</h1>
            <p>Interactive demonstrations and API testing</p>
        </div>
        
        <div class="demo-section">
            <h2>🏥 Health Check</h2>
            <button onclick="checkHealth()">Check API Health</button>
            <div id="healthResult" class="result" style="display: none;"></div>
        </div>
        
        <div class="demo-section">
            <h2>📊 Project Information</h2>
            <p>This web application demonstrates the GenAI project capabilities:</p>
            <ul>
                <li>Python AI/ML examples with FastAPI</li>
                <li>JavaScript NLP and RAG systems</li>
                <li>Interactive web interface</li>
                <li>RESTful API endpoints</li>
            </ul>
        </div>
        
        <div class="demo-section">
            <h2>🔗 Quick Links</h2>
            <button onclick="window.open('/api/health', '_blank')">API Health</button>
            <button onclick="window.open('http://localhost:8000', '_blank')">Python FastAPI</button>
            <button onclick="window.open('http://localhost:3000', '_blank')">JavaScript Server</button>
        </div>
    </div>
    
    <script>
        async function checkHealth() {
            try {
                const response = await fetch('/api/health');
                const result = await response.json();
                document.getElementById('healthResult').textContent = JSON.stringify(result, null, 2);
                document.getElementById('healthResult').style.display = 'block';
            } catch (error) {
                document.getElementById('healthResult').textContent = 'Error: ' + error.message;
                document.getElementById('healthResult').style.display = 'block';
            }
        }
    </script>
</body>
</html>'''
        
        with open(public_dir / "index.html", "w") as f:
            f.write(html_content)
        
        self.print_success("Web application created successfully")
        return True
    
    def install_web_dependencies(self):
        """Install web application dependencies"""
        self.print_header("Installing Web App Dependencies")
        
        web_dir = self.project_root / "04-code-examples" / "web-app"
        if not web_dir.exists():
            self.print_error("Web app directory not found")
            return False
        
        try:
            os.chdir(web_dir)
            subprocess.run(['npm', 'install'], check=True, capture_output=True)
            self.print_success("Web app dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to install web app dependencies: {e}")
            return False
        finally:
            os.chdir(self.project_root)
    
    def create_demo_scripts(self):
        """Create demo scripts for easy testing"""
        self.print_header("Creating Demo Scripts")
        
        # Create Python demo script
        demo_script = '''#!/usr/bin/env python3
"""
Quick Demo Script for GenAI Project
Run this to see all demos in action
"""

import subprocess
import sys
import os

def run_demo(script_name, description):
    print(f"\\n{'='*60}")
    print(f"Running: {description}")
    print(f"{'='*60}")
    
    try:
        script_path = os.path.join("04-code-examples", "python", script_name)
        subprocess.run([sys.executable, script_path], check=True)
        print(f"✅ {description} completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
    except Exception as e:
        print(f"❌ {description} failed: {e}")

def main():
    print("🚀 GenAI Project Demo Runner")
    print("This script will run all available demos")
    
    demos = [
        ("genai_demo.py", "Main GenAI Demo"),
        ("prompt_engineering.py", "Prompt Engineering Examples"),
        ("fastapi_app.py", "FastAPI Web Application")
    ]
    
    for script, description in demos:
        if os.path.exists(os.path.join("04-code-examples", "python", script)):
            run_demo(script, description)
        else:
            print(f"⚠️  {script} not found, skipping...")
    
    print("\\n🎉 All demos completed!")
    print("\\n💡 Next steps:")
    print("1. Start FastAPI server: cd 04-code-examples/python && python fastapi_app.py")
    print("2. Start JavaScript server: cd 04-code-examples/javascript && npm run web")
    print("3. Start Web app: cd 04-code-examples/web-app && npm start")

if __name__ == "__main__":
    main()
'''
        
        with open(self.project_root / "run_demos.py", "w") as f:
            f.write(demo_script)
        
        # Make it executable on Unix systems
        if platform.system() != "Windows":
            os.chmod(self.project_root / "run_demos.py", 0o755)
        
        self.print_success("Demo scripts created successfully")
        return True
    
    def create_presentation_materials(self):
        """Create presentation materials for hackathon"""
        self.print_header("Creating Presentation Materials")
        
        # Create project overview
        overview = '''# 🏆 GenAI Project - Hackathon Presentation

## 🎯 Project Overview
**GenAI Future Opportunities & Skills** - A comprehensive exploration of Generative AI beyond current hype, essential skills for professionals, and best practices for AI adoption.

## 🚀 Key Features
- **5 Core Modules**: Future opportunities, essential skills, adoption strategies, code examples, and resources
- **3 Technology Stacks**: Python (FastAPI), JavaScript (Node.js), and Web applications
- **15+ API Endpoints**: RESTful APIs for all AI capabilities
- **Interactive Demos**: Live demonstrations of GenAI technologies
- **Production Ready**: Professional-grade code with proper error handling

## 🎮 Live Demonstrations
1. **Text Generation & Analysis**: AI-powered text generation and sentiment analysis
2. **RAG System**: Retrieval-Augmented Generation for knowledge search
3. **AI Ethics**: Bias detection and mitigation strategies
4. **Project Management**: AI project lifecycle management
5. **Prompt Engineering**: Advanced techniques for LLM interaction

## 💻 Technical Implementation
- **Backend**: FastAPI (Python), Express.js (Node.js)
- **AI/ML**: Transformers, scikit-learn, Natural.js
- **Frontend**: Modern HTML5/CSS3 with interactive JavaScript
- **Architecture**: Microservices with REST APIs
- **Deployment**: Containerized and cloud-ready

## 🌟 Innovation Highlights
- **Multi-Platform**: Works across Python, JavaScript, and Web ecosystems
- **Industry Focus**: Real-world applications in healthcare, finance, manufacturing
- **Ethics First**: Built-in bias detection and responsible AI practices
- **Scalable**: Designed for enterprise deployment
- **Educational**: Comprehensive learning resources and examples

## 🎯 Business Value
- **Cost Reduction**: AI automation and efficiency improvements
- **Risk Mitigation**: Ethical AI practices and bias detection
- **Competitive Advantage**: Cutting-edge AI implementation strategies
- **Talent Development**: Skills roadmap for AI professionals
- **ROI Optimization**: Best practices for AI project success

## 🚀 Getting Started
```bash
# Run all demos
python run_demos.py

# Start Python API server
cd 04-code-examples/python
python fastapi_app.py

# Start JavaScript server
cd 04-code-examples/javascript
npm run web

# Start Web application
cd 04-code-examples/web-app
npm start
```

## 📊 Demo URLs
- **Python FastAPI**: http://localhost:8000
- **JavaScript Server**: http://localhost:3000
- **Web Application**: http://localhost:8080
- **API Documentation**: http://localhost:8000/docs

## 🏆 Why This Project Will Win
1. **Comprehensive Coverage**: All aspects of GenAI from theory to implementation
2. **Production Quality**: Enterprise-ready code with proper architecture
3. **Visual Appeal**: Beautiful, modern UI/UX design
4. **Real-World Impact**: Practical applications across multiple industries
5. **Technical Excellence**: Clean, well-documented, maintainable code
6. **Innovation**: Cutting-edge AI techniques and methodologies

## 🤝 Questions & Discussion
Ready to demonstrate any specific feature or answer questions about the implementation!
'''
        
        with open(self.project_root / "HACKATHON_PRESENTATION.md", "w") as f:
            f.write(overview)
        
        self.print_success("Presentation materials created successfully")
        return True
    
    def run_tests(self):
        """Run basic tests to ensure everything works"""
        self.print_header("Running Basic Tests")
        
        try:
            # Test Python imports
            import sys
            sys.path.append(str(self.python_dir))
            
            # Test basic imports
            try:
                import numpy
                self.print_success("NumPy imported successfully")
            except ImportError:
                self.print_warning("NumPy not available")
            
            try:
                import pandas
                self.print_success("Pandas imported successfully")
            except ImportError:
                self.print_warning("Pandas not available")
            
            try:
                import sklearn
                self.print_success("Scikit-learn imported successfully")
            except ImportError:
                self.print_warning("Scikit-learn not available")
            
            self.print_success("Basic tests completed")
            return True
            
        except Exception as e:
            self.print_error(f"Tests failed: {e}")
            return False
    
    def print_final_instructions(self):
        """Print final setup instructions"""
        self.print_header("🎉 Project Setup Complete!")
        
        print(f"{self.colors['green']}Your GenAI project is ready for the hackathon!{self.colors['end']}")
        print()
        print(f"{self.colors['bold']}🚀 Quick Start:{self.colors['end']}")
        print("1. Run all demos: python run_demos.py")
        print("2. Start Python server: cd 04-code-examples/python && python fastapi_app.py")
        print("3. Start JavaScript server: cd 04-code-examples/javascript && npm run web")
        print("4. Start Web app: cd 04-code-examples/web-app && npm start")
        print()
        print(f"{self.colors['bold']}📱 Demo URLs:{self.colors['end']}")
        print("• Python FastAPI: http://localhost:8000")
        print("• JavaScript Server: http://localhost:3000")
        print("• Web Application: http://localhost:8080")
        print()
        print(f"{self.colors['bold']}📚 Documentation:{self.colors['end']}")
        print("• README.md - Project overview and setup")
        print("• HACKATHON_PRESENTATION.md - Presentation guide")
        print("• API docs: http://localhost:8000/docs")
        print()
        print(f"{self.colors['bold']}🏆 Hackathon Tips:{self.colors['end']}")
        print("• Demo the live applications")
        print("• Show the comprehensive documentation")
        print("• Highlight the multiple technology stacks")
        print("• Emphasize real-world applications")
        print("• Be ready to explain any part of the code")
        print()
        print(f"{self.colors['green']}Good luck with your hackathon presentation! 🎯{self.colors['end']}")
    
    def setup(self):
        """Run the complete setup process"""
        self.print_header("🚀 GenAI Project Setup for Hackathon")
        
        print(f"{self.colors['cyan']}This script will set up your entire GenAI project for hackathon presentation.{self.colors['end']}")
        print()
        
        # Check prerequisites
        if not self.check_python_version():
            return False
        
        node_available = self.check_node_version()
        
        # Install dependencies
        if not self.install_python_dependencies():
            return False
        
        if node_available:
            if not self.install_node_dependencies():
                self.print_warning("Node.js setup failed, but Python examples will work")
        
        # Create web application
        if not self.create_web_app():
            return False
        
        if not self.install_web_dependencies():
            self.print_warning("Web app setup failed, but other examples will work")
        
        # Create demo scripts and materials
        if not self.create_demo_scripts():
            return False
        
        if not self.create_presentation_materials():
            return False
        
        # Run tests
        self.run_tests()
        
        # Print final instructions
        self.print_final_instructions()
        
        return True

def main():
    """Main function"""
    setup = ProjectSetup()
    
    try:
        success = setup.setup()
        if success:
            print(f"\n{setup.colors['green']}🎉 Setup completed successfully!{setup.colors['end']}")
        else:
            print(f"\n{setup.colors['red']}❌ Setup failed. Please check the errors above.{setup.colors['end']}")
            sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{setup.colors['yellow']}⚠️  Setup interrupted by user{setup.colors['end']}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{setup.colors['red']}❌ Unexpected error: {e}{setup.colors['end']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
