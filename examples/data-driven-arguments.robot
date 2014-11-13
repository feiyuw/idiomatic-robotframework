# -*- coding: robot -*-
*** Test Case ***
Plus Operation Should Work
    [Template]  The Result of ${value1} plus ${value2} should be ${result}
    1   2   3
    1   -2  -1
    -1  -3  -4

*** Keywords ***
The Result of ${value1} plus ${value2} should be ${result}
    ${actual result}    Evaluate    ${value1} + ${value2}
    Should Be Equal As Integers    ${result}   ${actual result}
