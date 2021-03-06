'''A module for handling Data Mining 2015 course data set.'''

import re
import apriori

ALL_GRADES = set(['0', '1', '2', '3', '4', '5'])
FAILED_GRADES = set(['0'])
# PASSED_GRADES = ['1', '2', '3', '4', '5', 'Hyv.', 'HT', 'TT']
PASSED_GRADES = ALL_GRADES - FAILED_GRADES

all_courses = set()
students = []
timestamps = set()

OHJ_PER = set(['Ohjelmoinnin perusteet'])
OHJ_JAT = set(['Ohjelmoinnin jatkokurssi'])
OHJ_JAT2 = set([('Ohjelmoinnin jatkokurssi', 'Java-ohjelmointi')])


def read_students():
    '''Read all student information from file'''

    f = open("data.txt", "r")
    lines = f.readlines()
    f.close()

    global all_courses
    all_courses = set()
    global students
    students = []
    global timestamps
    timestamps = set()

    def _parse_student_row(row):
        '''Parse a row'''

        reg_year, row = row.split(' ', 1)
        row += ' '  # For unpacking rows last split

        s_courses = []

        while row:
            course_time, row = row.split(' ', 1)
            course_code, row = row.split(' ', 1)

            name_matches = re.match(r'(\")(.*?)(\" \d+\.\d)', row)
            course_name = name_matches.group(2)
            row = row[name_matches.start(3) + 2:]

            course_credits, row = row.lstrip().split(' ', 1)
            course_grade, row = row.split(' ', 1)

            s_courses.append((course_time, course_code, course_name, course_credits, course_grade.rstrip()))

        return reg_year, s_courses

    for line in lines:
        reg_year, courses = _parse_student_row(line)

        student = Student(reg_year)
        students.append(student)

        for course in courses:
            student.add_course(*course)
            all_courses.add((course[1], course[2]))
            timestamps.add(course[0])

        student.create_course_sequence()


class Student(object):
    '''Single student course history'''

    def __init__(self, reg_time):
        self.registration_year = reg_time
        self.courses = []
        self.course_sequence = []
        self.course_sequence_timestamps = []  # TODO: implement usage

    def add_course(self, time, code, name, credits, grade):
        self.courses.append(dict(time=time, code=code, name=name, credits=credits, grade=grade))

    def filter_courses(self, courses, grades=(), timespan=()):
        return [c for c in courses if ((not grades or c.get('grade') in grades) and
                                       (not timespan or timespan[0] <= c.get('time') <= timespan[1]))]

    def get_course_by_name(self, c_name, grades=(), timespan=()):
        '''
        Get course dict by course name. Filter by grades and timespan.

        :param c_name: course name as string OR tuple to allow for multiple names of single course
        :param grades: list of grades to use
        :param timespan: timespan start and end as tuple
        :rtype: list[dict]
        '''
        if isinstance(c_name, basestring):
            correct_names = [c for c in self.courses if c.get('name') == c_name]
        else:
            correct_names = [c for c in self.courses if c.get('name') in c_name]

        return self.filter_courses(correct_names, grades=grades, timespan=timespan)

    def create_course_sequence(self):
        """Create a sequence (list) of students' course names"""
        course_dict = {}
        for c in self.courses:
            if c['time'] in course_dict:
                course_dict[c['time']] += [c['name']]
            else:
                course_dict[c['time']] = [c['name']]

        #for time in timestamps:
        #    if time not in course_dict:
        #        course_dict[time] = [(0,)]

        self.course_sequence = [tuple(course_dict[key]) for key in sorted(course_dict)]


def count_course_attempts(course_name, grades=()):
    '''
    Count how many attempts have been taken at a course. Filter by grades if given.

    :param course_name: Course name (finnish)
    :param grades: list of grades to use (use all if not given)
    '''
    count = 0
    for stud in students:
        courses = stud.get_course_by_name(course_name, grades=grades)
        if courses:
            count += 1

    return count


def filter_students_by_courses(studs, courses, grades=(), timespan=()):
    """
    :param studs: list[Student]
    :param courses: enhanced itemset of course names (or tuples for multiple possible names of single course)
    :param grades: grades to use (use all if not given)
    :return: set[Student]
    """
    assert not isinstance(courses, basestring)  # Common error to forget to put single course name to list

    return set([stud for stud in studs if
                all([stud.get_course_by_name(course, grades=grades, timespan=timespan) for course in courses])])


def support_count(course_set, studs=students, grades=()):
    '''Measure support count for an (enhanced) itemset'''

    return len(filter_students_by_courses(studs, course_set, grades=grades))


def support(course_set, studs=students, grades=()):
    '''Calculate support for an (enhanced) itemset'''

    return support_count(course_set, studs=studs, grades=grades) / float(len(studs))


def rule_implication(a, b):
    '''Check how much itemset a implies itemset b. Returns support and confidence as a tuple.'''

    return support(a | b), support_count(a | b) / float(support_count(a))


def get_course_transactions():
    return [tuple(set([course['name'] for course in stud.courses])) for stud in students]


def get_all_course_names():
    return list(set([name for (code, name) in all_courses]))  # There are duplicates


def get_closed_frequent_itemsets(minsup, verbose=True):
    """
    Get closed frequent itemsets from the course dataset

    :param minsup:
    :return:
    """

    read_students()
    transactions = get_course_transactions()
    frequent = apriori.apriori(transactions, get_all_course_names(), minsup, verbose=verbose)

    pruned = []

    for itemset in frequent:
        for itemset_longer in [freq for freq in frequent if len(freq) == len(itemset) + 1]:
            if itemset in apriori.generate_transaction_subsets(itemset_longer, len(itemset)) and \
                    apriori.support_count(itemset, transactions) != apriori.support_count(itemset_longer, transactions):
                pruned += [itemset]
                break

    return pruned


def get_courses_with_categories():
    '''Transform categorical attributes to items and add them to course transactions'''

    itemsets = []
    for stud in students:
        stud_items = []
        for course in stud.courses:
            stud_items.append(course['name'])
            grade = int(course['grade'])
            passed = 'PASS'
            if grade >= 4:
                grade = '4-5'
            elif grade >= 1:
                grade = '1-3'
            else:
                grade = 'FAIL'
                passed = 'FAIL'

            stud_items.append("%s - grade: %s" % (course['name'], grade))
            stud_items.append("%s - passed: %s" % (course['name'], passed))

        enrolled = int(stud.registration_year)
        enrolled = '> 2010' if enrolled > 2010 else '< 2010' if enrolled < 2010 else '2010'

        stud_items.append("Enrollment Year %s" % enrolled)

        itemsets.append(stud_items)

    #alphabet = set([item for itemset in itemsets for item in itemset])
    return itemsets #, alphabet