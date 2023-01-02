import time
from collections import Counter
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from plotly.offline import plot

def log_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'Execution time of {func.__name__}: {end_time - start_time} seconds')
        return result, end_time - start_time
    return wrapper

@log_execution_time
def count_words_dict(text):
    words = text.split()
    word_counts = {}
    for word in words:
        if word not in word_counts:
            word_counts[word] = 1
        else:
            word_counts[word] += 1
    return word_counts

@log_execution_time
def count_words_counter(text):
    words = text.split()
    word_counts = Counter(words)
    return word_counts

def fig_trend_series(series1, series2, series1_name, series2_name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=series1.index, y=series1, name=series1_name))
    fig.add_trace(go.Scatter(x=series2.index, y=series2, name=series2_name))
    return fig

def plot_template():
    serie1, serie2 = get_trend_series()
    fig = fig_trend_series(serie1, serie2, 'Dictionary', 'Counter')
    return plot(fig, output_type='div', include_plotlyjs=False)

def get_trend_series():
    def read_txt_file(filename):
        with open(filename, 'r') as f:
            return f.read()
    text = read_txt_file('data/shakespeare.txt')
    loop_time_log, counter_time_log = [], []
    for i in range(100):
        count1, time1 = count_words_dict(text[:100+i*100])
        count2, time2 = count_words_counter(text[:100+i*100])
        loop_time_log.append(time1)
        counter_time_log.append(time2)
    return pd.Series(loop_time_log), pd.Series(counter_time_log)

if __name__ == '__main__':
    serie1, serie2 = get_trend_series()
    fig_trend_series(serie1, serie2, 'Dictionary', 'Counter').show()
    print('Mean time taken dictionary method : ',np.mean(serie1),' seconds')
    print('Mean time taken counter method : ',np.mean(serie2),' seconds')