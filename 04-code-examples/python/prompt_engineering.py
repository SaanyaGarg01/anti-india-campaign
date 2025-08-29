#!/usr/bin/env python3
"""
Prompt Engineering Examples for GenAI
Demonstrates various prompt engineering techniques and best practices
"""

import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PromptExample:
    name: str
    description: str
    prompt: str
    expected_output: str
    technique: str
    difficulty: str

class PromptEngineeringDemo:
    """Demonstrates various prompt engineering techniques"""
    
    def __init__(self):
        self.examples = self._load_examples()
        self.techniques = {
            "zero_shot": "Direct question without examples",
            "few_shot": "Provide examples before asking",
            "chain_of_thought": "Step-by-step reasoning",
            "role_playing": "Assign specific roles or personas",
            "constraints": "Set specific limitations or requirements",
            "formatting": "Specify exact output format"
        }
    
    def _load_examples(self) -> List[PromptExample]:
        """Load prompt engineering examples"""
        return [
            PromptExample(
                name="Zero-Shot Classification",
                description="Classify text without training examples",
                prompt="Classify the following text as positive, negative, or neutral: 'I absolutely love this new AI technology!'",
                expected_output="positive",
                technique="zero_shot",
                difficulty="beginner"
            ),
            PromptExample(
                name="Few-Shot Learning",
                description="Provide examples to guide the model",
                prompt="""Here are some examples of sentiment classification:

Text: "I love this product!"
Sentiment: positive

Text: "This is terrible quality."
Sentiment: negative

Text: "The product works okay."
Sentiment: neutral

Now classify: "I'm not sure about this purchase."
Sentiment:""",
                expected_output="neutral",
                technique="few_shot",
                difficulty="intermediate"
            ),
            PromptExample(
                name="Chain of Thought",
                description="Encourage step-by-step reasoning",
                prompt="""Let's solve this step by step:

Problem: A company wants to implement AI for customer service. They have 1000 customer inquiries per day, and currently each inquiry takes 5 minutes to resolve. If AI can reduce this to 2 minutes, how much time will be saved per day?

Let me think through this:
1. Current time per inquiry: 5 minutes
2. New time per inquiry: 2 minutes
3. Time saved per inquiry: 5 - 2 = 3 minutes
4. Total inquiries per day: 1000
5. Total time saved per day: 1000 × 3 = 3000 minutes
6. Convert to hours: 3000 ÷ 60 = 50 hours

Answer: The company will save 50 hours per day.""",
                expected_output="50 hours per day",
                technique="chain_of_thought",
                difficulty="advanced"
            ),
            PromptExample(
                name="Role Playing",
                description="Assign specific roles or expertise",
                prompt="""You are an expert data scientist with 15 years of experience in machine learning. You specialize in healthcare AI applications and have published over 50 papers in top-tier journals.

As this expert, explain to a business executive why their company should invest in AI-powered predictive maintenance for their manufacturing equipment. Use business language and focus on ROI and risk reduction.""",
                expected_output="Professional business explanation with ROI focus",
                technique="role_playing",
                difficulty="intermediate"
            ),
            PromptExample(
                name="Output Formatting",
                description="Specify exact output structure",
                prompt="""Analyze the following customer feedback and provide insights in JSON format:

Customer Feedback: "The new AI chatbot is helpful but sometimes gives incorrect information. I like the 24/7 availability but wish it could handle complex queries better."

Please format your response as:
{
  "positive_aspects": ["list", "of", "positive", "points"],
  "negative_aspects": ["list", "of", "negative", "points"],
  "improvement_suggestions": ["list", "of", "suggestions"],
  "overall_sentiment": "positive/negative/neutral",
  "priority_level": "high/medium/low"
}""",
                expected_output="Structured JSON response",
                technique="formatting",
                difficulty="intermediate"
            ),
            PromptExample(
                name="Constraint-Based",
                description="Set specific limitations or requirements",
                prompt="""Write a product description for an AI-powered smart home device. 

Requirements:
- Maximum 100 words
- Target audience: tech-savvy homeowners aged 25-45
- Include exactly 3 benefits
- Use active voice only
- Avoid technical jargon
- End with a call-to-action

Product: SmartTherm AI - Intelligent temperature control system""",
                expected_output="Concise product description meeting all constraints",
                technique="constraints",
                difficulty="advanced"
            )
        ]
    
    def get_examples_by_technique(self, technique: str) -> List[PromptExample]:
        """Get examples filtered by technique"""
        return [ex for ex in self.examples if ex.technique == technique]
    
    def get_examples_by_difficulty(self, difficulty: str) -> List[PromptExample]:
        """Get examples filtered by difficulty"""
        return [ex for ex in self.examples if ex.difficulty == difficulty]
    
    def analyze_prompt_effectiveness(self, prompt: str) -> Dict[str, Any]:
        """Analyze prompt effectiveness based on best practices"""
        analysis = {
            "clarity_score": 0,
            "specificity_score": 0,
            "constraint_score": 0,
            "examples_score": 0,
            "format_score": 0,
            "overall_score": 0,
            "suggestions": []
        }
        
        # Clarity analysis
        if len(prompt.split()) < 50:
            analysis["clarity_score"] += 2
            analysis["suggestions"].append("Consider adding more context for clarity")
        elif len(prompt.split()) < 200:
            analysis["clarity_score"] += 4
        else:
            analysis["clarity_score"] += 5
        
        # Specificity analysis
        if "?" in prompt:
            analysis["specificity_score"] += 2
        if any(word in prompt.lower() for word in ["specific", "exact", "precise", "detailed"]):
            analysis["specificity_score"] += 2
        if len(prompt.split()) > 100:
            analysis["specificity_score"] += 1
        
        # Constraint analysis
        if any(word in prompt.lower() for word in ["maximum", "minimum", "exactly", "only", "must", "should"]):
            analysis["constraint_score"] += 3
        if any(word in prompt.lower() for word in ["format", "structure", "json", "xml", "table"]):
            analysis["constraint_score"] += 2
        
        # Examples analysis
        if "example" in prompt.lower() or "for instance" in prompt.lower():
            analysis["examples_score"] += 3
        
        # Format analysis
        if any(word in prompt.lower() for word in ["format", "output", "response", "answer"]):
            analysis["format_score"] += 2
        
        # Calculate overall score
        analysis["overall_score"] = sum([
            analysis["clarity_score"],
            analysis["specificity_score"],
            analysis["constraint_score"],
            analysis["examples_score"],
            analysis["format_score"]
        ]) / 5
        
        # Add improvement suggestions
        if analysis["overall_score"] < 3:
            analysis["suggestions"].append("Consider using few-shot examples")
            analysis["suggestions"].append("Add specific output format requirements")
        if analysis["overall_score"] < 2:
            analysis["suggestions"].append("Review prompt clarity and specificity")
        
        return analysis
    
    def generate_prompt_template(self, use_case: str, technique: str) -> str:
        """Generate a prompt template for specific use case and technique"""
        templates = {
            "classification": {
                "zero_shot": "Classify the following {input_type} as {categories}: {input_text}",
                "few_shot": "Here are some examples:\n{examples}\n\nNow classify: {input_text}",
                "chain_of_thought": "Let's solve this step by step:\n\nProblem: {problem}\n\nLet me think through this:\n{steps}\n\nAnswer:"
            },
            "generation": {
                "role_playing": "You are {role} with {expertise}. {task_description}",
                "constraints": "Create {output_type} with these requirements:\n{requirements}\n\n{task_description}",
                "formatting": "Generate {output_type} in this exact format:\n{format_specification}\n\n{task_description}"
            }
        }
        
        if use_case in templates and technique in templates[use_case]:
            return templates[use_case][technique]
        else:
            return "Custom prompt template for your specific needs"
    
    def demonstrate_techniques(self):
        """Demonstrate all prompt engineering techniques"""
        print("🎯 Prompt Engineering Techniques Demonstration")
        print("=" * 60)
        
        for technique, description in self.techniques.items():
            print(f"\n🔧 {technique.upper().replace('_', ' ')}")
            print(f"Description: {description}")
            
            examples = self.get_examples_by_technique(technique)
            if examples:
                example = examples[0]
                print(f"Example: {example.name}")
                print(f"Prompt: {example.prompt[:100]}...")
                print(f"Expected Output: {example.expected_output}")
                print(f"Difficulty: {example.difficulty}")
        
        print("\n📊 Prompt Analysis Example")
        print("-" * 30)
        
        sample_prompt = "Write a blog post about AI in healthcare"
        analysis = self.analyze_prompt_effectiveness(sample_prompt)
        
        print(f"Sample Prompt: {sample_prompt}")
        print(f"Overall Score: {analysis['overall_score']:.1f}/5.0")
        print("Suggestions:")
        for suggestion in analysis["suggestions"]:
            print(f"  - {suggestion}")

def main():
    """Main demonstration function"""
    demo = PromptEngineeringDemo()
    
    print("🚀 Prompt Engineering for GenAI")
    print("=" * 50)
    
    # Show all techniques
    demo.demonstrate_techniques()
    
    # Interactive prompt analysis
    print("\n🔍 Interactive Prompt Analysis")
    print("-" * 30)
    
    test_prompts = [
        "Explain machine learning",
        "You are an expert data scientist. Explain machine learning in simple terms for a business audience. Focus on practical applications and ROI.",
        "Here are examples of good explanations:\nExample 1: Clear and concise\nExample 2: Uses analogies\n\nNow explain machine learning following these examples."
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\nPrompt {i}: {prompt}")
        analysis = demo.analyze_prompt_effectiveness(prompt)
        print(f"Score: {analysis['overall_score']:.1f}/5.0")
        if analysis['suggestions']:
            print("Suggestions:")
            for suggestion in analysis['suggestions']:
                print(f"  - {suggestion}")
    
    print("\n✅ Prompt Engineering demo completed!")
    print("\n💡 Key Takeaways:")
    print("- Clear, specific prompts yield better results")
    print("- Few-shot examples improve model performance")
    print("- Constraints and formatting guide output quality")
    print("- Role-playing adds context and expertise")

if __name__ == "__main__":
    main()
