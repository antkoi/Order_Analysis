import dash
from dash import dcc, html
import pandas as pd
from dash.dependencies import Input, Output

file_path = 'orders_autumn_2020.csv'
data = pd.read_csv(file_path)
data['TIMESTAMP'] = pd.to_datetime(data['TIMESTAMP'])
data.set_index('TIMESTAMP', inplace=True)
daily_orders = data.resample('D').size()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Daily Order Counts'),
    dcc.Graph(id='daily-orders-plot'),
    html.P('Select date range:'),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=daily_orders.index.min(),
        end_date=daily_orders.index.max(),
        display_format='MMM D, YYYY'
    )
])

@app.callback(
    Output('daily-orders-plot', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graph(start_date, end_date):
    filtered_data = daily_orders.loc[start_date:end_date]
    
    fig = {
        'data': [{'x': filtered_data.index, 'y': filtered_data.values, 'type': 'bar'}],
        'layout': {
            'title': 'Daily Order Counts',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Number of Orders'}
        }
    }
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)