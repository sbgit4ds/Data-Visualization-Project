import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv("supermarket_sales.csv", encoding='unicode_escape')

# df.head()

# df.dtypes

# df.info()

df['Date'] = pd.to_datetime(df['Date'])
df['Day'] = df['Date'].dt.day
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

df['Time'] = pd.to_datetime(df['Time'])

df['Hour'] = df['Time'].dt.hour

app = dash.Dash(__name__,)
app.layout = html.Div([

html.Div([
    html.Br(), html.Br(),
    html.H1('Supermarket Sales Dashboard')],
    style={'margin-left': '2%','color':'#2b2618','width': '50%', 'display': 'inline-block'

    }),

html.Div([
    html.Br(), html.Br(),
    html.H3('Prepared by: Salim Bouaichi')],
    style={'color':'#17202A','width': '30%', 'display': 'inline-block', 'float': 'right'

    }),

html.Div([
        html.Label('Select a City:'),
        dcc.Dropdown(id='c_city',
                     multi=False,
                     clearable=True,
                     value='Yangon',
                     placeholder='Select a City',
                     options=[{'label': c, 'value': c}
                              for c in (df['City'].unique())])

         ], style={'width': '10%','margin-left': '5%'}),

# Comparing quantity ordered to Unit price using bar and line charts
html.Div([
    html.Br(),
    dcc.Graph(id='bar_l1',
              config={'displayModeBar': False}),

        ],style={'margin-left': '1.4%','width': '50%', 'display': 'inline-block'}),

# Comparing Total ordered to Unit price using bar and line charts
html.Div([
    html.Br(),
    dcc.Graph(id='bar_l2',
              config={'displayModeBar': False}),

        ],style={'width': '48.6%', 'display': 'inline-block', 'float': 'right'}),

# Comparing Total ordered and quantity ordered using bar and line charts
html.Div([
    html.Br(),
    dcc.Graph(id='two_bar_3',
              config={'displayModeBar': False}),

        ],style={'margin-left': '1.4%','width': '50%', 'display': 'inline-block'}),

 # Comparing Total ordered and quantity ordered using a scatter chart
html.Div([
        html.Br(),
        dcc.Graph(id='scat_4',
                  config={'displayModeBar': False}),

    ], style={'width': '48.6%', 'display': 'inline-block', 'float': 'right', 'margin-bottom':'3%'}),


  ], style={'background-color': '#e6e6e6'})       

@app.callback(Output('bar_l1', 'figure'),
              [Input('c_city', 'value')])
def update_graph(c_city):
    product_df = df.groupby(['Product line', 'City'])['Quantity'].sum().reset_index()
    product_df2 = df.groupby(['Product line', 'City'])['Unit price'].mean().reset_index()
    return {
        'data': [go.Bar(x=product_df[product_df['City'] == c_city]['Product line'],
                        y=product_df[product_df['City'] == c_city]['Quantity'],
                        text=product_df[product_df['City'] == c_city]['Quantity'],
                        name='Quantity Ordered',
                        texttemplate='%{text:.2s}',
                        textposition='auto',
                        marker=dict(
                            color=product_df[product_df['City'] == c_city]['Quantity'],
                            colorscale='phase',
                            showscale=False),
                        yaxis='y1',
                        hoverinfo='text',
                        hovertext=
                        '<b>City</b>: ' + product_df[product_df['City'] == c_city]['City'].astype(str) + '<br>'+
                        '<b>Q.Ordered</b>: ' + [f'{x:,.0f}' for x in product_df[product_df['City'] == c_city]['Quantity']] + '<br>'+
                        '<b>Product</b>: ' + product_df[product_df['City'] == c_city]['Product line'].astype(str) + '<br>'
                        ),

                go.Scatter(
                            x=product_df2[product_df2['City'] == c_city]['Product line'],
                            y=product_df2[product_df2['City'] == c_city]['Unit price'],
                            name='Price of Product',
                            text=product_df2[product_df2['City'] == c_city]['Unit price'],
                            mode='markers + lines',
                            marker=dict(color='#bd3786'),
                            yaxis='y2',
                            hoverinfo='text',
                            hovertext=
                            '<b>City</b>: ' + product_df2[product_df2['City'] == c_city]['City'].astype(str) + '<br>'+
                            '<b>Price</b>: $' + [f'{x:,.0f}' for x in product_df2[product_df2['City'] == c_city]['Unit price']] + '<br>'+
                            '<b>Product</b>: ' + product_df2[product_df2['City'] == c_city]['Product line'].astype(str) + '<br>'
                            )],


        'layout': go.Layout(
             width=780,
             height=520,
             title={
                'text': 'Quantity ordered and unit price for each category : ' + (c_city),
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={'family': 'Times New Roman',
                        'color': 'rgb(230, 34, 144)',
                        'size': 25},

             hovermode='x',

             xaxis=dict(title='<b>Category</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(17, 37, 239)'
                        )

                ),

             yaxis=dict(title='<b>Quantity Ordered</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                        )

                ),
             yaxis2=dict(title='<b>Unit price by category ($)</b>', overlaying='y', side='right',
                         color='rgb(230, 34, 144)',
                         showline=True,
                         showgrid=False,
                         showticklabels=True,
                         linecolor='rgb(104, 204, 104)',
                         linewidth=2,
                         ticks='outside',
                         tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                         )

                 ),

             legend=dict(title='',
                         x=0.25,
                         y=1.08,
                         orientation='h',
                         bgcolor='rgba(255, 255, 255, 0)',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=12,
                              color='#000000')),
                         legend_title_font_color="green",
                         uniformtext_minsize=12,
                         uniformtext_mode='hide',

                 )

    }

@app.callback(Output('bar_l2', 'figure'),
              [Input('c_city', 'value')])
def update_graph(c_city):
# Data for bar
    product_df3 = df.groupby(['Product line', 'City'])['Total'].sum().reset_index()
# Data for line
    product_df4 = df.groupby(['Product line', 'City'])['Unit price'].mean().reset_index()

    return {
        'data': [go.Bar(x=product_df3[product_df3['City'] == c_city]['Product line'],
                        y=product_df3[product_df3['City'] == c_city]['Total'],
                        text=product_df3[product_df3['City'] == c_city]['Total'],
                        name='Total Price',
                        texttemplate='%{text:.2s}',
                        textposition='auto',
                        marker=dict(
                            color=product_df3[product_df3['City'] == c_city]['Total'],
                            colorscale='blackbody',
                            showscale=False),
                        yaxis='y1',
                        hoverinfo='text',
                        hovertext=
                        '<b>City</b>: ' + product_df3[product_df3['City'] == c_city]['City'].astype(str) + '<br>'+
                        '<b>Total</b>: $' + [f'{x:,.0f}' for x in product_df3[product_df3['City'] == c_city]['Total']] + '<br>'+
                        '<b>Product</b>: ' + product_df3[product_df3['City'] == c_city]['Product line'].astype(str) + '<br>'

                        ),

                go.Scatter(
                            x=product_df4[product_df4['City'] == c_city]['Product line'],
                            y=product_df4[product_df4['City'] == c_city]['Unit price'],
                            name='Unit Price',
                            text=product_df4[product_df4['City'] == c_city]['Unit price'],
                            mode='markers + lines',
                            marker=dict(color='#bd3786'),
                            yaxis='y2',
                            hoverinfo='text',
                            hovertext=
                            '<b>City</b>: ' + product_df4[product_df4['City'] == c_city]['City'].astype(str) + '<br>'+
                            '<b>Product</b>: ' + product_df4[product_df4['City'] == c_city]['Product line'].astype(str) + '<br>'+
                            '<b>Price</b>: $' + [f'{x:,.0f}' for x in product_df4[product_df4['City'] == c_city]['Unit price']] + '<br>'
                            )],


        'layout': go.Layout(
             width=780,
             height=520,
             title={
                'text': 'Total Price vs Unit price : ' + (c_city),
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={'family': 'Times New Roman',
                        'color': 'rgb(230, 34, 144)',
                        'size': 25},
             hovermode='x',

             xaxis=dict(title='<b>Category</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(17, 37, 239)'
                        )
                ),
             yaxis=dict(title='<b>Total Price</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                        )
                ),
             yaxis2=dict(title='<b>Unit price for each category ($)</b>', overlaying='y', side='right',
                         color='rgb(230, 34, 144)',
                         showline=True,
                         showgrid=False,
                         showticklabels=True,
                         linecolor='rgb(104, 204, 104)',
                         linewidth=2,
                         ticks='outside',
                         tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                         )
                 ),

             legend=dict(title='',
                         x=0.25,
                         y=1.08,
                         orientation='h',
                         bgcolor='rgba(255, 255, 255, 0)',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=12,
                              color='#000000')),

                         legend_title_font_color="green",
                         uniformtext_minsize=12,
                         uniformtext_mode='hide',

                 )
    }

@app.callback(Output('two_bar_3', 'figure'),
              [Input('c_city', 'value')])
def update_graph(c_city):
# Data for bar
    product_df5 = df.groupby(['Product line', 'City'])['Total'].sum().reset_index()
# Data for line
    product_df6 = df.groupby(['Product line', 'City'])['Quantity'].sum().reset_index()

    return {
        'data': [go.Bar(x=product_df5[product_df5['City'] == c_city]['Product line'],
                        y=product_df5[product_df5['City'] == c_city]['Total'],
                        text=product_df5[product_df5['City'] == c_city]['Total'],
                        name='Total Price',
                        texttemplate='%{text:.2s}',
                        textposition='auto',
                        yaxis='y1',
                        offsetgroup=1,
                        hoverinfo='text',
                        hovertext=
                        '<b>City</b>: ' + product_df5[product_df5['City'] == c_city]['City'].astype(str) + '<br>'+
                        '<b>Product</b>: ' + product_df5[product_df5['City'] == c_city]['Product line'].astype(str) + '<br>'+
                        '<b>Total Price</b>: $' + [f'{x:,.0f}' for x in product_df5[product_df5['City'] == c_city]['Total']] + '<br>'
                        ),

                go.Bar(
                            x=product_df6[product_df6['City'] == c_city]['Product line'],
                            y=product_df6[product_df6['City'] == c_city]['Quantity'],
                            name='Total Quantity',
                            text=product_df6[product_df6['City'] == c_city]['Quantity'],
                            texttemplate='%{text:.2s}',
                            textposition='auto',
                            marker=dict(color='rgb(112, 123, 124)'),
                            yaxis='y2',
                            offsetgroup=2,
                            hoverinfo='text',
                            hovertext=
                            '<b>City</b>: ' + product_df6[product_df6['City'] == c_city]['City'].astype(str) + '<br>'+
                            '<b>Product</b>: ' + product_df6[product_df6['City'] == c_city]['Product line'].astype(str) + '<br>'+
                            '<b>Total Quantity</b>: ' + [f'{x:,.0f}' for x in product_df6[product_df6['City'] == c_city]['Quantity']] + '<br>'
                            )],


        'layout': go.Layout(
             width=780,
             height=520,
             title={
                'text': 'Total and Quantity ordered of each category : ' + (c_city),
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={'family': 'Times New Roman',
                        'color': 'rgb(230, 34, 144)',
                        'size': 25},

             hovermode='x',

             xaxis=dict(title='<b>Category</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(17, 37, 239)'
                        )
                ),

             yaxis=dict(title='<b>Total Price</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                        )
                ),
             yaxis2=dict(title='<b>Total Quantity Ordered</b>', overlaying='y', side='right',
                         color='rgb(230, 34, 144)',
                         showline=True,
                         showgrid=False,
                         showticklabels=True,
                         linecolor='rgb(104, 204, 104)',
                         linewidth=2,
                         ticks='outside',
                         tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                         )
                 ),
             legend=dict(title='',
                         x=0.25,
                         y=1.08,
                         orientation='h',
                         bgcolor='rgba(255, 255, 255, 0)',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=12,
                              color='#000000')),

                         legend_title_font_color="green",
                         uniformtext_minsize=12,
                         uniformtext_mode='hide',

                 )
    }
@app.callback(Output('scat_4', 'figure'),
              [Input('c_city', 'value')])
def update_graph(c_city):
    scatter = df.groupby(['City','Product line'])[['Quantity', 'Total']].sum().reset_index()
    return {
        'data': [go.Scatter(x=scatter[scatter['City'] == c_city]['Quantity'],
                        y=scatter[scatter['City'] == c_city]['Total'],
                        text=scatter[scatter['City'] == c_city]['Total'],
                        mode='markers',
                        hoverinfo='text',
                        hovertext=
                        '<b>City</b>: ' + scatter[scatter['City'] == c_city]['City'].astype(str) + '<br>'+
                        '<b>Product</b>: ' + scatter[scatter['City'] == c_city]['Product line'].astype(str) + '<br>'+
                        '<b>Q.Ordered</b>: ' + [f'{x:,.0f}' for x in scatter[scatter['City'] == c_city]['Quantity']] + '<br>'+
                        '<b>Total</b>: $' + [f'{x:,.0f}' for x in scatter[scatter['City'] == c_city]['Total']] + '<br>',
                            marker=dict(
                                size=25,
                                color=scatter[scatter['City'] == c_city]['Quantity'],
                                colorscale='turbo',
                                showscale=False
                            )
                            )],

        'layout': go.Layout(
             width=780,
             height=520,
             title={
                'text': 'Total of ordered quantity : ' + (c_city),
                'y': 0.93,
                'x': 0.43,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={'family': 'Times New Roman',
                        'color': 'rgb(230, 34, 144)',
                        'size': 25},
             hovermode='x',

             xaxis=dict(title='<b>Quantity Ordered</b>',

                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(17, 37, 239)'
                        )
                ),
             yaxis=dict(title='<b>Total Price</b>',
                        color='rgb(230, 34, 144)',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(104, 204, 104)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='rgb(17, 37, 239)'
                        )
                ),
             )

    }


if __name__ == '__main__':
    app.run_server(debug=True)