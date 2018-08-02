#!/usr/bin/env python3

# Copyright (c) 2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

if __name__ != '__main__':
    raise ImportError(u"%s may only be run as a script" % __file__)

from subprocess import call
import argparse
import json
import os
import subprocess
import time

parser = argparse.ArgumentParser(description='Run tests for elements explorer.')
parser.add_argument('--dbs', default='postgres', help='Specify a coma separated list of dbs to run (default: postgres).')
parser.add_argument('--tests', default='all', help='Specify a coma separated list of tests to run (default: all).')
args = parser.parse_args()

AVAILABLE_DBS = [
    'postgres',
]
RUN_DBS = args.dbs.split(',')
assert len(RUN_DBS) > 0
for db_name in RUN_DBS:
    if db_name not in AVAILABLE_DBS:
        print('ERROR: in --dbs: db %s not available' % db_name)
        exit(1)

AVAILABLE_TESTS = os.listdir('./explorer/tests')
if args.tests == 'all':
    RUN_TESTS = AVAILABLE_TESTS
else:
    target_tests = args.tests.split(',')
    assert len(target_tests) > 0
    for test_name in target_tests:
        if test_name not in AVAILABLE_TESTS:
            print('ERROR: in --tests: test %s not available' % test_name)
            exit(1)
    RUN_TESTS = target_tests


# A common function that destroys, starts and stops docker for testing
# individual test files for a given db
def test_file_with_db(db, test_file, env_file_export):
    print('---------------------------------------------------')
    call(['rm', '-rf', '/tmp/test-elements-explorer'])
    call(['mkdir', '/tmp/test-elements-explorer'])
    call(['mkdir', '/tmp/test-elements-explorer/db'])
    call(['mkdir', '/tmp/test-elements-explorer/db/postgresql'])
    call(['mkdir', '/tmp/test-elements-explorer/elementsregtest'])
    call(['mkdir', '/tmp/test-elements-explorer/keys'])
    call(['mkdir', '/tmp/test-elements-explorer/regtest'])
    call(['mkdir', '/tmp/test-elements-explorer/target'])

    try:
        call('export CURRENT_UID=$(id -u):$(id -g) && docker-compose up --build -d',
             shell=True, cwd='./docker/test-%s' % db, stdout=subprocess.PIPE)
    except Exception as e:
        print("docker-compose up: Error in %s:" % (test_file), type(e), e)
        return False

    print('Testing %s: Running file %s' % (db, test_file))
    print('---------------------------------------------------')

    status = 1
    time.sleep(20) # Wait for db to start and be created from scratch
    test_init_time = time.time()
    try:
        call_command = "docker exec -it rpcexplorer_explorer_1 /bin/sh -c '%s python ./explorer/tests/%s'" % (
            env_file_export, test_file)
        # print('call_command', call_command)
        status = call(call_command, cwd='./docker/test-%s' % db, shell=True)

        test_final_time = time.time()
    except Exception as e:
        print("python3: Error in %s:" % (test_file), type(e), e)
        return False

    print('%s INIT TIME: %s' % (test_file, test_init_time))
    print('%s FINAL TIME: %s' % (test_file, test_final_time))
    print('%s DIFF TIME: %s' % (test_file, test_final_time - test_init_time))
    print('---------------------------------------------------')

    if status != 0:
        # status2 = call('docker ps -a', shell=True)
        # status2 = call('docker logs rpcexplorer_explorer_1', shell=True)
        # status2 = call('docker logs rpcexplorer_postgres_1', shell=True)
        # status2 = call('docker logs rpcexplorer_bitcoin_1', shell=True)
        # status2 = call('docker logs rpcexplorer_elements_1', shell=True)
        status2 = call('docker ps -a', shell=True)

    try:
        call('export CURRENT_UID=$(id -u):$(id -g) && docker-compose stop',
             shell=True, cwd='./docker/test-%s' % db)
    except Exception as e:
        print("docker-compose stop: Error in %s:" % (test_file), type(e), e)
        return False

    if status != 0:
        return False

    return True


print('---------------------------------------------------')
print('RUN_DBS', RUN_DBS)
print('RUN_TESTS', RUN_TESTS)
print('Testing %s DBs' % (len(RUN_DBS)))
print('Testing with %s test files' % (len(RUN_TESTS)))
print('Total tests: %s * %s = %s ' % (
    len(RUN_DBS),
    len(RUN_TESTS),
    len(RUN_DBS) * len(RUN_TESTS),
))

global_init_time = time.time()
for db in RUN_DBS:
    env_file = open('./docker/test-%s/conf/explorer.env' % db, 'r').readlines()
    env_file_export = ''
    for line in env_file:
        if line and line[0] != '\n' and line[0] != '#':
            env_file_export += 'export %s ; ' % line.rstrip()

    for test in RUN_TESTS:
        if not test_file_with_db(db, test, env_file_export):
            exit(1)

global_final_time = time.time()
print('---------------------------------------------------')
print('GLOBAL INIT TIME: %s' % (global_init_time))
print('GLOBAL FINAL TIME: %s' % (global_final_time))
print('GLOBAL DIFF TIME: %s' % (global_final_time - global_init_time))
