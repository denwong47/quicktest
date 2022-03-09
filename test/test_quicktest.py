import secrets
from typing import Any
import warnings

import numpy as np
import pandas as pd

import quicktest
from quicktest import TestCase

_make_float = lambda: secrets.randbelow(2**31) / (secrets.randbelow(2*30)+1)

_test_int = secrets.randbelow(2**31)
_test_float = _make_float()
_test_str = secrets.token_urlsafe(65536)
_test_bytes = secrets.token_bytes(2**10)
_test_list = [
    _make_float() for _ in range(2048)
]
_test_records = [
    {
        f"col{_id}":_make_float() \
            for _id in range(secrets.randbelow(32))
    } for _ in range(2048)
]






def test_return(
    *args,
    answer:Any,
    **kwargs,
):
    return answer

def test_exception(
    *args,
    answer:Exception,
    **kwargs,
):
    if (isinstance(
        answer,
        Exception
    )):
        raise answer
    elif (isinstance(
        answer,
        Warning,
    )):
        warnings.warn(answer)
    else:
        return test_return(
            *args,
            answer=answer,
            **kwargs
        )


class TestQuickTest(TestCase):
    
    
    def test_value(self)->None:

        _tests = [
            # Basic tests that really shouldn't go wrong
            # Test immutable values
            {
                "args":{
                    "answer": None,
                },
                "answer": None
            },
            {
                "args":{
                    "answer": _test_int,
                },
                "answer": _test_int
            },
            {
                "args":{
                    "answer": _test_float,
                },
                "answer": _test_float
            },
            {
                "args":{
                    "answer": _test_str,
                },
                "answer": _test_str
            },
            {
                "args":{
                    "answer": _test_bytes,
                },
                "answer": _test_bytes
            },
            {
                "args":{
                    "answer": (
                        _test_int,
                        _test_str,
                        _test_bytes,
                    ),
                },
                "answer": (
                    _test_int,
                    _test_str,
                    _test_bytes,
                ),
            },

            # Test mutable values
            {
                "args":{
                    "answer": [
                        _test_int,
                        _test_str,
                        _test_bytes,
                    ],
                },
                "answer": [
                    _test_int,
                    _test_str,
                    _test_bytes,
                ],
            },
            {
                "args":{
                    "answer": _test_list,
                },
                "answer": _test_list,
            },
            {
                "args":{
                    "answer": _test_records,
                },
                "answer": _test_records,
            },

            # Test Returned Exception
            {
                "args":{
                    "answer": RuntimeError("Test Error"),
                },
                "answer": RuntimeError
            },
        ]

        self.conduct_tests(
            test_return,
            _tests,
        )



    def test_exception(self)->None:
        _tests = [
            {
                "args":{
                    "answer": RuntimeError("Test Error")
                },
                "answer": RuntimeError
            },
        ]

        self.conduct_tests(
            test_exception,
            _tests,
        )



    def test_numpy(self)->None:
        _tests = [
            {
                "args":{
                    "answer": np.float64(2**0.5),
                },
                "answer": np.float64(2**0.5)
            },
            {
                "args":{
                    "answer": np.float64(2**0.5),
                },
                "answer": np.float64(2**0.5) - 1e-08
            },
            {
                "args":{
                    "answer": np.array(_test_list),
                },
                "answer": np.array(_test_list)
            },
            {
                "args":{
                    "answer": np.array(_test_list),
                },
                "answer": np.array(_test_list) - 1e-04
            },
        ]

        self.conduct_tests(
            test_return,
            _tests,
        )




    def test_pandas(self)->None:
        _tests = [
            {
                "args":{
                    "answer": pd.DataFrame.from_records(_test_records),
                },
                "answer": pd.DataFrame.from_records(_test_records),
            },
        ]

        self.conduct_tests(
            test_return,
            _tests,
        )

if (__name__=="__main__"):
    quicktest.main()

    