import json
import os
import unittest
import HTMLTestRunner
import testcases as tc2
from datetime import datetime


def create_file(args):
    with open(args[0], 'w') as f:
        f.write(args[1])
    os.chmod(args[0], int(args[2], 8))


def read_setup_descriptions(path):
    with open(path) as f:
        text = f.read()
    return json.loads(text)


def create_user(user_name):
    os.system('sudo useradd {a} -p {a}'.format(a=user_name))


def delete_user(user_name):
    os.system('sudo userdel -r {a}'.format(a=user_name))


def add_test_methods(test_class, func, files, user):
    """Function adds test methods to a class. Each test case will be named as file mode and name in postfix:
        test_{mode}_{file_name}
    """
    for file_info in files:
        for name, content, mode in file_info:
            test = func(test_class, user, name, content, mode)
            setattr(test_class, 'test_{id}_{file}'.format(id=mode, file=name), test)


def add_env_methods(test_class, func, name):
    """Function adds to the main test class setUp and tearDown methods."""
    test = func(test_class)
    setattr(test_class, name, test)


def setup_gen(test_class):
    """Function generates the main logic for setUp method."""
    def test(self):
        setup_description = read_setup_descriptions('setUp.json')
        create_user(setup_description['user'])
# creating all catalogues and files
        for cat in setup_description['file_system']:
            os.mkdir(cat['catalog']['name'], int(cat['catalog']['mode'], 8))
            files_info = map(lambda x: (os.path.join(cat['catalog']['name'], x['name']), x['content'], x['mode']), \
                             cat['catalog']['files'])
            map(create_file, files_info)

    return test


def teardown_gen(test_class):
    """Function generates the main logic for tearDown method."""
    def test(self):
        setup_description = read_setup_descriptions('setUp.json')
        delete_user(setup_description['user'])
# deletion all catalogues and files
        for cat in setup_description['file_system']:
            file_names = map(lambda x: os.path.join(cat['catalog']['name'], x['name']), cat['catalog']['files'])
            map(os.remove, file_names)
            os.rmdir(cat['catalog']['name'])

    return test


def setup_env_new():
    catalog = []
    files = []
    setup_description = read_setup_descriptions('setUp.json')
    user = setup_description['user']
    for cat in setup_description['file_system']:
        catalog.append(cat['catalog']['name'])
        files_info = map(lambda x: (os.path.join(cat['catalog']['name'], x['name']), x['content'], x['mode']), \
                         cat['catalog']['files'])
        files.append(files_info)
    return catalog,files, user


def main():
    catalog, files, user = setup_env_new()

# adding setUp and tearDown methods to the main test class
    add_env_methods(tc2.TestMain, setup_gen, 'setUp')
    add_env_methods(tc2.TestMain, teardown_gen, 'tearDown')

# adding test case methods to test classes
    add_test_methods(tc2.TestFileAccess, tc2.test_access_generator, files, user)
    add_test_methods(tc2.TestWriteFile, tc2.test_write_content_gen, files, user)
    add_test_methods(tc2.TestOwnerAccess, tc2.test_owners_access_gen, files, user)

    test_loader = unittest.TestLoader()
    suite = test_loader.loadTestsFromModule(tc2)

# running test suite and printing results in HTML doc
    with open('report_{date}.html'.format(date=datetime.now()), 'wb') as fp:
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=fp,
            title='Test Task. Testing Of Linux File System.',
            description='This report demonstrates the result of testing Linux Test Environment.', verbosity=2)
        runner.run(suite)


main()
