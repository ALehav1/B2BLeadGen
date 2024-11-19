# B2B Lead Finder

An intelligent B2B lead generation system that uses AI agents to analyze products and identify potential customers based on web and social media signals.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a .env file with your API keys:
```
OPENAI_API_KEY=your_key_here
```

## Project Structure

- `agents/`: Contains specialized AI agents
  - `product_analyzer.py`: Analyzes product websites and marketing materials
  - `company_researcher.py`: Researches companies and their needs
  - `lead_qualifier.py`: Qualifies and ranks potential leads

- `tools/`: Contains utility functions
  - `web_scraper.py`: Web scraping utilities
  - `data_processor.py`: Data processing and analysis tools

- `main.py`: Main application entry point

## Usage

Run the application:
```bash
python main.py
```
