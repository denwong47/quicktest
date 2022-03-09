
import unittest

_import_exceptions = (
    ImportError,
    ModuleNotFoundError,
)

def empty_function(*args, **kwargs)->bool:
    return True

try:
    import numpy as np
except _import_exceptions as e:
    np = None

try:
    import pandas as pd
    from pandas.testing import  assert_frame_equal, \
                                assert_series_equal, \
                                assert_index_equal, \
                                assert_extension_array_equal
except _import_exceptions as e:
    pd = None
    assert_frame_equal          = empty_function
    assert_series_equal         = empty_function
    assert_index_equal          = empty_function
    assert_extension_array_equal= empty_function



_float_py = (
    float,
)
_float_numpy = (
    np.float_,
    np.float16,
    np.float32,
    np.float64,
    np.float128,
    np.longfloat,
    np.half,
    np.single,
    np.double,
    np.longdouble,
)

_float_types = (
    *_float_py,
    *_float_numpy,
)

class TestCase(unittest.TestCase):
    
    """
    unittest TestCase with additional methods
    """

    def conduct_tests(
        self,
        func,
        tests:dict,
        ):

        """
        Conducts a series of tests against a single function using the supplied arguments.
        This is designed for quick establishmenet of unittests in TDD process.

        It makes assumptions about what the tests are asserting by looking at the type of answer expected;
        which when wrong can give false positives. Hence for integration into CI/CD, this module is not recommended.

        Receives a list of dicts, tests, in form of:
        [
            {
                "args":{
                    "arg1":...,
                    "arg2":...,
                    ...
                },
                "answer":...,
            },
            {
                ...
            },
            {
                ...
            }
        ]
        
        func will be called in form of
            func(**test["args"]) for test in tests
        
        the return of which will be matched against test["answer"] with the following logic:
        - if test["answer"] is a type, and
            - test["answer"] is a subclass of Exception, it will assert either
                - an Exception of subclass of test["answer"] be raised; or
                - such an Exception was returned by func().
            - test["answer"] is any other classes, it will assert either
                - the return of func() be an instance of test["answer"]; or
                - the return of func() be a type that is a subclass of test["answer"].
        - if test["answer"] is a list, tuple or dict, use the unittest methods of assertListEqual, assertTupleEqual or assertDictEqual.
            - TODO iterate through these to allow for float determinations
            - TODO iterate through these to allow for subset etc
        - if test["answer"] is a float or numpy float, assert values being close
        - if test["answer"] is a numpy array of dtype
            - float, assert values being close
            - all others, assert values being equal
        - if test["answer"] is a pandas DataFrame or Series, asser them being close using default arguments.
        """

        for _test in tests:
            if (issubclass(_test["answer"], Exception) if (isinstance(_test["answer"], type)) else False):
                """
                Case: EXCEPTIONS

                If an Exception is passed as the answer, it could mean either:
                - an Exception will be raised in func(); or
                - an Exception will be returned by func().

                So we will need to take the return value, and if its an Exception, raise it.
                """

                _assertion = None   # This requires a context manager - so this does not go through the _assertion route.
                with self.assertRaises(Exception) as context:
                    _return = func(
                        **_test["args"]
                    )
                    if (isinstance(_return, Exception)):
                        raise _return

                self.assertTrue(isinstance(context.exception, _test["answer"]))

            elif (isinstance(_test["answer"], type)):
                """
                Case: TYPE

                If its a class being passed, check that the output is an instance of the answer.
                Or, if the output is a class, check that the output is a subclass of the answer.
                """

                _assertion = lambda output, answer: self.assertTrue(
                    isinstance(
                        output,
                        answer
                    ) if not (isinstance(output, type)) else \
                    issubclass(
                        output,
                        answer
                    )
                )

            elif (isinstance(_test["answer"], _float_py)):
                """
                Case: FLOATS
                
                If its is a scalar float, then assert them all close.
                """
                _assertion = self.assertAlmostEqual

            elif (isinstance(_test["answer"], list)):
                """
                Case: LISTS
                """
                _assertion = self.assertListEqual

            elif (isinstance(_test["answer"], tuple)):
                """
                Case: TUPLES
                """
                _assertion = self.assertTupleEqual

            elif (isinstance(_test["answer"], dict)):
                """
                Case: DICTIONARIES
                """
                _assertion = self.assertDictEqual

            elif (isinstance(_test["answer"], np.ndarray)):
                """
                Case: NUMPY ARRAYS
                
                If dtype is a kind of float, then assert them all close.
                Otherwise, assert all equal.
                """

                if (_test["answer"].dtype in _float_numpy):
                    _assertion = np.testing.assert_allclose
                else:
                    _assertion = np.testing.assert_array_equal

            elif (isinstance(_test["answer"], _float_numpy)):
                """
                Case: NUMPY FLOATS
                
                If its is a scalar float, then assert them all close.
                """
                _assertion = np.testing.assert_approx_equal

            elif (isinstance(_test["answer"], pd.DataFrame)):
                """
                Case: Pandas DataFrame
                """

                _assertion = assert_frame_equal
                
            elif (isinstance(_test["answer"], pd.Series)):
                """
                Case: Pandas Series
                """
                _assertion = assert_series_equal
            
            elif (isinstance(_test["answer"], (pd.Index, ))):
                """
                Case: Pandas Index
                """
                _assertion = assert_index_equal
            
            else:
                _assertion = self.assertEqual

            # Do the assertion
            if (_assertion):
                _assertion(
                    func(
                        **_test["args"]
                    ),
                    _test["answer"],
                )

