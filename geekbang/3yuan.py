attributes = ['name', 'dob', 'gender']

values =[['jason', '2000-01-01', 'male'], ['mike', '1999-01-01', 'male'], ['nancy', '2001-02-01', 'female']]

l = []
ll = []
for value in values:
    d = {}
    for i in range(0, len(attributes)):
        d[attributes[i]] = value[i]
    l.append(d)

    dd = {}
    for index, item in enumerate(attributes):
        dd[item]=value[index]
    ll.append(dd)

print(l)
print(ll)

nl = [dict(zip(attributes, v)) for v in values]
print(nl)

