import apriori as a
import students as s

s.read_students()
#cc = [c[1] for c in s.all_courses]
trans = [tuple([course['code'] for course in stud.courses]) for stud in s.students]

#new_cc = [c[0] for c in a.apriori(trans, cc, 0.05, fixed_k=1)]

#assert len(new_cc) == 102

# Map course names to integers

course_map_to_int = {}
course_map_to_str = {}

i = 0
courses = []

for code, name in s.all_courses:
    course_map_to_int[code] = i
    course_map_to_str[i] = name
    courses.append(i)
    i += 1

#print 'Course map <%s>: %s' % (len(course_map), course_map)

#print trans[4]

#print course_map_to_int

#print [course_map[t] for t in trans[4] if t in new_cc]
#quit()

new_trans = [[course_map_to_int[course] for course in tr] for tr in trans]


assert len(new_trans) == len(trans)
assert 0 < len(new_trans[666]) == len(trans[666]), new_trans

assert len(new_trans[371]) == 18, len(new_trans[371])

#del cc
del trans
del s


print 'This will take a while...'

best = a.apriori(new_trans, courses, 0.05, verbose=True)[-1]

print [course_map_to_str[code_index] for code_index in best]

