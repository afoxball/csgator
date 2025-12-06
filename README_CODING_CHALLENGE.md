# CS Gator - Coding Challenge Setup Guide

## New Feature: AI-Powered Coding Challenges 🚀

Your CS Gator application now includes an AI-powered coding challenge system where users can:
- View coding problems with detailed descriptions
- Write solutions in multiple programming languages (Python, JavaScript, Java, C++, C#)
- Submit their code for AI-powered grading
- Receive detailed feedback and scoring from Google AI Studio

## Setup Instructions

### 1. Install Dependencies

First, install the required Python packages:

```bash
pip install -r requirements.txt
```

### 2. Get Your Google AI Studio API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API Key" or "Create API Key"
4. Copy your API key

### 3. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` and replace `your_google_api_key_here` with your actual API key:
   ```
   GOOGLE_API_KEY=AIzaSyA...your_actual_key_here
   ```

### 4. Run the Application

Start the Flask development server:

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## How It Works

### User Flow:
1. User clicks "Coding Challenge" button on homepage
2. User sees a coding problem with description, examples, and constraints
3. User selects their preferred programming language
4. User writes their solution in the code editor (powered by CodeMirror)
5. User submits their code
6. Google AI Studio (Gemini) analyzes the code
7. User receives:
   - A score (0-100)
   - Detailed feedback on correctness, code quality, efficiency
   - Specific suggestions for improvement

### Grading Categories:
- **90-100**: Excellent ⭐
- **70-89**: Good 👍
- **50-69**: Needs Work 📚
- **0-49**: Keep Practicing 💪

## Customizing Coding Prompts

You can add more coding problems by editing the `CODING_PROMPTS` dictionary in `app.py`:

```python
CODING_PROMPTS = {
    'default': {
        'title': 'Your Problem Title',
        'description': 'Problem description here',
        'examples': 'Input/Output examples',
        'constraints': ['List', 'of', 'constraints']
    },
    'problem2': {
        # Add more problems...
    }
}
```

## File Structure

```
csgator/
├── app.py                          # Main Flask application with AI grading logic
├── requirements.txt                # Python dependencies
├── .env                           # Your API keys (not in git)
├── .env.example                   # Template for environment variables
├── .gitignore                     # Prevents committing sensitive files
├── templates/
│   ├── index.html                 # Homepage with navigation
│   ├── coding_prompt.html         # Coding challenge page with editor
│   └── grading_result.html        # Results page with feedback
└── README_CODING_CHALLENGE.md     # This file
```

## Features

### Code Editor:
- Syntax highlighting for multiple languages
- Line numbers
- Auto-indentation
- Bracket matching
- Theme: Monokai (dark theme)

### AI Grading Evaluates:
- ✅ **Correctness**: Does it solve the problem?
- ✅ **Code Quality**: Is it clean and readable?
- ✅ **Efficiency**: Time and space complexity
- ✅ **Best Practices**: Language-specific conventions
- ✅ **Improvements**: Specific suggestions

## Troubleshooting

### "Configuration Error: Google API key is not configured"
- Make sure you created a `.env` file (not just `.env.example`)
- Verify your API key is correct in the `.env` file
- Restart the Flask application after adding the API key

### "Error during grading"
- Check your internet connection
- Verify your Google API key is valid and has quota remaining
- Check the console/terminal for detailed error messages

### Code editor not loading
- Check browser console for JavaScript errors
- Ensure CodeMirror CDN is accessible
- Try clearing browser cache

## API Usage Notes

- Google AI Studio (Gemini) has free tier limits
- Each code submission counts as one API call
- Monitor your usage at [Google AI Studio](https://makersuite.google.com/)
- For production, consider implementing rate limiting

## Next Steps / Enhancements

Consider adding:
- Multiple coding problems with difficulty levels
- User authentication to track progress
- Leaderboards and achievements
- Test case execution
- Database to store submissions and results
- Admin panel to manage problems
- Time limits for challenges

## Security Notes

- Never commit your `.env` file to version control
- Keep your API key secure
- Consider adding rate limiting for production
- Validate and sanitize all user inputs

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Google AI Studio documentation
3. Check Flask documentation for routing issues

---

Built with ❤️ using Flask, Google AI Studio (Gemini), and Bootstrap
