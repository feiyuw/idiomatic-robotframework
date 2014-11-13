# -*- coding: robot -*-
*** Test Case ***
Integer plus Integer Should Work
    [tags]  owner-y168zhan  phase-rt
    Given I have 1 and 2
    When I add 1 and 2
    Then result should be 3

Integer plus Negative Integer Should Work
    [tags]  owner-y168zhan  phase-rt
    Given I have 1 and -2
    When I add 1 and -2
    Then result should be -1

*** Keywords ***
I have ${value1} and ${value2}
    Log     ${value1} + ${value2}

I add ${value1} and ${value2}
    ${result}   Evaluate    ${value1} + ${value2}
    Set Test Variable   ${result}

Result should be ${expect result}
    Should Be Equal As Integers    ${result}   ${expect result}
