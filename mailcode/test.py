import os
import subprocess


res2 = os.system("bash test1.sh")
res1 = subprocess.Popen("bash test1.sh", stdout=subprocess.PIPE, shell=True)

res = subprocess.Popen("bash test.sh", stdout=subprocess.PIPE, shell=True)

(output, err) = res.communicate()
p_status = res.wait()
print "Command output : ", output
print "Command exit status/return code : ", p_status
print err

print "---------"

print res2
#
#
#
# if res1 == 0:
#     print "success"
# else:
#     print(type(res1))
#     print("1-{}-1".format(res1))
#     print "failed"

(output1, err1) = res1.communicate()
p_status1 = res1.wait()
print "Command output : ", output1
print "Command exit status/return code : ", p_status1
