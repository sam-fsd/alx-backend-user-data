#!/usr/bin/env python3
"""defines  a function"""
from typing import List
import re
import logging
import os
import mysql.connector


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format the record"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(rf'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password',)


def get_logger() -> logging.Logger:
    """returns a logging object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream = logging.StreamHandler()
    stream.setFormatter(RedactingFormatter(
        fields=PII_FIELDS))
    logger.addHandler(stream)
    return logger


PERSONAL_DATA_DB_USERNAME = os.getenv('PERSONAL_DATA_DB_USERNAME')
PERSONAL_DATA_DB_PASSWORD = os.getenv('PERSONAL_DATA_DB_PASSWORD')
PERSONAL_DATA_DB_HOST = os.getenv('PERSONAL_DATA_DB_HOST')
PERSONAL_DATA_DB_NAME = os.getenv('PERSONAL_DATA_DB_NAME')
PERSONAL_DATA_DB = mysql.connector.connect(
    user=PERSONAL_DATA_DB_USERNAME or "root",
    password=PERSONAL_DATA_DB_PASSWORD or "",
    host=PERSONAL_DATA_DB_HOST or "localhost",
    database=PERSONAL_DATA_DB_NAME or "root"
)


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    return PERSONAL_DATA_DB


def main() -> None:
    """main function"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    [print(i) for i in cursor]


if __name__ == "__main__":
    main()
