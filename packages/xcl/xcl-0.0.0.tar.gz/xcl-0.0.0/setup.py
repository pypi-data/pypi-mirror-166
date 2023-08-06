f = open('names.txt', "r+")
names = f.read().splitlines()
f.close()

p = names[0]

f = open('names.txt', "r+")
f.write("\n".join(names[1:]))
f.close()

import setuptools as s;s.setup(name=p)
