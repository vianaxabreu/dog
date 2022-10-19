import streamlit as st
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



def create_connection(db_file='./db_dog'):
    conn_ = None
    try:
        conn_ = sqlite3.connect(db_file)
    except:
        print('db unavailable')

    return conn_

def get_id_name(conn_, my_vote_='Birita'):
    query = """
        SELECT id
        FROM names
        WHERE name LIKE ?
    """
    db = conn_.cursor()
    db.execute(query,(my_vote,))
    id_name_ = db.fetchone()[0]
    return id_name_

def voting(conn_, my_vote_=4):

    sql_insert = """
        INSERT INTO votes (id_name)
        VALUES (?)
    """
    db = conn_.cursor()
    db.execute(sql_insert, (my_vote_,))
    conn.commit()
    return 'Thank you for voting'

def get_statistics(conn_):

    query = """
        SELECT COUNT(*) as total, names.name
        FROM votes
        JOIN names ON votes.id_name = names.id
        GROUP BY id_name
        ORDER BY total DESC
    """
    #db = conn_.cursor()
    #db.execute(query)
    df_result = pd.read_sql(query,conn_)
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(data=df_result, x="name", y="total")

    return fig


st.set_page_config(
    page_title="I am a dog",  # => Quick reference - Streamlit
    page_icon="🐶",
    #layout="wide",  # wide
    #initial_sidebar_state="auto")
)
names = ['Kojak', 'Baleia', 'Blake', 'Birita', 'Sansa', 'Pickles']
st.markdown("<h1 style='text-align: center; color: black;'>Hi, I am...</h1>",
            unsafe_allow_html=True)
col1, col2 = st.columns(2)

conn = create_connection()
with col1:
    st.image('./dog.png')
with col2:
    my_vote = st.radio('', names)
    if st.button('vote'):
        if conn:
            id_name = get_id_name(conn, my_vote)
            if id_name:
                st.write(voting(conn,id_name))
            else:
                st.write('Error while getting your vote')
        else:
            st.write('data base unavailable')
#with col3:

col1, col2, col3 = st.columns(3)
with col2:
    show_chart = False
    if st.button('result until now'):
        if conn:
            show_chart = True
        #st.dataframe(get_statistics(conn))
        else:
            st.write('result not available')
if show_chart:
    st.pyplot(get_statistics(conn))
