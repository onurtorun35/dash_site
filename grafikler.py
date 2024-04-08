import pandas as pd
import dash
from dash import dcc,html
import plotly.graph_objects as go
import plotly.express as px

colors   = {"background":"#2A2F34 ","background2":"#D5DBDB","text":"#17202A","myfav":"#D94829","grid":"#B6C1CB","bar":"#2E86C1"}
colors_1 = {"1":"#383737 ","2":"#4D4E4F","3":"#662549","4":"#AE445A","5":"#F39F5A","6":"#FEF5E7"}
colors_2 = ["#1E8449","#A93226","#6C3483"]
class Grafikler:
    def __init__(self,df,title=""):
        self.df = df
        self.title = df.columns[1]


    def barPlot(self,sonDonemSayisi=5):
        maksDonem = len(self.df[self.df.columns[1]].values)
        if sonDonemSayisi > maksDonem:
            sonDonemSayisi = maksDonem 
        
        x_val = self.df[self.df.columns[0]].values[-sonDonemSayisi:]
        y_val = self.df[self.df.columns[1]].values[-sonDonemSayisi:]
        y_val_str = [f'{val/1e9:.2f}Mr' for val in y_val]
        fig = go.Figure(data=[go.Bar(x=x_val, y=y_val, marker_color = colors["bar"],text=y_val_str,hovertemplate='<b>X:</b> %{x}<br><b>Y:</b> %{y/1e9}<br>', textposition="auto")])  # text=y_val,textposition="top"
        fig.update_layout(title=self.title,
                          title_x = 0.5,  # title centered
                          title_font=dict(color="white", size=25, family='Comic Sans MS'),
                          xaxis_title=self.df.columns[0],
                          plot_bgcolor="#17202A",
                          paper_bgcolor="#17202A",
                          yaxis=dict(title_font=dict(color="white", family='Comic Sans MS',size=14),gridcolor="#5B5858",
                                    tickfont=dict(color="white", size=14, family='Comic Sans MS')),
                          xaxis = dict(title_font=dict(color = "white",family='Comic Sans MS' ,size=14),
                                      tickfont=dict(color="white", size=14, family='Comic Sans MS'))

                          )
        
        return fig

    def linePlot(self,sonDonemSayisi=5):
        maksDonem = len(self.df[self.df.columns[1]].values)

        if sonDonemSayisi > maksDonem:
            sonDonemSayisi = maksDonem 

        x_val     = self.df[self.df.columns[0]].values[-sonDonemSayisi:]
        y_val     = self.df[self.df.columns[1]].values[-sonDonemSayisi:]
        

        fig = go.Figure(data=[go.Scatter(x=x_val, y=y_val, marker_color="#E67E22",mode="markers+lines")])
        fig.update_layout(title=self.title,
                          title_x=0.5,  # title centered
                          title_font=dict(color="white", size=25, family='Comic Sans MS'),
                          #xaxis_title=self.df.columns[0],
                          #yaxis_title=self.df.columns[1],
                          plot_bgcolor=colors_1["1"],
                          paper_bgcolor="#17202A",
                          yaxis=dict(
                                     title_font=dict(color="white", family='Comic Sans MS', size=15),gridcolor="#5B5858",
                                     tickfont=dict(color="white", size=15, family='Comic Sans MS'),zeroline=False),
                          xaxis=dict(title_font=dict(color="white", family='Comic Sans MS', size=15),gridcolor="#5B5858",
                                     tickfont=dict(color="white", size=15, family='Comic Sans MS'))
                          )
        fig.update_traces(line=dict(width=3)) 
        return fig

    def pieChart(self):
        DataDf = self.df
        colors = ["#229954","#EC7063","#CB4335"] # yesil, hafif kirmizi, koyu kirmizi
        fig = px.pie(DataDf, values=DataDf.columns[1], names=DataDf.columns[0],hole=0.5,color_discrete_sequence=colors)
        fig.update_layout(
                          plot_bgcolor="#17202A",
                          paper_bgcolor = "#17202A",
                          legend=dict(
                            orientation='h',  # Horizontal orientation
                            yanchor='middle',  # Anchor legend to the bottom
                            y=-0.1,  # Position the legend slightly below the chart
                            xanchor='center',  # Anchor legend to the right
                            x=0.5,  # Position the legend at the rightmost side
                            font = dict(size = 14, family='Comic Sans MS',color = "white")
                            )
                        )                
        return fig



