import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from grafikler import Grafikler
import hisseGetir
import plotly.graph_objects as go


def hisseSec():
    hisse =  "THYAO"
    return hisse

hisse = hisseSec()


hisse_finansal = pd.read_excel(f"database/{hisse}_bilanco.xlsx" , index_col=0)


FinansalVeriler = hisseGetir.finansalVeriBasliklari(hisse_finansal)



# Create an instance of PlottingFunctions


app = dash.Dash(__name__)
server = app.server
#KARLILIK
aktifKarlilik         = FinansalVeriler.aktifKarlilik()
grafik1               = Grafikler(aktifKarlilik,hisse)
ozSermayeKarliligi    = FinansalVeriler.ozSermayeKarliligi()
grafik2               = Grafikler(ozSermayeKarliligi,hisse)
brutKarMarji          = FinansalVeriler.brutKarMarji()
grafik3               = Grafikler(brutKarMarji,hisse)


brutKarMarji_Quad    = FinansalVeriler.brutKarMarji_Quad()
grafik4              = Grafikler(brutKarMarji_Quad,hisse)
netKarMarji_Quad     = FinansalVeriler.netKarMarji_Quad()
grafik5              = Grafikler(netKarMarji_Quad,hisse)
FAVOKMarji_Quad      = FinansalVeriler.FAVOKMarji_Quad()
grafik6              = Grafikler(FAVOKMarji_Quad,hisse)
#FAALİYET ETKİNLİK 
aktifDevirHizi        = FinansalVeriler.aktifDevirHizi()
grafik7               = Grafikler(aktifDevirHizi,hisse)
stokDevirHizi         = FinansalVeriler.stokDevirHizi()
grafik8               = Grafikler(stokDevirHizi,hisse)
ozKaynakDevirHizi     = FinansalVeriler.ozKaynakDevirHizi()
grafik9               = Grafikler(ozKaynakDevirHizi,hisse)  
alacakDevirHizi       = FinansalVeriler.alacakDevirHizi()
grafik10              = Grafikler(alacakDevirHizi,hisse)
#NAKİT ORANLARI
cariOran              = FinansalVeriler.cariOran()
grafik11              = Grafikler(cariOran,hisse)
asitTestOrani         = FinansalVeriler.asitTestOrani()
grafik12              = Grafikler(asitTestOrani,hisse)  
nakitOran             = FinansalVeriler.nakitOran()
grafik13              = Grafikler(nakitOran,hisse)
#OZET FINANSALLAR
netIsletmeSermayesi   = FinansalVeriler.netIsletmeSermayesi()
grafik14              = Grafikler(netIsletmeSermayesi,hisse)
netIStoSatislar       = FinansalVeriler.netIStoSatislar()
grafik15              = Grafikler(netIStoSatislar,hisse)  
FAVOK_CUM             = FinansalVeriler.FAVOK_CUM()
grafik16              = Grafikler(FAVOK_CUM,hisse)

FAVOK_Quad            = FinansalVeriler.FAVOK_Quad()
grafik17              = Grafikler(FAVOK_Quad,hisse)
netKar_Quad           = FinansalVeriler.netKar_Quad()
grafik18              = Grafikler(netKar_Quad,hisse)  
satislar_Quad         = FinansalVeriler.satislar_Quad()
grafik19              = Grafikler(satislar_Quad,hisse)

satislarinMaliyeti_Quad              = FinansalVeriler.satislarinMaliyeti_Quad()
grafik20                             = Grafikler(satislarinMaliyeti_Quad,hisse)
FreeCashFlow                         = FinansalVeriler.FreeCashFlow()
grafik21                             = Grafikler(FreeCashFlow,hisse)  
FreeCashFlow_Quad                    = FinansalVeriler.FreeCashFlow_Quad()
grafik22                             = Grafikler(FreeCashFlow_Quad,hisse)

barDf = FinansalVeriler.SatMalKarOz()
barPlot_1 = Grafikler(barDf["Satışlar"])
_barPlot_1 = barPlot_1.barPlot()
barPlot_2 = Grafikler(barDf["Satışların Maliyeti"])
_barPlot_2 = barPlot_2.barPlot()
barPlot_3 = Grafikler(barDf["Net Kar"])
_barPlot_3 = barPlot_3.barPlot()
barPlot_4 = Grafikler(barDf["Öz Kaynaklar"])
_barPlot_4 = barPlot_4.barPlot()





F_K      = FinansalVeriler.FKOrani()
FD_FAVOK = FinansalVeriler.FDFAVOK()
pd_dd    = FinansalVeriler.PDDD()
peg      = FinansalVeriler.PEG()
HBK      = FinansalVeriler.HBK()

#PIE CHART
pieChart1 = Grafikler(FinansalVeriler.kaynakveBorclar(),hisse)





# ORANLAR TABLOSU
oranlarTable = [
    ["F/K", "FD/FAVÖK","PD/DD","PEG","HBK"],
    [F_K,FD_FAVOK,pd_dd,peg,HBK] ]



fig_table = go.Figure(data=[go.Table(header=dict(values=['Oranlar', 'Değer'],
                               fill_color='#17202A',
                               align='center',line_color='#273746',font=dict(color='white')),
                               cells=dict(values=oranlarTable,fill_color="#17202A",height=45,line_color='#273746',font=dict(color='white')))
                      ])

fig_table.update_layout(
    autosize=False,
    width=500,  # Set the width of the table
    height=300,  # Set the height of the table
    margin=dict(l=20, r=20, t=20, b=20),  # Set the margins
    paper_bgcolor="#17202A",
    #columnwidth=[100,100,100,100,100]  # Set the width of each column
)




app.layout = html.Div(style={'backgroundColor': '#17202A', 'height': '100vh'}, children=[
    
    html.Div([    
        html.H1('Oranlar', style={'textAlign': 'center',"color":"#979A9A"}),
        dcc.Graph(id='table1', figure=fig_table,style={'width': '50%', 'height': '50vh','display': 'inline-block'}),
        dcc.Graph(id='plot18', figure=pieChart1.pieChart(),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'})
        ],style = {'backgroundColor': '#17202A'}),  


    html.Div([    
        html.H1('Özet Bilgiler', style={'textAlign': 'center',"color":"#979A9A"}),
        dcc.Graph(id='barp1', figure=_barPlot_1,style={'width': '50%', 'height': '50vh','display': 'inline-block'}),
        dcc.Graph(id='barp2', figure=_barPlot_2,style={'width': '50%', 'height': '50vh','display': 'inline-block'}),
        dcc.Graph(id='barp3', figure=_barPlot_3,style={'width': '50%', 'height': '50vh','display': 'inline-block'}),
        dcc.Graph(id='barp4', figure=_barPlot_4,style={'width': '50%', 'height': '50vh','display': 'inline-block'}),
        html.H1('Özet Finansallar', style={'textAlign': 'center',"color":"#979A9A"}),
        dcc.Graph(id='plot14', figure=grafik14.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        dcc.Graph(id='plot15', figure=grafik15.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        dcc.Graph(id='plot16', figure=grafik16.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        dcc.Graph(id='plot17', figure=grafik17.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        dcc.Graph(id='plot18', figure=grafik18.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        dcc.Graph(id='plot19', figure=grafik19.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        dcc.Graph(id='plot20', figure=grafik20.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        dcc.Graph(id='plot21', figure=grafik21.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        dcc.Graph(id='plot22', figure=grafik22.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),   
        html.H1('Karlılık Analizi', style={'textAlign': 'center',"color":"#979A9A"}),
        dcc.Graph(id='plot1', figure=grafik1.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        dcc.Graph(id='plot2', figure=grafik2.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        dcc.Graph(id='plot3', figure=grafik3.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        dcc.Graph(id='plot4', figure=grafik4.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        dcc.Graph(id='plot5', figure=grafik5.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        dcc.Graph(id='plot6', figure=grafik6.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        html.H2('Faaliyet Etkinlik Oranları', style={'textAlign': 'center',"color":"#979A9A"}), 
        dcc.Graph(id='plot7', figure=grafik7.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        dcc.Graph(id='plot8', figure=grafik8.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        dcc.Graph(id='plot9', figure=grafik9.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        dcc.Graph(id='plot10', figure=grafik10.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        html.H2('Nakit Oranlar', style={'textAlign': 'center',"color":"#979A9A"}), 
        dcc.Graph(id='plot11', figure=grafik11.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        dcc.Graph(id='plot12', figure=grafik12.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'}),
        dcc.Graph(id='plot13', figure=grafik13.linePlot(10),style={'width': '50%', 'height': '50vh', 'display': 'inline-block'})
        ],style = {'backgroundColor': '#17202A'}),        
]
)
html_content = app.index_string

with open("dashboard.html", "w") as file:
    file.write(html_content)


#if __name__ == '__main__':
 #   app.run_server(debug=True)



