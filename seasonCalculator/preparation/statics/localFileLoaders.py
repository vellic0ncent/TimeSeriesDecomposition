import pandas as pd
from datetime import datetime
from typing import NoReturn
import os

ROOT_PATH = r".\PycharmProjects\DS-Seasonality"
ARTEFACTS_FOLDER_NAME = "Artifacts"
ARTEFACT_PATH = os.path.join(ROOT_PATH, ARTEFACTS_FOLDER_NAME)
ENCODING = "cp1251"
SEP = ";"


def save_to_csv(dataframe: pd.DataFrame,
                result_file_name: str = None, today: str = datetime.today().date().isoformat(),
                path: str = ARTEFACT_PATH, file_format: str = ".csv") -> NoReturn:
    dataframe.to_csv(os.path.join(
        path, "_".join([result_file_name, today])) + file_format, encoding=ENCODING, index=False, sep=SEP)
