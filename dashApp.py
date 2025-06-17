from dash import Dash, html, dash_table, Input, Output,dcc
import dash_bootstrap_components as dbc
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


#Data preprocessing 
df = pd.read_csv('HIV_ANC_Testing_2024.csv')
df_copied = df.copy()
indicator_mapping = {'Number of pregnant women presenting at ANC who were tested for HIV or already knew their HIV positive status':'Number of Pregnant Women tested for HIV at ANC',
                     'Per cent of pregnant women presenting at ANC who were tested for HIV or already knew their HIV positive status':'Percent of Pregnant Women tested for HIV at ANC'
                     }

def clean_numeric_column(value):
    if isinstance(value,str):
        if "<1" in value or value == ".":
            return 0.0
        elif ">95" in value:
            return np.random.choice([96.0, 97.0, 98.0, 99.0])
        value = value.replace(',', '')  # Remove commas
    return pd.to_numeric(value, errors='coerce') 

df_copied['Value'] = df_copied['Value'].apply(clean_numeric_column)
df_copied['Indicator'] = df_copied['Indicator'].map(indicator_mapping)

df_copied.columns = df_copied.columns.map(lambda x : x.replace('/','_').replace(' ','_'))


#  Adding column continent
# Countries by continent
africa = {'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cameroon','Congo',
          'Central African Republic', 'Chad', 'Comoros', "Côte d'Ivoire", 'Democratic Republic of the Congo',
          'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia',
          'Ghana', 'Guinea', 'Guinea-Bissau', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi',
          'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda',
          'Sao Tome and Principe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa',
          'South Sudan', 'Sudan', 'Togo', 'Tunisia', 'Uganda', 'United Republic of Tanzania', 'Zambia', 'Zimbabwe'}

asia = {'Afghanistan', 'Armenia', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Bhutan', 'Brunei Darussalam', 'Cambodia',
        'China', 'Cyprus', 'Georgia', 'India', 'Indonesia', 'Iran (Islamic Republic of)', 'Iraq', 'Israel', 'Japan',
        'Jordan', 'Kazakhstan', 'Kuwait','Kyrgyzstan', "Lao People's Democratic Republic", 'Lebanon', 'Malaysia', 'Maldives',
        'Mongolia', 'Myanmar', 'Nepal', 'Oman', 'Pakistan', 'Philippines', 'Qatar', 'Republic of Korea', 'Saudi Arabia',
        'Singapore', 'Sri Lanka', 'Syrian Arab Republic', 'Tajikistan', 'Thailand', 'Timor-Leste', 'Turkey',
        'United Arab Emirates', 'Uzbekistan', 'Viet Nam', 'Yemen'}

europe = {'Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia',
          'Czechia', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland',
          'Italy', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Monaco', 'Montenegro', 'Netherlands',
          'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Republic of Moldova', 'Romania', 'Russian Federation',
          'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom'}

north_america = {'Antigua and Barbuda', 'Bahamas', 'Barbados', 'Belize', 'Canada', 'Costa Rica', 'Cuba', 'Dominica',
                 'Dominican Republic', 'El Salvador', 'Grenada', 'Guatemala', 'Haiti', 'Honduras', 'Jamaica', 'Mexico',
                 'Nicaragua', 'Panama', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines',
                 'Trinidad and Tobago', 'United States'}

south_america = {'Argentina', 'Bolivia (Plurinational State of)', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana',
                 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela (Bolivarian Republic of)'}

oceania = {'Australia','Cook Islands', 'Fiji', 'Kiribati', 'Marshall Islands', 'Micronesia (Federated States of)', 'Nauru', 'New Zealand',
           'Palau', 'Papua New Guinea', 'Samoa', 'Solomon Islands', 'Tonga', 'Tuvalu', 'Vanuatu'}


# Dictionary mapping
country_to_continent = {country: 'Africa' for country in africa}
country_to_continent.update({country: 'Asia' for country in asia})
country_to_continent.update({country: 'Europe' for country in europe})
country_to_continent.update({country: 'North America' for country in north_america})
country_to_continent.update({country: 'South America' for country in south_america})
country_to_continent.update({country: 'Oceania' for country in oceania})

# Mapping
df_copied['Continent'] = df_copied['Country_Region'].map(country_to_continent).fillna('Unknown')
# df_copied.to_excel('df_copied.xlsx', index=False)

# print(df_copied[df_copied['Continent']=='Unknown'].Country_Region)


app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
heading = html.Div(
    dcc.Markdown(children='# DashApp - HIV ANC Testing'),
    style={'textAlign': 'center', 'marginTop': '5px', 'marginBottom':'10px'}
)

dataTable = dash_table.DataTable(data=df_copied.to_dict('records'), 
                                 page_size=10)
country_dwn = dcc.Dropdown(df_copied.Country_Region.unique(),
                           placeholder='Select Country',
                           id='country_dwn',
                           searchable=True,
                           value='Angola'
                           )
kpi_dwn = dcc.Dropdown(
    df_copied.Indicator.unique(),
    placeholder='Select KPI',
    id='kpi_dwn',
    value=df_copied.Indicator.unique()[0]
)
country_display = html.Div(id='country_display')
brk = html.Br()
country_bar_graph = dcc.Graph(id='country_bar_graph')
country_line_graph = dcc.Graph(id='country_line_graph')

# Components for the second part - comparison

comp_line_graph = dcc.Graph(id='comp_line_graph')
country_dwn_multi = dcc.Dropdown(df_copied.Country_Region.unique(),
                           placeholder='Select Country',
                           id='country_dwn_multi',
                           multi=True,
                           searchable=True,
                           value=['Angola','Afghanistan']
                           )
kpi_dwn_comp = dcc.Dropdown(
    df_copied.Indicator.unique(),
    placeholder='Select KPI',
    id='kpi_dwn_comp',
    value=df_copied.Indicator.unique()[0]
)
sub_heading_1 = html.Div(
    dcc.Markdown(children='### HIV ANC Testing Comparison Between Countries'),
    style={'textAlign': 'center', 'marginTop': '5px', 'marginBottom':'10px'}
)

# Components for the Third Part - Continent based analysis

continent_bar_graph = dcc.Graph(id='continent_bar_graph')
continent_pie_graph = dcc.Graph(id='continent_pie_graph')
year_pie = dcc.Dropdown(
    df_copied.Year.unique(),
    placeholder='Select Year',
    id='year_pie'
)

sub_heading_2 = html.Div(
    dcc.Markdown(children='### HIV ANC Testing - Continent'),
    style={'textAlign': 'center', 'marginTop': '5px', 'marginBottom':'10px'}
)

year_slider = dcc.Slider(
    id='year-slider',
    min=df_copied['Year'].min(),   # Minimum year
    max=df_copied['Year'].max(),   # Maximum year
    step=1,
    value=df_copied['Year'].min(), # Initial value
    marks={str(year): str(year) for year in df_copied['Year'].unique()},
    tooltip={"placement": "bottom", "always_visible": True}
)

choropleth_map = dcc.Graph(id='choropleth_map')

#Container - Main component
app.layout= dbc.Container([heading,
                           dbc.Row(
                               [
                                   dbc.Col(country_dwn, width=4),
                                   dbc.Col(kpi_dwn, width=6)
                               ]
                           ),
                           dbc.Col(country_line_graph, width=8),
                        #   dbc.Row(
                        #       [
                        #            dbc.Col(country_bar_graph, width=6),
                        #            dbc.Col(country_line_graph, width=6)
                        #       ]
                        #   ),
                          brk,
                          sub_heading_1,
                          brk,
                          dbc.Row([
                              dbc.Col(country_dwn_multi,width=4),
                              dbc.Col(kpi_dwn_comp,width=6)
                          ]),
                          comp_line_graph,
                          brk,
                          sub_heading_2,
                          brk,
                          year_slider,
                          dbc.Row([
                             dbc.Col(continent_bar_graph,width=6),
                             dbc.Col(continent_pie_graph,width=6)
                          ]),
                          choropleth_map
                           ])

@app.callback(
    # Output(country_bar_graph, 'figure'),
    Output(country_line_graph,'figure'),
    Input(country_dwn, 'value'),
    Input(kpi_dwn,'value')
)
def update_bar_graph(selected_country,kpi):
    if selected_country is None or kpi is None:
        empty_bar = px.bar(title="Select a country to view data")
        empty_line = px.line(title='Select a country to view data')
        return empty_bar,empty_line
    
    country_df = df_copied[
        (df_copied['Country_Region']==selected_country) &
        (df_copied['Indicator'] == kpi)
        ]
    bar_graph = px.bar(
        country_df, 
        x='Year',
        y='Value',
        title=f'Bar graph - Yearly HIV ANC Testing: {selected_country}'
        )
    
    line_graph = px.line(
        country_df, 
        x='Year',
        y='Value',
        title=f'Line graph - Yearly HIV ANC Testing: {selected_country}',
        markers=True
        )
    return line_graph
    # return bar_graph, line_graph


@app.callback(
    Output(comp_line_graph, 'figure'),
    Input(country_dwn_multi, 'value'),
    Input(kpi_dwn_comp, 'value')
)
def update_comparison(selected_country,kpi):
    if selected_country is None or kpi is None:
        empty_line = px.line(title='Select a country to view data')
        return empty_line
    
    country_df = df_copied[
        (df_copied['Country_Region'].isin(selected_country)) &
        (df_copied['Indicator'] == kpi)
        ]
    
    line_graph = px.line(
        country_df, 
        x='Year',
        y='Value',
        color='Country_Region',
        title=f'HIV ANC Testing coverage between : {selected_country}',
        markers=True
        )
    return line_graph

# Pie graph - for continent
@app.callback(
    Output(continent_bar_graph, 'figure'),
    Output(continent_pie_graph, 'figure'),
    Output(choropleth_map, 'figure'),
    Input(year_slider,'value')
)
def update_bar(year):
    if year is None:
        empty_bar = px.bar(title='Select year to view data')
        empty_pie = px.pie(title='Select year to view data')
        empty_choropleth = px.choropleth(title='Select year to view HIV test distribution by continent')
        return empty_bar,empty_pie,empty_choropleth
    
    filtered_df = df_copied[(df_copied['Indicator']=='Number of Pregnant Women tested for HIV at ANC') & (df_copied['Year'] == year)]
    continent_data = filtered_df.groupby('Continent')['Value'].sum().reset_index()
    
    bar_graph = px.bar(continent_data, x='Continent', y='Value',
                 title=f'HIV Tests Conducted in {year}',
                 color='Continent',
                 labels={'Continent': 'Continent', 'Value': 'Number of Tests'}
                 )
    pie_graph = px.pie(
        continent_data, 
        names='Continent', 
        values='Value', 
        color='Continent',
        title=f'HIV Tests Proportions in {year}',
        labels={'Continent': 'Continent', 'Value': 'Number of Tests'}
    )

     # Map continents back to countries for visualization
    country_continent_data = df_copied[['Country_Region', 'Continent']].drop_duplicates()
    continent_data = pd.merge(country_continent_data, continent_data, on='Continent')
    
    # Create the choropleth map
    map = px.choropleth(
        continent_data,
        locations='Country_Region',
        locationmode='country names',
        color='Value',
        hover_name='Continent',
        # color='Continent',
        # hover_name='Value',
        color_continuous_scale='Blues', #Viridis, Plasma
        title=f'HIV Tests Conducted in {year} by Continent'
    )

    return bar_graph, pie_graph,map

if __name__ == '__main__':
    app.run(debug=True)