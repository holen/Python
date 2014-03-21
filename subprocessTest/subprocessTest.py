#-* coding:UTF-8 -*
#!/usr/bin/env python

import shlex, subprocess

command_line = raw_input()
args = shlex.split(command_line)
print args
# p = subprocess.Popen(args)
p = subprocess.Popen(args,stdout=subprocess.PIPE)
out = p.stdout.readlines()
print out

for line in out:
    print line.strip()

print subprocess.check_call('ls -ahl /tmp',shell=True)

cmd = "foo.txt > bar.txt"
ret = subprocess.call(cmd, shell=True)
if ret != 0:
    if ret < 0:
        print "Killed by signal", -ret
    else:
        print "Command failed with return code", ret
else:
    print "SUCCESS!!"
