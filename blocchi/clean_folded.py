import sys
f=open(sys.argv[1])
o=open(sys.argv[2], 'w')
line=f.readline()
while(line):
    o.write(line)
    line=f.readline()
    o.write(line)
    line=f.readline()
    line=f.readline()
