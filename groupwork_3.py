# coding=utf-8
from collections import defaultdict
import operator

import students as s
import apriori_sequential as a
import matplotlib.pyplot as plt
from pandas import Series, DataFrame
import joblib

s.read_students()

combos = {}
amounts = defaultdict(int)

for index1, course1 in enumerate(list(s.all_courses)[:1]):
    c1_name = course1[1]
    for index2, course2 in enumerate(list(s.all_courses)[index1 + 1:]):
        print index2
        c2_name = course2[1]
        for time in s.timestamps:
            for stud in s.students:
                c1 = stud.get_course_by_name(c1_name, grades=s.PASSED_GRADES, timespan=(time, time))
                c2 = stud.get_course_by_name(c2_name, grades=s.PASSED_GRADES, timespan=(time, time))
#                if len(c1) > 1:
#                    print 'Duplicate %s' % c1
#                if len(c2) > 1:
#                    print 'Duplicate %s' % c2
                if c1 and c2:
                    grade1 = max([c['grade'] for c in c1])
                    grade2 = max([c['grade'] for c in c2])
                    name1 = c1[0]['name']
                    name2 = c2[0]['name']
                    index = "%s & %s" % (c1, c2)
                    print "Combo: %s" % index
                    combos[index] = (int(grade1) + int(grade2)) / 2.0
                    amounts[index] += 1

for key in combos:
    combos[key] = combos[key] / float(amounts)

#combos['Foo & Bar'] = 5.0
#combos['Bar & Baz'] = 1.0

df = Series(combos)
df.plot()
plt.ylabel('grade difference')
plt.xlabel('courses')
plt.savefig('best_combos.pdf')

plt.close()

