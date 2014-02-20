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

print subprocess.call('ls -ahl /tmp',shell=True)
