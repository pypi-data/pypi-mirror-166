import io
import os
import pandas as pd
from pandas.io.common import file_path_to_url

import numpy as np
from datetime import date
import logging

logger = logging.getLogger(__name__)


def get_file(file_name, file_path=None):
    dest_file = os.path.join(file_path, file_name)
    return dest_file


def get_url(file_name, file_url=None):
    dest_url = file_path_to_url(os.path.join(file_url, file_name))
    return dest_url


