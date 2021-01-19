import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

# зчитуємо дані з .csv файлів
df_by_hosp = pd.read_csv('covid19_by_area_type_hosp_dynamics.csv')
df_by_settlement = pd.read_csv('covid19_by_settlement_dynamics.csv')
df_by_settlement_actual = pd.read_csv('covid19_by_settlement_actual.csv')

# масив імен деяких колонок
to_plot = ['Виявлено', 'Підозри', 'Летальні', 'Одужали', 'Хворіє']

colorArray = [
    "#63b598", "#ce7d78", "#ea9e70", "#a48a9e", "#c6e1e8", "#648177", "#0d5ac1",
    "#f205e6", "#1c0365", "#14a9ad", "#4ca2f9", "#a4e43f", "#d298e2", "#6119d0",
    "#d2737d", "#c0a43c", "#f2510e", "#651be6", "#79806e", "#61da5e", "#cd2f00",
    "#9348af", "#01ac53", "#c5a4fb", "#996635", "#b11573", "#4bb473", "#75d89e",
    "#2f3f94", "#2f7b99", "#da967d", "#34891f", "#b0d87b", "#ca4751", "#7e50a8",
    "#c4d647", "#e0eeb8", "#11dec1", "#289812", "#566ca0", "#ffdbe1", "#2f1179",
    "#935b6d", "#916988", "#513d98", "#aead3a", "#9e6d71", "#4b5bdc", "#0cd36d",
    "#250662", "#cb5bea", "#228916", "#ac3e1b", "#df514a", "#539397", "#880977",
    "#f697c1", "#ba96ce", "#679c9d", "#c6c42c", "#5d2c52", "#48b41b", "#e1cf3b"]

to_excel = pd.DataFrame()


# функція побудови лінійного графіка за заданим типом даних
def line_plot(df, data_type, flag, label, color):
    ax = plt.gca()
    if flag:
        df.plot(kind='line', y=data_type, ax=ax, figsize=(15, 10), linewidth=3, label=label, color=color)
    else:
        df.plot(kind='line', y=data_type, ax=ax, figsize=(15, 10), linewidth=5)
        plt.legend()
    plt.xlabel("Date", fontsize=23, labelpad=15)
    plt.ylabel('Dynamics', labelpad=15, fontsize=20)
    plt.grid(True)


def analyse_per_area(col):
    global df_by_hosp, to_excel
    area = df_by_hosp.loc[df_by_hosp['registration_area'] == col].groupby('zvit_date').sum().agg({'new_susp': 'cumsum',
                                                                                                  'new_confirm': 'cumsum',
                                                                                                  'new_death': 'cumsum',
                                                                                                  'new_recover': 'cumsum',
                                                                                                  })
    area['Хворіє'] = df_by_hosp.loc[df_by_hosp['registration_area'] == col].groupby('zvit_date').sum()['Хворіє']
    area.insert(0, "Область", col, True)
    area['Область'] = col
    to_excel = to_excel.append(df)
    return area


def type_to_plot():
    global to_plot
    print('Choose data to visualize')
    for index, i in enumerate(to_plot):
        print(index + 1, ' - ', i)
    return int(input())


def rename(df):
    df.rename(
        columns={'new_confirm': 'Виявлено', 'new_susp': 'Підозри', 'new_death': 'Летальні', 'new_recover': 'Одужали'},
        inplace=True)
    return df


# перейменовуємо колонку з 'active_confirm' на 'Хворіє'
df_by_hosp.rename(columns={'active_confirm': 'Хворіє'}, inplace=True)

# фільтруємо дані з датасету, і зберігаємо в новий датасет дані лише по Кіровоградській області
kirovograd = df_by_hosp.loc[df_by_hosp['registration_area'] == 'Кіровоградська']

# групуємо дані про Кіроградську область за колонкою 'zvit_date'
kirovograd_grouped = kirovograd.groupby('zvit_date').sum()

# додаємо колонку з інформацією про кількість госпіталізованих до датасету
kirovograd_grouped.insert(0, "Госпіталізації",
                          kirovograd.loc[kirovograd['is_required_hospitalization'] == 'Так'].groupby('zvit_date').sum()[
                              'new_susp'].cumsum(), True)

# додаємо колонку з інформацією про кількість підорз Covid-19 в області до датасету
kirovograd_grouped.insert(2, "Підозри", kirovograd_grouped['new_susp'].cumsum(), True)
# додаємо колонку з інформацією про кількість виявлених випадків Covid-19 в області до датасету
kirovograd_grouped.insert(4, "Виявлено", kirovograd_grouped['new_confirm'].cumsum(), True)
# додаємо колонку з інформацією про кількість летальних випадків Covid-19 в області до датасету
kirovograd_grouped.insert(7, "Летальні", kirovograd_grouped['new_death'].cumsum(), True)
# додаємо колонку з інформацією про кількість випадків одужання від Covid-19 в області до датасету
kirovograd_grouped.insert(9, "Одужали", kirovograd_grouped['new_recover'].cumsum(), True)

# виводимо згрупований датасет по Кіровоградській області
print(tabulate(kirovograd_grouped, headers='keys', tablefmt='psql'))

# динаміка захворюваннь Covid-19 в Кіровоградській області
# лінійний графік виявленних випадків Covid-19
for index, i in enumerate(to_plot):
    line_plot(kirovograd_grouped, i, False, '', colorArray[index])

# заголовок для графіка
plt.title("Динаміка Covid-19 у Кіровоградській області", y=1.02, fontsize=22)
# вивід графіка на полотно
plt.show()

areas = df_by_hosp['registration_area'].unique()

print('1 - all areas\n2 - choose which area to plot')
cmd = int(input())

if cmd == 1:
    cmd = type_to_plot()
    for index, i in enumerate(areas):
        df = analyse_per_area(i)
        df = rename(df)
        line_plot(df, to_plot[cmd - 1], True, i, colorArray[index])
    plt.title(to_plot[cmd - 1], fontsize=20)
    plt.show()

elif cmd == 2:
    cmd = type_to_plot()
    print('Choose area to visualize:')
    for index, i in enumerate(areas):
        print(index + 1, ' - ', i)
    analyze_areas = [areas[i - 1] for i in list(map(int, input().split(' ')))]
    for index, i in enumerate(analyze_areas):
        df = analyse_per_area(i)
        df = rename(df)
        line_plot(df, to_plot[cmd - 1], True, i, colorArray[index])
    plt.title(to_plot[cmd - 1], fontsize=20)
    plt.show()

# отримуємо кількість унікальних областей України
area = df_by_settlement['registration_area'].unique()
# створюємо пустий датасет
sick_by_area = pd.DataFrame(columns=['registration_area', 'sick'])

# наповнюємо датасет інформаціює про захворюваність по областях
for index, i in enumerate(area):
    res = df_by_settlement.loc[df_by_settlement['registration_area'] == i].groupby('zvit_date').sum()
    sick_by_area = sick_by_area.append({'registration_area': i, 'sick': res['active_confirm'].iloc[-1]},
                                       ignore_index=True)

print(tabulate(sick_by_area, headers='keys', tablefmt='psql'))

# сортований список районів України
region = sorted(df_by_settlement_actual['registration_region'].unique())
# масив для довготи районів
mean_lng_per_region = []
# масив для широти районів
mean_lat_per_region = []

# зберігаємо довготи в масив
for i in region:
    mean_lng_per_region.append(df_by_settlement_actual.loc[df_by_settlement_actual['registration_region'] == i][
                                   'registration_settlement_lng'].mean())

# зберігаємо широти в масив
for i in region:
    mean_lat_per_region.append(df_by_settlement_actual.loc[df_by_settlement_actual['registration_region'] == i][
                                   'registration_settlement_lat'].mean())

# групуємо за регіону і сумуємо за певними колонками
by_region = df_by_settlement_actual.groupby(['registration_region'])[
    ['total_susp', 'total_confirm', 'total_death', 'total_recover']].sum()

# додаємо нову колонку, де зберігатимемо довготу регіону
by_region['registration_settlement_lng'] = mean_lng_per_region
# додаємо нову колонку, де зберігатимемо широту регіону
by_region['registration_settlement_lat'] = mean_lat_per_region

# перейменовуємо деякі колонки
by_region.rename(columns={'total_susp': 'Підозр', 'total_confirm': 'Хворіє', 'total_death': 'Померло',
                          'total_recover': 'Одужало'}, inplace=True)

# групуємо за областями і сумуємо за певними колонками
by_area = df_by_settlement_actual.groupby(['registration_area'])[
    ['total_susp', 'total_confirm', 'total_death', 'total_recover']].sum()
# знову перейменовуємо деякі колонки
by_area.rename(columns={'total_susp': 'Підозр', 'total_confirm': 'Хворіє', 'total_death': 'Померло',
                        'total_recover': 'Одужало'}, inplace=True)

# записуємо в файл для відображення на картах
by_region.to_csv('sick_by_region.csv')
by_area.to_csv('sick_by_area.csv')

print(tabulate(by_region, headers='keys', tablefmt='psql'))
print(tabulate(by_area, headers='keys', tablefmt='psql'))

kirovograd_grouped.to_excel('kirivograd.xlsx')
by_region.to_excel('by_region_map.xlsx')
by_area.to_excel('by_area_map.xlsx')
to_excel.to_excel('analyze_area.xlsx')
