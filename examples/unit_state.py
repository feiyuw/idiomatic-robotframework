@unset_loss_expected_before_return
def change_unit_state (unit, state, mode="", expect_loss_mml='', boot_timeout='', child_unit_included=""):
    """This keyword configures a unit to the given state including intermediate steps.
    Functional and I/O units are supported.
    It uses the ZUSC or ZIHE command.
    MML: ZUSC, ZIHE

    | Input Parameters    | Man. | Description |
    | unit                | yes  | instance of Unit or name of the unit in  the format <unit type>-<index>. e.g. OMU-0, SCSI-01 |
    | state               | yes  | state which unit will have after processing format is <main state>-<substate>, e.g. WO-EX or simply WO |
    | mode                | no   | mode of the state change: controlled or forced. Default is controlled. |
    |                     |      | For forced mode should be "FCD". |
    | expect_loss_mml     | no   | parameter specifies that active OMU may loose MML Connection or not |
    |                     |      | default = 'False' means that active OMU will not loose MML Connection |
    |                     |      | 'True' means that active OMU may loose MML Connection |
    |                     |      | if inputed parameter is not 'True' (string or boolean type) handling |
    |                     |      | is the same as handling for default parameter |
    | boot_timeout        | no   | Timeout for the system restart. Default is 7 min. |
    | child_unit_included | no   | 'FULL' or '', default is child units in same state as parent are changed  |

    The keyword tries to finaly get to the given state and will set intermediate steps.
    The keyword checks if the main state (in case of SE also substate -OU or -NH) was reached but, will not wait until -EX is reached.
    If MML connection loss is allowed (expect_loss_mml = True) it will reestablish the connection and continue with outstanding states.
    (If the loss of connection was expected.)
    In some cases MML triggers a system restart after the keyword is finished. In this case the connection to the SUT will be lost some time after the keyword has finished.

    Also compare to the simpler 'Set Unit State' keyword.
    """
    if expect_loss_mml == '':
        expect_loss_mml = False
    if boot_timeout == '':
        boot_timeout = "7 min"
    
    unit_name = units_lib._get_unit_name(unit)
    expect_loss_mml = str(expect_loss_mml).lower() == 'true'

    current_unit = units_lib.get_units(unit_name, "")[0]
    current_state = current_unit.state

    # loose the -XX part of the states if it is not SE
    if (current_state != "SE-OU") and (current_state != "SE-NH"):
        current_state = current_state.split("-")[0]

    # loose the -XX part of the states if it is not SE
    if (state != "SE-OU") and (state != "SE-NH"):
        state = state.split("-")[0]

    if current_state == state:
        # Unit is already in state
        return

    # convert the timeout to seconds
    timeout = utils.timestr_to_secs(boot_timeout)


    eof_err_occured = False
    

    # build command depending on unit type
    if _is_IO_unit(unit_name):
        command = "ZIHE:OMU:%s,%s:" % (unit_name.split("-")[0], unit_name.split("-")[1])
    else:
        command = "ZUSC:%s,%s:" % (unit_name.split("-")[0], unit_name.split("-")[1])

    # determine required sequence
    sequence = _required_sequence(current_state, state, unit)

    # determine answer to the system restart question
    if (expect_loss_mml == True) or (expect_loss_mml == "True"):
        sleep_time = 15
        setattr(get_current_connection()._current, 'loss_expected', True)
    # if N+1 unit or IO unit, sleep 4 seconds after ZUSC
    elif (_is_IO_unit(unit_name)) or (_get_redundancy_type(unit_name)=='N+1'):
        sleep_time = 4
    # if have BL state, sleep  1 second
    elif 'BL' in sequence:
        sleep_time = 1.5
    else:
        sleep_time = 1.5 # as required, to set 1.5 s sleep as default value.
        
    # execute each step of the sequence
    for step in sequence:
        # ignore BL step, if mode is FCD. fix IPATA-208
        if not _is_IO_unit(unit_name) and state != "BL" and step == "BL" and mode == "FCD":
            continue
        
        # change mode to FCD for GTPU, fix IPATA-88
        unit_type = units_lib._get_unit_name(unit).split("-")[0]
        if unit_type == "GTPU" and step == "TE":
            old_mode = mode
            mode = "FCD"
            
        # complete the command
        if _is_IO_unit(unit_name):
            the_command = command + step + ";"
        else:
            the_command = command + step + "::" + mode + ":" + child_unit_included + ";"
        # change mode back to old mode, fix IPATA-88
        if unit_type == "GTPU" and step == "TE":
            mode = old_mode
            
        try:
            if sequence.__len__() > 1 and step == 'WO' and unit_type == 'NIS1P' and sequence[-2] == 'SP':
                time_to_wait_nis1p = 300
                time.sleep (time_to_wait_nis1p)
            
            # execute the command
            # keyword always answer "Y" for any confirmation. 
            connections.execute_mml(the_command, "Y", "Y")
            if unit_type == "LETGR" and step == "BL":
                # wait for LETGR to get to BL-ID state
                print "*DEBUG* sleep 4 seconds"
                time.sleep (4)
            else:
                print "*DEBUG* sleep %d seconds" % int(sleep_time)
                time.sleep (sleep_time)
        except EOFError:
            # Was this unexpected?
            if (expect_loss_mml == False) or (expect_loss_mml == "False"):
                # Re-raise as it was not expected
                raise
            eof_err_occured = True
            # connect again
            hostip = connections.get_current_connection()._current.host
            helper._run_keyword('Wait Until Keyword Successful', timeout, '30', 'Connect to Ipa', hostip)
            try:
                # send the command again as it might not have been executed
                connections.execute_mml_without_check(the_command, "Y", "Y")
                print "*DEBUG* sleep %d seconds" % int(sleep_time)
                time.sleep (sleep_time)
            except EOFError :
                # Still not up after timeout
                raise EOFError, "No MML connection after %s timeout" % (boot_timeout)

    # last checks
    try:
        units_lib.unit_should_be_in_state(unit_name, state)
    except EOFError :
        if (expect_loss_mml == False) or (expect_loss_mml == "False"):
            raise
        eof_err_occured = True
        # connect again
        hostip = connections.get_current_connection()._current.host
        helper._run_keyword('Wait Until Keyword Successful', timeout , '30', 'Connect to Ipa',hostip)
        units_lib.unit_should_be_in_state(unit_name, state)

    if not eof_err_occured and (expect_loss_mml == True or expect_loss_mml == "True"):
        try:
            for i in range(int(utils.timestr_to_secs(boot_timeout))):
                print "*DEBUG* sleep %d seconds" % int(1)
                time.sleep(1)
                connections.execute_mml_without_check('\n')
            raise RuntimeError, "Wait to lose the connection is timeout(%s)! " % boot_timeout
        except EOFError:
            helper._run_keyword('Wait Until Keyword Successful', '2 min' , "", 'Clone Connection')
            hasattr(get_current_connection()._current, 'loss_expected') and delattr(get_current_connection()._current, 'loss_expected')
