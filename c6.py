# -*- encoding: utf-8 -*-
'''
Algorithm: Skill Transfer

INPUT: skills.json
OUTPUT: Simulate of execute with random action time length.

TA impletemented,

SWEB
AAAAAAAAAA
BBBBBBB

SWEW
AAAAAAAAAA
BBBBBBBBBB

ES
AAAAAAAAAA
          BBBBBBB

SBEB
AAAAAAA
  BBBBBBB

SAEW
AAAAAAAAA
    BBBBB

SAEB
AAAAAAAAAAA
  BBBBBB

E 111111111    4444444455555555
R 111112222223333
T      222222    33333344444   555

1: E R SWEB
2: R T SWEW
3: R T ES
4: E T ES
5: E T ES
'''

import json
import random
from datetime import datetime, timedelta
import math


def readJson(filename):
    """
    Get data from JSON file
    """
    fp = open(filename, "r")
    obj = json.load(fp)
    fp.close()
    return obj


def insertJsData(taskNames, tasks):
    """
    var tasks = [{
        "startDate": new Date(2009,1,3,10,52,03),
        "endDate": new Date(2009,1,3,11,52,03),
        "taskName": "E Job",
        "status": "RUNNING"
    }, {
        "startDate": new Date(2009,1,3,10,52,03),
        "endDate": new Date(2009,1,3,12,52,03),
        "taskName": "A Job",
        "status": "RUNNING"
    }];

    var taskStatus = {
        "SUCCEEDED": "bar",
        "FAILED": "bar-failed",
        "RUNNING": "bar-running",
        "KILLED": "bar-killed"
    };

    var taskNames = ["D Job", "P Job", "E Job", "A Job", "N Job"];
    """

    taskstrings = []
    for task in tasks:
        s = ""
        s += '"startDate": new Date' + \
            str(task["startDate"].timetuple()[:6]) + ','
        s += '"endDate": new Date' + str(task["endDate"].timetuple()[:6]) + ','
        s += '"taskName": "' + task["taskName"] + '",'
        s += '"status": "' + task["status"] + '"'
        taskstrings.append(s)

    if len(tasks) > 0:
        print 'var tasks = [{'
        print '},{'.join(taskstrings)
        print '}];'
    else:
        print 'var tasks = [];'

    # generate task status
    print 'var taskStatus =',
    taskStatus = {
        "0": "bar0",
        "1": "bar1",
        "2": "bar2",
        "3": "bar3",
        "4": "barx0",
        "5": "barx1",
        "6": "barx2",
        "7": "barx3",
    }
    print json.dumps(taskStatus)+';'

    # generate task names
    print 'var taskNames =',
    print json.dumps(taskNames)+';'


def insertTbl1(skill, taskNames):
    """
    <tr><td>ID</td><td>A</td><td>B</td><td>TA</td></tr>
    """
    for op in skill["operations"]:
        ID = op["id"]
        A = op["action"]["A"]["id"]
        B = op["action"]["B"]["id"]
        TA = op["action"]["TA"]

        print '<tr><td>',
        print '</td><td>'.join([str(ID), taskNames[A], taskNames[B], TA])
        print '</td></tr>',


def insertTbl2(tasks, taskNames):
    """
    <tr>
        <th>Operation ID</th>
        <th>Operation name</th>
        <th>innate_skill</th>
        <th>Start Time</th>
        <th>EndTime</th>
        <th>Task Type</th>
    </tr>

    task["op_id"] = ID
    task["startDate"] = basetime + timedelta(minutes=startB+lb0)
    task["endDate"] = basetime + timedelta(minutes=startB+lb)
    task["taskName"] = taskNames[B]
    task["status"] = str(ID % 4 + 4)  # using color like ID % 4
    """
    for task in tasks:
        op_id = str(task["op_id"])
        taskName = task["taskName"]
        innate_skill = task["innate_skill"] if int(task["status"]) < 4 else "-"
        args = task["args"] if int(task["status"]) < 4 else "-"
        startDate = task["startDate"].strftime('%H:%M:%S')
        endDate = task["endDate"].strftime('%H:%M:%S')
        taskType = "Running" if int(task["status"]) < 4 else "Waiting"

        print '<tr><td>',
        record = [op_id,
                  taskName,
                  innate_skill,
                  args,
                  startDate,
                  endDate,
                  taskType
                  ]
        print '</td><td>'.join(record)
        print '</td></tr>',


def renderGantt(skill):
    # generate tasks, task length between 2-10 minutes
    taskNames, tasks = genTasks(skill, 2, 10, 1)

    f = open("gantt.tpl", "r")
    for line in f:
        if line == "{{INSERT_JS_DATA}}\n":
            insertJsData(taskNames.values(), tasks)
        elif line == "{{INSERT_TBL1}}\n":
            insertTbl1(skill, taskNames)
        elif line == "{{INSERT_TBL2}}\n":
            insertTbl2(tasks, taskNames)
        else:
            print line,
    f.close()


def getSkillById(skills, id):
    """
    Find target skill by id.
    """
    curSkill = None
    for skill in skills:
        if skill["id"] == id:
            curSkill = skill
            break

    if curSkill is None:
        print "[WARN] Not found target skill in skills!"

    return curSkill


def getStates():
    states = readJson("states.json")  # Get from measure, return a list of sr_p
    for state in states["states"]:
        yield state


def mapObjId(states_obj_id):
    """
    Run mapObjects() to generate `mapObjStatusSkill` before use this function.
    Here just leave as TODO.

    Args:
        states_obj_id: Object id in states.

    Returns:
        skill_obj_id: Object id in skill.
    """
    return states_obj_id


def transCoordinate(coordinate, x, y, z):
    # Here, trans difference coordinate types to one standard coordinate.
    return x, y, z


def distance(x, y, z):
    return math.sqrt(x*x + y*y + z*z)


def matchItem(sr_p, sets):
    """
    Match conditions.
    Here is just a simple demo of abstract the measure values that convert the
    3D vector (0,0,0) -> (x,y,z) to distance.

    Returns:
        True: If match
        False: Not match
    """
    x, y, z = transCoordinate(sr_p["coordinate"],
                              sr_p["x"], sr_p["y"], sr_p["z"])

    return mapObjId(sr_p["A"]) == sets["A"] and \
        mapObjId(sr_p["B"]) == sets["B"] and \
        distance(x, y, z) <= float(sets["d"])


def satisfySRS(op, sets):

    # simmulate syn read states one by one from robot
    for state in getStates():
        length = len(op[sets])
        for s in op[sets]:
            if any([matchItem(sr_p, s) for sr_p in state["sr_p"]]):
                length -= 1
        if length != 0:
            continue
        else:
            return

    print '[ERROR] data not complete, should not be here!'


def satisfy(minLen, maxLen):
    return random.randint(minLen, maxLen)


def genTasks(skill, minLen, maxLen, minDelay):
    """
    Generate tasks with random length of time that satisfy the TA.
    Execute time are begins from now.

    Args:
        skill    - given skill.
        minLen   - random length of task between minLen to maxLen in minutes.
        maxLen   - random length of task between minLen to maxLen in minutes.
        minDelay - the delay at least.

    Returns:
        taskNames - String list of task's class name.
        tasks - Current arrangement of tasks
    """
    taskNames = {}
    tasks = []
    plan = {}
    basetime = datetime.now()

    for obj in skill["objects"]:
        taskNames[obj["id"]] = obj["class"]
        plan[obj["id"]] = 0

    for op in skill["operations"]:
        ID = op["id"]
        A = op["action"]["A"]["id"]
        B = op["action"]["B"]["id"]
        TA = op["action"]["TA"]
        ISA = op["action"]["A"]["innate_skill"]
        ISB = op["action"]["B"]["innate_skill"]
        ARGA = op["action"]["A"]["args"]
        ARGB = op["action"]["B"]["args"]

        startA = plan[A]
        startB = plan[B]

        # task waste time at least

        # SIMULATING...

        # In real world case, while satisfySRS(op["pre"]) till True,
        # and while satisfySRS(op["post"]) till True.
        #
        # In here, satisfy(minLen, maxLen) returns a time span ==
        #   while-time of satisfySRS(op, "pre") +
        #   while-time of satisfySRS(op, "post") +
        #   while-time of satisfySRS(op["action"]["pA"], "pre") +
        #   while-time of satisfySRS(op["action"]["pA"], "post") +
        la = la0 = satisfy(minLen, maxLen)

        # In real world case, while satisfySRS(op["pre"]) till True,
        # and while satisfySRS(op["post"]) till True.
        #
        # In here, satisfy(minLen, maxLen) returns a time span ==
        #   while-time of satisfySRS(op, "pre") +
        #   while-time of satisfySRS(op, "post") +
        #   while-time of satisfySRS(op["action"]["pB"], "pre") +
        #   while-time of satisfySRS(op["action"]["pB"], "post") +
        lb = lb0 = satisfy(minLen, maxLen)

        # SWEB
        # AAAAAAAAA
        # BBBBBBB..
        # '..' means the delay at least (minDelay)
        if TA == "SWEB":
            # extend la/lb to satisfy the TA
            la = max([la, lb + minDelay])

            baseline = max([plan[A], plan[B]])
            startA = startB = baseline

        # SWEW
        # AAAAAAAAAA
        # BBBBBBBBBB
        elif TA == "SWEW":
            # extend la/lb to satisfy the TA
            la = lb = max([la, lb])

            baseline = max([plan[A], plan[B]])
            startA = startB = baseline

        # ES
        # AAAAAAAAAA
        #           BBBBBBB
        elif TA == "ES":
            baseline = max([plan[A], plan[B] - la])
            startA = baseline
            startB = baseline + la

        # SBEB
        # AAAAAAA..
        #   ..
        # ..BBBBBBB
        # '..' means the delay at least (minDelay)
        # B started EXACTLY delay minDelay with A started here.
        elif TA == "SBEB":
            # extend la/lb to satisfy the TA
            la = max([la, minDelay + minDelay])
            lb = max([la, lb])

            baseline = max([plan[A], plan[B]-minDelay])
            startA = baseline
            startB = startA + minDelay

        # SAEW
        # AAAAAAA
        # ...BBBB
        # B started delay minDelay with A at least, but can be more.
        elif TA == "SAEW":
            # extend la/lb to satisfy the TA
            la = max([la, minDelay + lb])

            baseline = max([plan[A], plan[B] + lb - la])
            startA = baseline
            startB = baseline + la - lb

        # SAEB
        # AAAAAAAAAA
        # ..BBBBBB..
        # '..' means the delay at least (minDelay)
        # B started EXACTLY delay minDelay with A started here.
        # A ended delay with A minDelay at least.
        elif TA == "SAEB":
            # extend la/lb to satisfy the TA
            la = max([la, lb + minDelay + minDelay])

            baseline = max([plan[A], plan[B] - minDelay])
            startA = baseline
            startB = baseline + minDelay

        else:
            print "[WARN] Unknown TA detected:", TA

        plan[A] = startA + la
        plan[B] = startB + lb

        # Create tasks with startA, startB, la, lb, la0, lb0

        # create task: startA ~ startA+la0
        task = {}
        task["op_id"] = ID
        task["startDate"] = basetime + timedelta(minutes=startA)
        task["endDate"] = basetime + timedelta(minutes=startA+la0)
        task["taskName"] = taskNames[A]
        task["status"] = str(ID % 4)
        task["innate_skill"] = ISA
        task["args"] = ARGA
        tasks.append(task)

        # create task: startA+la0 ~ startA+la (extend part if have)
        if la > la0:
            task = {}
            task["op_id"] = ID
            task["startDate"] = basetime + timedelta(minutes=startA+la0)
            task["endDate"] = basetime + timedelta(minutes=startA+la)
            task["taskName"] = taskNames[A]
            task["status"] = str(ID % 4 + 4)  # using color like ID % 4
            task["innate_skill"] = ISA
            task["args"] = ARGA
            tasks.append(task)

        # create task: startB ~ startB+lb0
        task = {}
        task["op_id"] = ID
        task["startDate"] = basetime + timedelta(minutes=startB)
        task["endDate"] = basetime + timedelta(minutes=startB+lb0)
        task["taskName"] = taskNames[B]
        task["status"] = str(ID % 4)
        task["innate_skill"] = ISB
        task["args"] = ARGB
        tasks.append(task)

        # create task: startB+lb0 ~ startB+lb (extend part if have)
        if lb > lb0:
            task = {}
            task["op_id"] = ID
            task["startDate"] = basetime + timedelta(minutes=startB+lb0)
            task["endDate"] = basetime + timedelta(minutes=startB+lb)
            task["taskName"] = taskNames[B]
            task["status"] = str(ID % 4 + 4)  # using color like ID % 4
            task["innate_skill"] = ISB
            task["args"] = ARGB
            tasks.append(task)

    return taskNames, tasks


def main():
    """
    Arrange tasks from skills
    """
    # `skills` is the total memory of robot.
    skills = readJson("skills.json")

    # using skill (id=1)
    skill = getSkillById(skills, 1)

    # render gantt graph with the data of target skill
    renderGantt(skill)


if __name__ == '__main__':
    main()
