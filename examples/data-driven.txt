*** Setting ***
Test Template     The Result of plus operation should be OK

*** Test Case ***
1 Plus 2 Should be 3
    [Timeout]    1 millisecond
    1    2    3

1 Plus -2 Should be -1
    1    -2    -1

-1 Plus -3 Should be -4
    -1    -3    -4

Other Scenario
    [Template]    The Result of plus operation should be OK
    0    1    1
    -1    0    -1
    1    99    100
    -1    1    0

*** Keywords ***
The Result of plus operation should be OK
    [Arguments]    ${value1}    ${value2}    ${result}
    ${actual result}    Evaluate    ${value1} + ${value2}
    Should Be Equal As Integers    ${result}    ${actual result}
