import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv("Accidents/Data/us_accidents_.csv")
df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce')
df['End_Time'] = pd.to_datetime(df['End_Time'], errors='coerce')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Accidents Dashboard"

weekday_options = ['All'] + df['Accident Day of Week'].unique().tolist()
time_of_day_options = ['All'] + df['Time of Day'].unique().tolist()
accident_duration_options = ['All'] + df['Duration_Bin'].unique().tolist()
temperature_options = ['All'] + df['Temperature_Ranges'].unique().tolist()
precip_options = ['All'] + df['Precipitation_Ranges'].unique().tolist()
wind_options = ['All'] + df['Wind_Speed_Bin'].unique().tolist()
state_options=['All'] + df['State'].unique().tolist()
# Sidebar filters
sidebar = dbc.Col([
    html.H5("Filters", className="text-white mt-3 mb-4", style={"fontFamily": "Segoe UI, sans-serif"}),
    html.Hr(style={"borderColor": "#777"}),

    html.Label('State', className="text-light"),
    dcc.Dropdown(
        id='state',
        options=[{'label': i, 'value': i} for i in state_options],
        value='All',
        clearable=False,
        className="mb-3"
    ),

    html.Label('Day of the Week', className="text-light"),
    dcc.Dropdown(
        id='day-of-week',
        options=[{'label': i, 'value': i} for i in weekday_options],
        value='All',
        clearable=False,
        className="mb-3"
    ),

    html.Label('Time of Day', className="text-light"),
    dcc.Dropdown(
        id='time-of-day',
        options=[{'label': i, 'value': i} for i in time_of_day_options],
        value='All',
        clearable=False,
        className="mb-3"
    ),

    html.Label('Accident Duration', className="text-light"),
    dcc.Dropdown(
        id='accident-duration',
        options=[{'label': i, 'value': i} for i in accident_duration_options],
        value='All',
        clearable=False,
        className="mb-3"
    ),

    html.Label('Temperature Range', className="text-light"),
    dcc.Dropdown(
        id='temperature',
        options=[{'label': i, 'value': i} for i in temperature_options],
        value='All',
        clearable=False,
        className="mb-3"
    ),

    html.Label('Precipitation Range', className="text-light"),
    dcc.Dropdown(
        id='precip',
        options=[{'label': i, 'value': i} for i in precip_options],
        value='All',
        clearable=False,
        className="mb-3"
    ),

    html.Label('Wind Speed', className="text-light"),
    dcc.Dropdown(
        id='wind',
        options=[{'label': i, 'value': i} for i in wind_options],
        value='All',
        clearable=False,
        className="mb-3"
    ),

    html.Label("Is Weekend", className="text-light"),
    dbc.RadioItems(
        id='is-weekend',
        options=[
            {'label': 'All', 'value': 'All'},
            {'label': 'Yes', 'value': True},
            {'label': 'No', 'value': False}
        ],
        value='All',
        inline=True,
        className='text-light mb-3'
    ),

    html.Label("Is Rush Hour", className="text-light"),
    dbc.RadioItems(
        id='is-rush-hour',
        options=[
            {'label': 'All', 'value': 'All'},
            {'label': 'Yes', 'value': True},
            {'label': 'No', 'value': False}
        ],
        value='All',
        inline=True,
        className='text-light mb-3'
    ),

    html.Label("Is Severe Accident", className="text-light"),
    dbc.RadioItems(
        id='is-severe',
        options=[
            {'label': 'All', 'value': 'All'},
            {'label': 'Yes', 'value': True},
            {'label': 'No', 'value': False}
        ],
        value='All',
        inline=True,
        className='text-light mb-3'
    ),

    html.Label('Number of Traffic Obstacles', className='text-light'),
    dcc.RangeSlider(
        id='traffic-obstacles',
        min=df['Number_of_Traffic_Obstacles'].min(),
        max=df['Number_of_Traffic_Obstacles'].max(),
        step=1,
        value=[df['Number_of_Traffic_Obstacles'].min(), df['Number_of_Traffic_Obstacles'].max()],
        marks={i: str(i) for i in range(df['Number_of_Traffic_Obstacles'].min(), df['Number_of_Traffic_Obstacles'].max() + 1)},
        tooltip={"placement": "bottom", "always_visible": False},
        className="mb-4"
    )
], width=2, style={
    'backgroundColor': "#3F648A",
    'height': '100vh',
    'position': 'sticky',
    'top': 0,
    'padding': '20px',
    'overflowY': 'auto',  
    'fontFamily': 'Segoe UI, sans-serif'
})

# Main content
main_content = dbc.Col([
    html.H3("📊 Accidents Dashboard",
            className="text-center mt-3 mb-3",
            style={"fontFamily": "Segoe UI, Roboto, Helvetica, sans-serif",
                   "fontWeight": "bold",
                   "fontSize": "28px"}),

    dbc.Row([
        dbc.Col(dbc.Card([dbc.CardHeader("Average Accidents per Day", className="fw-bold"),
                          dbc.CardBody(html.H5(id="avg-accidents", className=" fw-bold"))]), width=3),
        dbc.Col(dbc.Card([dbc.CardHeader("Total Accidents", className="fw-bold"),
                          dbc.CardBody(html.H5(id="total-accidents", className=" fw-bold"))]), width=3),
        dbc.Col(dbc.Card([dbc.CardHeader("Top State", className="fw-bold"),
                          dbc.CardBody(html.H5(id="top-state", className=" fw-bold"))]), width=3),
        dbc.Col(dbc.Card([dbc.CardHeader("Peak Accident Hour", className="fw-bold"),
                          dbc.CardBody(html.H5(id="peak-hour", className=" fw-bold"))]), width=3),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id="graph-1", figure={}, style={"height": "100%", "width": "100%"}), style={"height": "400px"}), width=6, className="mb-4"),
        dbc.Col(dbc.Card(dcc.Graph(id="graph-2", figure={}, style={"height": "100%", "width": "100%"}), style={"height": "400px"}), width=6, className="mb-4"),
    ]),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id="graph-3", figure={}, style={"height": "100%", "width": "100%"}), style={"height": "300px"}), width=4, className="mb-4"),
        dbc.Col(dbc.Card(dcc.Graph(id="graph-4", figure={}, style={"height": "100%", "width": "100%"}), style={"height": "300px"}), width=4, className="mb-4"),
        dbc.Col(dbc.Card(dcc.Graph(id="graph-5", figure={}, style={"height": "100%", "width": "100%"}), style={"height": "300px"}), width=4, className="mb-4"),
    ]),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id="graph-6", figure={}, style={"height": "100%", "width": "100%"}), style={"height": "300px"}), width=6, className="mb-4"),
        dbc.Col(dbc.Card(dcc.Graph(id="graph-8", figure={}, style={"height": "100%", "width": "100%"}), style={"height": "300px"}), width=3, className="mb-4"),
        dbc.Col(dbc.Card(dcc.Graph(id="graph-9", figure={}, style={"height": "100%", "width": "100%"}), style={"height": "300px"}), width=3, className="mb-4"),
    ]),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id="graph-10", figure={}, style={"height": "100%", "width": "100%"}), style={"height": "400px"}), width=12, className="mb-4"),
    ])
], width=10)

app.layout = dbc.Container([
    dbc.Row([sidebar, main_content], justify="start")
], fluid=True)

@app.callback(
    Output("avg-accidents", "children"),
    Output("total-accidents", "children"),
    Output("top-state", "children"),
    Output("peak-hour", "children"),
    Output("graph-1", "figure"),
    Output("graph-2", "figure"),
    Output("graph-3", "figure"),
    Output("graph-4", "figure"),
    Output("graph-5", "figure"),
    Output("graph-6", "figure"),
    Output("graph-8", "figure"),
    Output("graph-9", "figure"),
    Output("graph-10", "figure"),
    
    Input("state", "value"),
    Input("day-of-week", "value"),
    Input("time-of-day", "value"),
    Input("accident-duration", "value"),
    Input("temperature", "value"),
    Input("precip", "value"),
    Input("wind", "value"),
    Input("is-weekend", "value"),
    Input("is-rush-hour", "value"),
    Input("is-severe", "value"),
    Input("traffic-obstacles", "value")
)
def update_dashboard(state,day_of_week, time_of_day, accident_duration, temperature,
                     precip, wind, is_weekend, is_rush_hour, is_severe,
                     traffic_obstacles):
    dff = df.copy()
    
    # Filtering
    if  state!= "All":
        dff = dff[dff['State'] == state]
    if day_of_week != 'All':
        dff = dff[dff['Accident Day of Week'] == day_of_week]
    if time_of_day != "All":
        dff = dff[dff['Time of Day'] == time_of_day]
    if accident_duration != "All":
        dff = dff[dff['Duration_Bin'] == accident_duration]
    if temperature != "All":
        dff = dff[dff['Temperature_Ranges'] == temperature]
    if precip != "All":
        dff = dff[dff['Precipitation_Ranges'] == precip]
    if wind != "All":
        dff = dff[dff['Wind_Speed_Bin'] == wind]
    if is_weekend != "All":
        dff = dff[dff['IsWeekend'] == is_weekend]
    if is_rush_hour != "All":
        dff = dff[dff['IsRushHour'] == is_rush_hour]
    if is_severe != "All":
        dff = dff[dff['IsSevere'] == is_severe]
    dff = dff[(dff['Number_of_Traffic_Obstacles'] >= traffic_obstacles[0]) &
              (dff['Number_of_Traffic_Obstacles'] <= traffic_obstacles[1])]
    
    # Data cards
    avg_accidents = round(dff.shape[0] / dff['Start_Time'].dt.date.nunique(), 2) if not dff.empty else 0
    total_accidents = dff.shape[0]
    top_state = dff['State'].mode()[0] if not dff.empty else "N/A"
    peak_hour = dff['Accident_Hour'].mode()[0] if not dff.empty else "N/A"
    
    
    # Figures
    city_counts = dff['City'].value_counts().head(10).reset_index()
    city_counts.columns = ['City', 'Count']

    fig1 = px.bar(
        city_counts,
        x='City',
        y='Count',
        title="Top Cities with Most Accidents",
        labels={'City': 'City', 'Count': 'Number of Accidents'},
        opacity=0.9
    )
    fig1.update_layout(
        xaxis_tickangle=-45,
        yaxis_title="Number of Accidents",
        bargap=0.2
    )



    state_counts = dff['State'].value_counts().reset_index()
    state_counts.columns = ['State', 'Count']
    map_fig = px.choropleth(
        state_counts, locations='State', locationmode="USA-states", color='Count',
        scope="usa", title="Accidents per State"
    )
    map_fig.update_layout(autosize=True, margin=dict(l=10,r=10,t=50,b=10))
    
    fig3=px.pie(dff,names='Time of Day',
                   title='Accidents Per Time of Day')


    day_counts = dff['Accident Day of Week'].value_counts().reset_index()
    day_counts.columns = ['Day', 'Count']
    day_counts = day_counts.sort_values(by='Count', ascending=False)

    fig4 = px.bar(
        day_counts,
        x='Day',
        y='Count',
        title="Accidents per Day of the Week",
        labels={'Day': 'Day of Week', 'Count': 'Number of Accidents'},
        opacity=0.9
    )
    fig4.update_layout(
        xaxis_tickangle=-45,
        yaxis_title="Number of Accidents",
        bargap=0.2
    )
    duration_counts = dff['Duration_Bin'].value_counts().reset_index()
    duration_counts.columns = ['Duration', 'Count']

    fig5 = px.pie(
        duration_counts,
        names='Duration',
        values='Count',
        title='Accident Duration Distribution',
        hole=0.3  
    )
    accidents_per_day = dff.groupby(dff['Start_Time'].dt.date).size().reset_index(name='Count')
    fig6=px.line(accidents_per_day, x='Start_Time', y='Count',
              title='Daily Accident Counts Over Time')
    fig6.update_layout(    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="1W", step="day", stepmode="backward"),
                dict(count=14, label="2W", step="day", stepmode="backward"),
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=2, label="2M", step="month", stepmode="backward"),
                dict(step="all", label='All')  
            ])
        ),
        type="date"
    )
)
    fig8=px.pie(dff, names='Temperature_Ranges', title='Accidents by Temperature')
    
    fig8.update_traces(textinfo='percent+label', textposition='inside')
    fig8.update_layout(
        showlegend=False,
        margin=dict(t=40, b=10,r=20,l=20)
    )
    fig9=px.pie(dff,names='IsRushHour', title='Is a Rush Hour?')
    fig9.update_layout(
        margin=dict(t=40,b=10,r=10,l=10)
    )
    
    
    
    visibility_counts = df['Visibility_Ranges'].value_counts().reset_index()
    visibility_counts.columns = ['Visibility', 'Count']

    visibility_counts = visibility_counts.sort_values(by='Count', ascending=False)

    fig7 = px.bar(
        visibility_counts,
        x='Visibility',
        y='Count',
        title='Accidents by Visibility',
        labels={'Visibility': 'Visibility Range', 'Count': 'Number of Accidents'},
        opacity=0.9
    )

    fig7.update_layout(
        xaxis_tickangle=-45,
        yaxis_title="Number of Accidents",
        bargap=0.2
    )

    return (avg_accidents, total_accidents, top_state, peak_hour,
            fig1, map_fig, fig3, fig4, fig5,
            fig7, fig8, fig9, fig6)

if __name__ == '__main__':
    app.run(debug=True)  