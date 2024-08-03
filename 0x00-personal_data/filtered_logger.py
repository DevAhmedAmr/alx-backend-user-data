#!/usr/bin/env python3
"""
Module for handling Personal Data
"""
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Filter out fields that are not in fields arg list .

    Args:
        fields (list[str]): a list of strings representing all fields to obfuscate

        redaction (str): a string representing by what the field will be obfuscated

        message (str):  a string representing the log line

        separator (str): a string representing by which character is separating
                         all fields in the log line (message)

    Returns:
        [str]:  the log message obfuscated
    """

    pattern = r"(" + "|".join(re.escape(field)
                              for field in fields) + f")=[^{separator}]*"

    return re.sub(pattern, r"\1=" + redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
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

        return super(RedactingFormatter, self).format(record)
