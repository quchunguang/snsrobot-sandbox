
Input: state_list as the robot's state list from measure.
       known_skills as robot's all known skills.
output: match_skills as robot's matching skills with given states_list.

match_skills <- [ ]
for skill in known_skills:
    # The initial post before the first atom_skill in skill is consider to universal set (I).
    post <- I

    if len(state_list) < len(skill):
        # not match: length of state_list must be longer than or equal to the skill
        continue

    for i, atom_skill in enumerate(skill):
        pre <- skill.pre
        diff_set = different_set_between(pre, post)
        if state_list[i] not in diff_set:
            # not match
            break
        post <- skill.post
    else:
        match_skills.append(skill)
