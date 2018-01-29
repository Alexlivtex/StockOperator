import pandas as pd
import numpy as np

MAX_WINDOW_SIZE = 100

def calc_score(stock_ticker):
    data = pd.read_csv(stock_ticker)
    data = data.iloc[1:-1]
    close_list = np.asarray(data['Close'])
    date_list = np.asarray(data['Date'])
    close_list = list(close_list)
    date_list = list(date_list)

    score_list = []

    total_len = len(close_list)

    if total_len > MAX_WINDOW_SIZE:
        for quote_index in range(total_len - MAX_WINDOW_SIZE):
            time_used = 0
            for window_index in range(90):
                base_price = close_list[quote_index]
                current_price = close_list[window_index + quote_index]
                #score = ((current_price - base_price) / base_price) * 100 - 0.3 * (float(time_used) / float(MAX_WINDOW_SIZE)) * 100
                score = ((current_price - base_price) / base_price) * 100
                score_list.append(round(score, 3))
                time_used += 1
            print("The max score is {} and the date is {}".format(max(score_list), date_list[
                quote_index + score_list.index(max(score_list))]))
            print("The min score is {} and the date is {}".format(min(score_list), date_list[
                quote_index + score_list.index(min(score_list))]))
            score_list.clear()

calc_score("JD.csv")
