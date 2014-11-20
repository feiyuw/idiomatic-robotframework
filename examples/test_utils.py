import os
from unittest import TestCase
import utils

class TestUtils(TestCase):
    def test_add_to_env_variable_on_linux_where_env_not_exist(self):
        import sys
        sys.platform = 'linux2'
        if 'UTPATH' in os.environ:
            del os.environ['UTPATH']
        utils.add_to_env_variable('UTPATH')
        self.assertEquals(os.environ['UTPATH'], '')

    def test_add_to_env_variable_on_linux_where_env_not_exist_and_append_one(self):
        import sys
        sys.platform = 'linux2'
        if 'UTPATH' in os.environ:
            del os.environ['UTPATH']
        utils.add_to_env_variable('UTPATH', 'a')
        self.assertEquals(os.environ['UTPATH'], 'a')

    def test_add_to_env_variable_on_linux_where_env_not_exist_and_append_some(self):
        import sys
        sys.platform = 'linux2'
        if 'UTPATH' in os.environ:
            del os.environ['UTPATH']
        utils.add_to_env_variable('UTPATH', 'a', 'b')
        self.assertEquals(os.environ['UTPATH'], 'a:b')

    def test_add_to_env_variable_on_linux_where_env_exist_and_append_none(self):
        import sys
        sys.platform = 'linux2'
        os.environ['UTPATH'] = 'x'
        utils.add_to_env_variable('UTPATH')
        self.assertEquals(os.environ['UTPATH'], 'x')

    def test_add_to_env_variable_on_linux_where_env_exist_and_append_one(self):
        import sys
        sys.platform = 'linux2'
        os.environ['UTPATH'] = 'x'
        utils.add_to_env_variable('UTPATH', 'a')
        self.assertEquals(os.environ['UTPATH'], 'a:x')

    def test_add_to_env_variable_on_linux_where_env_exist_and_append_some(self):
        import sys
        sys.platform = 'linux2'
        os.environ['UTPATH'] = 'x'
        utils.add_to_env_variable('UTPATH', 'a', 'b')
        self.assertEquals(os.environ['UTPATH'], 'a:b:x')

    def test_add_to_env_variable_on_windows_where_env_not_exist(self):
        import sys
        sys.platform = 'win32'
        if 'UTPATH' in os.environ:
            del os.environ['UTPATH']
        utils.add_to_env_variable('UTPATH')
        self.assertEquals(os.environ['UTPATH'], '')

    def test_add_to_env_variable_on_windows_where_env_not_exist_and_append_one(self):
        import sys
        sys.platform = 'win32'
        if 'UTPATH' in os.environ:
            del os.environ['UTPATH']
        utils.add_to_env_variable('UTPATH', 'a')
        self.assertEquals(os.environ['UTPATH'], 'a')

    def test_add_to_env_variable_on_windows_where_env_not_exist_and_append_some(self):
        import sys
        sys.platform = 'win32'
        if 'UTPATH' in os.environ:
            del os.environ['UTPATH']
        utils.add_to_env_variable('UTPATH', 'a', 'b')
        self.assertEquals(os.environ['UTPATH'], 'a;b')

    def test_add_to_env_variable_on_windows_where_env_exist_and_append_none(self):
        import sys
        sys.platform = 'win32'
        os.environ['UTPATH'] = 'x'
        utils.add_to_env_variable('UTPATH')
        self.assertEquals(os.environ['UTPATH'], 'x')

    def test_add_to_env_variable_on_windows_where_env_exist_and_append_one(self):
        import sys
        sys.platform = 'win32'
        os.environ['UTPATH'] = 'x'
        utils.add_to_env_variable('UTPATH', 'a')
        self.assertEquals(os.environ['UTPATH'], 'a;x')

    def test_add_to_env_variable_on_windows_where_env_exist_and_append_some(self):
        import sys
        sys.platform = 'win32'
        os.environ['UTPATH'] = 'x'
        utils.add_to_env_variable('UTPATH', 'a', 'b')
        self.assertEquals(os.environ['UTPATH'], 'a;b;x')
        
    def test_add_to_env_variable_on_windows_where_env_exist_and_append_some_already_exist(self):
        import sys
        sys.platform = 'win32'
        os.environ['UTPATH'] = 'x'
        utils.add_to_env_variable('UTPATH', 'x', 'a', 'b')
        self.assertEquals(os.environ['UTPATH'], 'a;b;x')
        
    def test_add_to_env_variable_on_linux_where_env_exist_and_append_some_already_exist(self):
        import sys
        sys.platform = 'linux2'
        os.environ['UTPATH'] = 'x'
        utils.add_to_env_variable('UTPATH', 'x', 'a', 'b')
        self.assertEquals(os.environ['UTPATH'], 'a:b:x')

