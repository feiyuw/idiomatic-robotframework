import os
import sys
import logging

def add_to_env_variable(var_name, *args):
    _norm_env_var = lambda x: os.path.normpath(x)
    conn_char = sys.platform == 'linux2' and ':' or ';'
    cur_env_value = os.getenv(var_name, None)
    if cur_env_value is None:
        cur_env_list = []
    else:
        cur_env_list = map(_norm_env_var, cur_env_value.split(conn_char))
    arg_list = []
    for e in args:
        env_var = _norm_env_var(e)
        if env_var not in cur_env_list:
            arg_list.append(env_var)
    arg_list += cur_env_list
    os.environ[var_name] = conn_char.join(arg_list)
    logging.debug('update env variable "%s" to "%s"' % (var_name, os.environ[var_name]))
