# B2B Lead Finder

An AI-powered B2B lead generation platform that helps you identify and qualify potential customers based on your product description. The system analyzes target markets, identifies matching companies, and generates personalized outreach emails.

## Features

- 🎯 Smart Market Analysis
- 🔍 AI-Powered Company Matching
- 📊 Real-time Progress Tracking
- ✉️ Personalized Email Generation
- 💡 Custom Value Propositions

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/ALehav1/B2BLeadGen.git
cd B2BLeadGen
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```bash
touch .env
```

5. Add your OpenAI API key to the `.env` file:
```
OPENAI_API_KEY=your_key_here
```

## Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your default web browser. Follow these steps:

1. Enter your product description and company name
2. Review and edit the AI-generated market analysis
3. Set optional search preferences (location, company types)
4. View matched companies with:
   - Match reasons
   - Recent signals
   - Value propositions
   - Generated outreach emails

## Project Structure

- `app.py`: Streamlit web interface
- `main.py`: Core business logic and AI integration
- `agents/`: Specialized AI agents for different tasks
- `tools/`: Utility functions and helpers
- `requirements.txt`: Project dependencies
- `.env`: API key configuration (create this yourself)

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for AI and research capabilities

## Security Note

- Never commit your `.env` file
- Keep your API keys secure
- The `.gitignore` file is configured to protect sensitive information

## Contributing

Feel free to:
- Open issues
- Submit pull requests
- Suggest improvements

## License

MIT License - feel free to use and modify as needed!
