###############################################ячейка №1 в Google Colab#############################
#импорт пакетов
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import datetime
import pandas as pd
import psycopg2
import traceback
import threading
from google.colab import files

global connection_string #глобальная переменная строка подключения 
connection_string = 'postgresql://mg123456%40gmail.com:FTPjaeZ8I5El@ep-old-cell-77818429.eu-central-1.aws.neon.tech/MagazinoCRM_db?sslmode=require' #ваша строка подключения к БД

#создание директории для сохранения отчетов
!mkdir -p /content/reports

# Функция получения помесячной выручки из БД (сумма всех заказов, сгруппированных по месяцам)
def db_read_monthly_income_count(start, finish):
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT to_char(orders.date_order, 'Month') AS mes, ROUND(SUM(orders.order_amount)::numeric,2) AS income, COUNT(orders.order_amount) AS quantity
            FROM orders
            WHERE EXTRACT(MONTH FROM orders.date_order) BETWEEN %s::integer AND %s::integer
            GROUP BY mes
            ORDER BY (MIN(orders.date_order))
        """, (start, finish))
        results = cursor.fetchall()
        return results
    except Exception as e:  # ловить конкретные исключения и сохранять информацию об исключении в переменную 'e'
        traceback.print_exc()
        return 'Ошибка при получении данных из базы данных'
    finally:
        cursor.close() #закрыть курсор, который выполняет запросы
        conn.close()  #закрыть соединение с базой данных

# Функция получения суммарного веса всех товаров в заказах по месяцам
def db_read_products_statiscics_count(start, finish):
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT ROUND(SUM(items.weight)::numeric,2) , to_char(orders.date_order, 'Month') AS mes
            FROM items
            join order_items ON items.id=order_items.items_id
            join orders ON orders.id=order_items.order_id
            WHERE EXTRACT(MONTH FROM orders.date_order) BETWEEN %s::integer AND %s::integer
            GROUP BY mes
            ORDER BY (SUM(items.weight))          
        """, (start, finish))
        results = cursor.fetchall()
        return results
    except Exception as e:  # ловить конкретные исключения и сохранять информацию об исключении в переменную 'e'
        traceback.print_exc()
        return 'Ошибка при получении данных из базы данных'
    finally:
        cursor.close() #закрыть курсор, который выполняет запросы
        conn.close()  #закрыть соединение с базой данных


###############################################ячейка №3 в Google Colab############################################################################
start = 1 #месяц начала сбора статистики
finish = 12 #месяц окончания сбора статистики

# Создание DataFrame c получением помесячной выручки из БД (сумма всех заказов, сгруппированных по месяцам)
df = pd.DataFrame(db_read_monthly_income_count(start, finish), columns=['МЕСЯЦ', 'ДОХОД', 'КОЛИЧЕСТВО ЗАКАЗОВ'])

# Создание DataFrame с получением суммарного веса всех товаров в заказах по месяцам
df2 = pd.DataFrame(db_read_products_statiscics_count(start, finish), columns=['Суммарный вес', 'Месяц'])

# Получаем текущую дату
current_date = datetime.datetime.now()

# Форматируем дату в строку (например, '2023-12-02')
date_str = current_date.strftime('%Y-%m-%d')

# Создание PDF-файла для сохранения графиков и таблиц. В название файла включаем текущую дату
filename = '/content/reports/report_' + date_str + '.pdf'

# Запись данных в PDF-файл
with PdfPages(filename) as pdf:

# подробности по месячной выручке
    # Создание фигуры и осей для таблицы
    fig_table, ax_table = plt.subplots(figsize=(8, 6))  # Выберите подходящий размер фигуры

    # Задание заголовка
    ax_table.set_title(f"Доходы по месяцам, с {start}-го месяца по {finish}-й месяц")

    # Задание содержимого таблицы со статистикой
    ax_table.axis('tight') # задаем границы области для таблицы так, чтобы они плотно обрамляли содержимое
    ax_table.axis('off') # выключаем отображение осей для таблицы (нет границ и делений)
    table = ax_table.table(cellText=df.values, colLabels=df.columns, loc='center') #задаем содержимое ячеек таблицы, заголовки столбцов и расположение таблицы
    table.set_fontsize(10) # устанавливаем размер шрифта для текста в таблице вручную
    table.scale(1.2, 1.2)  # Можно изменить масштаб таблицы для лучшего отображения

    # Сохранение в pdf и закрытие страницы в файле, чтобы освободить память, связанную с этим объектом Figure в Matplotlib
    pdf.savefig(fig_table)
    plt.close(fig_table)

    # Создание фигуры и осей для гистограммы
    fig_hist, ax_hist = plt.subplots(figsize=(14, 6))  # Выберите подходящий размер фигуры

    # Установим метки на оси X с названиями месяцев
    ax_hist.set_xticks(range(1+len(df['МЕСЯЦ'])))

    # Строим столбики гистограммы
    ax_hist.bar(df['МЕСЯЦ'], df['ДОХОД'], width=0.4, edgecolor="white", label='доход за месяц', linewidth=0.7)

    # Рисуем число заказов
    ax_hist.plot(df['МЕСЯЦ'], 5000*df['КОЛИЧЕСТВО ЗАКАЗОВ'], 'r', label='количество заказов (в масштабе x5000)', linewidth=2.0)

    # Задание содержимого таблицы со статистикой
    ax_hist.set_title(f"Доход от заказов и их количество по месяцам, с {start}-го месяца по {finish}-й месяц")

    #Задание осей гистограммы
    ax_hist.set_xlabel('Месяц')
    ax_hist.set_ylabel('Доход')

    # Добавляем легенду на график
    ax_hist.legend()

    #Сохранение в pdf и закрытие страницы в файле, чтобы освободить память, связанную с этим объектом Figure в Matplotlib
    pdf.savefig(fig_hist)
    plt.close(fig_hist)

    # Создание фигуры и осей для таблицы
    fig_table, ax_table = plt.subplots(figsize=(8, 6))  # Выберите подходящий размер фигуры


# для суммарного веса товаров по месяцам
    #Задание заголовка
    ax_table.set_title(f"Суммарный вес товаров, с {start}-го месяца по {finish}-й месяц")
    
    # Задание содержимого таблицы со статистикой
    ax_table.axis('tight') #задаем границы области для таблицы так, чтобы они плотно обрамляли содержимое
    ax_table.axis('off') #выключаем отображение осей для таблицы (нет границ и делений)
    table = ax_table.table(cellText=df2.values, colLabels=df2.columns, loc='center') #задаем содержимое ячеек таблицы, заголовки столбцов и расположение таблицы
    #table.auto_set_font_size(True)
    table.set_fontsize(10) #устанавливаем размер шрифта для текста в таблице вручную
    table.scale(1.2, 1.2)  # Можно изменить масштаб таблицы для лучшего отображения

    #Сохранение в pdf и закрытие страницы в файле, чтобы освободить память, связанную с этим объектом Figure в Matplotlib
    pdf.savefig(fig_table)
    plt.close(fig_table)

# Скачиваем файл на локальную машину
files.download(filename)
