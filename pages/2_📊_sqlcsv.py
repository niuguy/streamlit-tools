import streamlit as st
import pandas as pd
import sqlalchemy
import os
import dotenv

dotenv.load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def sql_to_df(sql, db_credentials):
    # Create engine connection
    engine = sqlalchemy.create_engine(db_credentials)

    # Execute SQL query
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text(sql))

    # Fetch all results
    data = result.fetchall()
    columns = result.keys()

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=columns)

    return df


st.title("Run SQL and download CSV")

query_sql = st.text_input("Sql")


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


if st.button("Run"):
    df = sql_to_df(query_sql, DATABASE_URL)
    st.write(df)
    if df.size > 0:
        csv = convert_df(df)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name="large_df.csv",
            mime="text/csv",
        )
