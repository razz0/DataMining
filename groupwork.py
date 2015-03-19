import students as s

s.read_students()

OLD_TIME = ('1900-01', '2010-01')
NEW_TIME = ('2010-02', '2020-01')

INTERESTING_COURSESETS = [s.OHJ_PER, s.OHJ_JAT, s.OHJ_PER | s.OHJ_JAT]

for courseset in INTERESTING_COURSESETS:

    passed_old = s.filter_students_by_courses(s.students, courseset, grades=s.PASSED_GRADES, timespan=OLD_TIME)
    failed_old = s.filter_students_by_courses(s.students, courseset, grades=s.FAILED_GRADES, timespan=OLD_TIME)
    passed_new = s.filter_students_by_courses(s.students, courseset, grades=s.PASSED_GRADES, timespan=NEW_TIME)
    failed_new = s.filter_students_by_courses(s.students, courseset, grades=s.FAILED_GRADES, timespan=NEW_TIME)

    print 'Percentage of participants passing old %s: %s' % \
          (list(courseset), len(passed_old) / float(len(passed_old | failed_old)))
    print 'Percentage of participants passing new %s: %s' % \
          (list(courseset), len(passed_new) / float(len(passed_new | failed_new)))
