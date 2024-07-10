import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from combination_functions import combinations
import numpy as np

def process_inputs(input1, input2, input3, option1, option2, option3, df, seed=95):
   if input1 is None or input2 is None or input3 is None:
       return pd.DataFrame(columns=['PRODUCTS', 'ZONES', 'PLAN_TYPE', 'AGE_BAND', 'SUM_INSURED', 'PREMIUM', 'CITIES'])
   combination_df, result_index = combinations(df, input1, input2, input3, seed)
   policy_combinations = [combination_df.loc[i] for i in result_index]
   if option1 == [0] and option2 == [] and option3 == []:
     result = policy_combinations[0][['PRODUCTS', 'ZONES', 'PLAN_TYPE', 'AGE_BAND', 'SUM_INSURED', 'PREMIUM', 'CITIES']]
     return result, len(result)
   elif option1 == [] and option2 == [1] and option3 == []:
     result = policy_combinations[1][['PRODUCTS', 'ZONES', 'PLAN_TYPE', 'AGE_BAND', 'SUM_INSURED', 'PREMIUM', 'CITIES']]
     return result, len(result)
   elif option1 == [] and option2 == [] and option3 == [2]:
     result = policy_combinations[2][['PRODUCTS', 'ZONES', 'PLAN_TYPE', 'AGE_BAND', 'SUM_INSURED', 'PREMIUM', 'CITIES']]
     return result, len(result)

df = pd.read_csv(r"Z:\Policy combination for a set commission income\Data\commission_processed_final.csv")
app = dash.Dash(__name__)
server = app.server

city_options = [
  {'label': 'Mumbai', 'value': 'MUMBAI'},
  {'label': 'Delhi', 'value': 'DELHI'},
  {'label': 'Kolkata', 'value': 'KOLKATA'},
  {'label': 'Chennai', 'value': 'CHENNAI'},
  {'label': 'Bangalore', 'value': 'BANGALORE'},
  {'label': 'Hyderabad', 'value': 'HYDERABAD'},
  {'label': 'Ahmedabad', 'value': 'AHMEDABAD'},
  {'label': 'Pune', 'value': 'PUNE'},
  {'label': 'Surat', 'value': 'SURAT'},
  {'label': 'Jaipur', 'value': 'JAIPUR'},
  {'label': 'Kanpur', 'value': 'KANPUR'},
  {'label': 'Lucknow', 'value': 'LUCKNOW'},
  {'label': 'Nagpur', 'value': 'NAGPUR'},
  {'label': 'Ghaziabad', 'value': 'GHAZIABAD'},
  {'label': 'Indore', 'value': 'INDORE'},
  {'label': 'Coimbatore', 'value': 'COIMBATORE'},
  {'label': 'Patna', 'value': 'PATNA'},
  {'label': 'Alwar', 'value': 'ALWAR'},
  {'label': 'Baroda', 'value': 'BARODA'},
  {'label': 'Bhiwani', 'value': 'BHIWANI'},
  {'label': 'Bulandshahar', 'value': 'BULANDSHAHAR'},
  {'label': 'Ernakulam', 'value': 'ERNAKULAM'},
  {'label': 'Faridabad', 'value': 'FARIDABAD'},
  {'label': 'Fatehabad', 'value': 'FATEHABAD'},
  {'label': 'Gurgaon', 'value': 'GURGAON'},
  {'label': 'Gwalior', 'value': 'GWALIOR'},
  {'label': 'Jind', 'value': 'JIND'},
  {'label': 'Kaithal', 'value': 'KAITHAL'},
  {'label': 'Karnal', 'value': 'KARNAL'},
  {'label': 'Kollam', 'value': 'KOLLAM'},
  {'label': 'Kurukshetra', 'value': 'KURUKSHETRA'},
  {'label': 'Meerut', 'value': 'MEERUT'},
  {'label': 'Mumbai Andheri Suburban', 'value': 'MUMBAI_ANDHERI_SUBURBAN'},
  {'label': 'Mumbai Dadar Suburban', 'value': 'MUMBAI_DADAR_SUBURBAN'},
  {'label': 'Mumbai Dombivali Suburban', 'value': 'MUMBAI_DOMBIVALI_SUBURBAN'},
  {'label': 'Mumbai Ghatkopar Suburban', 'value': 'MUMBAI_GHATKOPAR_SUBURBAN'},
  {'label': 'Mumbai Goregaon Suburban', 'value': 'MUMBAI_GOREGAON_SUBURBAN'},
  {'label': 'Mumbai Vasai Suburban', 'value': 'MUMBAI_VASAI_SUBURBAN'},
  {'label': 'Mumbai Virar Suburban', 'value': 'MUMBAI_VIRAR_SUBURBAN'},
  {'label': 'Nashik', 'value': 'NASHIK'},
  {'label': 'Noida', 'value': 'NOIDA'},
  {'label': 'Panipat', 'value': 'PANIPAT'},
  {'label': 'Rest of Gujarat', 'value': 'REST_OF_GUJARAT'},
  {'label': 'Rohtak', 'value': 'ROHTAK'},
  {'label': 'Saharanpur', 'value': 'SAHARANPUR'},
  {'label': 'Sirsa', 'value': 'SIRSA'},
  {'label': 'Sonipat', 'value': 'SONIPAT'},
  {'label': 'Thane', 'value': 'THANE'},
  {'label': 'Trivandrum', 'value': 'TRIVANDRUM'},
  {'label': 'Rest of India', 'value': 'REST_OF_INDIA'}
]

app.layout = html.Div([
   html.H1("User Input", style={'textAlign': 'center', 'color': '#4CAF50'}),
   html.Div([
       html.Div([
           html.Label('Commission To Earn'),
           html.Div([
               dcc.Input(id='input1', type='number', 
                         style={'margin': '5px','width': '89%', 'padding': '15px', 'border': '1px solid #ccc', 'borderRadius': '20px'})
           ], style={'margin': '5px', 'padding': '5px','width': '92%', 'border': '1px solid #ccc', 'borderRadius': '20px'}),
               dcc.Checklist(
                id='option1',
                options=[{'label': 'Option 1', 'value': 0}],
                value=[],
                labelStyle={'display': 'block'},
                style={'margin': '10px', 'padding': '10px', 'border': '1px solid #ccc', 'borderRadius': '20px'}
            )
       ], style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '30%', 'marginRight': '2%'}),
       html.Div([
           html.Label('Select City'),
           dcc.Dropdown(id='input2', options=city_options,
                        style={'margin': '5px', 'padding': '5px', 'border': '1px solid #ccc', 'borderRadius': '20px'}),
           dcc.Checklist(
                id='option2',
                options=[{'label': 'Option 2', 'value': 1}],
                value=[],
                labelStyle={'display': 'block'},
                style={'margin': '10px', 'padding': '10px', 'border': '1px solid #ccc', 'borderRadius': '20px'}
            )
       ], style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '30%', 'marginRight': '2%'}),
       html.Div([
           html.Label('Number of Policies'),
           dcc.Dropdown(id='input3', options=[
               {'label': 'Low', 'value': 'High Premium'},
               {'label': 'Medium', 'value': 'Medium Premium'},
               {'label': 'High', 'value': 'Low Premium'}
           ],
           style={'margin': '5px', 'padding': '5px', 'border': '1px solid #ccc', 'borderRadius': '20px'}),
           dcc.Checklist(
                id='option3',
                options=[{'label': 'Option 3', 'value': 2}],
                value=[],
                labelStyle={'display': 'block'},
                style={'margin': '10px', 'padding': '10px', 'border': '1px solid #ccc', 'borderRadius': '20px'}
            )
       ], style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '30%'}),       
       html.Button('Submit', id='submit-button', n_clicks=0,
                   style={'margin': '10px', 'padding': '10px 20px', 'backgroundColor': '#4CAF50', 'color': 'white', 'border': 'none', 'borderRadius': '5px'}),
       dcc.Store(id='store-previous-inputs')
   ], style={'textAlign': 'center'}),
   html.Div(id='output-container', style={'marginTop': '20px'})
], style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f9f9f9', 'padding': '20px'})

@app.callback(
   [Output('output-container', 'children'),
    Output('store-previous-inputs', 'data')],
   [Input('submit-button', 'n_clicks')],
   [State('input1', 'value'),
    State('input2', 'value'),
    State('input3', 'value'),
    State('option1', 'value'),
    State('option2', 'value'),
    State('option3', 'value'),
    State('store-previous-inputs', 'data')]
)
def update_output(n_clicks, input1, input2, input3, option1, option2, option3, previous_inputs):
   if n_clicks > 0:
       current_inputs = {'input1': input1, 'input2': input2, 'input3': input3, 'option1': option1, 'option2': option2, 'option3': option3}
       if previous_inputs == current_inputs:
           return dash.no_update, previous_inputs
         
       result, length = process_inputs(input1, input2, input3, option1, option2, option3, df)
     
       table_length = html.Div([
           html.H3(f"Number of Policies to be Sold: {length}")
       ])

       table_result = dash.dash_table.DataTable(
           columns=[{"name": i, "id": i} for i in result.columns],
           data=result.to_dict('records'),
           style_cell={'textAlign': 'center', 'padding': '10px'},
           style_header={
               'backgroundColor': '#4CAF50',
               'fontWeight': 'bold',
               'color': 'white'
           },
           style_data={
               'backgroundColor': '#f9f9f9',
               'border': '1px solid #ccc'
           },
           style_table={'width': '80%', 'margin': '0 auto'}
       )
     
       return [table_length, table_result], current_inputs
   return dash.no_update, previous_inputs

   return html.Div([html.P("Please Enter City and Premium Type then Submit",
                           style={'textAlign': 'center', 'color': '#ff0000'})]), previous_inputs

if __name__ == '__main__':
   app.run_server(debug=True, port=8059)
