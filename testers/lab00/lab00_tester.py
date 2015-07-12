#!/usr/bin/python

import subprocess
import sys
import os
import filecmp

mycmd = "python"
myarg = "hello.py"
student_out = 'student_out'
student_err = 'student_err'
golden = 'golden.txt'

f_student_out = open(student_out, 'w')
f_student_err = open(student_err, 'w')

# Execute program
try:
    retcode = subprocess.call(mycmd + ' ' + myarg, stdout=f_student_out, stderr=f_student_err)
    if retcode < 0:
        print("Child was terminated by signal", -retcode, file=f_student_stderr);
    else:
        if retcode != 0:
            print("Child returned", retcode, file=f_student_stderr);
except OSError as e:
    print("Execution failed:", e, file=f_student_stderr);

f_student_out.close()
f_student_err.close()
#sys.stdout.close()
#sys.stderr.close()

# Clean pre-existing pass/fail files
try:
    os.remove('pass')
except OSError:
    pass
try:
    os.remove('fail')
except OSError:
    pass


# Check outputs
if retcode != 0:
    passfail = 'fail'
else:
    f_student_out = open(student_out, 'r')
    f_golden = open('golden.txt', 'r')
    set_student = set(f_student_out)
    set_golden = set(f_golden)

    same = set_student.intersection(set_golden);
    same.discard('\n')

    #diff = set_student.difference(set_golden).union(set_golden.difference(set_student))
    # Writes in order {Golden, Student}
    diff = set_golden.difference(set_student).union(set_student.difference(set_golden))
    diff.discard('\n')

    f_results = open('results.txt', 'w')
    print("Sames(%d):%s"%(len(same), same), file = f_results)
    print("Diffs(%d):%s"%(len(diff), diff), file = f_results)

    if (len(diff) == 0):
        passfail = 'pass'
    else:
        passfail = 'fail'



f_passfail = open(passfail, 'w')
f_passfail.close()
