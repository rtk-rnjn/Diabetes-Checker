from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps
from typing import TYPE_CHECKING, Any, Callable, Literal, TypedDict

if TYPE_CHECKING:
    from quart import Request


class _MissingSentinel:
    __slots__ = ()

    def __eq__(self, other) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self):
        return "..."


MISSING: Any = _MissingSentinel()


class Data(TypedDict):
    age: int
    bmi: float
    hb1ac_level: float
    blood_glucose_level: float
    heart_disease: int
    gender: Literal["Male", "Female"]
    hypertension: int
    smoking_history: Literal["never", "former", "current"]


def converter(
    entity: str | None, check: Callable[..., bool], func: Callable[..., Any]
) -> Any:
    if not entity:
        return None

    if check(entity):
        return func(entity)


def get_data(req: Request) -> Data:
    age = converter(req.args.get("age"), lambda x: x.isdigit(), int)
    weight = converter(req.args.get("weight"), lambda x: x.isdigit(), float)
    height = converter(req.args.get("height"), lambda x: x.isdigit(), float)
    hb1ac_level = converter(req.args.get("hb1acLevel"), lambda x: x.isdigit(), float)
    heart_disease = converter(req.args.get("heartDisease"), lambda x: x.isdigit(), int)
    blood_glucose_level = converter(
        req.args.get("bloodGlucoseLevel"), lambda x: x.isdigit(), float
    )

    gender = converter(req.args.get("gender"), lambda x: x in ("Male", "Female"), str)
    hypertension = converter(req.args.get("hypertension"), lambda x: x.isdigit(), int)
    smoking = converter(
        req.args.get("smoking"), lambda x: x in ("never", "former", "current"), str
    )
    bmi = weight / ((height / 100) ** 2)

    return {
        "age": age,
        "bmi": bmi,
        "hb1ac_level": hb1ac_level,
        "blood_glucose_level": blood_glucose_level,
        "heart_disease": heart_disease,
        "gender": gender,
        "hypertension": hypertension,
        "smoking_history": smoking,
    }


class ToAsync:
    def __init__(self, *, executor: ThreadPoolExecutor | None = None) -> None:
        self.executor = executor

    def __call__(self, blocking) -> Callable:
        @wraps(blocking)
        async def wrapper(*args, **kwargs) -> Any:
            loop = asyncio.get_event_loop()
            if not self.executor:
                self.executor = ThreadPoolExecutor()

            func = partial(blocking, *args, **kwargs)

            return await loop.run_in_executor(self.executor, func)

        return wrapper
