# quicktest
Subclass of unittest.TestCase for quicker writing of Python unit tests

Conducts a series of tests against a single function using the supplied arguments.
This is designed for quick establishmenet of unittests in TDD process.

It makes assumptions about what the tests are asserting by looking at the type of answer expected;
which when wrong can give false positives. Hence for integration into CI/CD, this module is not recommended.

Receives a list of dicts, tests, in form of:
```
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
```

func will be called in form of
`    func(**test["args"]) for test in tests`

the return of which will be matched against test["answer"] with the following logic:
- if `test["answer"]` is a type, and
    - `test["answer"]` is a subclass of Exception, it will assert either
        - an Exception of subclass of `test["answer"]` be raised; or
        - such an Exception was returned by func().
    - `test["answer"]` is any other classes, it will assert either
        - the return of `func()` be an instance of `test["answer"]`; or
        - the return of `func()` be a type that is a subclass of `test["answer"]`.
- if `test["answer"]` is a list, tuple or dict, use the unittest methods of `assertListEqual`, `assertTupleEqual` or `assertDictEqual`.
    - TODO iterate through these to allow for float determinations
    - TODO iterate through these to allow for subset etc
- if `test["answer"]` is a float or numpy float, assert values being close
- if` test["answer"]` is a numpy array of dtype
    - float, assert values being close
    - all others, assert values being equal
- if `test["answer"]` is a pandas DataFrame or Series, asser them being close using default arguments.