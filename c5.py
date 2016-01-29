# -*- encoding: utf-8 -*-
'''
Algorithm: Offline Mapping Task Performance onto Known Skill Primitives.

INPUT: state_list(Si), skill_primitive_list (SPk)
OUTPUT: A list of skill instance

SP_instance = [{"sp_id": k,
                 "pre_st_id": i,
                 "post_st_id": j
                 }]
'''

import json
import math


def readJson(filename):
    """
    Get data from JSON file
    """
    fp = open(filename, "r")
    obj = json.load(fp)
    fp.close()
    return obj


def writeJson(filename, obj):
    """
    Write out data to JSON file
    """
    fp = open(filename, "w")
    json.dump(obj, fp, indent=4, sort_keys=True)
    fp.close()


mapObjStatusSkill = {}


def mapObjects(states, skill):
    """
    Algorithm Entry - Mapping objects.

    Mapping objects in real world (itself) to abstracted world (its class).
    Mapping object id from `states["objects"]` to `skill["objects"]`.

    There's three types of class in abstracted world (meta-class),
        target    - The final goal target objects.
        reference - Middle-wares,Tools,Supporters or sub-targets inside skill.
        effector  - Some parts of robot itself. Head, left-hand, etc.
    """
    for ost in states["objects"]:
        for osk in skill["objects"]:
            if ost["class"] == osk["class"]:
                mapObjStatusSkill[ost["id"]] = osk["id"]

    print "Mapping objects:", mapObjStatusSkill


def mapObjId(states_obj_id):
    """
    Run mapObjects() to generate `mapObjStatusSkill` before use this function.

    Args:
        states_obj_id: Object id in states.

    Returns:
        skill_obj_id: Object id in skill.
    """
    try:
        return mapObjStatusSkill[states_obj_id]
    except KeyError:
        return -1  # if not found


def transCoordinate(coordinate, x, y, z):
    # Here, trans difference coordinate types to one standard coordinate.
    return x, y, z


def distance(x, y, z):
    return math.sqrt(x * x + y * y + z * z)


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


def match(state, op, sets):
    """
    Only if each item in the skill appears in the state, returns True.
    But the state can have items that not in the skill.
    The `sets` can be "pre" or "post".
    """
    for s in op[sets]:
        if any([matchItem(sr_p, s) for sr_p in state["sr_p"]]):
            continue
        else:
            return False
    return True


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


def mapStatesToSkill(states, skill):
    """
    Algorithm Entry - Mapping states to pre/post op of known skill.

    Map task performance onto known skill primitives.
    """
    for state in states["states"]:
        for op in skill["operations"]:
            if match(state, op, "pre"):
                print state["id"], "state <=>", op["id"], "op-pre"
            if match(state, op, "post"):
                print state["id"], "state <=>", op["id"], "op-post"


def testKnownSkill():
    """
    Simulates the states of robot matches the skills in memory.
    Using 'ijson' instead if read large JSON from file iteratively.
    """

    print '------ Begin mapping states to a known skill ------'

    # `skills` is the total memory of robot.
    skills = readJson("skills.json")

    # `states` simulates the states of robot got from measure continuously.
    states = readJson("states.json")

    skill = getSkillById(skills, 1)

    if skill is None:
        print "[ERROR] Target skill not exist in the skills memory!"
        return

    # objects mapping
    mapObjects(states, skill)

    # map task performance onto known skill primitives
    print "Matching states to pre/post op of skill, id=1 in skills."
    mapStatesToSkill(states, skill)

    print '------ End mapping states to a known skill ------'
    print


def mapStatesToUnknownSkill(states, skill_id):
    '''
    Algorithm: Offline Mapping Task Performance onto Known Skill Primitives.

    INPUT: state_list(Si), action_list(act)
    OUTPUT: A list of stages (its data structure is the same to operations
        in skill.json)

    '''
    skill = {}
    skill["id"] = skill_id

    # Generate objects
    # {
    #     "id": 1,
    #     "name": "book_A",
    #     "class": "target1",
    #     "pose": "robot_view"
    # }
    # ==>
    # {
    #     "id": 1,
    #     "class": "target1",
    #     "type": "vision"
    # }
    objs = []
    for obj in states["objects"]:
        del obj["name"]
        del obj["pose"]
        obj["type"] = "vision"  # TODO
        objs.append(obj)
    skill["objects"] = objs

    # Generate operations
    if len(states["states"]) < 2:
        print "[ERROR] At least 2 states needed to generate a skill"
        return skill

    operations = []

    op_id = 1
    op_name = ""
    pres = []
    posts = []
    posts_total = []
    action = {}

    state0 = states["states"][0]
    action0 = states["actions"][0]
    pre_op_id = op_id
    init_crf = state0["cr_f"]

    for state, action in zip(states["states"][1:], states["actions"][1:]):
        # print state0["id"], state["id"]

        # posts needs to merge
        posts = genPosts(state0, state)
        posts_total = mergeSrps(posts_total, posts)

        # only care pres in first state of a stage
        if op_name == "":
            pres = genPres(state0, state, objs)

        op_name += str(state0["id"]) + ","
        if state0["cr_f"] != state["cr_f"]:
            # all sr_p in pres with action["A"]["id"] or action["B"]["id"]
            action_a_pre = genSrpsWithId(action["A"]["id"], pres)
            action_b_pre = genSrpsWithId(action["B"]["id"], pres)

            action_a_post = genSrpsWithId(action["A"]["id"], posts_total)
            action_b_post = genSrpsWithId(action["B"]["id"], posts_total)

            # new stage detected
            operation = {}
            operation["id"] = op_id
            operation["name"] = op_name
            operation["pre"] = pres
            operation["post"] = posts_total
            action["A"]["pre"] = action_a_pre
            action["A"]["post"] = action_a_post
            action["B"]["pre"] = action_b_pre
            action["B"]["post"] = action_b_post
            operation["action"] = action
            operations.append(operation)

            goal_crf = state["cr_f"]
            post_op_id = op_id

            op_id += 1
            op_name = ""
            pres = []
            posts_total = []
            action = {}

        state0 = state

    skill["operations"] = operations

    # Generate init_feature
    skill["init_feature"] = {
        "cr_f": init_crf,
        "pre_op_id": pre_op_id
    }

    # Generate goal_feature
    skill["goal_feature"] = {
        "cr_f": goal_crf,
        "post_op_id": post_op_id
    }

    return skill


def genPres(state0, state, objs):
    pres = []
    for srp in state["sr_p"]:
        for srp0 in state0["sr_p"]:
            if srp["A"] == srp0["A"] and srp["B"] == srp0["B"]:
                # this srp in state0
                if srp["p_n"] != srp0["p_n"]:   # p_n changed
                    pres.append({
                        "A": srp0["A"],
                        "B": srp0["B"],
                        "p_n": srp0["p_n"],
                        "d": srp0["d"],
                        "type": "p_n~"
                    })
                elif srp["d"] != srp0["d"]:     # p_n no change and d changed
                    pres.append({
                        "A": srp0["A"],
                        "B": srp0["B"],
                        "p_n": srp0["p_n"],
                        "d": srp0["d"],
                        "type": "d~"
                    })
                else:                           # nothing changed
                    pass
                break
        else:
            # new item: this srp not in state0
            # 1. A new in S'
            # 2. B new in S'
            # 3. A and B both new in S'
            # 4. A and B both exist in S', but pair (A, B) not exist in S or S'
            pres += genPresNotInPair(srp["A"], state0, objs)
            pres += genPresNotInPair(srp["B"], state0, objs)
            pass

    for srp0 in state0["sr_p"]:
        for srp in state["sr_p"]:
            if srp["A"] == srp0["A"] and srp["B"] == srp0["B"]:
                break
        else:
            # this srp0 not in state
            pres.append({
                "A": srp0["A"],
                "B": srp0["B"],
                "p_n": srp0["p_n"],
                "d": srp0["d"],
                "type": "disappear"
            })

    return pres


def genPresNotInPair(obj_id, state0, objs):
    ret = []
    # if obj_id in state0, return all pres
    ret = genSrpsWithId(obj_id, state0["sr_p"])
    if ret == []:
        return ret

    # obj_id not in any pair (A,B) in state0
    # check parents of obj_id
    # get parents: parent and grandparent and so on
    parents = []
    parent_id = obj_id
    while parent_id != 0:
        for obj in objs:
            if obj["id"] == parent_id:
                parent_id = obj["parent"]
                if parent_id != 0:
                    parents.append(parent_id)
                break

    for parent in parents:
        ret += genSrpsWithId(parent, state0["sr_p"])

    return ret


def genSrpsWithId(obj_id, srps):
    ret = []
    for srp in srps:
        if srp["A"] == obj_id:
            ret.append(srp)
        if srp["B"] == obj_id:
            ret.append(srp)
    return ret


def mergeSrps(set1, set2):
    """
    Merge srps together, and
        1. duplicated items leave the last one
        2. remove disappeared items
    """
    ret = []
    for s1 in set1:
        # remove disappeared items in set1
        if s1["type"] == "disappear":
            continue

        for s2 in set2:
            if s1["A"] == s2["A"] and s1["B"] == s2["B"]:
                # duplicated items leave the last one
                ret.append(s2)
                break
        else:
            # insert item only exist in set1
            ret.append(s1)

    for s2 in set2:
        # remove disappeared items in set2
        if s2["type"] == "disappear":
            continue

        for s1 in set1:
            if s1["A"] == s2["A"] and s1["B"] == s2["B"]:
                break
        else:
            # insert item only exist in set2
            ret.append(s2)

    return ret


def genPosts(state0, state):
    posts = []
    for srp in state["sr_p"]:
        for srp0 in state0["sr_p"]:
            if srp["A"] == srp0["A"] and srp["B"] == srp0["B"]:
                # this srp in state0
                if srp["p_n"] != srp0["p_n"]:   # p_n changed
                    type = "p_n~"
                elif srp["d"] != srp0["d"]:     # p_n no change and d changed
                    type = "d~"
                else:                           # nothing changed
                    type = "-"
                break
        else:
            type = "new"                        # this srp not in state0

        if type != "-":
            posts.append({
                "A": srp["A"],
                "B": srp["B"],
                "p_n": srp["p_n"],
                "d": srp["d"],
                "type": type
            })

    for srp0 in state0["sr_p"]:
        for srp in state["sr_p"]:
            if srp["A"] == srp0["A"] and srp["B"] == srp0["B"]:
                break
        else:
            # this srp0 not in state
            posts.append({
                "A": srp0["A"],
                "B": srp0["B"],
                "p_n": srp0["p_n"],
                "d": srp0["d"],
                "type": "disappear"
            })

    return posts


def testUnknownSkill():
    print '------ Begin abstract states to a new skill ------'

    # `states` simulates the states of robot got from measure continuously.
    states = readJson("states.json")

    # map task performance onto known skill primitives
    print "Mapping states to a unknown skill with id=1."
    skill = mapStatesToUnknownSkill(states, 1)

    skills = []
    skills.append(skill)
    writeJson("skills_create.json", skills)

    print '------ End abstract states to a new skill ------'
    print


def genStates():
    """
    Algorithm 1:  Task Segmentation

    # TODO: Offline Processing

    For each monitoring time instance:
           if (int(agent.effector_moved) or int(agent.effector_changed)):
                cr_f = agent.body_moved + agent.effector_changed +
                        object.position_changed  +   object.property_changed
                sr_p = createSRP(
                    targeted_object_list,
                    dominant_effector_list,
                    predicate_name out,
                    distance_constraints
                    )
                state_list.append[cr_f, sr_p]
                action_list.append[dominant_effector, innate_skill]
    """
    targeted_object_list = {"book_A", "table", "book_B", "book_C"}
    dominant_effector_list = {"robot_W.torso", "robot_W.torso2"}
    observe_iterator = [{
        "agent_effector_moved": 1,
        "agent_effector_changed": 0,
        "agent_body_moved": 0,
        "object_position_changed": 0,
        "object_property_changed": 0,
        "distance_constraints": 9,
        "x": 0,
        "y": 0,
        "z": 0,
        "coordinate": "robot_view",
        "agent_start": 0.1,
        "agent_end": 0.5,
    }]

    states = []
    for item in observe_iterator:
        if item["agent_effector_moved"] == 1 or \
           item["agent_effector_changed"] == 1:

            cr_f = item["agent_body_moved"] + \
                item["agent_effector_changed"] + \
                item["object_position_changed"] + \
                item["object_position_changed"]

            sr_p, predicate_name = createSRP(
                targeted_object_list,
                dominant_effector_list,
                item["x"], item["y"], item["z"],
                item["coordinate"],
                item["distance_constraints"]
            )

            TA = genTA(item, item)  # TODO: here should compare with A and B
            states.append({
                "cr_f": cr_f,
                "sr_p": sr_p,
                "TA": TA})
            # action_list.append[dominant_effector, innate_skill]
    writeJson("states_create.json", states)


def genTA(A, B):
    """
    Generate TA from monitoring a pare agents' start/end time.
    """

    if A["agent_start"] == B["agent_start"] and \
       B["agent_end"] < A["agent_end"]:
        return 'SWEB'
    elif A["agent_start"] < B["agent_start"] and \
            A["agent_end"] == B["agent_end"]:
        return 'SAEW'
    elif A["agent_start"] == B["agent_start"] and \
            A["agent_end"] == B["agent_end"]:
        return 'SWEW'
    elif A["agent_start"] < B["agent_start"] and \
            A["agent_end"] < B["agent_end"]:
        return 'SBEB'
    elif A["agent_start"] < B["agent_start"] and \
            A["agent_end"] > B["agent_end"]:
        return 'SAEB'
    elif A["end"] == B["agent_start"]:
        return 'ES'

# TODO: Generate srps


def createSRP(targeted_object_list,
              dominant_effector_list,
              x, y, z,
              coordinate,
              distance_constraints):
    sr_p = {}
    predicate_name = ""
    return sr_p, predicate_name


def testGenerateStates():
    genStates()


def main():
    testGenerateStates()
    testKnownSkill()
    testUnknownSkill()


if __name__ == '__main__':
    print  # web output directly need a blank line
    main()
