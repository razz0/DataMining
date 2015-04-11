'''
Doctests for students.py.

>>> import students as s
>>> s.read_students()
>>> print len(s.filter_students_by_courses(s.students, s.OHJ_PER))
574
>>> print len(s.filter_students_by_courses(s.students, s.OHJ_JAT2, grades=s.PASSED_GRADES))
457
>>> print len(s.filter_students_by_courses(s.students, s.OHJ_PER | s.OHJ_JAT2))
467
>>> print "%.3f - %.3f" % s.rule_implication(s.OHJ_PER, s.OHJ_JAT2)
0.298 - 0.814

Test Student class:

>>> a = s.Student('2008')
>>> a.add_course('2010-10', '007', 'Test course', '4.0', '5')
>>> len(a.get_course_by_name('Test course'))
1
>>> len(a.get_course_by_name('Not existing course'))
0
>>> len(a.get_course_by_name(('Test course', 'Not existing course')))
1
>>> len(a.get_course_by_name('Test course', timespan=('2010-09', '2010-11')))
1
>>> len(a.get_course_by_name('Test course', grades=['5']))
1
>>> a.create_course_sequence()
>>> print a.course_sequence
[('Test course',)]

Apriori:

>>> import apriori as a
>>> cc = [c[0] for c in s.all_courses]
>>> trans = [tuple([course['code'] for course in stud.courses]) for stud in s.students]
>>> a.apriori(trans, cc, 0.4)
[('57016',), ('57043',)]

'''

if __name__ == "__main__":
    print 'Running doctests'
    import doctest
    res = doctest.testmod()
    if not res[0]:
        print 'OK!'

