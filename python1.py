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
            SELECT to_char(orders.date_order, 'Month') AS mes, SUM(orders.order_amount) AS income, COUNT(orders.order_amount) AS quantity
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
            SELECT SUM(items.weight), to_char(orders.date_order, 'Month') AS mes
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

        