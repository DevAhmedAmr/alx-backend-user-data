#!/usr/bin/env python3
"""
Module for handling Personal Data
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Filter out fields that are not in fields arg list .

    Args:
        fields (list[str]): [description]
        redaction (str): [description]
        message (str): [description]
        separator (str): [description]

    Returns:
        [type]: [description]
    """

    pattern = r"(" + "|".join(re.escape(field)
                              for field in fields) + f")=[^{separator}]*"

    print(re.search(pattern, message))

    return re.sub(pattern, r"\1=" + redaction, message)
