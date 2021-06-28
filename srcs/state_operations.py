def is_falsy(env, fact):
	return (fact == env.facts.enum['FALSE'] or fact == env.facts.enum['FALSE_UNSET'])


def is_true(env, fact):
	return (fact == env.facts.enum['TRUE'])


def is_undefined(env, fact):
	return (fact == env.facts.enum['UNDEFINED'])


def has_an_undefined_member(status):
	return (status % 10 == 2)


def both_are_identical(status):
	return (status % 10 == status // 10)


def at_least_a_true(status):
	return (status // 10 == 1)


def both_are_true(status):
	return (status == 11)


def at_least_a_false(status):
	return (status != 11 and status != 22 and status != 12)


# Every logical operation here are commutative, so we treat both combinations at once
def get_setting(env, left, right):
	"""
        Retrieve the current states combinations.
		2 represents an undefined state
		1 represents a true state
		0 represents a false state
    """
	if (is_true(env, left) and is_true(env, right)):
		return (11)
	elif ((is_true(env, left) and is_falsy(env, right)) or (is_true(env, right) and is_falsy(env, left))):
		return (10)
	elif ((is_true(env, left) and is_undefined(env, right)) or (is_true(env, right) and is_undefined(env, left))):
		return (12)
	elif ((is_undefined(env, left) and is_falsy(env, right)) or (is_undefined(env, right) and is_falsy(env, left))):
		return (2)
	elif (is_undefined(env, left) and is_undefined(env, right)):
		return (22)
	return (0)
