#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = [i for i in range(1980, 2024)]

# Create the layout of the app
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center',
            'color': '#503D36', 'font-size': 24}),
    
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='report-type',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select a report type',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'textAlign': 'center'}
        )
    ]),
    
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=2020,  # default value
            placeholder='Select a year'
        )
    ]),
    
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flex-direction': 'column'})
])

# Define the callback to enable/disable year dropdown based on report type
@app.callback(
    Output('select-year', 'disabled'),
    [Input('report-type', 'value')]
)
def update_input_container(report_type):
    if report_type == 'Yearly Statistics':
        return False
    else:
        return True

# Callback to update the output container with graphs
@app.callback(
    Output('output-container', 'children'),
    [Input('report-type', 'value'), Input('select-year', 'value')]
)
def update_output_container(report_type, input_year):
    if report_type == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
        # Create plots for Recession Period Statistics
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales Fluctuation Over Recession Period")
        )
        
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Number of Vehicles Sold by Vehicle Type")
        )
        
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, 
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Expenditure Share by Vehicle Type During Recessions')
        )
        
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'], as_index=False)['Automobile_Sales'].mean()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                title='Effect of Unemployment Rate on Vehicle Type and Sales')
        )

        return [
            html.Div(className='chart-item', children=[R_chart1, R_chart2], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[R_chart3, R_chart4], style={'display': 'flex'})
        ]

    elif report_type == 'Yearly Statistics' and input_year:
        yearly_data = data[data['Year'] == input_year]
        
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas,
                x='Year',
                y='Automobile_Sales',
                title='Yearly Automobile Sales for the Whole Period')
        )
        
        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales')
        )
        
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type in the Year {}'.format(input_year))
        )
        
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertisement Expenditure for Each Vehicle')
        )

        return [
            html.Div(className='chart-item', children=[Y_chart1, Y_chart2], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[Y_chart3, Y_chart4], style={'display': 'flex'})
        ]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
