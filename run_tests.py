#!/usr/bin/env python3

# Copyright (c) 2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from subprocess import call
import json
import os
import subprocess
import time

AVAILABLE_DBS = {
    'postgres' : {},
}
AVAILABLE_DBS_ITEMS = AVAILABLE_DBS.items()
print('AVAILABLE_DBS', AVAILABLE_DBS)

AVAILABLE_TESTS = os.listdir('./explorer/tests')
print('AVAILABLE_TESTS', AVAILABLE_TESTS)

my_env = os.environ.copy()
my_env["PATH"] = "/usr/sbin:/sbin:" + my_env["PATH"]

# A common function that destroys, starts and stops docker for testing
# individual functions for a given db
def test_function_with_db(db, test_file, env_file_export):
    # TODO Remove use of sudo
    call(['sudo', 'rm', '-rf', '/tmp/test-elemements-explorer'])
    call(['mkdir', '/tmp/test-elemements-explorer'])

    try:
        call(['docker-compose', 'up', '--build', '-d'], cwd='./docker/test-%s' % db, stdout=subprocess.PIPE)
    except Exception as e:
        print("docker-compose: Error in %s:" % (test_file), type(e), e)
        return False

    print('---------------------------------------------------')
    print('Testing %s: Running file %s' % (db, test_file))

    status = 1
    time.sleep(20) # Wait for db to start and be created from scratch
    func_init_time = time.time()
    try:
        call_command = "docker exec -it rpcexplorer_explorer_1 /bin/sh -c '%s python ./explorer/tests/%s'" % (
            env_file_export, test_file)
        print('call_command', call_command)
        status = call(call_command, cwd='./docker/test-%s' % db, shell=True)
    except Exception as e:
        print("python3: Error in %s:" % (test_file), type(e), e)
        return False

    func_final_time = time.time()
    diff_time = func_final_time - func_init_time
    print('FUNCTION INIT TIME: %s' % (func_init_time))
    print('FUNCTION FINAL TIME: %s' % (func_final_time))
    print('FUNCTION DIFF TIME: %s' % (diff_time))
    print('---------------------------------------------------')

    if status != 0:
        status2 = call('docker ps -a', shell=True)
        status2 = call('docker logs rpcexplorer_explorer_1', shell=True)
        # status2 = call('docker logs rpcexplorer_postgres_1', shell=True)
        # status2 = call('docker logs rpcexplorer_bitcoin_1', shell=True)
        # status2 = call('docker logs rpcexplorer_elements_1', shell=True)
        status2 = call('docker ps -a', shell=True)

    try:
        call(['docker-compose', 'stop'], cwd='./docker/test-%s' % db)
    except Exception as e:
        print("docker-compose: Error in %s:" % (test_file), type(e), e)
        return False

    if status != 0:
        return False

    return True

print('---------------------------------------------------')
init_time = time.time()
print('GLOBAL INIT TIME: %s' % (init_time))

print('Testing %s DBs' % (len(AVAILABLE_DBS_ITEMS)))
print('Testing with %s test files' % (len(AVAILABLE_TESTS)))
print('Total tests: %s * %s = %s ' % (
    len(AVAILABLE_DBS_ITEMS),
    len(AVAILABLE_TESTS),
    len(AVAILABLE_DBS_ITEMS) * len(AVAILABLE_TESTS),
))

for db, db_properties in AVAILABLE_DBS_ITEMS:
    env_file = open('./docker/test-%s/conf/explorer.env' % db, 'r').readlines()
    env_file_export = ''
    for line in env_file:
        if line and line[0] != '\n' and line[0] != '#':
            env_file_export += 'export %s ; ' % line.rstrip()

    for test in AVAILABLE_TESTS:
        if not test_function_with_db(db, test, env_file_export):
            exit(1)

final_time = time.time()
print('---------------------------------------------------')
print('GLOBAL FINAL TIME: %s' % (final_time))

diff_time = final_time - init_time
print('GLOBAL DIFF TIME: %s' % (diff_time))

time.sleep(0.00001) # REM How to add "uncalled-for" waits
