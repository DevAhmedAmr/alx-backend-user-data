#!/usr/bin/env python3
"""
Module for handling Personal Data
"""
import logging.handlers
import re
from typing import List
import logging
import os
import mysql.connector


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the message to log .
        """
        record.msg = filter_datum(

            self.fields, self.REDACTION, record.msg, self.SEPARATOR
        )

        return super().format(record)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Filter out fields that are not in fields arg list .

    Args:
        fields (list[str]): a list of strings representing all fields to
        obfuscate

        redaction (str): a string representing by what the field will be
        obfuscated

        message (str):  a string representing the log line

        separator (str): a string representing by which character is separating
                         all fields in the log line (message)

    Returns:
        [str]:  the log message obfuscated
    """

    pattern = r"(" + "|".join(re.escape(field)
                              for field in fields) + f")=[^{separator}]*"

    return re.sub(pattern, r"\1=" + redaction, message)


def get_logger() -> logging.Logger:
    """ Get a logger for user_data .

    Returns:
        logging.Logger: logger object
    """
    logger = logging.getLogger("user_data")
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Get a mysql database connection from environment
        variables .

    Returns:
        mysql.connector.connection.MySQLConnection: [description]
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD")
    host = os.getenv("PERSONAL_DATA_DB_HOST")
    dataBase_name = os.getenv("PERSONAL_DATA_DB_NAME")
    mydb = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=dataBase_name
    )
    return mydb


PII_FIELDS = ("name", "email", "phone", "ssn", "password")
