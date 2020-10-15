import matplotlib.pyplot as plt


def scatter_plot(df, data_type):
    df.reset_index().plot(kind='scatter', x='Date', y=data_type, color='red', legend=True)
    plt.xticks(rotation=90)
    plt.legend(data_type)
    plt.title("Scatter graphic of " + data_type, y=1.02, fontsize=22)
    plt.show()


def linear_plot(df, data_type):
    ax = plt.gca()
    df.plot(kind='line', y=data_type, ax=ax, figsize=(15, 10))
    plt.xlabel("Date", fontsize=20, labelpad=15,)
    plt.ylabel(data_type, labelpad=15, fontsize=20)
    plt.title("Line graphic of " + data_type, y=1.02, fontsize=22)
    plt.legend(fontsize=22)
    plt.show()


def bar_plot(df, data_type):
    df.groupby('Date')[data_type].nunique().plot(kind='bar', legend=True)
    plt.title("Bar graphic of " + data_type, y=1.02, fontsize=22)
    plt.legend(fontsize=13)
    plt.show()


def pie_plot(df, data_type):
    font = {'size': 25}
    plt.rc('font', **font)
    labels = list(df[data_type].unique())
    colors = ['red', 'gold', 'yellowgreen', 'blue', 'tan', 'lightskyblue', 'dodgerblue', 'cyan', 'crimson',
              'darkorange', 'deeppink', 'firebrick', 'fuchsia', 'greenyellow', 'salmon', 'sienna', 'slateblue', 'springgreen', 'tomato']
    sum = df.groupby([data_type]).size()
    sum.plot.pie(y=data_type, figsize=(15, 15), shadow=False,
                 startangle=90, autopct='%1.1f%%', labels=None, colors=colors, fontsize=22)
    plt.xlabel(data_type)
    plt.ylabel(None)
    plt.xticks(rotation=90)
    plt.legend(sorted(labels), fontsize=25)
    plt.title("Pie graphic of " + data_type, y=1.02, fontsize=25)
    plt.show()


def hist_plot(df, data_type):
    df[data_type].plot(kind='hist', legend=True)
    plt.xlabel(data_type)
    plt.title("Histogram graphic of " + data_type, y=1.02, fontsize=22)
    plt.legend(fontsize=22)
    plt.show()


def get_data():
    types = ['Temperature', 'Dew Point', 'Humidity', 'Wind Speed', 'Wind Gust', 'Pressure']
    for index, elem in enumerate(types):
        print(index + 1, ' - ', elem)
    command = [types[i - 1] for i in list((map(int, input().split(' '))))]
    return command


def menu_helper(df, func):
    types = get_data()
    for i in types:
        func(df, i)


def get_plot():
    print('Which data type do you want to display?\n'
          '1 - Scatter\n'
          '2 - Linear\n'
          '3 - Bar\n'
          '4 - Pie\n'
          '5 - Hist\n'
          'any command - exit')

    command = int(input())
    return command


def ploting(df):
    while True:
        plot = get_plot()
        if plot == 1:
            menu_helper(df, scatter_plot)
        elif plot == 2:
            menu_helper(df, linear_plot)
        elif plot == 3:
            menu_helper(df, bar_plot)
        elif plot == 4:
            print('1 - Wind\n'
                  '2 - Condition')
            types = ['Wind', 'Condition']
            command = [types[i - 1] for i in list((map(int, input().split(' '))))]
            for i in command:
                pie_plot(df, i)
        elif plot == 5:
            menu_helper(df, hist_plot)
        else:
            break
