# coding=utf-8
from collections import defaultdict, OrderedDict
import operator
import pylab

import students as s
import apriori as a
import matplotlib.pyplot as plt
from pandas import Series, DataFrame
import joblib

s.read_students()

combos = defaultdict(int)
separates = defaultdict(int)
amounts = defaultdict(int)

timestamps = sorted(s.timestamps)
#for time in sorted(s.timestamps)[:50]:
for time_index, time in enumerate(timestamps):
    print 'Timestamp: %s' % time
    time_start = time
    time_end = time
    #time_end = timestamps[time_index + 1]
    for stud in s.students:
        courses_now = stud.filter_courses(stud.courses, grades=s.PASSED_GRADES, timespan=(time_start, time_end))
        if len(courses_now) < 2:
            continue
        course_ids = [c['code'] for c in courses_now]
        course_combinations = a._apriori_gen(sorted([(course,) for course in set(course_ids)]))
        #print 'Courses: %s, Combos: %s' % (len(courses_now), len(course_combinations))
        for combo_ids in course_combinations:
            c1 = [c for c in courses_now if c['code'] == combo_ids[0]]
            c2 = [c for c in courses_now if c['code'] == combo_ids[1]]
            if c1 and c2:
                grade1 = max([c['grade'] for c in c1])
                grade2 = max([c['grade'] for c in c2])
                name1 = c1[0]['name']
                name2 = c2[0]['name']
                index = (name1, name2)
                #print "Combo: %s" % index
                combos[index] += (int(grade1) + int(grade2)) / 2.0
                amounts[index] += 1

good_combos = {}
bad_combos = {}
good_diffs = {}

uninteresting_courses = ['Säteilykentät ja fotonit',
                         'Johdatus fysiikan opettajan opintoihin',
                         'Biologinen kemia',
                         'Yleinen kemia I',
                         'Yleinen kemia II',
                         'Fysiikan perusopintojen laboratoriotyöt',
                         'Orgaaninen kemia I',
                         'Orgaaninen kemia II',
                         'Kemian orientoivat opinnot',
                         'Matematiikkaa kemisteille',
                         'Epäorgaanisen kemian perustyöt IA',
                         'Epäorgaanisen kemian perustyöt IB',
                         'Termodynamiikka ja dynamiikka',
                         'Liike ja voimat',
                         'Topologia I',
                         'Lukiomatematiikan kertauskurssi',
                         'Henkilökohtainen opintosuunnitelma kandidaatintutkintoa varten',
                         'Sähkömagnetismi',
                         'Turvallinen työskentely laboratoriossa',
                         'Fysikaalisten tieteiden esittely',
                         'Ohjaajatuutorointiin osallistuminen, kevätlukukausi',
                         'Ohjaajatuutorointiin osallistuminen, syyslukukausi',
                         'Äidinkieli',
                         'Mekaniikka',
                         'Matemaattiset apuneuvot I',
                         'Suhteellisuusteorian perusteet',
                         'Kvanttifysiikan perusteet',
                         ]

uninteresting_combos = ['Algebra I &\n Logiikka I',
                        ]

for key in combos:
    combos[key] /= float(amounts[key])
    index = ' &\n '.join(key)
    if amounts[key] > 30 and not (set(uninteresting_courses) & set(key)) and not index in uninteresting_combos:

        good_combos[index] = combos[key]

#        grade_sum = 0
#        grade_n = 0
#        for stud in s.students:
#            courses = stud.filter_courses(stud.courses, grades=s.PASSED_GRADES)
#            courses = [c for c in courses if c['name'] in key]
#            grade_sum += sum(courses)
#            grade_n += 1
            # TODO: Get difference

ordered = sorted(good_combos.items(), key=operator.itemgetter(1))  # Sort by value
#print ordered
good_combos = OrderedDict(ordered[-10:])
bad_combos = OrderedDict(ordered[10:0:-1])

#combos['Foo & Bar'] = 5.0
#combos['Bar & Baz'] = 1.0

#df = Series(good_combos)
df = DataFrame.from_dict(good_combos, orient='index')

df.plot()
df.plot(kind='barh', figsize=(18, 10), fontsize=14, legend=False)
plt.xlabel('Average grade')
plt.ylabel('Courses')
#ax = pylab.add_subplot(111)
#ax.bar( [0,1,2], [1,3,5] )
#ax.set_xticks( [ 0.5, 1.5, 2.5 ] )
#ax.set_xticklabels( ['tom','dick','harry'], rotation=45)
plt.savefig('best_combos.pdf', bbox_inches='tight', dpi=100)

plt.close()

df = DataFrame.from_dict(bad_combos, orient='index')
df.plot()
df.plot(kind='barh', figsize=(18, 10), fontsize=14, legend=False)
plt.xlabel('Average grade')
plt.ylabel('Courses')
#ax = pylab.add_subplot(111)
#ax.bar( [0,1,2], [1,3,5] )
#ax.set_xticks( [ 0.5, 1.5, 2.5 ] )
#ax.set_xticklabels( ['tom','dick','harry'], rotation=45)
plt.savefig('worst_combos.pdf', bbox_inches='tight', dpi=100)

plt.close()

joblib.dump(combos, 'combos.pkl')