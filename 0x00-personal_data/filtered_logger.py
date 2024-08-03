#!/usr/bin/env python3
"""
Module for handling Personal Data
"""
import re


def filter_datum(fields: list[str], redaction: str,
                 message: str, separator: str):
    """This function is called when the datum has been modified .
    """

    pattern = r"(" + "|".join(re.escape(field)
                              for field in fields) + f")=[^{separator}]*"

    print(re.search(pattern, message))

    return re.sub(pattern, r"\1=" + redaction, message)
