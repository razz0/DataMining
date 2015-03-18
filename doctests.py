'''
Doctests for students.py.

>>> import students as s
>>> s.read_students()
>>> print len(s.filter_students_by_courses(s.students, s.OHJ_PER))
1200
>>> print len(s.filter_students_by_courses(s.students, s.OHJ_JAT, grades=s.PASSED_GRADES))
856
>>> print len(s.filter_students_by_courses(s.students, s.OHJ_PER | s.OHJ_JAT))
983
>>> print "%.3f - %.3f" % s.rule_implication(s.OHJ_PER, s.OHJ_JAT)
0.342 - 0.819

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

'''

if __name__ == "__main__":
    print 'Running doctests'
    import doctest
    res = doctest.testmod()
    if not res[0]:
        print 'OK!'

