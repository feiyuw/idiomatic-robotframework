# -*- coding: robot -*-
*** Test Case ***
Firefox should be able to open when VIM opened
    Open VIM
    VIM should be ready
    Open Firefox
    Firefox should be ready

VIM should be able to open when Firefox opened
    Open Firefox
    Firefox should be ready
    Open VIM
    VIM should be ready

Chrome should be able to view Google when Firefox opened
    Open Firefox
    Firefox should be ready
    Visit Google in Chrome
    Google HomePage is visible

*** Keywords ***
Open VIm
    Log     Open VIM

Open Firefox
    Log     Open Firefox

Open Chrome
    Log     Open Chrome

VIM should be ready
    Log     VIM is ready

Firefox should be ready
    Log     Firefox is ready

Chrome should be ready
    Log     Chrome is ready

Visit Google in Chrome
    Open Chrome
    Visit Google

Visit Google
    Log     Visit Google

Google HomePage is visible
    Log     Google is ready
