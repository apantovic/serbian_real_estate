import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash_daq as daq
from joblib import load
from functions import municipality_mapping, floor_mapping, heating_mapping, remap_df, find_coordinates, get_flag_switch

model = load('models/GBR_Model.joblib') 
df = pd.read_csv("C:/Users/neven/Desktop/Projekti/Aleksandar/Housing/belgrade_data.csv")


flag_switch1, flag_switch2, flag_switch3, dct = get_flag_switch()

switches1 = dbc.FormGroup([dbc.Checklist(options=[{'label':i, 'value':flag_switch1[i]} for i in flag_switch1.keys()],value=[],id="flags1",switch=True,),])
switches2 = dbc.FormGroup([dbc.Checklist(options=[{'label':i, 'value':flag_switch2[i]} for i in flag_switch2.keys()],value=[],id="flags2",switch=True,),])
switches3 = dbc.FormGroup([dbc.Checklist(options=[{'label':i, 'value':flag_switch3[i]} for i in flag_switch3.keys()],value=[],id="flags3",switch=True,),])


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])


app.layout = dbc.Container([

        html.Div([
                dbc.Row([
                        dbc.Col(html.H1('Real Estate Appraisal Tool')),
                ],style={"margin-top":"10px","margin-bottom":"30px"}, justify="center"),
                dbc.Row([
                        dbc.Col(dcc.Dropdown(id="opstina", placeholder='Opština', options=[{'label':i, 'value':i} for i in df['City_Area'].fillna('N/A').unique()]),md=3),    
                        dbc.Col(dcc.Dropdown(id="tip_obj", placeholder='Tip Objekta', options=[{'label':i, 'value':i} for i in df['Object_Type'].fillna('N/A').unique()]),md=3),
                        dbc.Col(dcc.Dropdown(id="stanje", placeholder='Stanje Objekta', options=[{'label':i, 'value':i} for i in df['Condition'].fillna('N/A').unique()]),md=3),        
                        dbc.Col(dcc.Dropdown(id="grejanje", placeholder='Način Grejanja', options=[{'label':i, 'value':i} for i in df['Heating'].fillna('N/A').unique()]),md=3),                                
                        ],align="center", justify="center"),
                dbc.Row([
                        dbc.Col(dcc.Dropdown(id="kvadratura", placeholder='Veličina Stana', options=[{'label':i, 'value':i} for i in range(1,1000)]),md=3),        
                        dbc.Col(dcc.Dropdown(id="br_soba", placeholder='Broj Soba', options=[{'label':i, 'value':i} for i in [str(i) for i in range(0,5)] + [' 5+']]),md=3),        
                        dbc.Col(dcc.Dropdown(id="sprat", placeholder='Sprat', options=[{'label':i, 'value':i} for i in ['SUT', 'PSUT', 'PR', 'VPR'] + [str(i) for i in range(1,30)]]),md=3),        
                        dbc.Col(dcc.Dropdown(id="max_sprat", placeholder='Maksimalni Broj Spratova', options=[{'label':i, 'value':i} for i in range(100)]),md=3),                                
                        ],style={"margin-top":"10px","margin-bottom":"30px"},align="center", justify="center"),
                dbc.Input(id="ulica", placeholder="Unesite Naziv Ulice", type="text"),
                dbc.Row([
                        dbc.Col(dbc.Form([switches1]),md=3),
                        dbc.Col(dbc.Form([switches2]),md=3),
                        dbc.Col(dbc.Form([switches3]),md=3),
                        ],style={"margin-top":"10px","margin-bottom":"30px"},align="center", justify="center"),
    dbc.Row([
            dbc.Button("Apprise", id="button", className="mr-2"),
            ]),
    ]),        

    html.Div(id = 'map'),
    
])        
    
@app.callback(
     dash.dependencies.Output("map", "children"),
      [dash.dependencies.Input("opstina", "value"),
      dash.dependencies.Input("tip_obj", "value"),
      dash.dependencies.Input("stanje", "value"),
      dash.dependencies.Input("ulica", "value"),
      dash.dependencies.Input("grejanje", "value"),
      dash.dependencies.Input("kvadratura", "value"),
      dash.dependencies.Input("br_soba", "value"),
      dash.dependencies.Input("sprat", "value"),
      dash.dependencies.Input("max_sprat", "value"),
      dash.dependencies.Input("flags1", "value"),
      dash.dependencies.Input("flags2", "value"),
      dash.dependencies.Input("flags3", "value"),
      dash.dependencies.Input("button", "n_clicks")],
)
def update_figure(opstina, ulica, tip_obj, stanje, grejanje, kvadratura, br_soba, sprat, max_sprat, flags1, flags2,flags3,click):
    if click:
        values = [opstina, ulica, tip_obj, stanje, grejanje, kvadratura, br_soba, sprat, max_sprat] + flags1 + flags2 + flags3
        
        if None in values:
            return html.Div([
                    html.H1('Nepravilno popunjene vrednosti! Molimo ispravite.'),
                            ])
        else:
            
            flag_switch1, flag_switch2, flag_switch3, dct = get_flag_switch()
             
            dct['City_Area']=opstina
            dct['Street']=ulica
            dct['Object_Type']=tip_obj
            dct['Condition']=stanje
            dct['Heating']=grejanje
            dct['Property_Size_sqmtr']=kvadratura
            dct['No_of_Rooms']=br_soba
            dct['Floor']=sprat
            dct['Max_Floors']=max_sprat
            
            if flags1:
                for i in range(len(flags1)):
                    dct[flags1[i]]=1
            if flags2:
                for i in range(len(flags2)):
                    dct[flags2[i]]=1
            if flags3:
                for i in range(len(flags3)):
                    dct[flags3[i]]=1
                     
            
            dff = pd.DataFrame([dct])
        
            dff = remap_df(dff)
            pred_price = int(model.predict(dff.head(1))[0])
            
            g = find_coordinates(ulica + ', ' + opstina + ', Belgrade, Serbia')
            fig = px.scatter_mapbox(lat=g['lat'], lon=g['lng'], hover_name=pred_price, hover_data=[ulica, br_soba],
                                  color_discrete_sequence=["fuchsia"], zoom=6, height=400)
            fig.update_layout(mapbox_style="open-street-map")
     
            return html.Div([
                    html.H1('Procenjena Vrednost'),
                    dbc.Row([dbc.Col([
                        dbc.Row([
                            dbc.Col([
                            daq.LEDDisplay(label='Procenjena Vrednost',color="#FF5E5E", value=str(pred_price)),
                            daq.LEDDisplay(label='Prosečna Vrednost stana u datoj opštini',color="#FF5E5E", value='100000'),
                                ],md=6)]),
                            
                            dbc.Row([
                            dbc.Col(dcc.Graph(id="map",figure=fig),md=6),
                            ],style={"margin-bottom":"30px"},align="center", justify="center"),
                        ],md=12),
                ]),
            ])
                
    
if __name__ == '__main__':
     app.run_server(debug=True)
