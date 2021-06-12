# Copyright (c) 2008 Nokia Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This script parses the output of the regrtest.py script and
# transforms it into the XML format suitable for the CruiseControl web
# interface.

import re
import sys
import os
import pprint

expected_skip_list = ['test_aepack',
        'test_al',
        'test_applesingle',
        'test_cd',
        'test_cl',
        'test_cmd_line',
        'test_commands',
        'test_crypt',
        'test_ctypes',
        'test_hotshot',
        'test_plistlib',
        'test_sundry',
        'test_bsddb',
        'test_bsddb185',
        'test_bsddb3',
        'test_bz2',
        'test_dbm',
        'test_gdbm',
        'test_gl',
        'test_imageop',
        'test_rgbimg',
        'test_audioop',
        'test_gettext',
        'test_curses',
        'test_dl',
        'test_fork1',
        'test_grp',
        'test_imgfile',
        'test_ioctl',
        'test_largefile',
        'test_linuxaudiodev',
        'test_macfs',
        'test_macostools',
        'test_macpath',
        'test_mhlib',
        'test_mmap',
        'test_nis',
        'test_openpty',
        'test_ossaudiodev',
        'test_pep277',
        'test_poll',
        'test_popen',
        'test_popen2',
        'test_pty',
        'test_pwd',
        'test_resource',
        'test_scriptpackages',
        'test_signal',
        'test_startfile',
        'test_sqlite',
        'test_subprocess',
        'test_sunaudiodev',
        'test_tcl',
        'test_threadsignals',
        'test_wait3',
        'test_wait4',
        'test_winreg',
        'test_winsound',
        'test_zipfile64']


def replaceXMLentities(s):
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace("'", '&apos;')
    s = s.replace('"', '&quot;')

    def replace_non_printable(obj):
        if ord(obj.group(0)) > 31 and ord(obj.group(0)) < 126:
            return obj.group(0)
        else:
            return '?'
    return re.sub('[^ a-zA-Z0-9\n]', replace_non_printable, s)

# This regexp matches both the plain test start header "test_foo" and
# the "Re-running test 'test_foo' in verbose mode" header.
re_run = re.compile("^(Re-running test '|)(test_[^ \n]+)(' in verbose mode|)$")
# Matches the end of test outputs and beginning of reporting
re_finish = re.compile("^[0-9]+ tests (OK.|skipped:)$")
re_unexpected = re.compile("test (test_.*) produced unexpected output:(.*)")
re_skipped = re.compile("(test_.*) skipped --")
re_crashed = re.compile("test (test_.*) crashed --")
re_failed = re.compile("test (test_.*) failed --")
re_time = re.compile("Ran ([0-9]+) test[s]{0,1} in (.*)s")
re_unexp_skips = re.compile("(.*) skip[s]{0,1} unexpected on")
re_sis_build_time = re.compile("Sis build time :(.*)")

# Build information that has to be displayed on CC should be in the
# regrtest_emu log in this format
re_build_info = re.compile("Build Info -- Name : <(.*)>, Value : <(.*)>")

# A metric should be printed to regrtest log in the format :
# "Measurement -- Name : <>, Value : <>, Unit : <>, Threshold : <>,
# higher_is_better : <>"
# Note : All special characters in the above string are compulsary
# Threshold should always be a positive number
# higher_is_better should be either 'yes' or 'no'
re_measurement = re.compile("Measurement -- Name : <(.*)>, Value : <(.*)>," +
               " Unit : <(.*)>, Threshold : <(.*)>, higher_is_better : <(.*)>")

new_state = old_state = {'passed': [],
                         'failed': [],
                         'skipped_expected': [],
                         'skipped_unexpected': []}
changeset = {}
results = {}
current_case = None
unexp_skips = None
unexp_skip_list = []
measurements = {}
sis_build_time = ''
dev_metrics_log = None
build_info = {}

# Remove 'regrtest_' & '_xxx.log' from the log name
# Some sample target names : aalto, emulator, merlin
target_name = sys.argv[1][9:-8]

# regrtest_xxx.log and the corresponding xml file is placed here.
base_dir = 'build\\test'

log_directory = 'C:\\Program Files\\CruiseControl\\logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
dev_metrics_log_file = os.path.join(log_directory, 'ngopy_metrics.log')

# sys.argv[1] is the log filename passed when calling this script
# Eg: regrtest_aino_3_1.log, regrtest_merlin_3_2.log
regrtest_log = open(os.path.join(base_dir, sys.argv[1]), 'rt')
# XML filenames will be -- aalto_resuls.xml, merlin_results.xml etc.
regrtest_xml = open(os.path.join(base_dir, target_name + '_results.xml'), 'w')

# state_file contains the state (passed/failed/skipped) of each test case
# in the previous build
try:
    state_file = open(os.path.join(log_directory, 'state_' +
                                         target_name + '.txt'), 'rt')
except IOError:
    state_file = None

# Logging of metrics not required for emulator and linux builds
if target_name not in ['linux', 'emulator']:
    dev_metrics_log = open(dev_metrics_log_file, 'a+')

# First split output file based on the case names
for line in regrtest_log:
    if re_finish.match(line):
        current_case=None
        continue
    m = re_run.match(line)
    if m:
        # beginning of processing for new case
        case_name = m.group(2)
        assert case_name
        if case_name != 'test_pystone':
            current_case = {'time': "1", 'output': []}
            results[case_name] = current_case
    else:
        x1 = re_time.match(line)
        if x1:
            current_case['time'] = x1.group(2)
        if current_case:
            current_case['output'].append(line)

    sis_build_time_match = re_sis_build_time.match(line)
    if sis_build_time_match:
        sis_build_time = sis_build_time_match.group(1)
        continue

    re_build_info_match = re_build_info.match(line)
    if re_build_info_match:
        build_info[re_build_info_match.group(1)] = \
                                        re_build_info_match.group(2)
        continue

    re_measurement_match = re_measurement.match(line)
    if re_measurement_match:
        measurements[re_measurement_match.group(1)] = {}
        measurements[re_measurement_match.group(1)]['value'] = \
                                           float(re_measurement_match.group(2))
        measurements[re_measurement_match.group(1)]['unit'] = \
                                                  re_measurement_match.group(3)
        measurements[re_measurement_match.group(1)]['threshold'] = \
                                           float(re_measurement_match.group(4))
        measurements[re_measurement_match.group(1)]['higher_is_better'] = \
                                                  re_measurement_match.group(5)
        measurements[re_measurement_match.group(1)]['direction'] = 'Neutral'
        measurements[re_measurement_match.group(1)]['delta'] = 0
        continue
    # For linux we believe regrtest, but for emu and devices we decide what is
    # expected and unexpected skip (refer : expected_skip_list)
    if target_name == 'linux':
        if unexp_skips:
            unexp_skip_list.extend(line.strip().rsplit(' '))
            unexp_skips=None
        unexp_skips = re_unexp_skips.match(line)
regrtest_log.close()

# Analyze further to determine result from the test
count_unexpected = 0
count_skipped = 0
count_crashed = 0
count_failed = 0
count_passed = 0
count_skipped_unexpected = 0
count_skipped_expected = 0

for case_name, result in results.items():
    out = ''.join(result['output'])
    result['output'] = out
    # if others don't match, the case is assumed to be passed
    if re_unexpected.search(out):
        result['state'] = 'unexpected_output'
        count_unexpected += 1
    elif re_skipped.search(out):
        result['state'] = 'skipped'
        count_skipped += 1
    elif re_crashed.search(out):
        result['state'] = 'crashed'
        count_crashed += 1
    elif re_failed.search(out):
        result['state'] = 'failed'
        count_failed += 1
    else:
        result['state'] = 'passed'
        count_passed += 1

# Report results
print "Full results:"
pprint.pprint(results)
states = set(results[x]['state'] for x in results)
print "Summary:"
for state in states:
    cases = [x for x in results if results[x]['state'] == state]
    print "%d %s: %s" % (len(cases), state, ' '.join(cases))

total_cases = count_unexpected + count_skipped + count_crashed + \
                                                count_failed + count_passed
failed_testcases = count_unexpected + count_crashed + count_failed

testcase_metric_names = ['Number of Failed Test Cases',
'Number of Skipped Test Cases - Unexpected',
'Number of Successful Test Cases',
'Number of Skipped Test Cases - Expected']

# Initialize the 'measurements' dictionary related data for test case counts
# and then dump values. skipped_expected_count and skipped_unexpected_count
# are assigned later as our expected and unexpected list is not the same as the
# one calculated by regrtest in the log.
for item in testcase_metric_names:
    measurements[item] = {}
    measurements[item]['value'] = 0
    measurements[item]['threshold'] = 1
    if item == 'Number of Successful Test Cases':
        measurements[item]['higher_is_better'] = 'yes'
    else:
        measurements[item]['higher_is_better'] = 'no'
    measurements[item]['delta'] = 0
    measurements[item]['direction'] = 'Neutral'
    measurements[item]['unit'] = ''

measurements['Number of Failed Test Cases']['value'] = failed_testcases
measurements['Number of Successful Test Cases']['value'] = count_passed

regrtest_xml.write('<xml>\n')
regrtest_xml.write('<testsuites>\n')
regrtest_xml.write('    <testsuite_%(target)s name="testcases_%(target)s"\
 tests="%(total_cases)s" time="%(time)s" >\n' % {'target': target_name,
 'total_cases': total_cases, 'time': sis_build_time})

if state_file:
    old_state = eval(state_file.read())
    state_file.close()


def check_state_change(testcase, state):
    if testcase not in old_state[state]:
        return 'yes'
    else:
        return 'no'

# Each testcase has a 'new' attribute to indicate if it moved to this
# state in this build
for i in sorted(results.keys()):
    if ((results[i]['state'] == 'failed') or
        (results[i]['state'] == 'unexpected') or
        (results[i]['state'] == 'crashed')):
        state_changed = check_state_change(i, 'failed')
        regrtest_xml.write('        <testcase name="' + i + '" time="1" ' +
            'new="' + state_changed + '"> <failure>' +
            replaceXMLentities(results[i]['output']) +
            '</failure></testcase>\n')
        new_state['failed'].append(i)

for i in sorted(results.keys()):
    if (results[i]['state'] == 'skipped'):
        if i not in expected_skip_list and target_name != 'linux':
            unexp_skip_list.append(i)
        if i in unexp_skip_list:
            state_changed = check_state_change(i, 'skipped_unexpected')
            regrtest_xml.write('        <testcase name="' + i + '" time="1" ' +
                'new="' + state_changed + '"> <skipped_unexpected>' +
                replaceXMLentities(results[i]['output']) +
                '</skipped_unexpected></testcase>\n')
            new_state['skipped_unexpected'].append(i)
            count_skipped_unexpected += 1

for i in sorted(results.keys()):
    if (results[i]['state'] == 'passed'):
        state_changed = check_state_change(i, 'passed')
        regrtest_xml.write('        <testcase name="' + i + '" time="1" ' +
                'new="' + state_changed + '"> <success>' +
                replaceXMLentities(results[i]['output']) +
                '</success></testcase>\n')
        new_state['passed'].append(i)

for i in sorted(results.keys()):
    if (results[i]['state'] == 'skipped'):
        if i not in unexp_skip_list:
            state_changed = check_state_change(i, 'skipped_expected')
            regrtest_xml.write('        <testcase name="' + i + '" time="1" ' +
                'new="' + state_changed + '"> <skipped_expected>' +
                replaceXMLentities(results[i]['output']) +
                '</skipped_expected></testcase>\n')
            new_state['skipped_expected'].append(i)
            count_skipped_expected += 1

measurements['Number of Skipped Test Cases - Expected']['value'] = \
                                                       count_skipped_expected
measurements['Number of Skipped Test Cases - Unexpected']['value'] = \
                                                       count_skipped_unexpected

# 'measurements' dictionary's 'delta' will contain the difference in metrics
# w.r.t the previous run. 'delta' can be positive or negative
for item in measurements.keys():
    new_state[item] = measurements[item]['value']
    if item in old_state:
        measurements[item]['delta'] = new_state[item] - old_state[item]

# Identify the test cases which have changed states (Eg. Failed->Passed )
for state in ['failed', 'passed', 'skipped_expected', 'skipped_unexpected']:
    s1 = set(new_state[state])
    s2 = set(old_state[state])
    s1.difference_update(s2)
    changeset[state] = list(s1)

# Adding the test cases that have changed states as a measurement and also in
# state_changes tag. 'threshold' and 'direction' are omitted as color coding
# in CC is not necessary.
regrtest_xml.write('        <state_changes>\n')
for state in ['failed', 'passed', 'skipped_expected', 'skipped_unexpected']:
    regrtest_xml.write('          <' + state + ' count="' +
                                           str(len(changeset[state])) + '">\n')
    regrtest_xml.write(repr(changeset[state]))
    regrtest_xml.write('          </' + state + '>\n')
    if changeset[state]:
        measurements[state.capitalize() + ' - New'] = {}
        measurements[state.capitalize() + ' - New']['value'] = \
                                                         repr(changeset[state])
        measurements[state.capitalize() + ' - New']['delta'] = 0
        measurements[state.capitalize() + ' - New']['unit'] = ''
regrtest_xml.write('        </state_changes>\n')

regrtest_xml.write('    <measurements>\n')
# direction - dictates the color coding in CruiseControl. it will be set only
# when the delta crosses threshold. direction can be 'Good', 'Bad', 'Neutral'
for item in measurements.keys():
    if measurements[item]['delta'] == 0:
        measurements[item]['direction'] = 'Neutral'
    elif measurements[item]['higher_is_better'] == 'yes':
        if measurements[item]['delta'] >= measurements[item]['threshold']:
            measurements[item]['direction'] = 'Good'
        elif measurements[item]['delta'] <= -(measurements[item]['threshold']):
            measurements[item]['direction'] = 'Bad'
    else:
        if measurements[item]['delta'] >= measurements[item]['threshold']:
            measurements[item]['direction'] = 'Bad'
        elif measurements[item]['delta'] <= -(measurements[item]['threshold']):
            measurements[item]['direction'] = 'Good'


def write_measurement(item, log_metrics=False):
    regrtest_xml.write('       <measurement>\n')
    regrtest_xml.write('           <name>' + item + '</name>\n')
    regrtest_xml.write('           <value>' +
                       str(measurements[item]['value']) + ' ' +
                       str(measurements[item]['unit']) + '</value>\n')
    regrtest_xml.write('           <direction>' +
                       measurements[item]['direction'] + '</direction>\n')
    if measurements[item]['delta']:
        regrtest_xml.write('           <delta>' +
                           str(measurements[item]['delta']) + '</delta>\n')
    regrtest_xml.write('       </measurement>\n')

    # Update the device specific log file, which is used to draw metrics graph
    if dev_metrics_log and log_metrics:
        dev_metrics_log.write(',%s=%s' %
                              (item, str(measurements[item]['value'])))

# Write the testcase related metrics first and then the memory/time benchmark
# related data so that CC also displays in that order
s = set(measurements.keys())
for item in testcase_metric_names:
    write_measurement(item)
s.difference_update(set(testcase_metric_names))

if dev_metrics_log:
    dev_metrics_log.write('Device=' + target_name)
    dev_metrics_log.write(',Time=' + sis_build_time)

for item in s:
    write_measurement(item, True)
regrtest_xml.write('    </measurements>\n')

regrtest_xml.write('    <build_info>\n')
for item in build_info.keys():
    regrtest_xml.write('    <item>\n')
    regrtest_xml.write('        <name>\n')
    regrtest_xml.write(item)
    regrtest_xml.write('        </name>\n')
    regrtest_xml.write('        <value>\n')
    regrtest_xml.write(str(build_info[item]) + '\n')
    regrtest_xml.write('        </value>\n')
    regrtest_xml.write('    </item>\n')
regrtest_xml.write('    </build_info>\n')

if dev_metrics_log:
    dev_metrics_log.write('\n')
    dev_metrics_log.close()

regrtest_xml.write('    </testsuite_' + target_name + '>\n')
state_file = open(os.path.join(log_directory, 'state_' +
                                            target_name + '.txt'), 'wt')
state_file.write(repr(new_state))
state_file.close()
regrtest_xml.write('</testsuites>\n')
regrtest_xml.write('</xml>')
regrtest_xml.close()
