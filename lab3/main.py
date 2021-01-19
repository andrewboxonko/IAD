import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from tabulate import tabulate

covid_by_area_hosp = pd.read_csv('covid19_by_area_type_hosp_dynamics.csv')
areas = covid_by_area_hosp['registration_area'].unique()
dates = covid_by_area_hosp['zvit_date'].unique()


def heat_map(df):
    sns.heatmap(df, cmap=sns.color_palette("mako", as_cmap=True), linewidths=.5)
    plt.show()


def crosscorr(x, y, lag):
    corr = x.corr(y)
    max_lag, max_corr = 0, 0
    for i in [x for x in range(-lag, lag + 1) if x != 0]:
        max_corr = x.corr(y.shift(i))
        if corr < max_corr:
            corr = max_corr
            max_lag = i
    return corr, max_lag


def rename(df):
    df.rename(columns={'new_susp': 'Підозр', 'new_confirm': 'Виявлено', 'active_confirm': 'Хворіє',
                       'new_death': 'Смертей', 'new_recover': 'Одужало'}, inplace=True)


df = pd.DataFrame()
rename(covid_by_area_hosp)

df['Date'] = dates[::-1]

for index, i in enumerate(areas):
    sick = [0] * (len(dates))
    area = covid_by_area_hosp.loc[covid_by_area_hosp['registration_area'] == i].groupby(
        ["zvit_date"]).sum()['Хворіє'] \
        .reset_index()
    for j in range(len(list(area['Хворіє']))):
        sick[j] = list(area['Хворіє'])[::-1][j]
    df[i] = sick[::-1]

# print(tabulate(df, headers='keys', tablefmt='psql'))
# print(tabulate(df.corr(), headers='keys', tablefmt='psql'))


# lag_corr, corr = pd.DataFrame(columns=areas, index=areas), pd.DataFrame(columns=areas, index=areas)
#
# for i in areas:
#     arr = []
#     for j in areas:
#         arr.append(crosscorr(df[i], df[j], 250))
#     temp1 = [j[0] for j in arr]
#     temp2 = [j[1] for j in arr]
#     corr[i] = temp1
#     lag_corr[i] = temp2
#
# corr.to_csv('corr_table.csv')
# lag_corr.to_csv('lag_table.csv')

corr = pd.read_csv('corr_table.csv', header=0, index_col=0)
lag_corr = pd.read_csv('lag_table.csv', header=0, index_col=0)

print(tabulate(lag_corr, headers='keys', tablefmt='psql'))
print(tabulate(corr, headers='keys', tablefmt='psql'))

heat_map(corr), heat_map(lag_corr)
#
# leader = df.set_index('Date').iloc[-1:].idxmax(axis=1)[0]
#
top_4 = df.tail(1).set_index('Date').apply(pd.Series.nlargest, axis=1, n=4).columns

for i in top_4:
    leader_area = df[i]

    for area in areas:
        if lag_corr.at[area, i] >= 0:
            continue
        analyzed_area = df[area]
        lag = lag_corr.at[area, i]
        shifted_analyzed, shifted_leader = analyzed_area.shift(lag)[:lag], leader_area[:lag]

        leader_train, leader_test, shifted_train, shifted_test = train_test_split(shifted_leader, shifted_analyzed,
                                                                                  test_size=7, shuffle=False)

        regression = LinearRegression().fit([[i] for i in leader_train], [[i] for i in shifted_train])

        predict = regression.predict([[i] for i in leader_test])

        dates = df['Date'].tail(7)
        actual = df[area].tail(7)
        pred = list(np.asarray(predict).flatten())
        pred_actual = pd.DataFrame(data={'Date': dates, 'Predicted': pred, 'Actual': actual})
        print('\n' + i + ' (leader) ' + area + '\n', pred_actual)

        plt.plot(pred_actual['Date'], pred_actual['Predicted'], color='blue', label='Pred')
        plt.legend()
        plt.ylabel(area)

        plt.plot(pred_actual['Date'], pred_actual['Actual'], color='red', label='Actual')
        plt.title('Predicted data and Actual data in ' + i)
        plt.legend()
        plt.grid()
        plt.ylabel(area)

        plt.show()

        err = (np.sqrt(metrics.mean_squared_error(shifted_test, predict)) / np.mean(shifted_analyzed)) * 100

        leader_pred = regression.predict([[i] for i in shifted_leader])

        plt.scatter(leader_train, shifted_train, color='orange', s=50)
        plt.plot(shifted_leader, leader_pred, color='k')

        plt.title('Regression ' + i + ' - ' + area)
        plt.ylabel(area)
        plt.grid()
        plt.show()

        if err <= 30 and abs(lag) >= 8:

            leader_future = leader_area[lag:lag + 7]
            future_pred = regression.predict([[i] for i in leader_future])
            plt.scatter(leader_future, future_pred, color='blue', s=30)
            plt.scatter(leader_train, shifted_train, color='red', s=30)
            plt.plot(shifted_leader, leader_pred, color='k')
            plt.title('Future pred ' + i + ' - ' + area)
            plt.ylabel(area)
            plt.grid()
            plt.show()
