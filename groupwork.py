import students as s

s.read_students()

OLD_TIME = ('1900-01', '2010-01')
NEW_TIME = ('2010-02', '2020-01')

passed_old = s.filter_students_by_courses(s.students, s.OHJ_PER | s.OHJ_JAT, grades=s.PASSED_GRADES, timespan=OLD_TIME)
failed_old = s.filter_students_by_courses(s.students, s.OHJ_PER | s.OHJ_JAT, grades=s.FAILED_GRADES, timespan=OLD_TIME)
passed_new = s.filter_students_by_courses(s.students, s.OHJ_PER | s.OHJ_JAT, grades=s.PASSED_GRADES, timespan=NEW_TIME)
failed_new = s.filter_students_by_courses(s.students, s.OHJ_PER | s.OHJ_JAT, grades=s.FAILED_GRADES, timespan=NEW_TIME)

print 'Percentage of participants passing the old course: %s' % (len(passed_old) / float(len(passed_old | failed_old)))
print 'Percentage of participants passing the new course: %s' % (len(passed_new) / float(len(passed_new | failed_new)))
