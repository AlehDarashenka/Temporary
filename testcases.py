import unittest
import subprocess as sb
import os


def test_access_generator(test_class, user, file_name, content, mode):
    """Generates methods for TestFileAccess class """
    def test(self):
        #if mask of mode for a file from 0770 to 0773, the access should be forbidden.
        if int(mode, 8) <=0773:
            #check access to file for a give user
            with self.assertRaises(sb.CalledProcessError) as cm:
                sb.check_output(['sudo', '-u', user, 'cat', file_name], stderr=sb.STDOUT)
        else:
            file_content = sb.check_output(['sudo', '-u', user, 'cat', file_name], stderr=sb.STDOUT)
            self.assertEqual(file_content, content)
    return test

def test_write_content_gen(test_class, user, file_name, content, mode):
    """Generates methods for TestWriteFile class.
       Despite the fact that function gets parameters which aren't necessary for it,
       parameters are passed into function. Generators look uniform and it helps to call them in a loop.
    """
    def test(self):
        #trying to write some content to a file. If it's possible, test will fail.
        with self.assertRaises(sb.CalledProcessError) as cm:
            sb.check_output(['echo {edit}| sudo -u {user} tee -a {name}'.format(
                edit='test1234',user=user, name=file_name
            )], stderr=sb.STDOUT, shell=True)
    return test


def test_owners_access_gen(test_class, user, file_name, content, mode):
    """Generates methods for TestOwnerAccess class.
       Despite the fact that function gets parameters which aren't necessary for it,
       parameters are passed into function. Generators look uniform and it helps to call them in a loop.
    """
    def test(self):
        # check access to a file for owners
        os.system('sudo chown {user} {file}'.format(user=user, file=file_name))
        file_content = sb.check_output(['sudo', '-u', user, 'cat', file_name], stderr=sb.STDOUT)
        self.assertEqual(file_content, content)
    return test


class TestMain(unittest.TestCase):
    """Parent class. Here is setUp and tearDown methods are created on fly from control file.
    """
    pass


class TestFileAccess(TestMain):
    """
       Class inherits setUp and tearDown methods from TestMain class.
       Test cases as methods are created on fly. This class is used for checking file access, therefore for each created
       file will be created test case as method of the class.
    """
    pass


class TestWriteFile(TestMain):
    """
       Class inherits setUp and tearDown methods from TestMain class.
       Test cases as methods are created on fly. This class is used for checking permission for writing into file,
       therefore for each created file will be created test case as method of the class.
    """
    pass


class TestOwnerAccess(TestMain):
    """
       Class inherits setUp and tearDown methods from TestMain class.
       Test cases as methods are created on fly. This class is used for checking file access for user who got owner's
       permissions, therefore for each created file will be created test case as method of the class.
    """
    pass


if __name__ == '__main__':
    unittest.main(verbosity=1)