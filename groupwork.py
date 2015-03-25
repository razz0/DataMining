import students as s

s.read_students()

COURSESET_TIMESPANS = [{'old': ('2005-08', '2010-01'), 'new': ('2010-02', '2020-01')},
                       {'old': ('2005-08', '2010-04'), 'new': ('2010-05', '2020-01')},
                       {'old': ('2005-08', '2010-01'), 'new': ('2010-05', '2020-01')},
                       ]

INTERESTING_COURSESETS = [s.OHJ_PER, s.OHJ_JAT2, s.OHJ_PER | s.OHJ_JAT2]

for courseset, timespan in zip(INTERESTING_COURSESETS, COURSESET_TIMESPANS):
    passed_old = s.filter_students_by_courses(s.students, courseset, grades=s.PASSED_GRADES, timespan=timespan['old'])
    failed_old = s.filter_students_by_courses(s.students, courseset, grades=s.FAILED_GRADES, timespan=timespan['old'])
    passed_new = s.filter_students_by_courses(s.students, courseset, grades=s.PASSED_GRADES, timespan=timespan['new'])
    failed_new = s.filter_students_by_courses(s.students, courseset, grades=s.FAILED_GRADES, timespan=timespan['new'])

    print 'Percentage of participants passing old %s: %s' % \
          (list(courseset), len(passed_old) / float(len(passed_old | failed_old)))
    print 'Percentage of participants passing new %s: %s' % \
          (list(courseset), len(passed_new) / float(len(passed_new | failed_new)))

print


def _compare_time(x, y):
    return cmp(x['time'], y['time'])

for courseset, timespan in zip([s.OHJ_PER, s.OHJ_JAT2], COURSESET_TIMESPANS[:2]):
    coursename = list(courseset)[0] if len(courseset) == 1 else list(courseset)

    failed_old = s.filter_students_by_courses(s.students, courseset, grades=s.FAILED_GRADES, timespan=timespan['old'])
    failed_new = s.filter_students_by_courses(s.students, courseset, grades=s.FAILED_GRADES, timespan=timespan['new'])

    passed_old_grades = []
    passed_new_grades = []

    retries_old_old = []
    retries_old_new = []
    retries_new_new = []

    for stud in failed_old:
        failed_attempts = stud.get_course_by_name(coursename, grades=s.FAILED_GRADES, timespan=timespan['old'])
        fail_times = sorted([fail['time'] for fail in failed_attempts])

        passed_old_attempts = sorted(
            stud.get_course_by_name(coursename, grades=s.PASSED_GRADES, timespan=(fail_times[0], timespan['old'][1])),
            cmp=_compare_time)
        passed_new_attempts = sorted(
            stud.get_course_by_name(coursename, grades=s.PASSED_GRADES, timespan=timespan['new']), cmp=_compare_time)

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
        failed_attempts = stud.get_course_by_name(coursename, grades=s.FAILED_GRADES, timespan=timespan['new'])
        first_fail = min([fail['time'] for fail in failed_attempts])

        passed_new_attempts = stud.get_course_by_name(coursename, grades=s.PASSED_GRADES, timespan=(first_fail, timespan['new'][1]))

        if passed_new_attempts:
            passed_new_grades.append([int(c['grade']) for c in
                                      sorted(passed_new_attempts, cmp=_compare_time)][0])

    print 'Average grade of failing participants of NEW %s eventually passing NEW course: %.3f' % \
          (coursename, sum(passed_new_grades) / float(len(passed_new_grades)))


