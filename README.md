# AI Ticket Evaluator

This project evaluates customer support ticket replies using the OpenAI GPT-4 API.


## Prerequisites

- [Python](https://www.python.org/downloads/release/python-31211/) v. 3.12+ installed
- `pip` installed
- [OpenAI API Key](https://platform.openai.com/account/api-keys)
- (Optional) [Docker](https://www.docker.com/get-started) installed if you want to run in a container

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd <repository-folder>
```

2. Create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create a .env file in the project root with your API key:
```bash
OPENAI_API_KEY="your_api_key_here"
```


## Usage

Run the main script to evaluate tickets and generate the output CSV:

```bash
python main.py
```

· Input file should be at data/tickets.csv

· Output file with evaluations will be saved as data/tickets_evaluated.csv

## Docker Usage (Optional)
If you prefer not to install dependencies locally, you can use Docker:

1. Build the Docker image:

```bash
docker build -t ai-evaluator .
```
2. Run the container passing your API key as an environment variable:

```bash
docker run --rm -v "$(pwd)/data:/app/data" -e OPENAI_API_KEY="your_openai_api_key_here" ai-evaluator
```

- This command maps your local data folder to the container's /app/data folder.

- The input file tickets.csv must be inside the local data folder.

- The output file tickets_evaluated.csv will be saved in the same data folder locally.