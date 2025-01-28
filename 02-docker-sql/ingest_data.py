import psycopg2
import os
import csv

# Параметры подключения к базе данных
DB_SETTINGS = {
    "dbname": "ny_taxi",
    "user": "root",
    "password": "root",
    "host": "localhost",
    "port": 5432,
}

# Путь к папке с файлами
DATA_FOLDER = "data"

# Размер чанка (количество строк для загрузки за раз)
CHUNK_SIZE = 10000

def sanitize_table_name(file_name):
    """Приводит имя таблицы в формат, совместимый с PostgreSQL."""
    table_name = os.path.splitext(file_name)[0]  # Убираем расширение
    return table_name.replace("-", "_").lower()  # Меняем "-" на "_"


def infer_column_types(csv_file):
    """Определяет типы данных для каждой колонки на основе первой строки данных."""
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)  # Получаем заголовки
        first_row = next(reader)  # Читаем первую строку данных

    column_types = []
    for value in first_row:
        if value.isdigit():
            column_types.append("INT")
        else:
            try:
                float(value)  # Проверяем, можно ли преобразовать в float
                column_types.append("FLOAT")  # Указываем тип FLOAT для дробных чисел
            except ValueError:
                column_types.append("VARCHAR(255)")  # Если это не число, задаем VARCHAR

    return headers, column_types



def create_table_query(table_name, headers, column_types):
    """Генерирует SQL-запрос для создания таблицы."""
    columns = ", ".join(
        f"{header} {col_type}" for header, col_type in zip(headers, column_types)
    )
    print(f"SQL statement")
    print(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
    return f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"


def load_large_csv_to_table(conn, file_name):
    """Создает таблицу и загружает данные из большого CSV файла частями."""
    table_name = sanitize_table_name(file_name)  # Имя таблицы из имени файла
    file_path = os.path.join(DATA_FOLDER, file_name)

    # Определяем заголовки и типы данных
    headers, column_types = infer_column_types(file_path)

    # Генерируем запрос на создание таблицы
    create_table_sql = create_table_query(table_name, headers, column_types)

    with conn.cursor() as cursor:
        # Создаем таблицу
        print(f"Создаю таблицу {table_name}...")
        cursor.execute(create_table_sql)
        conn.commit()

        # Загружаем данные частями
        print(f"Загружаю данные из файла {file_name} частями...")
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            next(reader)  # Пропускаем заголовки

            chunk = []
            for i, row in enumerate(reader, start=1):
                chunk.append(row)
                if i % CHUNK_SIZE == 0:
                    insert_chunk(conn, table_name, headers, chunk)
                    chunk = []  # Очищаем чанк

            # Загружаем оставшиеся строки
            if chunk:
                insert_chunk(conn, table_name, headers, chunk)

        conn.commit()
        print(f"Данные из файла {file_name} успешно загружены в таблицу {table_name}!")


def insert_chunk(conn, table_name, headers, chunk):
    """Вставляет часть данных в таблицу."""
    with conn.cursor() as cursor:
        # Создаем строку для вставки данных
        placeholders = ", ".join(["%s"] * len(headers))
        insert_sql = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({placeholders})"
        cursor.executemany(insert_sql, chunk)
        conn.commit()


def main():
    # Подключение к базе данных
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        print("Успешное подключение к базе данных!")

        # Обрабатываем все CSV файлы в папке
        for file_name in os.listdir(DATA_FOLDER):
            if file_name.endswith(".csv"):
                print(f"Starting insert {file_name} in DB")
                load_large_csv_to_table(conn, file_name)
                print(f"Ending insert {file_name} in DB")


    except Exception as e:
        print(f"Ошибка подключения или выполнения операции: {e}")

    finally:
        if conn:
            conn.close()
            print("Подключение к базе данных закрыто.")


if __name__ == "__main__":
    main()
