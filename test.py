import os
import pymysql

MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123456',
    'database': 'chip',
    'charset': 'utf8mb4'
}

connection = pymysql.connect(**MYSQL_CONFIG)

with connection.cursor() as cursor:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cid VARCHAR(64) NOT NULL,
            name VARCHAR(255) NOT NULL,
            `usage` TEXT,
            recommend TEXT,
            param TEXT
        )
        ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ''')