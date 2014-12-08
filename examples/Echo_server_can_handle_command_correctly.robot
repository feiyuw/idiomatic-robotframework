*** Settings ***
Suite Setup       Connect To Echo Server
Suite Teardown    Disconnect From Echo Server
Test Template     Send "${data}" to Server should return "${expect data}" back
Library           echo_client.EchoClient    127.0.0.1    WITH NAME    EchoClient

*** Test Cases ***
Echo server will send same data back when received data
    hello    hello
    Hello    Hello
    hello world!    hello world!
    HELLO WORLD!    HELLO WORLD!
    &12345$    &12345$
    1234567890    1234567890

*** Keywords ***
Connect To Echo Server
    EchoClient.connect

Send "${data}" to Server should return "${expect data}" back
    EchoClient.send    ${data}
    ${received data}    EchoClient.read
    Should Be Equal    ${received data}    ${data}

Disconnect From Echo Server
    EchoClient.disconnect
