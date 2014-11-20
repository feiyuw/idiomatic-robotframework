def change_tm500_script_file(src_File_Dir, target_File_Dir, Need_to_Modify=''):
    """Change tm500 attach_script file if the script changed and copy modified file with new name to target.

    | Input Paramaters | Man. | Description |
    | src_File_Dir     | yes  | Absolute path of attach_script file you want to modify |
    | target_File_Dir  | yes  | new attach_script file name(No path informatino,share absolute path with src_File_Dir) |
    | Need_to_Modify   | no   | new  [key:value] list you want to modify |

    Example
    | ${list}= | Create List | PHYCONFIGULTIMING:0 |
    | Change Tm500 Script File | C:\\Temp\\attach.xml | C:\\Temp\\attach_new_file.xml | ${list} |

    Note:
    if Need_to_Modify is string type but not empty string,the function will raise ValueError exception,
    if Need_to_Modify is neither string type nor list type,the function will raise TypeError exception.
    """

    path = os.path.dirname(src_File_Dir)
    target_name_temp=target_File_Dir
    if path == '':
        target_File_Dir='.\\'+target_File_Dir
    else:
        target_File_Dir = path + '\\'+target_File_Dir

    #step 1: if the Need_to_Modify is empty string,the function just do copy job,if it's othertype,raise TypeError
    if type(Need_to_Modify)is not types.ListType:
        if Need_to_Modify=='':
            shutil.copyfile(src_File_Dir, target_File_Dir)
            return
        else:
            print 'ERROR:The input must be a empty string or a LIST(3rd parameter)!'
            raise TypeError

    #step 2:  order parameters
    Key_List = []
    Value_List = []
    para_len=0
    try:
        for target in Need_to_Modify:
             if len(target)==0:
                para_len=para_len+1
                continue
             tmp = target.split(':')
             Key_List.append(tmp[0].upper())
             Value_List.append(tmp[1].upper())
        if  para_len ==  len(Need_to_Modify):
             #if Need_to_Modify is a list['','',''],copy the old script.
             shutil.copyfile(src_File_Dir, target_File_Dir)
             return
    except:
        print ''''ERROR:The input parameter must be one ':' involved (3rd parameter)!'''
        raise TypeError

    #step 3: renew  parameters
    f = file(src_File_Dir,'r')
    file_target = open(target_File_Dir,'w')
    try:
        for line in f.readlines():
            line=line.upper()
            temp=line
            if  len(line.strip())==0 or line.startswith('#'):
                continue
            for i in range(0,len(Key_List)):
                 pattern = re.compile(('%s\s+.*\\n') % Key_List[i])
                 if re.search(pattern,line):
                    if Key_List[i] == 'USIMCONFIG' and 15==len(Value_List[i]):                        
                        old = re.search("\[(\d{15})\s", line)
                        if old:
                            old_sim = old.groups()[0]
                            temp = line.replace(old_sim, Value_List[i])   
                        else:
                            print "Not find USIMCONFIG"
                    else:
                        temp = re.sub(pattern,'%s %s\\n'% (Key_List[i],Value_List[i]),line)
                        
            file_target.write(temp)
    finally:
        f.close()
        file_target.close()
