import streamlit as st
import os
import pandas as pd
import sqlalchemy as sa
from dotenv.main import load_dotenv

load_dotenv()
#Set Up my credentials
database_link = os.environ["DATABASE_LINK"]
engine = sa.create_engine(database_link)

#Query my loanbook table
#I have updated my database table with columns which I intend to use only.
df = pd.read_sql_query('select * from loanbook limit 5;',con=engine)
df