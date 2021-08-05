import streamlit as st
import pandas as pd
import base64
from pathlib import Path
from PIL import Image
import plotly.express as px
from io import BytesIO



st.set_page_config(layout="wide")

# Page layout (continued)
## Divide page to 3 columns (col1 = sidebar, col2 and col3 = )
col1 = st.sidebar
col2, col3 = st.beta_columns(2)


directory = Path("c:/RégiGép/Turn up the workin' !!!!!!!/#MODELS/###GA MODELS/#REPLENISHMENT/ReplModel_2021/Others/Repl_model_streamlit/Github_repo_Repl_model/")


# Image - Opening
image = Image.open(directory / 'repl.png')
col2.image(image, width=500)


col2.title('Replenishement Model')

col2.markdown("""
This app performs simple webscraping of Replenishement Model data!
* **Departments:** Grocery, GM, Prepacked Dairy, Produce
* **Python libraries:** base64, pandas, streamlit

""")




# Data - opening


@st.cache
def get_data():

    df = pd.read_excel(directory / "OPB_DEP_Q3.xlsx")  
    df = df[df.Country != 'PL']
    return df

df = get_data()


# Sidebar - Country selection

sorted_unique_country = sorted(df.Country.unique())
selected_country = col1.multiselect('Country', sorted_unique_country, sorted_unique_country)

# Sidebar - Format selection
sorted_unique_format = df['Format'].loc[df['Country'].isin(selected_country)].unique()
selected_format = col1.multiselect('Format', sorted_unique_format, sorted_unique_format)

# Sidebar - Store selection
sorted_unique_store = df.Store.loc[(df.Country.isin(selected_country)) & (df.Format.isin(selected_format))].unique()

# select all
container = col1.beta_container()
all = col1.checkbox("Select all Stores")
 
if all:
    selected_store = col1.multiselect("Store",
      sorted_unique_store,sorted_unique_store)
else:
    selected_store =  col1.multiselect("Store",
    sorted_unique_store)


# Sidebar - Division selection
sorted_unique_division = df['Division'].loc[df['Country'].isin(selected_country)].unique()
selected_division = col1.multiselect('Division', sorted_unique_division, sorted_unique_division)

# Sidebar - Dep selection
sorted_unique_dep = df['Dep'].loc[df['Division'].isin(selected_division)].unique()
selected_dep = col1.multiselect('Department', sorted_unique_dep, sorted_unique_dep)

# Filtering data
df_selected_data = df[(df.Country.isin(selected_country)) & (df.Store.isin(selected_store)) & (df.Format.isin(selected_format)) & (df.Division.isin(selected_division)) & (df.Dep.isin(selected_dep))]



#df_selected_data_str = df_selected_data.applymap(str)

col3.header('Display Model Stats of Selected Data')
col3.write('Data Dimension: ' + str(df_selected_data.shape[0]) + ' rows and ' + str(df_selected_data.shape[1]) + ' columns')
col3.dataframe(df_selected_data.style.format({'Variable Hours': '{:.2f}', 'Fix Hours': '{:.2f}', 'Yearly GBP': '{:.2f}','Total Hours': '{:.2f}', 'Additional_Hours': '{:.2f}'}))

if len(selected_store) > 0:
# --- PLOT PIE CHART
    pie_chart = px.pie(df_selected_data,
                title=f' <b>Division Breakdown</b>',
                values='Total Hours',
                names='Division')

    col3.plotly_chart(pie_chart)

    grouped_df = df_selected_data.groupby(['Division','Dep']).sum()['Total Hours'].round(1).reset_index()

    # --- PLOT BAR CHART
    bar_chart = px.bar(grouped_df,
                   x='Dep',
                   y='Total Hours',
                   text= 'Total Hours',
                   hover_data={'Total Hours':':.1f'},
                   color = 'Division',
                   color_continuous_scale=['red', 'yellow', 'green'],
                   template= 'plotly_white',
                   title = f' <b>Departments by Divisions</b>'
                   )
    col3.plotly_chart(bar_chart)


# Download Repl model stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index = False)
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download xlsx file</a>' # decode b'abc' => abc

df = ... # your dataframe
col1.markdown(get_table_download_link(df_selected_data), unsafe_allow_html=True)


# # practice
# chart_data = pd.DataFrame(
#       np.random.randn(20, 3),
#       columns=['a', 'b', 'c'])

# st.line_chart(chart_data)


# map_data = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#     columns=['lat', 'lon'])

# st.map(map_data)


# if st.checkbox('Show dataframe'):
#     chart_data = pd.DataFrame(
#         np.random.randn(20, 3),
#         columns=['a', 'b', 'c'])

#     chart_data


# option = st.selectbox(
#     'Which number do you like best?',
#       df['Store'])

# 'You selected: ', option




# left_column, right_column = st.beta_columns(2)
# pressed = left_column.button('Press me?')
# if pressed:
#     right_column.write("Woohoo!")

# expander = st.beta_expander("FAQ")
# expander.write("Here you could put in some really, really long explanations...")



# import time


# 'Starting a long computation...'

# # Add a placeholder
# latest_iteration = col1.empty()
# bar = col4.progress(0)

# for i in range(100):
#   # Update the progress bar with each iteration.
#   latest_iteration.text(f'Iteration {i+1}')
#   bar.progress(i + 1)
#   time.sleep(0.1)

# '...and now we\'re done!'





