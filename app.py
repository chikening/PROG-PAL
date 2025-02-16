from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)

# Get API key from environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
class ProgrammingLearningAssistant:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        self.programming_languages = [
            "Python", "JavaScript", "Java", "C++", "C#", "Ruby", "Go", 
            "Swift", "Kotlin", "PHP", "TypeScript", "Rust", "SQL"
        ]
        
    def validate_programming_topic(self, topic):
        # Check if the topic is related to programming
        programming_keywords = [
    # General terms
        "programming", "coding", "development", "software", "web", "app",
        "algorithm", "data structure", "framework", "library", "api",

    # Common programming keywords (language-agnostic)
        "function", "method", "class", "object", "module", "import", "export",
        "package", "interface", "namespace", "typedef", "constant", "variable",
        "parameter", "argument", "return", "static", "final", "virtual", "override",
        "extends", "implements", "abstract", "constructor", "get", "set", "new",
        "this", "super", "null", "true", "false",

    # Control flow
        "if", "else", "switch", "case", "default", "for", "while", "do", "break",
        "continue", "goto", "return", "yield", "throw", "catch", "finally", "try",

    # Access Modifiers
        "public", "private", "protected", "internal", "friend", "readonly", "sealed",

    # Data types
        "int", "float", "double", "char", "string", "bool", "byte", "long",
        "short", "decimal", "var", "let", "const", "dynamic", "enum", "array",
        "dictionary", "list", "tuple", "set", "map", "queue", "stack", "pointer",

    # Operators
        "and", "or", "not", "xor", "is", "in", "instanceof", "typeof",
        "sizeof", "await", "async", "defer",

    # Error handling
        "try", "catch", "throw", "finally", "assert", "raise", "panic",

    # Common scripting language constructs
        "print", "echo", "input", "read", "write", "exec", "eval",

    # Miscellaneous
        "main", "def", "lambda", "del", "pass", "global", "nonlocal",
        "inline", "macro", "template", "typedef", "union", "volatile",
        "friend", "constexpr", "namespace", "export",

    # Specific language keywords
        *self.programming_languages,  # Include any dynamically loaded languages
]
        return any(keyword.lower() in topic.lower() for keyword in programming_keywords)
    
    def generate_response(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def create_study_plan(self, topic, current_level, goal, timeframe):
        if not self.validate_programming_topic(topic):
            return "Please provide a programming-related topic for your study plan."
            
        prompt = f"""
        Create a detailed programming study plan for:
        Topic: {topic}
        Current Level: {current_level}
        Learning Goal: {goal}
        Duration: {timeframe} weeks

        Please structure the response in markdown format with specific focus on:

        # Programming Study Plan: {topic}

        ## Technical Overview
        - Current Programming Level: {current_level}
        - Technical Goal: {goal}
        - Duration: {timeframe} weeks
        - Required Development Environment

        ## Weekly Technical Schedule

        **Week 1**
        **Core Programming Concepts**
        - [List 3-4 main programming topics]
    
        **Coding Activities**
        - [Daily coding exercises]
        - [Programming challenges]
    
        **Programming Projects**
        - [2-3 hands-on coding projects]
        - [GitHub repository setup]
    
        **Technical Resources**
        - Official documentation
        - Code examples
        - Development tools

        [Continue similar structure for remaining weeks...]

        ## Development Setup
        **Required Tools**
        - IDE/Code editor
        - Version control
        - Package managers
        - Testing frameworks

        **Learning Resources**
        - Official documentation
        - GitHub repositories
        - Coding platforms
        - Technical blogs
        - Video tutorials

        ## Best Coding Practices
        - Code style guidelines
        - Testing practices
        - Documentation standards
        - Version control workflow
        
        ## Advanced Topics
        - Design patterns
        - Architecture concepts
        - Performance optimization
        - Security considerations
        """
        return self.generate_response(prompt)

    def explain_concept(self, concept, language, depth="intermediate"):
        if not self.validate_programming_topic(concept):
            return "Please provide a programming-related concept for explanation."
            
        prompt = f"""
        Explain the following programming concept in {language} at {depth} level:
        {concept}
        
        Structure the explanation as follows:

        1. Technical Definition
        2. Syntax and Usage
        3. Code Examples with Best Practices
        4. Common Programming Pitfalls
        5. Performance Considerations
        6. Real-world Applications
        7. Advanced Implementation Details
        8. Testing Approaches
        9. Security Considerations (if applicable)
        10. Related Design Patterns or Concepts

        Include clear, well-commented code examples in {language}.
        Focus on practical implementation and industry best practices.
        """
        return self.generate_response(prompt)
    
    def generate_quiz(self, topic, difficulty="medium"):
        if not self.validate_programming_topic(topic):
            return "Please provide a programming-related topic for the quiz."
            
        prompt = f"""
        Create a programming quiz about {topic} at {difficulty} difficulty level.
        Generate 5 technical multiple-choice questions focusing on:
        1. Code understanding
        2. Debugging
        3. Best practices
        4. Performance optimization
        5. Common programming pitfalls
    
        Format as JSON with the following structure:
        {{
             "questions": [
                {{
                    "question": "...",
                    "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
                    "correct_answer": "A",
                    "explanation": "..."
                }}
            ]
        }}

        Include actual code snippets and focus on practical programming scenarios.
        """
        return self.generate_response(prompt)

assistant = ProgrammingLearningAssistant()

@app.route('/')
def home():
    return render_template('landingpage.html')

@app.route('/index')
def content_page():
    return render_template('index.html')

@app.route('/api/study-plan', methods=['POST'])
def create_study_plan():
    data = request.json
    plan = assistant.create_study_plan(
        data['topic'],
        data['current_level'],
        data['goal'],
        data['timeframe']
    )
    return jsonify({'plan': plan})

@app.route('/api/explain', methods=['POST'])
def explain_concept():
    data = request.json
    explanation = assistant.explain_concept(
        data['concept'],
        data['language'],
        data.get('depth', 'intermediate')
    )
    return jsonify({'explanation': explanation})

@app.route('/api/quiz', methods=['POST'])
def generate_quiz():
    data = request.json
    quiz = assistant.generate_quiz(
        data['topic'],
        data.get('difficulty', 'medium')
    )
    return jsonify({'quiz': quiz})

if __name__ == '__main__':
    app.run(debug=True)