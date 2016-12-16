import unittest
import os
from exceptions import OSError
import subprocess as sb


class Test_Perm_0770(unittest.TestCase):

    def setUp(self):
        # create an user
        self.user = 'new_user1'
        self.path = '/home/aleh/Test'
        self.file = '/home/aleh/Test/file1'
        self.content = 'Hello!'
        os.system('sudo useradd {a} -p {a}'.format(a=self.user))

        self.gid = grp.getgrnam(self.user).gr_gid
        self.uid = pwd.getpwnam(self.user).pw_uid

        # create a catalogue
        os.mkdir(self.path)
        # create a file
        with open(self.file, 'w') as f:
            f.write(self.content)
        os.chmod(self.file, 0770)

    def test_case1(self):
        #check access to file for others
        with self.assertRaises(OSError) as cm:
             sb.call('sudo -u {user} cat {file}'.format(user=self.user,file=self.file))

    def test_case2(self):
        # check access to file for owners
        os.system('sudo chown new_user1 /home/aleh/Test/file1')
        file_content = sb.check_output(['sudo', '-u', 'new_user1', 'cat', '/home/aleh/Test/file1'])
        self.assertEqual(file_content, self.content)

    def tearDown(self):
        #delete the user
        os.system('sudo userdel -r {a}'.format(a=self.user))
        #delete catalogues
        os.system('rm -rf {dirname}'.format(dirname=self.path))
        #for i in os.listdir(self.path):
        #    os.remove(i)
        #os.rmdir(self.path)

class Test_permission_0774(unittest.TestCase):
    def setUp(self):
        # create an user
        self.user = 'new_user1'
        self.path = '/home/aleh/Test'
        self.file = '/home/aleh/Test/file2'
        self.content = 'Hello!'
        os.system('sudo useradd {a} -p {a}'.format(a=self.user))
        # create a catalogue
        os.mkdir(self.path)
        # create a file
        with open(self.file, 'w') as f:
            f.write(self.content)
        os.chmod(self.file, 0774)

    def test_case3(self):
        # check access to file for others
        file_content = sb.check_output(['sudo', '-u', self.user, 'cat', self.path])
        self.assertEqual(file_content, self.content)




    def tearDown(self):
        # delete the user
        os.system('sudo userdel -r {a}'.format(a=self.user))
        # delete catalogues
        os.system('rm -rf {dirname}'.format(dirname=self.path))
        # for i in os.listdir(self.path):
        #    os.remove(i)
        # os.rmdir(self.path)




if __name__ == '__main__':
    unittest.main()