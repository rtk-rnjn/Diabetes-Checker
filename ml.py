from __future__ import annotations

from collections import namedtuple
from typing import Literal

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

from utils import MISSING, Cache, ToAsync

Patient = namedtuple(
    "Patient",
    [
        "gender",
        "age",
        "hypertension",
        "heart_disease",
        "smoking_history",
        "bmi",
        "HbA1c_level",
        "blood_glucose_level",
    ],
)


class ML:
    _encode_gender: ColumnTransformer
    _encode_smoking: ColumnTransformer
    _inputs: list[tuple]
    _classifier: RandomForestClassifier

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.data = pd.read_csv(self.file_name)
        self.cache = Cache("cached.sqlite")

    def init(self) -> None:
        self._x = self.data.iloc[:, :-1]
        self._y = self.data.iloc[:, -1]

        self.encoded_gender()
        self.encoded_smoking()

    def encoded_gender(self) -> ColumnTransformer:
        encode_gender = ColumnTransformer(
            transformers=[("encode", OneHotEncoder(), [0])], remainder="passthrough"
        )
        self._encode_gender = encode_gender

        self._x = np.array(self._encode_gender.fit_transform(self._x))
        self._inputs = np.array(self._encode_gender.transform(self._inputs))

        return self._encode_gender

    def encoded_smoking(self) -> ColumnTransformer:
        encode_smoking = ColumnTransformer(
            transformers=[("encode", OneHotEncoder(), [6])], remainder="passthrough"
        )
        self._encode_smoking = encode_smoking

        self._x = np.array(self._encode_smoking.fit_transform(self._x))
        self._inputs = np.array(self._encode_smoking.transform(self._inputs))

        return self._encode_smoking

    def prepare_classifier(
        self, train_size: float = 0.9, random_state: int = 0
    ) -> RandomForestClassifier:
        x_train, x_test, y_train, y_test = train_test_split(
            self._x, self._y, train_size=train_size, random_state=random_state
        )

        classifier = RandomForestClassifier(n_estimators=10, random_state=0)
        classifier.fit(x_train, y_train)

        self._classifier = classifier
        return self._classifier

    async def try_cache(self, **kwargs) -> None:
        r = await self.cache.is_diabetic(**kwargs)
        return r if r != -1 else None

    @ToAsync()
    def predict(
        self,
        input_data: tuple | None = None,
        *,
        gender: Literal["Male", "Female"] = MISSING,
        age: float = MISSING,
        hypertension: int = MISSING,
        heart_disease: int = MISSING,
        smoking_history: Literal["current", "former", "never"] = MISSING,
        bmi: float = MISSING,
        hb1ac_level: float = MISSING,
        blood_glucose_level: float = MISSING,
    ) -> int:
        if input_data:
            self._inputs = [input_data]
        else:
            self._inputs = [
                Patient(
                    gender,
                    age,
                    hypertension,
                    heart_disease,
                    smoking_history,
                    bmi,
                    hb1ac_level,
                    blood_glucose_level,
                )
            ]
        self.init()
        self.prepare_classifier()

        y_pred = self._classifier.predict(self._inputs)
        return y_pred[0]


if __name__ == "__main__":
    data = Patient("Male", 78.0, 1, 1, "current", 38.05, 13.0, 190)
    ml = ML(r"quart_app/assests/datasets.csv")
    r = ml.predict(input_data=data)
    r = ml.predict(input_data=data)
    print(r)
