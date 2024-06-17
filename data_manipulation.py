import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import Error
import pandas as pd
from sqlalchemy import update, URL, create_engine
from sqlalchemy.orm import sessionmaker
from DB import Users, Trips, UserTrips, SavedCategory, ClimatData, DymanicSearchTips, \
    MeteostationInfo, DataMeteostations, MeteostationAverageDATA
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
import re
import math
import random
import gzip
import shutil
import os
import re
import openpyxl as oxl
import pandas as pd
import pyexcel as p
import json
import traceback


# china_meteo_stations_index = df['Синоптический индекс'].loc[df['Страна']=='China']
# china_meteo_stations_index = china_meteo_stations_index.to_list()





class MiningData:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.get('https://rp5.ru/Архив_погоды_в_Шицзячжуане')
        # print(self.browser)

    def random_sleep(self, mode):
        if mode == 1:
            return random.randint(1, 3)
        elif mode == 2:
            return random.randint(2, 4)
        elif mode == 3:
            return random.randint(3, 6)

    def close_ad_vidget(self):
        try:
            geo_vidget = self.browser.find_element(By.ID, 'geo-vidget-close')
            geo_vidget.click()  # Закрыть рекламу
            sleep(self.random_sleep(mode=2))
        except Exception as err:
            print(err)

    def station_input(self, index, seconds=10):
        try:
            index_station_input = self.browser.find_element(By.NAME, 'wmo_id')
            index_station_input.clear()
            index_station_input.send_keys(index)  # Очистить и ввести номер метеостанции
            sleep(self.random_sleep(1))
            WebDriverWait(self.browser, seconds).until_not(
                expected_conditions.text_to_be_present_in_element_attribute((By.NAME, 'wmo_id'), 'class', 'ac_loading'))
            sleep(self.random_sleep(2))
            index_station_input.send_keys(Keys.ENTER)
            sleep(self.random_sleep(3))
        except Exception as err:
            print(err)
            print(f'station - {index}')
            # global not_found_stations
            # not_found_stations.append(index)
            return 'continue'

    def go_archive(self, browser):
        try:
            download_archive_button = browser.find_element(By.ID, 'tabSynopDLoad')
            download_archive_button.click()  # Перейти в раздел с архивом данных
            sleep(self.random_sleep(2))
        except Exception as err:
            print(err)
    def set_dates(self, end_data, start_data='01.02.2005'):
        try:
            data_calender_start = self.browser.find_element(By.ID, 'calender_dload')
            data_calender_start.clear()
            data_calender_start.send_keys(start_data)  # Очистить и ввести дату начала
            sleep(self.random_sleep(3))
            data_calender_start.send_keys(Keys.ESCAPE)
            data_calender_end = self.browser.find_element(By.ID, 'calender_dload2')
            data_calender_end.clear()
            data_calender_end.send_keys(end_data)  # Очистить и ввести дату начала
            sleep(self.random_sleep(3))
            data_calender_end.send_keys(Keys.ESCAPE)
        except Exception as err:
            print(err)
        # sleep(random_sleep(1))

    def set_format_csv(self):
        try:
            input_format_radio = self.browser.find_element(By.XPATH,
                                                           "//tr[@class='menu-row3']/td[3]/label[@class='input_radio']")
            input_format_radio.click()  # Формат - CSV
            sleep(self.random_sleep(2))
        except Exception as err:
            print(err)


    def set_format_coding_utf8(self):
        try:
            coding_radio = self.browser.find_element(By.XPATH, "//tr[@class='menu-row4']/td[3]/label[@class='input_radio']")
            coding_radio.click()  # UTF-8
            sleep(self.random_sleep(2))
        except Exception as err:
            print(err)
    def get_download_url(self):
        try:
            download_button_get_url = self.browser.find_element(By.XPATH,
                                                                "//td[@class='download'][1]/div[@class='archButton']/div[@class='inner']")
            download_button_get_url.click()  # Получить ссылку на скачивание
            sleep(self.random_sleep(3))
        except Exception as err:
            print(err)
    def download_data_from_station(self):
        try:
            WebDriverWait(self.browser, 10).until(
                expected_conditions.element_to_be_clickable((By.XPATH, "//span[@id='f_result']/a")))
            download_button = self.browser.find_element(By.XPATH, "//span[@id='f_result']/a")
            download_button.click()  # Скачать
            sleep(self.random_sleep(1))
        except Exception as err:
            print(err)

def start_process():
    try:
        skip_indexes = []
        # engine = create_engine("postgresql+psycopg2://postgres:hf,jnf67yt@localhost/fqw")
        engine = create_engine(
            "postgresql+psycopg2://fqw_owner:9ZtOP6dnYbKC@ep-snowy-rain-a2h4f9s6.eu-central-1.aws.neon.tech/fqw?sslmode=require")
        engine.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        existing_stations_index = session.query(DataMeteostations.index_meteostation).group_by(
            DataMeteostations.index_meteostation).all()
        china_indexies_station = session.query(MeteostationInfo.index_meteostation).filter(MeteostationInfo.country=='Российская Федерация').all()
        session.commit()

        md = MiningData()
        sleep(md.random_sleep(mode=3))
        md.close_ad_vidget()
        md.station_input(china_indexies_station[0])
        md.go_archive(md.browser)
        md.set_dates('09.06.2024')
        md.get_download_url()
        md.download_data_from_station()
        existing_stations_index = [i[0] for i in existing_stations_index]
        for index in china_indexies_station[1:]:
            # print(index)
            # print(not(index[0] in existing_stations_index))
            if not(index[0] in existing_stations_index):
                mode = md.station_input(index[0], seconds=20)
                if mode == 'continue':
                    print(index[0])
                    skip_indexes.append(index[0])
                    continue
                md.get_download_url()
                md.download_data_from_station()
            else:
                print(index[0])
                skip_indexes.append(index[0])
        md.browser.quit()
    # return 0

    except Exception as e:
        print(e)
        traceback.print_exc()
        session.close()
        engine.dispose()
    finally:
        with open('skiped_indexes', 'a') as f:
            for index in skip_indexes:
                f.write(f'{index}\n')
        session.close()
        engine.dispose()




def get_insert_data_meteostation():
    url = "http://meteomaps.ru/meteostation_codes.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    html = requests.get(url, headers=headers)
    bs = BeautifulSoup(html.content, 'html.parser')
    meteo_indexes = []
    for row in bs.find_all(name='tr'):
        meteo_indexes.append([x.get_text() for x in row.find_all(name='td')])
    df = pd.DataFrame(meteo_indexes[1:], columns=meteo_indexes[0])
    df['Высота над уровнем моря, м'].loc[df['Высота над уровнем моря, м'] == ''] = '120'
    df['Широта, °'] = df['Широта, °'].apply(lambda x: x.replace(',', '.')).astype(float)
    df['Долгота, °'] = df['Долгота, °'].apply(lambda x: x.replace(',', '.')).astype(float)
    df['Высота над уровнем моря, м'] = df['Высота над уровнем моря, м'].astype(int)
    df['Синоптический индекс'] = df['Синоптический индекс'].astype(int)
    try:
        engine = create_engine("postgresql+psycopg2://postgres:hf,jnf67yt@localhost/fqw")
        # engine = create_engine(
        #     "postgresql+psycopg2://fqw_owner:9ZtOP6dnYbKC@ep-snowy-rain-a2h4f9s6.eu-central-1.aws.neon.tech/fqw?sslmode=require")
        engine.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        for item in [tuple(i) for i in df.values.tolist()]:
            session.add(MeteostationInfo(index_meteostation=int(item[0]), name_meteostation=item[1],
                                         lattitude=float(item[2]), longitude=float(item[3]), HSL=int(item[4]),
                                         country=item[5]))
        session.commit()
    except Exception as e:
        print(e)
        traceback.print_exc()
        session.close()
        engine.dispose()
    finally:
        session.close()
        engine.dispose()


def get_indexes_meteostation(country):
    try:
        engine = create_engine("postgresql+psycopg2://postgres:hf,jnf67yt@localhost/fqw")
        # engine = create_engine(
        #     "postgresql+psycopg2://fqw_owner:9ZtOP6dnYbKC@ep-snowy-rain-a2h4f9s6.eu-central-1.aws.neon.tech/fqw?sslmode=require")
        engine.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        china_meteo_stations_index = session.query(MeteostationInfo.index_meteostation).filter(
            MeteostationInfo.country == country).all()
        session.commit()
        china_meteo_stations_index = [i[0] for i in china_meteo_stations_index]
        print(china_meteo_stations_index)
    except Exception as e:
        print(e)
        session.close()
        engine.dispose()
    finally:
        session.close()
        engine.dispose()


def data_transfer():
    pattern = re.compile(r'\d{5}.01.02.2005.*.utf8.0{8}.xls.gz')
    # Указываем путь к директории
    directory = r"C:\Users\filos\Downloads"
    dir = r"D:\data\new"
    # Получаем список файлов
    # Распаковка архива, преобразование файла .xls к .xlsx
    filtered_files = [f for f in os.listdir(directory) if pattern.match(f)]
    os.chdir(dir)
    for name in filtered_files:
        file = name[:len(name) - 3]
        with gzip.open(directory + "\\" + name, 'rb') as file_in, open(dir + "\\" + file, 'wb') as file_out:
            shutil.copyfileobj(file_in, file_out)
        print(directory + "\\" + name)
        # os.remove(directory + "\\" + name)
        p.save_book_as(file_name=dir + "\\" + file, dest_file_name=dir + "\\" + file + 'x')
        print(dir + "\\" + file)
        os.remove(dir + "\\" + file)
        wb = oxl.load_workbook(dir + "\\" + file + 'x')
        wb['Архив Погоды rp5'].delete_rows(1, amount=5)
        wb.save(dir + "\\" + file + 'x')
        # Сохранение данных в csv формате из xlsx
        data = pd.read_excel(dir + "\\" + file + 'x', 'Архив Погоды rp5', index_col=None)
        print(dir + "\\" + file + 'x')
        os.remove(dir + "\\" + file + 'x')
        # data.to_csv(dir + "\\" + file[:len(file) - 5] + '.csv', encoding='utf-8', sep='|', index=False, header=False)
        data.to_csv(dir + "\\" + file[:len(file) - 5] + '.csv', encoding='utf-8', sep='|', index=False, header=False)
        with open(dir + "\\" + file[:len(file) - 5] + '.csv', encoding='utf-8') as old, open(dir + "\\" + file[:5] + '.csv', 'w', encoding='utf-8') as new:
            lines = old.readlines()
            new_lines = []
            new_lines.append('station_index|date_time|T|Tn|Tx'+'\n')
            for line in lines[1:]:
                line = line.split('|')
                new_lines.append(name[:5] + '|' + line[0] + '|' + line[1] + '|' + line[14] + '|' + line[15] + '\n')
                # new_lines.append(name[:5] + '|' + line.replace('"', "'"))
            new.writelines(new_lines)
        print(dir + "\\" + file[:len(file) - 5] + '.csv')
        os.remove(dir + "\\" + file[:len(file) - 5] + '.csv')



def insert_meteo_data():
    try:
        engine = create_engine("postgresql+psycopg2://postgres:hf,jnf67yt@localhost/fqw")
        # engine = create_engine(
        #     "postgresql+psycopg2://fqw_owner:9ZtOP6dnYbKC@ep-snowy-rain-a2h4f9s6.eu-central-1.aws.neon.tech/fqw?sslmode=require")
        engine.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        os.chdir(r"D:\data\new")
        files = [f for f in os.listdir(r"D:\data\new")]
        for file in files:
            # print(file)
            with open(file, 'r',  encoding='utf-8') as f:
                lines = f.readlines()
                lines = lines[1:]
                lines.reverse()
                for line in lines:
                    line = line.replace('\n', '').split('|')
                    session.add(DataMeteostations(index_meteostation=line[0], date_time=line[1], temperature=line[2], Tn=line[3], Tx=line[4]))
                session.commit()
    except Exception as e:
        print(e)
        session.close()
        engine.dispose()
    finally:
        session.close()
        engine.dispose()


def climat_china():
    try:
        engine = create_engine("postgresql+psycopg2://postgres:hf,jnf67yt@localhost/fqw")
        # engine = create_engine(
        #     "postgresql+psycopg2://fqw_owner:9ZtOP6dnYbKC@ep-snowy-rain-a2h4f9s6.eu-central-1.aws.neon.tech/fqw?sslmode=require")
        engine.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        with open('climat_china.txt', 'r', encoding='utf-8') as f:
            data = [i.replace('\n', '').split('|') for i in f.readlines()]
        new_data = {}
        for i in data:
            new_data[i[0]] = {'t_max': float(i[1]), 't_min': float(i[2]), 'p': float(i[3]), 'ufI': int(i[4])}
        session.add(ClimatData(country='china', climat_data=json.dumps(new_data, ensure_ascii=False)))
        session.commit()
    except Exception as e:
        print(e)
        session.close()
        engine.dispose()
    finally:
        session.close()
        engine.dispose()


def cities_china():
    try:
        engine = create_engine("postgresql+psycopg2://postgres:hf,jnf67yt@localhost/fqw")
        # engine = create_engine(
        #     "postgresql+psycopg2://fqw_owner:9ZtOP6dnYbKC@ep-snowy-rain-a2h4f9s6.eu-central-1.aws.neon.tech/fqw?sslmode=require")
        engine.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        with open('cities_china.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            item = line.replace('\n', '').replace('\t', '').replace(' ', '').split('|')
            session.add(DymanicSearchTips(name=item[0], region=item[1], lon=float(item[2]), lat=float(item[3]),
                                          country=item[4]))
        session.commit()
    except Exception as e:
        print(e)
        session.close()
        engine.dispose()
    finally:
        session.close()
        engine.dispose()


def preparation_data_to_convert_average():
    try:
        engine = create_engine("postgresql+psycopg2://postgres:hf,jnf67yt@localhost/fqw")
        # engine = create_engine(
        #     "postgresql+psycopg2://fqw_owner:9ZtOP6dnYbKC@ep-snowy-rain-a2h4f9s6.eu-central-1.aws.neon.tech/fqw?sslmode=require")
        engine.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        data = session.query(DataMeteostations.index_meteostation, DataMeteostations.date_time,
                      DataMeteostations.temperature, DataMeteostations.Tn, DataMeteostations.Tx).all()

        session.commit()

        df = pd.DataFrame(data, columns=['index', 'date', 't', 'tn', 'tx'])
        df[['t', 'tn', 'tx']] = df[['t', 'tn', 'tx']].replace([''], -10000)
        df['t'] = df['t'].astype(float)
        df['tn'] = df['tn'].astype(float)
        df['tx'] = df['tx'].astype(float)
        # print(df.head())
        df['date'] = df['date'].astype('datetime64[ns]')
        # Создаем список уникальных дат
        df['m-d'] = pd.to_datetime(df['date']).dt.strftime('%m-%d')# Извлекаем день и месяц и форматируем без года
        df['h'] = pd.to_datetime(df['date']).dt.strftime('%H')
        df.to_pickle('data.pkl')

    except Exception as e:
        print(e)
        traceback.print_exc()
        session.close()
        engine.dispose()
    finally:
        session.close()
        engine.dispose()

def average_data():
    try:
        engine = create_engine("postgresql+psycopg2://postgres:hf,jnf67yt@localhost/fqw")
        # engine = create_engine(
        #     "postgresql+psycopg2://fqw_owner:9ZtOP6dnYbKC@ep-snowy-rain-a2h4f9s6.eu-central-1.aws.neon.tech/fqw?sslmode=require")
        engine.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        # data = session.query(DataMeteostationsChina.index_meteostation, DataMeteostationsChina.date_time,
        #               DataMeteostationsChina.temperature, DataMeteostationsChina.Tn, DataMeteostationsChina.Tx).all()
        #
        # session.commit()
        #
        # df = pd.DataFrame(data, columns=['index', 'date', 't', 'tn', 'tx'])
        # # print(df.head())
        # df['date'] = df['date'].astype('datetime64[ns]')
        # # Создаем список уникальных дат
        # df['m-d'] = pd.to_datetime(df['date']).dt.strftime('%m-%d')# Извлекаем день и месяц и форматируем без года
        # df['h'] = pd.to_datetime(df['date']).dt.strftime('%H')
        df = pd.read_pickle('data.pkl')
        print(df.head())
        print(df.info())
        unique_dates = df['m-d'].unique()
        mean_values_regions = {}
        dict_station_region = {'пров.Аньхой': [54909, 54916],
                               'АРВМ': [50434, 50603, 50527, 50603, 50548, 50557, 50727, 54026, 54135, 54226, 54115,
                                        54012, 54208, 54102, 53192, 53083, 53068, 53391, 53480, 53463, 53352, 53149,
                                        53336, 53513, 53231, 52378, 52495, 53502],
                               'Шанхай': [54945, 54857],
                               'Макао': [59493, 59673],
                               'пров.Ганьсу': [52323, 52436, 52533, 52652, 52681, 52787, 56080, 52996, 56096, 53915,
                                               53923],
                               'пров.Гуандун': [59456, 59673, 59493, 59501, 59658],
                               'Гонконг': [59493, 59501, 59673],
                               'ГЧАР': [59431, 59632, 59644, 59456],
                               'пров.Гуйчжоу': [59431, 56196, 56172, 56182, 56096],
                               'пров.Ляонин': [54157, 54236, 54259, 54346, 54324, 54337, 54471, 54493, 54497, 54662],
                               'НХАР': [53614, 53705, 53723, 53915],
                               'Пекин': [54511, 54405, 54308],
                               'СУАР': [51053, 51076, 51156, 51133, 51243, 51334, 51463, 51379, 51495, 51542, 51573,
                                        52203, 51644, 51656, 51711, 51730, 51765, 51716, 51811, 51818, 51828, 51886],
                               'пров.Сычуань': [56196, 56182, 56172, 56152, 56146, 56144, 56247, 56257, 56357],
                               'ТАР': [55228, 56004, 55664, 55773, 55578, 55591, 56312, 55299, 56116, 56137],
                               'Тяньцзинь': [54527, 54534, 54511],
                               'пров.фуцзянь': [59493, 59501, 59559],
                               'пров.Хайнань': [59758, 59845, 59855, 50838, 59948],
                               'пров.Хубей': [54909, 53975, 53959, 56196, 59501],
                               'пров.Хунань': [56196, 53959, 59431, 59456, 59493],
                               'пров.Хэбэй': [54539, 54534, 54436, 54311, 54308, 54401, 54405, 54593, 54602, 53698,
                                              54618, 53798],
                               'пров.Хэйлунцзян':[50136, 50353, 50468, 50564, 50658, 50745, 50774, 50844, 50854, 50953,
                                                  50888, 50978],
                               'пров.Хэнань': [53959, 53975, 54909],
                               'пров.Цзилинь':[50844, 50949, ],
                               'пров.Цзянси': [59493, 59501, 54909],
                               'пров.Цзянсу': [54909, 54916, 54945, 54857],
                               'пров.Цинхай':[51886, 52602, 52713, 52737, 52754, 52818, 52836, 52866, 52908],
                               'пров.Чжэцзян': [54945, 54857, 59501],
                               'Чунцин': [56172, 56182, 56096, 56196],
                               'пров.Шаньдун': [54776, 54751, 54753, 54863, 54857, 54843, 54945, 54836, 54725, 54715,
                                                54826, 54808, 54916, 54909],
                               'пров.Шаньси': [53564, 53487, 53588, 53673, 53772, 53764, 53863, 53975, 53959],
                               'пров.Шэньси': [53564, 53646, 53723, 53845, 56196],
                               'пров.Юньнань': [56247, 56257, 56357, 59431]}
        for region, stations_index in dict_station_region.items():
            temp = []
            for date in unique_dates:
                mean_values = {}
                values = df[['t', 'tx', 'tn']].loc[
                    (df['m-d'] == date) & ((df['h'] == '02') | (df['h'] == '14')) & (~df['tx'].isnull()) & (
                        ~df['tn'].isnull()) & (df['index'].isin(stations_index)) & (df['t'] != -10000) & (
                                df['tn'] != -10000) & (df['tx'] != -10000)
                    ].mean().to_dict()
                mean_values['date'] = date
                mean_values['t'] = round(values['t'], 1)
                mean_values['t_max'] = round(values['tx'], 1)
                mean_values['t_min'] = round(values['tn'], 1)
                temp.append(mean_values)
            mean_values_regions[region] = temp

                # data.append(mean_values)
        # mean_values = {'date': date, 't': df[['temperature', 'rrr']].loc[df['d-m']=='13-03'].mean().to_dict() for date in unique_dates}
        with open('save_1.txt', 'w') as f:
            try:
                f.write(str(mean_values_regions))
            except Exception as e:
                print(e)
        with open('save_2.txt', 'w') as f:
            try:
                f.write(json.dumps(mean_values_regions))
            except Exception as e:
                print(e)
        with open('save_3.json', 'w') as f:
            try:
                json.dump(mean_values_regions, f)
            except Exception as e:
                print(e)
        for region, data in mean_values_regions.items():
            for elem in data:
                session.add(MeteostationAverageDATA(region=region, date=elem['date'], t=elem['t'], t_max=elem['t_max'],
                                                    t_min=elem['t_min'], country='China'))
        session.commit()

        # df_mean = pd.DataFrame(mean_values_regions)
        # print(df_mean.head())

    except Exception as e:
        print(e)
        traceback.print_exc()
        session.close()
        engine.dispose()
    finally:
        session.close()
        engine.dispose()

    # df = pd.read_csv('df.csv', sep='|')
    # df['date_time'] = df['date_time'].astype('datetime64[ns]')
    # # Создаем список уникальных дат
    # df['m-d'] = pd.to_datetime(df['date_time']).dt.strftime('%m-%d')  # Извлекаем день и месяц и форматируем без года
    # df['h'] = pd.to_datetime(df['date_time']).dt.strftime('%H')
    # unique_dates = df['m-d'].unique()
    # data = []
    # for date in unique_dates:
    #     mean_values = {}
    #     values = df[['temperature', 'tx', 'tn']].loc[
    #         (df['m-d'] == date) & ((df['h'] == '02') | (df['h'] == '14')) & (~df['tx'].isnull()) & (
    #             ~df['tn'].isnull())].mean().to_dict()
    #     mean_values['date'] = date
    #     mean_values['t'] = values['temperature']
    #     mean_values['t_max'] = values['tx']
    #     mean_values['t_min'] = values['tn']
    #     data.append(mean_values)
    # # mean_values = {'date': date, 't': df[['temperature', 'rrr']].loc[df['d-m']=='13-03'].mean().to_dict() for date in unique_dates}
    #
    # df_mean = pd.DataFrame(columns=['date', 't', 't_max', 't_min'], data=data)


def get_map():
    import folium
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    # Загружаем данные из GeoJSON
    with open('example.geojson', 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
    # Создаем карту
    map_china = folium.Map(location=[34.26, 108.34], zoom_start=4, tiles='CartoDB positron')
    # Функция стиля
    def style_function(feature):
        return {
            'fillColor': '#0000ff',
            'color': '#000000',
            'weight': 1,
            'fillOpacity': 0.5
        }
    # Функция подсветки
    def highlight_function(feature):
        return {
            'fillColor': '#0000ff',
            'color': '#000000',
            'weight': 2,
            'fillOpacity': 0.7
        }
    # Создаем FeatureGroup для каждого Feature
    feature_groups = {}
    for feature in geojson_data['features']:
        name = feature['properties']['NAME']
        if name not in feature_groups:
            feature_groups[name] = folium.FeatureGroup(name=name)
        # Добавляем GeoJson объект к FeatureGroup
        folium.GeoJson(
            data=feature,  # Используем 'feature' напрямую
            style_function=style_function,
            highlight_function=highlight_function,
            popup=feature['properties']['NAME']
        ).add_to(feature_groups[name])
    # Добавляем FeatureGroups на карту
    for feature_group in feature_groups.values():
        feature_group.add_to(map_china)

    try:
        engine = create_engine("postgresql+psycopg2://postgres:hf,jnf67yt@localhost/fqw")
        engine.connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        true_stations = session.execute(text("SELECT index_meteostation FROM data_meteostations_china "
                                             "GROUP BY index_meteostation")).all()
        session.commit()
        true_stations = tuple(i[0] for i in true_stations)
        print(true_stations)
        stations = session.execute(text("SELECT index_meteostation, lattitude, longitude FROM meteostation_info "
                                        f"WHERE index_meteostation in {true_stations}")).all()
        session.commit()
        for station in stations:
            # print(station.index_meteostation)
            folium.CircleMarker(
                location=[station.lattitude, station.longitude],
                radius=10,  # Радиус в километрах (приближенно)
                color="green",
                fill=True,
                fill_color="green",
                fill_opacity=0.5,
                popup=f"Метеостанция {station.index_meteostation}"  # Добавить название метеостанции, если есть
            ).add_to(map_china)

    except Exception as e:
        print(e)
        session.close()
        engine.dispose()
    finally:
        session.close()
        engine.dispose()

    # Добавляем контроллер слоев
    folium.LayerControl().add_to(map_china)

    # Сохраняем карту
    map_china.save('map.html')


def get_china_names():
    def random_sleep(mode):
        if mode == 1:
            return random.randint(1, 3)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    html = requests.get("https://rp5.ru/Погода_в_Китае", headers=headers)
    bs = BeautifulSoup(html.content, 'html.parser')
    random_sleep(1)
    exceptions = ['Баошань', 'Пекин', 'Тяньцзинь', 'Чунцин']
    h3 = bs.select('h3>a')
    region_links = {i.text: i.get('href') for i in h3}
    full_list = {}
    for region, link in region_links.items():
        print('===============')
        print(region)
        print('===============')
        # Страница региона с внутренним административным делением
        if region in exceptions:
            wrapper = bs.find('div', class_='countryMap')
            if region == 'Баошань':
                link_region = wrapper.find('a', string='Шанхай').get('href')
                html_city_Ex = requests.get(f"https://rp5.ru/{link_region}", headers=headers)
                city_ex = BeautifulSoup(html_city_Ex.content, 'html.parser')
                coords = city_ex.find('a', string='См. на карте').get('onclick').split(', ')
                coords = [round(float(coords[0].split('(')[1]), 2), round(float(coords[1]), 2)]
                full_list['ГЦП Шанхай'] = [
                    {'locality': 'Шанхай', 'region': 'ГЦП Шанхай', 'lat': coords[0], 'lon': coords[1]}]
                print({'locality': 'Шанхай', 'region': 'ГЦП Шанхай', 'lat': coords[0], 'lon': coords[1]})
            elif region == 'Пекин':
                link_region = wrapper.find('a', string='Пекин').get('href')
                html_city_Ex = requests.get(f"https://rp5.ru/{link_region}", headers=headers)
                city_ex = BeautifulSoup(html_city_Ex.content, 'html.parser')
                coords = city_ex.find('a', string='См. на карте').get('onclick').split(', ')
                coords = [round(float(coords[0].split('(')[1]), 2), round(float(coords[1]), 2)]
                full_list['ГЦП Пекин'] = [
                    {'locality': 'Пекин', 'region': 'ГЦП Пекин', 'lat': coords[0], 'lon': coords[1]}]
                print({'locality': 'Пекин', 'region': 'ГЦП Пекин', 'lat': coords[0], 'lon': coords[1]})
            elif region == 'Тяньцзинь':
                link_region = wrapper.find('a', string='Тяньцзинь').get('href')
                html_city_Ex = requests.get(f"https://rp5.ru/{link_region}", headers=headers)
                city_ex = BeautifulSoup(html_city_Ex.content, 'html.parser')
                coords = city_ex.find('a', string='См. на карте').get('onclick').split(', ')
                coords = [round(float(coords[0].split('(')[1]), 2), round(float(coords[1]), 2)]
                full_list['ГЦП Тяньцзинь'] = [
                    {'locality': 'Тяньцзинь', 'region': 'ГЦП Тяньцзинь', 'lat': coords[0], 'lon': coords[1]}]
                print({'locality': 'Тяньцзинь', 'region': 'ГЦП Тяньцзинь', 'lat': coords[0], 'lon': coords[1]})
            elif region == 'Чунцин':
                link_region = wrapper.find('a', string='Чунцин').get('href')
                html_city_Ex = requests.get(f"https://rp5.ru/{link_region}", headers=headers)
                city_ex = BeautifulSoup(html_city_Ex.content, 'html.parser')
                coords = city_ex.find('a', string='См. на карте').get('onclick').split(', ')
                coords = [round(float(coords[0].split('(')[1]), 2), round(float(coords[1]), 2)]
                full_list['ГЦП Чунцин'] = [
                    {'locality': 'Чунцин', 'region': 'ГЦП Чунцин', 'lat': coords[0], 'lon': coords[1]}]
                print({'locality': 'Чунцин', 'region': 'ГЦП Чунцин', 'lat': coords[0], 'lon': coords[1]})
        else:
            html_reg = requests.get(f"https://rp5.ru/{link}", headers=headers)
            bs_reg = BeautifulSoup(html_reg.content, 'html.parser')
            full_list[region] = []
            names = bs_reg.find('div', class_='countryMap').find_all('h3')
            for name in names:
                name_locality = name.find('a').text
                locals = name.find_next_sibling('div').find_all('a')
                if len(locals) == 1:
                    html_local = requests.get(f"https://rp5.ru/{name.find('a').get('href')}", headers=headers)
                    local = BeautifulSoup(html_local.content, 'html.parser')
                    random_sleep(1)
                    coords = local.find('a', string='См. на карте').get('onclick').split(', ')
                    coords = [round(float(coords[0].split('(')[1]), 2), round(float(coords[1]), 2)]
                    full_list[region].append(
                        {'locality': name_locality, 'region': f'пров.{region}', 'lat': coords[0], 'lon': coords[1]})
                    print({'locality': name_locality, 'region': f'пров.{region}', 'lat': coords[0], 'lon': coords[1]})
                elif len(locals) > 1:
                    html_locals = requests.get(f"https://rp5.ru/{locals[-1].get('href')}", headers=headers)
                    locals_bs = BeautifulSoup(html_locals.content, 'html.parser')
                    random_sleep(1)
                    for city in locals_bs.find_all('div', class_='city_link'):  # find_all for BeautifulSoup
                        city = city.find('a')
                        name_city = city.text
                        html_city = requests.get(f"https://rp5.ru/{city.get('href')}", headers=headers)
                        city_bs = BeautifulSoup(html_city.content, 'html.parser')
                        random_sleep(1)
                        coords = city_bs.find('a', string='См. на карте').get('onclick').split(', ')
                        coords = [round(float(coords[0].split('(')[1]), 2), round(float(coords[1]), 2)]
                        full_list[region].append(
                            {'locality': f'{name_city}, {name_locality}', 'region': f'пров.{region}', 'lat': coords[0],
                             'lon': coords[1]})
                        print(
                            {'locality': f'{name_city}, {name_locality}', 'region': f'пров.{region}', 'lat': coords[0],
                             'lon': coords[1]})

    with open('save_names_1.txt', 'w') as f:
        try:
            f.write(str(full_list))
        except Exception as e:
            print(e)
    with open('save_names_2.txt', 'w') as f:
        try:
            f.write(json.dumps(full_list, ensure_ascii=False))
        except Exception as e:
            print(e)
    with open('save_names_3.json', 'w') as f:
        try:
            json.dump(full_list, f, ensure_ascii=False)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # average_data()
    # get_china_names()
    start_process()

    # pattern = re.compile(r'\d{5}.*.utf8.0{8}.xls.gz')
    # # Указываем путь к директории
    # directory = r"C:\Users\filos\Downloads"
    # dir = r"D:\data"
    # # Получаем список файлов
    # # Распаковка архива, преобразование файла .xls к .xlsx
    # C:\Users\filos\.virtualenvs\dip\Scripts\python.exe
    # X:\dip\data_manipulation.py
    # stations = ['53336', '53352', '53391', '53463', '53480', '53487', '53502', '53513', '53529', '53543', '53564',
    #             '53588', '53593', '53614', '53646', '53673', '53698', '53698', '53705', '53723', '53764', '53772',
    #             '53787', '53798', '53845', '53863', '53898', '53915', '53923', '53959', '53975', '54012', '54026',
    #             '54027', '54049', '54094', '54096', '54102', '54115', '54135', '54157', '54161', '54186', '54208',
    #             '54218', '54226', '54236', '54259', '54273', '54292', '54308', '54311', '54324', '54337', '54346',
    #             '54374', '54377', '54386', '54401', '54405', '54423', '54436', '54471', '54493', '54497', '54511',
    #             '54527', '54534', '54539', '54602', '54618', '54662', '54715', '54725', '54751', '54753', '54776',
    #             '54808', '54823', '54826', '54836', '54843', '54857', '54863', '54909', '54916', '54945', '55228',
    #             '55299', '55578', '55591', '55664', '55773', '56004', '56018', '56021', '56029', '56033', '56046',
    #             '56065', '56079', '56080', '56096', '56116', '56137', '56144', '56146', '56152', '56167', '56172',
    #             '56182', '56196', '56247', '56257', '56287', '56312', '56357', '56374', '59431', '59456', '59493',
    #             '59501', '59559', '59567', '59632', '59644', '59658', '59663', '59673', '59758', '59792', '59838',
    #             '59845', '59855', '59948', '59981', '59985']
    #
    #
    # # filtered_files = [int(f[:5]) for f in os.listdir(directory) if pattern.match(f)]
    # stations = [int(i) for i in stations]
    # try:
        # skip_indexes = []
        # engine = create_engine("postgresql+psycopg2://postgres:hf,jnf67yt@localhost/fqw")
        # # engine = create_engine(
        # #     "postgresql+psycopg2://fqw_owner:9ZtOP6dnYbKC@ep-snowy-rain-a2h4f9s6.eu-central-1.aws.neon.tech/fqw?sslmode=require")
        # engine.connect()
        # Session = sessionmaker(bind=engine)
        # session = Session()
        # existing_stations_index = session.query(DataMeteostationsChina.index_meteostation).group_by(DataMeteostationsChina.index_meteostation).all()
        # china_indexies_station = session.query(MeteostationInfo.index_meteostation).filter(MeteostationInfo.country=='China').all()
        # session.commit()

    #     md = MiningData()
    #     sleep(md.random_sleep(mode=3))
    #     md.close_ad_vidget()
    #     md.station_input(stations[7])
    #     md.go_archive(md.browser)
    #     md.set_dates('09.06.2024')
    #     md.get_download_url()
    #     md.download_data_from_station()
    #     # existing_stations_index = [i[0] for i in existing_stations_index]
    #     for index in stations[8:]:
    #         # print(index)
    #         # print(not(index[0] in existing_stations_index))
    #         # if not(index[0] in existing_stations_index):
    #         mode = md.station_input(index, seconds=20)
    #         if mode == 'continue':
    #             # print(index[0])
    #             # skip_indexes.append(index)
    #             continue
    #         md.set_dates('09.06.2024')
    #         md.get_download_url()
    #         md.download_data_from_station()
    #         # else:
    #         #     print(index[0])
    #         # skip_indexes.append(index[0])
    #     md.browser.quit()
    # # return 0
    #
    # except Exception as e:
    #     print(e)
    #     traceback.print_exc()
    #     # session.close()
    #     # engine.dispose()
    # data_transfer()
    # finally:
    #     # with open('skiped_indexes', 'a') as f:
    #     #     for index in skip_indexes:
    #     #         f.write(f'{index}\n')
    #     session.close()
    #     engine.dispose()


    # print(len(filtered_files), filtered_files)
    # try:
    #     engine = create_engine("postgresql+psycopg2://postgres:hf,jnf67yt@localhost/fqw")
    #     # engine = create_engine(
    #     #     "postgresql+psycopg2://fqw_owner:9ZtOP6dnYbKC@ep-snowy-rain-a2h4f9s6.eu-central-1.aws.neon.tech/fqw?sslmode=require")
    #     engine.connect()
    #     Session = sessionmaker(bind=engine)
    #     session = Session()
    #     stations = session.query(MeteostationInfo.index_meteostation, MeteostationInfo.lattitude,
    #                          MeteostationInfo.longitude).filter(MeteostationInfo.country=='China').all()
    #
    #     session.commit()
    # except Exception as e:
    #     print(e)
    #     session.close()
    #     engine.dispose()
    # finally:
    #     session.close()
    #     engine.dispose()
    # get_china_index_meteostation
    # data_transfer()
    # insert_meteo_data()
    # average_data()

    # md = MiningData()
    # print(md.browser)

    # start_process()


# browser= webdriver.Chrome()
# browser.get('https://rp5.ru/Архив_погоды_в_Шицзячжуане')

# sleep(random_sleep(3))
# close_ad_vidget()
#
# station_input(china_meteo_stations_index[0])
# go_archive()
# set_start_date()
# get_download_url()
# download_data_from_station()
#
# for index in china_meteo_stations_index[1:]:
#     mode = station_input(index)
#     if mode == 'continue':
#         continue
#     get_download_url()
#     download_data_from_station()
# browser.quit()


# url = "http://meteomaps.ru/meteostation_codes.html"
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
# html = requests.get(url, headers=headers)
# bs = BeautifulSoup(html.content, 'html.parser')
#
# pd.set_option('display.max_rows', None)
# meteo_indexes = []
# for row in bs.find_all(name='tr'):
#     meteo_indexes.append([x.get_text() for x in row.find_all(name='td')])
# df = pd.DataFrame(meteo_indexes[1:], columns =meteo_indexes[0])
# df['Высота над уровнем моря, м'].loc[df['Высота над уровнем моря, м']==''] = '120'
# df['Широта, °'] = df['Широта, °'].apply(lambda x: x.replace(',', '.') ).astype(float)
# df['Долгота, °'] = df['Долгота, °'].apply(lambda x: x.replace(',', '.') ).astype(float)
# df['Высота над уровнем моря, м'] = df['Высота над уровнем моря, м'].astype(int)
# df['Синоптический индекс'] = df['Синоптический индекс'].astype(int)
# try:
#     # Подключение к существующей базе данных
#     conn = psycopg2.connect(user="postgres",
#                                   # пароль, который указали при установке PostgreSQL
#                                   password="hf,jnf67yt",
#                                   host="127.0.0.1",
#                                   port="5432",
#                                     database="fqw")
#     # Курсор для выполнения операций с базой данных
#     cur = conn.cursor()
#     query = """ INSERT INTO meteostation_info("index_meteostation", "name_meteostation", "lattitude", "longitude", "HSL", "country")
#                 VALUES (%s,%s,%s,%s,%s,%s)"""
#     cur.executemany(query, [tuple(i) for i in df.values.tolist()])
#     conn.commit()
# except (Exception, Error) as error:
#     print("Ошибка при работе с PostgreSQL", error)
# finally:
#     if connection:
#         cur.close()
#         conn.close()
#         print("Соединение с PostgreSQL закрыто")
