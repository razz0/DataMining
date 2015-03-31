import apriori as a
import students as s

s.read_students()
cc = [c[0] for c in s.all_courses]
trans = [tuple([course['code'] for course in stud.courses]) for stud in s.students]

new_cc = a.apriori(trans, cc, 0.05, fixed_k=1)
new_trans = [[course for course in tr if course in new_cc] for tr in trans]

assert len(new_trans) == len(trans)
assert len(new_trans[666]) < len(trans[666])

del cc
del trans
del s

print 'This will take a while...'
print a.apriori(new_trans, new_cc, 0.05, verbose=True)[-1]