import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

# Dataset Processing
df = pd.read_csv('udemy_courses.csv')

# Filters options
subjects = df['subject'].unique()
dificulty = df['level'].unique()
payment = df['is_paid'].unique()

df['is_paid'] = df['is_paid'].astype('str')
subject_options = [{'label': t, 'value': t} for t in subjects] + [{'label': 'All', 'value':'all'}]
dificulty_level = [{'label': t, 'value': t} for t in dificulty] + [{'label': 'All', 'value':'all'}]
paid_option = [{'label': str(t).replace("True", "Paid").replace("False", "Free"), 'value': str(t)} for t in payment] + [{'label': 'All', 'value':'all'}]

# Building our Graphs

# Indicadores
totalCourses = df['course_id'].count()
maxPrice = df['price'].max()
numLectures = df['num_lectures'].sum()
totalHours = round(df['content_duration'].sum())



# The App itself
app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(children=[
    html.Div(className="app_banner", children=[
        html.Img(src=app.get_asset_url('udemy.png'), style={'height': '10%', 'width': '10%', 'margin-left': '170px'}),
    ]),
    html.Div(className="grid", style={'margin-top': '50px'}, children=[
        html.Div(className="filters dd-styles", children=[
            dcc.Dropdown(
                id='subjectsDrop',
                options=subject_options,
                value='all'
            )
        ]),  # filtro
        html.Div(className="filters dd-styles", children=[
            dcc.Dropdown(
                id='levelDrop',
                options=dificulty_level,
                value='all'
            )
        ]),  # filtro
        html.Div(className="filters dd-styles", children=[
            dcc.Dropdown(
                id='paidDrop',
                options=paid_option,
                value='all'
            )
        ]),  # filtro
    ]),

    html.Div(className="grid", children=[
        html.Div(className="filters dd-styles shadow",style={'border-color':'rgba(193, 66, 66, 0.5)'}, children=[
            html.P(className="indicator", id="totalCourses"),
            html.P('Courses', className="indicator", style={'font-size': '20px', 'margin-top': '0px'})
        ]),  # indicador
        html.Div(className="filters dd-styles shadow",style={'border-color':'rgba(193, 66, 66, 0.5)'}, children=[
            html.P(className="indicator", id="maxPrice"),
            html.P('Highest Price', className="indicator", style={'font-size': '20px', 'margin-top': '0px'})
        ]),  # indicador
        html.Div(className="filters dd-styles shadow",style={'border-color':'rgba(193, 66, 66, 0.5)'}, children=[
            html.P(id="numLectures", className="indicator"),
            html.P('Lectures', className="indicator", style={'font-size': '20px', 'margin-top': '0px'})
        ]),  # indicador
        html.Div(className="filters dd-styles shadow",style={'border-color':'rgba(193, 66, 66, 0.5)'}, children=[
            html.P(id="totalHours", className="indicator"),
            html.P('Total Hours', className="indicator", style={'font-size': '20px', 'margin-top': '0px'})
        ]),  # indicador
    ]),

    html.Div(className="grid", children=[
        html.Div(id="converted_leads_container", style={'height': '200px', 'width': '800px'}, children=[
            html.Div(className='shadow', children=[
                dcc.Graph(
                    id='example-graph2'
                )
            ])
        ]),  # indicador

        html.Div(id="converted_leads_container2", style={'height': '200px', 'width': '800px', 'margin': '7px', 'margin-top': '-1px'},
                 children=[
                     html.Div(className='shadow', children=[
                         dcc.Graph(
                             id='example-graph'
                         )
                     ])
                 ]),  # gráfico

    ]),

    html.Div(className="grid2", children=[
        html.Div(id="converted_leads_container3", style={'height': '200px', 'width': '800px', 'margin-right': '7px'}, children=[
            html.Div(className='shadow', children=[
                dcc.Graph(
                    id='graphLine'
                )
            ])
        ]),

        html.Div(id="converted_leads_container4", style={'height': '200px', 'width': '800px'},
                 children=[
                     html.Div(className='shadow', children=[
                         dcc.Graph(
                             id='graphScatter'
                         )
                     ])
                 ]),
        # indicador
    ]),
])


@app.callback(
    [Output(component_id='example-graph', component_property='figure'),
     Output(component_id='example-graph2', component_property='figure'),
     Output(component_id='graphLine', component_property='figure'),
     Output(component_id='graphScatter', component_property='figure'),
     Output(component_id='totalCourses', component_property='children'),
     Output(component_id='maxPrice', component_property='children'),
     Output(component_id='numLectures', component_property='children'),
     Output(component_id='totalHours', component_property='children')],
    [Input(component_id='paidDrop', component_property='value'),
     Input(component_id='levelDrop', component_property='value'),
     Input(component_id='subjectsDrop', component_property='value')],
)

def callback_1(input_value, levels, subjects):
    if input_value != 'all':
        df_filtered = df.loc[df['is_paid'] == input_value]
    else:
        df_filtered = df

    if levels != 'all':
        df_filtered = df_filtered.loc[df['level'] == levels]

    if subjects != 'all':
        df_filtered = df_filtered.loc[df['subject'] == subjects]

    totalCourses = df_filtered['course_id'].count()
    maxPrice = str(df_filtered['price'].max()) + ' €'
    numLectures = df_filtered['num_lectures'].sum()
    totalHours = round(df_filtered['content_duration'].sum())
    v = df_filtered.groupby("subject")["num_subscribers"].count().reset_index(name='Count').sort_values(by='Count',
                                                                                                   ascending=False)
    data_bar = dict(type='bar',
                    y=v['Count'],
                    x=v['subject'],
                    texttemplate='<b>%{y}</b>',
                    textposition='outside',
                    marker=dict(color='#c73f36')
                    )

    layout_bar = dict(yaxis=dict(range=(0, 2000),
                                 title='Number Subscribers'
                                 ),
                      xaxis=dict(title='Subjects'),
                      title=dict(
                          text='Number of courses by subject by year',
                          font=dict(family='Arial', size=18, color='black'),
                          x=.5,
                          y=.9
                      ),
                      margin=dict(l=100, t=100, b=100, r=100),  # left, top, bottom and right margin space (default=100)
                      paper_bgcolor='white',
                      plot_bgcolor='rgb(233,233,233)'
                      )

    totalPaid = df_filtered.loc[df_filtered['is_paid'] == 'True'].count()
    totalFree = df_filtered.loc[df_filtered['is_paid'] == 'False'].count()

    listPaid = [totalFree["is_paid"],totalPaid["is_paid"]]

    pie_paid_labels = list(set(df_filtered['is_paid'].replace("True", "Paid").replace("False", "Free")))
    pie_paid_values = listPaid


    pie_paid_data = dict(type='pie',
                         labels=pie_paid_labels,
                         values=pie_paid_values,
                         name='Pie Paid Courses',
                         marker=dict(colors = px.colors.sequential.RdBu)

                         )

    pie_paid_layout = dict(
            title=dict(
                text='Percentage of Paid vs Free Courses',
                font=dict(family='Arial', size=18, color='black'),
                x=.5,
                y=.9
                ),
            margin=dict(l=100,t=100,b=100,r=100), #left, top, bottom and right margin space (default=100)
            paper_bgcolor='white',
            plot_bgcolor='rgb(233,233,233)'
        )
    pd.to_datetime(df_filtered['published_timestamp'])

    df_filtered['Year'] = pd.DatetimeIndex(df_filtered['published_timestamp']).year

    y = df_filtered.groupby("Year")["course_id"].count().reset_index(name='Count').sort_values(by='Year', ascending=True).drop_duplicates()

    x = list(y['Year'])
    y2 = list(y['Count'])
    ex2_data = dict(type='scatter', x=x, y=y2, marker=dict(color='#c73f36'))

    ex2_layout = dict(
            title=dict(
                text='Number of courses evolution by Year',
                font=dict(family='Arial', size=18, color='black'),
                x=.5,
                y=.9
                ),
            margin=dict(l=100,t=100,b=100,r=100), #left, top, bottom and right margin space (default=100)
            paper_bgcolor='white',
            plot_bgcolor='rgb(233,233,233)'
        )

    reviewsTotal = df_filtered.groupby("subject")["num_reviews"].count().reset_index(name='CountReviews')

    scatterReviews = go.Figure(data=go.Scatter(
                    x=reviewsTotal['subject'],
                    y=v['Count'],
                    mode='markers',
                    marker=dict(size=reviewsTotal['CountReviews'] / 10,
                                color=px.colors.sequential.RdBu),
    ))

    scatterReviews.update_layout(dict(
            title=dict(
                text='Number of Courses by Subject and Number of Reviews',
                font=dict(family='Arial', size=18, color='black'),
                x=.2,
                y=.9
                ),
            margin=dict(l=100,t=100,b=100,r=100), #left, top, bottom and right margin space (default=100)
            paper_bgcolor='white',
            plot_bgcolor='rgb(233,233,233)'
        ))

    return go.Figure(data=data_bar, layout=layout_bar), go.Figure(data=pie_paid_data, layout=pie_paid_layout), go.Figure(data=ex2_data, layout=ex2_layout), scatterReviews, totalCourses, maxPrice, numLectures, totalHours


if __name__ == '__main__':
    app.run_server(debug=True)
