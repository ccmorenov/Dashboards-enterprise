import cx_Oracle
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import webbrowser
from dash import Dash, dcc, html, Input, Output
from plotly.subplots import make_subplots

try:
    connection=cx_Oracle.connect(

        user='ORAPX1',
        password='Or4*Xp1.2022',
        dsn='racsapathqa-scan:1528/PX1',
        encoding='UTF-8'
    )
    df = pd.read_sql('SELECT * FROM RESOURCES', con=connection)
    df2 = df.copy()
    df = df.drop('ID', axis=1) 
    df2 = df2.drop('ID', axis=1) 
    df= df.drop('STATE',axis=1)
    df= df.drop('DATE_EXTRACT',axis=1)
    groups=df.groupby("NAME", as_index=False).mean()

    labels = ["Utilization","Free"]
    url = 'http://127.0.0.1:8050'
    chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe %s'

    fig1= px.bar(df, x=groups['NAME'], y=groups['UTILIZATION'], color=groups['NAME'],labels={"x": "Hostnames","y": "Utilizacion VCPUs %","color": "Hostnames"},title="Utilizacion % de la VCPUs por maquina historicamente")
    fig1.update_layout(barmode ='stack', xaxis={'categoryorder': 'total ascending'})

    fig2= px.bar(df, x=groups['NAME'], y=groups['UTILIZATION1'], color=groups['NAME'],labels={"x": "Hostnames","y": "Utilizacion Memoria %","color": "Hostnames"},title="Utilizacion % de la MEMORIA por maquina historicamente")
    fig2.update_layout(barmode='stack', xaxis={'categoryorder': 'total ascending'})

    fig3= px.bar(df, x=groups['NAME'], y=groups['UTILIZATION2'], color=groups['NAME'],labels={"x": "Hostnames","y": "Utilizacion HARDDISK %","color": "Hostnames"},title="Utilizacion % del HARDDISK por maquina historicamente")
    fig3.update_layout(barmode='stack', xaxis={'categoryorder': 'total ascending'})

    app = Dash(__name__)

    app.layout = html.Div([
    html.Div([
    html.H2('Grafico de utilizacion de la VCPUs por maquina historicamente (media)'),
    dcc.Graph(figure=fig1)
    ]),
    html.Div([
    html.H2('Grafico de utilizacion de la MEMORIA por maquina historicamente (media)'),
    dcc.Graph(figure=fig2)
    ]),
    html.Div([
    html.H2('Grafico de utilizacion de la HARDDISK por maquina historicamente (media)'),
    dcc.Graph(figure=fig3)
    ]),
    html.Div([
        html.H2('Resumen general del dia'),
        dcc.DatePickerRange(
        id='my_date_picker_range0',
        min_date_allowed=df2['DATE_EXTRACT'].min(),
        max_date_allowed=df2['DATE_EXTRACT'].max(),
        start_date=df2['DATE_EXTRACT'].max(),
        end_date=df2['DATE_EXTRACT'].max(),
        start_date_placeholder_text="Start Period",
        end_date_placeholder_text="End Period",
        calendar_orientation='vertical'),
        dcc.Graph(id="pie-graph-all"),
    ],style={'textAlign': 'center'})
    ])

    @app.callback(
        Output("pie-graph-all", "figure"),
        Input("my_date_picker_range0", 'start_date'),
        Input("my_date_picker_range0", 'end_date')
        )

    def generate(start_date, end_date):
        figpiecalendar = make_subplots(rows=20,cols=3, specs=[[{'type':'pie'},{'type':'pie'},{'type':'pie'}],
                                                            [{'type':'pie'},{'type':'pie'},{'type':'pie'}],
                                                            [{'type':'pie'},{'type':'pie'},{'type':'pie'}],
                                                            [{'type':'pie'},{'type':'pie'},{'type':'pie'}],
                                                            [{'type':'pie'},{'type':'pie'},{'type':'pie'}],
                                                            [{'type':'pie'},{'type':'pie'},{'type':'pie'}],
                                                            [{'type':'pie'},{'type':'pie'},{'type':'pie'}],
                                                            [{'type':'pie'},{'type':'pie'},{'type':'pie'}],
                                                            [{'type':'pie'},{'type':'pie'},{'type':'pie'}],
                                                            [{'type':'pie'},{'type':'pie'},{'type':'pie'}],
                                                            [{'type':'pie'},{'type':'pie'},{'type':'pie'}],
                                                            [{'type':'pie'},{'type':'pie'},{'type':'pie'}],
                                                            [{'type':'pie'},{'type':'pie'},{'type':'pie'}],
                                                            [{'type':'pie'},{'type':'pie'},{'type':'pie'}],
                                                            [{'type':'pie'},{'type':'pie'},{'type':'pie'}],
                                                            [{'type':'pie'},{'type':'pie'},{'type':'pie'}],
                                                            [{'type':'pie'},{'type':'pie'},{'type':'pie'}],
                                                            [{'type':'pie'},{'type':'pie'},{'type':'pie'}],
                                                            [{'type':'pie'},{'type':'pie'},{'type':'pie'}],
                                                            [{'type':'pie'},{'type':'pie'},{'type':'pie'}]],
                                                            column_titles=["VCPUs","Memory","HardDisk"],                                                         
                                                            row_titles=['ATHCMPPRD101',"ATHCMPPRD102",'ATHCMPPRD103','ATHCMPPRD104','ATHCTRPRD100','ATHHPAPRD101','ATHHPAPRD102','ATHHPAPRD103','ATHHPAPRD104','ATHHPAPRD105',
                                                                        'ATHWEBPRD100','ATHXCOPRD104','ATHORRPRD121','ATHORRPRD122','ATHISSPRD101','ATHISSPRD102','ATHVASPRD101','ATHVASPRD102','ATHMETPRD101','ATHMETPRD102'])
        df2['DATE_EXTRACT'] = pd.to_datetime(df2['DATE_EXTRACT']) 
        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHCMPPRD101"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=1,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=1,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=1,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=1,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=1,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=1,col=3)     

        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHCMPPRD102"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=2,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=2,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=2,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=2,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=2,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=2,col=3) 

        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHCMPPRD103"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=3,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=3,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=3,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=3,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=3,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=3,col=3) 

        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHCMPPRD104"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=4,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=4,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=4,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=4,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=4,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=4,col=3) 

        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHCTRPRD100"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=5,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=5,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=5,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=5,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=5,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=5,col=3) 

        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHHPAPRD101"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=6,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=6,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=6,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=6,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=6,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=6,col=3) 

        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHHPAPRD102"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=7,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=7,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=7,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=7,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=7,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=7,col=3) 

        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHHPAPRD103"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=8,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=8,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=8,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=8,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=8,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=8,col=3) 

        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHHPAPRD104"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=9,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=9,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=9,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=9,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=9,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=9,col=3) 

        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHHPAPRD105"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=10,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=10,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=10,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=10,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=10,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=10,col=3) 

        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHWEBPRD100"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=11,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=11,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=11,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=11,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=11,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=11,col=3) 

        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHXCOPRD104"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=12,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=12,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=12,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=12,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=12,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=12,col=3) 

        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHORRPRD121"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=13,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=13,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=13,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=13,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=13,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=13,col=3) 

        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHORRPRD122"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=14,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=14,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=14,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=14,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=14,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=14,col=3) 

        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHISSPRD101"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=15,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=15,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=15,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=15,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=15,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=15,col=3) 

        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHISSPRD102"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=16,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=16,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=16,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=16,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=16,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=16,col=3) 

        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHVASPRD101"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=17,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=17,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=17,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=17,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=17,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=17,col=3) 

        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHVASPRD102"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=18,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=18,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=18,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=18,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=18,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=18,col=3) 

        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHMETPRD101"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=19,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=19,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=19,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=19,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=19,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=19,col=3) 

        dfdate = df2.loc[df2['DATE_EXTRACT'].between(*pd.to_datetime([start_date,end_date]))]
        dfdate = dfdate.loc[dfdate['NAME'] == "ATHMETPRD102"]
        dfdate = dfdate.drop('MEMORY',axis=1)
        dfdate = dfdate.drop('DISKSPACE',axis=1)
        dfdate = dfdate.drop('VCPU',axis=1)
        dfdate= dfdate.drop('STATE', axis=1)
        dfdate = dfdate.groupby("NAME", as_index=False).mean()
        a=dfdate['UTILIZATION'].values.tolist()
        b=dfdate['UTILIZATION1'].values.tolist()
        c=dfdate['UTILIZATION2'].values.tolist()
        if a[0] or b[0] or c[0]<80:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs"),row=20,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria"),row=20,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk"),row=20,col=3)
        else:
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[a[0],100-a[0]],name="Utilizacion % VCPUs",pull=[0, 0.2]),row=20,col=1)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[b[0],100-b[0]],name="Utilizacion % Memoria",pull=[0, 0.2]),row=20,col=2)
            figpiecalendar.add_trace(go.Pie(labels=labels, values=[c[0],100-c[0]],name="Utilizacion % Harddisk",pull=[0, 0.2]),row=20,col=3) 

        figpiecalendar.update_traces(marker=dict(colors=['red', 'green']))
        figpiecalendar.update_traces(hole=.2)
        figpiecalendar.update_layout(title_font=dict(size=30),title_text="INFORME CAPACIDADES SERVIDORES SAS AMBIENTE PRD",title_font_family="Times New Roman",title_font_color="red", title_x=0.5,autosize=False,width=1900,height=3000)  
        return figpiecalendar

    
    if __name__ == "__main__":
        app.run_server(debug=False)
        webbrowser.get(chrome_path).open(url)
        
except Exception as ex:
    print(ex)
    print("Ocurrio una excepcion")
finally:
    connection.close()
    print('Conexion finalizada')