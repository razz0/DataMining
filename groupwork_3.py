# coding=utf-8
from collections import defaultdict, OrderedDict
import operator
import pylab
import pprint

import students as s
import apriori as a
import matplotlib.pyplot as plt
from pandas import Series, DataFrame
import joblib

s.read_students()

combos = defaultdict(int)
separates = defaultdict(int)
amounts = defaultdict(int)

# Get simultaneous 2 course combinations and their grade sums

timestamps = sorted(s.timestamps)

for time_index, time in enumerate(timestamps):
    # print 'Timestamp: %s' % time
    time_start = time
    time_end = time
    # time_end = timestamps[time_index + 1]
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
                         'Termodynamiikka',
                         'TVT- ajokortti',
                         'Termofysiikan perusteet',
                         'Integroidut TVT-opinnot',
                         'Vuorovaikutukset ja kappaleet',
                         ]

uninteresting_combos = ['Algebra I &\n Logiikka I',
                        'Analyysi I &\n Lineaarialgebra ja matriisilaskenta II',
                        'Analyysi I &\n Johdatus diskreettiin matematiikkaan',
                        'Lineaarialgebra ja matriisilaskenta II &\n Johdatus diskreettiin matematiikkaan',
                        'Analyysi II &\n Logiikka I',
                        'Geometria &\n Logiikka I',
                        'Matemaattiset apuneuvot I &\n Maailmankaikkeus nyt',
                        ]

grade_sums = {}
grade_amounts = {}

for (course_code, course_name) in s.all_courses:
    grade_sum = 0
    grade_n = 0
    for stud in s.filter_students_by_courses(s.students, [course_name], grades=s.PASSED_GRADES):
        courses = stud.get_course_by_name(course_name)
        grade_sum += sum([int(c['grade']) for c in courses])
        grade_n += len(courses)
    if course_name not in grade_sums:
        grade_sums[course_name] = grade_sum
        grade_amounts[course_name] = grade_n
    else:
        if course_name not in \
                ['Ohjelmistotekniikan menetelmät', 'Käyttöjärjestelmät', 'TVT-ajokortti', 'Sähkömagnetismi']:
            raise Exception('Double course name found %s %s' % (course_code, course_name))
        else:
            grade_sums[course_name] += grade_sum
            grade_amounts[course_name] += grade_n

#print grade_sums['Java-ohjelmointi']
#print grade_amounts['Java-ohjelmointi']

good_diffs = {}

for key in combos:
    index = ' &\n '.join(key)
    if amounts[key] >= 10 and not (set(uninteresting_courses) & set(key)) and index not in uninteresting_combos \
            and grade_amounts[key[0]] - amounts[key] >= 10 and grade_amounts[key[1]] - amounts[key] >= 10:

        # good_combos[index] = combos[key] / float(amounts[key])
        good_diffs[index] = combos[key] / float(amounts[key]) - \
            ((grade_sums[key[0]] + grade_sums[key[1]]) / 2.0 - combos[key]) / \
            ((grade_amounts[key[0]] + grade_amounts[key[1]]) / 2.0 - amounts[key])

ordered = sorted(good_diffs.items(), key=operator.itemgetter(1))  # Sort by value

good_combos = OrderedDict(ordered[-10:])
bad_combos = OrderedDict(ordered[0:10][::-1])

print 'Best combos:'
pprint.pprint(ordered[-1:-10:-1])

print 'Worst combos:'
pprint.pprint(ordered[0:10])

df = DataFrame.from_dict(good_combos, orient='index')

df.plot()
df.plot(kind='barh', figsize=(18, 10), fontsize=18, legend=False)
plt.xlabel('Grade difference', fontsize=24)
plt.ylabel('Course combinations', fontsize=24)
#ax = pylab.add_subplot(111)
#ax.bar( [0,1,2], [1,3,5] )
#ax.set_xticks( [ 0.5, 1.5, 2.5 ] )
#ax.set_xticklabels( ['tom','dick','harry'], rotation=45)
plt.savefig('best_combos.pdf', bbox_inches='tight', dpi=100)

plt.close()

df = DataFrame.from_dict(bad_combos, orient='index')
df.plot()
df.plot(kind='barh', figsize=(18, 10), fontsize=18, legend=False, color='red')
plt.xlabel('Grade difference', fontsize=24)
plt.ylabel('Course combinations', fontsize=24)
#ax = pylab.add_subplot(111)
#ax.bar( [0,1,2], [1,3,5] )
#ax.set_xticks( [ 0.5, 1.5, 2.5 ] )
#ax.set_xticklabels( ['tom','dick','harry'], rotation=45)
plt.savefig('worst_combos.pdf', bbox_inches='tight', dpi=100)

plt.close()

joblib.dump(combos, 'combos.pkl')