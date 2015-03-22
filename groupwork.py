import students as s

s.read_students()

OLD_TIME = ('2005-08', '2010-01')
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

print

def _compare_time(x, y):
    return cmp(x['time'], y['time'])

for courseset in [s.OHJ_PER, s.OHJ_JAT2]:
    coursename = list(courseset)[0] if len(courseset) == 1 else list(courseset)

    failed_old = s.filter_students_by_courses(s.students, courseset, grades=s.FAILED_GRADES, timespan=OLD_TIME)
    failed_new = s.filter_students_by_courses(s.students, courseset, grades=s.FAILED_GRADES, timespan=NEW_TIME)

    passed_old_grades = []
    passed_new_grades = []

    retries_old_old = []
    retries_old_new = []
    retries_new_new = []

    for stud in failed_old:
        failed_attempts = stud.get_course_by_name(coursename, grades=s.FAILED_GRADES, timespan=OLD_TIME)
        fail_times = sorted([fail['time'] for fail in failed_attempts])

        passed_old_attempts = sorted(
            stud.get_course_by_name(coursename, grades=s.PASSED_GRADES, timespan=(fail_times[0], OLD_TIME[1])),
            cmp=_compare_time)
        passed_new_attempts = sorted(
            stud.get_course_by_name(coursename, grades=s.PASSED_GRADES, timespan=NEW_TIME), cmp=_compare_time)

        if passed_old_attempts:
            passed_old_grades.append([int(c['grade']) for c in passed_old_attempts][0])
        elif passed_new_attempts:
            passed_new_grades.append([int(c['grade']) for c in passed_new_attempts][0])

        #if len(fail_times) > 1 and fail_times[1] < passed_old_attempts[0]['time']:
        #    retries_old_old.append('fail')
        #elif

    print 'Average grade of failing participants of OLD %s eventually passing OLD course: %.3f' % \
          (coursename, sum(passed_old_grades) / float(len(passed_old_grades)))
    print 'Average grade of failing participants of OLD %s eventually passing NEW course: %.3f' % \
          (coursename, sum(passed_new_grades) / float(len(passed_new_grades)))

    passed_new_grades = []

    for stud in failed_new:
        failed_attempts = stud.get_course_by_name(coursename, grades=s.FAILED_GRADES, timespan=NEW_TIME)
        first_fail = min([fail['time'] for fail in failed_attempts])

        passed_new_attempts = stud.get_course_by_name(coursename, grades=s.PASSED_GRADES, timespan=(first_fail, NEW_TIME[1]))

        if passed_new_attempts:
            passed_new_grades.append([int(c['grade']) for c in
                                      sorted(passed_new_attempts, cmp=_compare_time)][0])

    print 'Average grade of failing participants of NEW %s eventually passing NEW course: %.3f' % \
          (coursename, sum(passed_new_grades) / float(len(passed_new_grades)))


