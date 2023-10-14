# streamlit-tools
A collection of tools built with [Streamlit](https://streamlit.io/).

Tools include:
1. [dbchat](https://github.com/niuguy/streamlit-tools/blob/main/pages/1_%F0%9F%92%A1_dbchat.py) - Chat to your DB

2. [sqlcsv](https://github.com/niuguy/streamlit-tools/blob/main/pages/2_%F0%9F%93%8A_sqlcsv.py) - Download sql query results as csv

3. [images](https://github.com/niuguy/streamlit-tools/blob/main/pages/3_%20%F0%9F%96%BC%EF%B8%8F%20_images.py) - Manage your Cloudflare images


## Installation
Please mind that do not use Python 3.12 as it is not supported by streamlit atm.
Recommand using venv to install the dependencies. Feel free to remove/add dependencies from requirements.txt as needed, e.g. replace pgcopy2 if you need to connect to other database than PostgreSQL

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


