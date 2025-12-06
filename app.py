from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Google AI Studio
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# Sample coding prompts (you can expand this or load from a database)
CODING_PROMPTS = {
    'default': {
        'title': 'Two Sum Problem',
        'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice.',
        'examples': 'Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: Because nums[0] + nums[1] == 9, we return [0, 1].',
        'constraints': [
            '2 <= nums.length <= 10^4',
            '-10^9 <= nums[i] <= 10^9',
            '-10^9 <= target <= 10^9',
            'Only one valid answer exists'
        ]
    }
}

@app.route('/')
def index():
    return render_template('index.html')

# Placeholder routes so your buttons work
@app.route('/register')
def register():
    return "Registration Page - Coming Soon!"

@app.route('/login')
def login():
    return "Login Page - Coming Soon!"

@app.route('/coding-prompt')
def coding_prompt():
    """Display the coding prompt page"""
    prompt_data = CODING_PROMPTS['default']
    return render_template('coding_prompt.html', 
                         prompt_title=prompt_data['title'],
                         prompt_description=prompt_data['description'],
                         prompt_examples=prompt_data.get('examples'),
                         prompt_constraints=prompt_data.get('constraints'))

@app.route('/submit-code', methods=['POST'])
def submit_code():
    """Handle code submission and grade it using Google AI Studio"""
    
    # Get form data
    code = request.form.get('code', '')
    language = request.form.get('language', 'python')
    prompt_title = request.form.get('prompt_title', '')
    prompt_description = request.form.get('prompt_description', '')
    
    # Validate inputs
    if not code.strip():
        return render_template('grading_result.html',
                             score='N/A',
                             score_class='score-poor',
                             score_category='Poor',
                             feedback='<p class="text-danger">No code was submitted. Please write some code before submitting.</p>',
                             code='',
                             language=language,
                             prompt_title=prompt_title,
                             prompt_description=prompt_description)
    
    # Check if API key is configured
    if not GOOGLE_API_KEY:
        return render_template('grading_result.html',
                             score='N/A',
                             score_class='score-poor',
                             score_category='Error',
                             feedback='<p class="text-danger"><strong>Configuration Error:</strong> Google API key is not configured. Please add your GOOGLE_API_KEY to the .env file.</p>',
                             code=code,
                             language=language,
                             prompt_title=prompt_title,
                             prompt_description=prompt_description)
    
    try:
        # Grade the code using Google AI Studio
        feedback, score = grade_code_with_ai(code, language, prompt_title, prompt_description)
        
        # Determine score category and styling
        score_category, score_class = get_score_category(score)
        
        # Format feedback for HTML display
        formatted_feedback = format_feedback_html(feedback)
        
        return render_template('grading_result.html',
                             score=score,
                             score_class=score_class,
                             score_category=score_category,
                             feedback=formatted_feedback,
                             code=code,
                             language=language,
                             prompt_title=prompt_title,
                             prompt_description=prompt_description)
    
    except Exception as e:
        # Handle any errors during grading
        error_message = f'<p class="text-danger"><strong>Error during grading:</strong> {str(e)}</p><p>Please try again or contact support if the issue persists.</p>'
        return render_template('grading_result.html',
                             score='Error',
                             score_class='score-poor',
                             score_category='Error',
                             feedback=error_message,
                             code=code,
                             language=language,
                             prompt_title=prompt_title,
                             prompt_description=prompt_description)

def grade_code_with_ai(code, language, prompt_title, prompt_description):
    """Use Google AI Studio to grade the submitted code"""
    
    # Create the grading prompt
    grading_prompt = f"""You are an expert programming instructor grading a student's code submission.

Problem: {prompt_title}
Description: {prompt_description}

Programming Language: {language}

Student's Code:
```{language}
{code}
```

Please evaluate this code and provide:
1. A numerical score from 0-100
2. Detailed feedback covering:
   - Correctness: Does the solution solve the problem correctly?
   - Code Quality: Is the code clean, readable, and well-structured?
   - Efficiency: Is the solution efficient in terms of time and space complexity?
   - Best Practices: Does it follow language-specific best practices?
   - Suggestions: What improvements could be made?

Format your response as:
SCORE: [number from 0-100]
FEEDBACK:
[Your detailed feedback here, using bullet points and paragraphs]
"""

    # Use Gemini model to generate feedback
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(grading_prompt)
    
    # Parse the response
    response_text = response.text
    
    # Extract score
    score_match = re.search(r'SCORE:\s*(\d+)', response_text)
    score = score_match.group(1) if score_match else '0'
    
    # Extract feedback
    feedback_match = re.search(r'FEEDBACK:\s*(.+)', response_text, re.DOTALL)
    feedback = feedback_match.group(1).strip() if feedback_match else response_text
    
    return feedback, score

def get_score_category(score):
    """Determine the category and CSS class based on score"""
    try:
        score_num = int(score)
        if score_num >= 90:
            return 'Excellent', 'score-excellent'
        elif score_num >= 70:
            return 'Good', 'score-good'
        elif score_num >= 50:
            return 'Needs Work', 'score-needs-work'
        else:
            return 'Poor', 'score-poor'
    except:
        return 'Unknown', 'score-poor'

def format_feedback_html(feedback):
    """Format the feedback text into HTML with proper styling"""
    # Convert markdown-style formatting to HTML
    feedback = feedback.replace('**', '<strong>').replace('**', '</strong>')
    
    # Convert bullet points
    lines = feedback.split('\n')
    formatted_lines = []
    in_list = False
    
    for line in lines:
        line = line.strip()
        if line.startswith('- ') or line.startswith('* '):
            if not in_list:
                formatted_lines.append('<ul>')
                in_list = True
            formatted_lines.append(f'<li>{line[2:]}</li>')
        else:
            if in_list:
                formatted_lines.append('</ul>')
                in_list = False
            if line:
                formatted_lines.append(f'<p>{line}</p>')
    
    if in_list:
        formatted_lines.append('</ul>')
    
    return '\n'.join(formatted_lines)

if __name__ == '__main__':
    # port 5000 is the default, but Render might set a PORT env var
    # This block is mainly for local testing
    app.run(debug=True)
