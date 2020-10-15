import pandas as pd
from tabulate import tabulate
import KN310Bokhonko2


def parse_date(df):
    df['Date'] = pd.to_datetime(df['Date'] + '.2019', format='%d.%b.%Y').dt.strftime('%d.%m.%Y')


def parse_time(df):
    df['Time'] = pd.to_datetime(df['Time'], format='%I:%M %p').dt.strftime('%H:%M')


def parse_humidity(df):
    df["Humidity"] = df["Humidity"].str[:-1].astype(int) / 100


def parse_wind(df):
    df['Wind Speed'], df['Wind Gust'] = df['Wind Speed'].str[:-5].astype(int), df['Wind Gust'].str[:-5].astype(int)


def parse_pressure(df):
    df['Pressure'] = df['Pressure'].str.replace(',', '.').astype(float)


def parse():
    df = pd.read_csv('DATABASE.csv', delimiter=';')
    df = df.rename(columns={'day/month': 'Date'})
    parse_date(df)
    parse_time(df)
    parse_humidity(df)
    parse_wind(df)
    parse_pressure(df)
    df.set_index('Date', inplace=True)
    print(tabulate(df, headers='keys', tablefmt='psql'))
    return df


def main():
    df = parse()
    KN310Bokhonko2.ploting(df)


if __name__ == '__main__':
    main()
