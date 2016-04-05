function taskNames, tasks = schedule_tasks(skill):
    /*
    Algorithm: Schedule tasks

    Schedule tasks with dependence of pre/post and TA.
    Run tasks as well.

    Args:
        skill    - given skill.

    Returns:
        taskNames - String list of task's class name.
        tasks - Current arrangement of tasks
    */

    foreach obj in skill.objects:
        taskNames[obj.id] = mapObjById(obj.id).name

    foreach op in skill.operations:
        // SIMULATING RUN ...
        check each satisfyXXX() inside when continuously in separated threads:
            when satisfySRS(op.pre) and
                satisfySRS(op.action.pA.pre) and
                satisfyTA(op.action.TA, START) and
                not satisfySRS(op.post) and
                not satisfySRS(op.action.pA.post) and
                not satisfyTA(B, op.action.TA, STOP):

                task = do_A(op.action.A.innate_skill(op.action.A.args))
                tasks.append(task)

            when satisfySRS(op.pre) and
                satisfySRS(op.action.pB.pre) and
                satisfyTA(B, op.action.TA, START) and
                not satisfySRS(op.post) and
                not satisfySRS(op.action.pB.post) and
                not satisfyTA(op.action.TA, STOP):

                task = do_B(op.action.B.innate_skill(op.action.B.args))
                tasks.append(task)

    return taskNames, tasks
