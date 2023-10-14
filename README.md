# streamlit-tools
A collection of tools built with [Streamlit](https://streamlit.io/).

Tools include:
1. dbchat - Chat to your DB

Dependencies: SQLAlchemy, openai, (your db driver e.g. psycopg2)

3. sqlcsv - Download sql query results as csv

4. cloudflareimages - Manage your Cloudflare images


## Installation
Please do not use Python 3.12 as it is not supported by streamlit yet.
Recommand using venv to install the dependencies.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Rename '.env.example' to '.env' and fill in the required information.


## Usage

```bash
streamlit run index.py
```


