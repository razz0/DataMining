# coding=utf-8
from collections import defaultdict
import operator

import students as s
import apriori_sequential as a
import matplotlib.pyplot as plt
from pandas import Series, DataFrame

s.read_students()

graduated = [stud for stud in s.students if
             stud.get_course_by_name('Kandidaatin tutkielma', grades=s.PASSED_GRADES) and
             stud.get_course_by_name('Ohjelmistotuotantoprojekti', grades=s.PASSED_GRADES)]

good_studs = []
bad_studs = []
course_cats = defaultdict(list)
thesis_cats = defaultdict(list)
time_cats = defaultdict(list)

for stud in graduated:
    #passed = stud.filter_courses(stud.courses, grades=s.PASSED_GRADES)

    grad_time = max(
        stud.get_course_by_name('Kandidaatin tutkielma', grades=s.PASSED_GRADES)[0]['time'],
        stud.get_course_by_name('Ohjelmistotuotantoprojekti', grades=s.PASSED_GRADES)[0]['time'],
    )

    start_time = min(
        [c['time'] for c in stud.filter_courses(stud.courses, grades=s.PASSED_GRADES, timespan=('1900-01', grad_time))]
    )

    stud.pre_grad_courses = stud.filter_courses(stud.courses, grades=s.PASSED_GRADES, timespan=('1900-01', grad_time))

    stud.average = sum([int(course['grade']) for course in stud.pre_grad_courses]) / float(len(stud.pre_grad_courses))
    stud.thesis = max([int(course['grade']) for course in stud.pre_grad_courses
                       if course['name'] == 'Kandidaatin tutkielma'])

    course_cats[len(stud.pre_grad_courses)].append(stud.average)
    thesis_cats[len(stud.pre_grad_courses)].append(stud.thesis)

    years = int(grad_time[:4]) + float(grad_time[5:7]) / 12 - (int(start_time[:4]) + float(start_time[5:7]) / 12)
    time_cats[years].append(stud.average)

    if stud.average >= 3.5:
        good_studs.append(stud)
    elif stud.average < 3.5:
        bad_studs.append(stud)

for key, value in course_cats.iteritems():
    course_cats[key] = sum(value) / float(len(value))

for key, value in thesis_cats.iteritems():
    thesis_cats[key] = sum(value) / float(len(value))

for key, value in time_cats.iteritems():
    time_cats[key] = sum(value) / float(len(value))

#ts = Series([stud.average for stud in graduated], [len(stud.pre_grad_courses) for stud in graduated])
#df = DataFrame(course_cats)
df = Series(course_cats)
df.plot()
plt.ylabel('average grade')
plt.xlabel('number of passed courses')
plt.savefig('passed_grades.pdf')

plt.close()

ts = Series(thesis_cats)
ts.plot()
plt.ylabel('thesis grade')
plt.xlabel('number of passed courses')
plt.savefig('passed_thesis.pdf')

plt.close()

ts = Series(time_cats)
ts.plot()
plt.ylabel('average grade')
plt.xlabel('years of studying')
plt.savefig('time_grades.pdf')

seqs = [stud.course_sequence for stud in graduated]
#        stud.get_course_by_name('Henkilökohtainen opintosuunnitelma kandidaatintutkintoa varten', grades=s.PASSED_GRADES) and

#print seqs[0]
#print len(seqs)
print 'Good students n: %s, courses: %.3f' % \
      (len(good_studs), sum([len(stud.pre_grad_courses) for stud in good_studs]) / float(len(good_studs)))
print 'Bad students n: %s, courses: %.3f' % \
      (len(bad_studs), sum([len(stud.pre_grad_courses) for stud in bad_studs]) / float(len(bad_studs)))

freq_seqs = a.apriori_sequential([stud.course_sequence for stud in good_studs], minsup=0.5, verbose=1)

biased_seqs = {}

for seq_dict in freq_seqs:
    seq = seq_dict.items()[0][0]
    assert len(seq_dict.items()) == 1
    if len(seq) > 5:
        avgs = [stud.average for stud in graduated if a.is_subsequence(seq, stud.course_sequence)]
        avgs = sum(avgs) / float(len(avgs))
        biased_seqs[seq] = seq_dict.items()[0][1] * (avgs * avgs)

#print freq_seqs[-1]
for seq in sorted(biased_seqs.items(), key=operator.itemgetter(1))[-10:]:
    print seq
print len(freq_seqs)


