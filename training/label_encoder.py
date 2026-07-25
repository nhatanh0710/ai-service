"""
label_encoder.py

Mục đích:
- Encode các cột dạng chuỗi sang số để huấn luyện mô hình.
- Lưu encoder để FastAPI có thể sử dụng lại khi dự đoán.
"""

import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder


class DatasetEncoder:
    """
    Quản lý toàn bộ Label Encoder của dataset.
    """

    def __init__(self):

        self.priority_encoder = LabelEncoder()

        self.complexity_encoder = LabelEncoder()

        self.risk_encoder = LabelEncoder()

    def fit(self, dataframe: pd.DataFrame) -> None:
        """
        Học toàn bộ giá trị của các cột dạng chuỗi.
        """

        self.priority_encoder.fit(
            dataframe["priority"]
        )

        self.complexity_encoder.fit(
            dataframe["task_complexity"]
        )

        self.risk_encoder.fit(
            dataframe["risk"]
        )

    def transform(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Chuyển đổi dữ liệu sang dạng số.
        """

        dataframe = dataframe.copy()

        dataframe["priority"] = (
            self.priority_encoder.transform(
                dataframe["priority"]
            )
        )

        dataframe["task_complexity"] = (
            self.complexity_encoder.transform(
                dataframe["task_complexity"]
            )
        )

        dataframe["risk"] = (
            self.risk_encoder.transform(
                dataframe["risk"]
            )
        )

        return dataframe

    def fit_transform(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        self.fit(dataframe)

        return self.transform(dataframe)

    def save(
        self,
        output_path: str,
    ) -> None:
        """
        Lưu encoder để FastAPI sử dụng lại.
        """

        joblib.dump(
            self,
            output_path,
        )