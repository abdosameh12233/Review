import psycopg2
import re
import streamlit as st
from urllib.parse import quote_plus
password = quote_plus("P@$$W0RdAs10109090")
DATABASE_URL = f'postgresql://postgres.nsrgeouvqnsmntgjsgff:{password}@aws-1-eu-central-1.pooler.supabase.com:6543/postgres'
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
cursor.execute('select product_id,product_name,review_id from product_reviews')
products=cursor.fetchall()
products_existing = [row[1] for row in products]
product_map = {row[1]: row[0] for row in products}
review_id_num = [int(re.sub(r'[^0-9]', '', raw[2])) for raw in products]
cursor.execute('select product_name,product_category from product_reviews')
cats = cursor.fetchall()
cats_map = {raw[0]:raw[1] for raw in cats}
cursor.execute('select product_name,product_subcategory from product_reviews')
subcats = cursor.fetchall()
subcats_map = {raw[0]:raw[1] for raw in subcats}
product_name = st.selectbox('Enter product name',options= ['new product'] + products_existing)
review_text = st.text_input('Enter your review')
submit = st.button('submit')
if submit:
    if product_name != 'new product':
        review_id = f'REV-{max(review_id_num) + 1}'
        product_id = product_map[product_name]
        product_cat = cats_map[product_name]
        product_subcat = subcats_map[product_name]
        cursor.execute('insert into product_reviews values(%s,%s,%s,%s,%s,%s)',(review_id,product_id,product_name,product_cat,product_subcat,review_text))
    conn.commit()
    st.success('review added successfully')
