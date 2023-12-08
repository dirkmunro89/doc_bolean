import os
import pymesh
#
# Assumes file naming as follows.
# At least one file msh_0_nul.stl, then
# msh_%d_%str.stl. We start with msh_0.stl,
# then apply bolean operations, sequentially,
# where %d is an integer running from 1 -> N
# and %str is either:
#   - dif : difference 
#   - uni : union
#   - int : intersection
#   - sym : symmetric difference
#
# rather defensive; if anything strange in file 
# namings, we abort
#
names=[]
for subdir, dirs, files in os.walk("/home/"):
#
    for file in files:
        if file.endswith((".stl")) and "msh_" in file:
            names.append(file)
        elif file.endswith((".stl")) and 'output' not in file:
            print('Error; stl in /home/ which does not follow naming convention:')
            print('%s'%file)
            os._exit(1)
#
N=len(names)
#
meshes=[]
numbers=[]
operations=[]
for i in range(N):
#
    tmp=names[i].split('_')
    num=int(tmp[1])
    opp=tmp[-1].split('.')[0]
    if opp != 'dif' and opp != 'nul' and opp != 'uni' and opp != 'sym' and opp != 'int':
        print('Error; unrecognised operation:')
        print('%s'%names[i])
    msh=pymesh.load_mesh("/home/"+names[i])
    operations.append(opp)
    numbers.append(num)
    meshes.append(msh)
#
if max(numbers) != N-1:
    print('Error')
    os._exit(1)
#
if len(set(numbers)) != len(numbers):
    print('Error')
    os._exit(1)
#
engine='igl'
flgs=[0]*N
for i in range(N):
#
    j=numbers.index(i)
    if i == 0:
        working=meshes[j]
        print('- mesh %d (nul): %s'%(i,names[j]))
    else:
        current=meshes[j]
        print('- mesh %d (%s): %s'%(i,operations[j],names[j]))
        if operations[j] == 'dif':
            working=pymesh.boolean(working, current, operation="difference",engine=engine)
        elif operations[j] == 'uni':
            working=pymesh.boolean(working, current, operation="union",engine=engine)
        elif operations[j] == 'int':
            working=pymesh.boolean(working, current, operation="intersection",engine=engine)
        elif operations[j] == 'sym':
            working=pymesh.boolean(working, current, operation="symmetric_difference",engine=engine)
        else:
            print('Error')
            os._exit(1)
#
print("Writing output to: %s"%('home/output.stl'))
pymesh.save_mesh("/home/output.stl",working)
os._exit(1)
#
