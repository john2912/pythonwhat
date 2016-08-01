from pythonwhat.Test import DefinedTest, EqualEnvironmentTest, EquivalentEnvironmentTest
from pythonwhat.State import State
from pythonwhat.Reporter import Reporter
from pythonwhat.Feedback import Feedback


def test_object(name,
                eq_condition="equal",
                do_eval=True,
                undefined_msg=None,
                incorrect_msg=None):
    """Test object.

    The value of an object in the ending environment is compared in the student's environment and the
    solution environment.

    Args:
        name (str): the name of the object which value has to be checked.
        eq_condition (str): the condition which is checked on the eval of the object. Can be "equal" --
          meaning that the operators have to evaluate to exactly the same value, or "equivalent" -- which
          can be used when you expect an integer and the result can differ slightly. Defaults to "equal".
        do_eval (bool): if False, the object will only be checked for existence. Defaults to True.
        undefined_msg (str): feedback message when the object is not defined
        incorrect_msg (str): feedback message if the value of the object in the solution environment doesn't match
          the one in the student environment.

    Examples:
        Student code

        | ``a = 1``
        | ``b = 5``

        Solution code

        | ``a = 1``
        | ``b = 2``

        SCT

        | ``test_object("a")``: pass.
        | ``test_object("b")``: fail.
    """
    state = State.active_state
    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_object")

    state.extract_object_assignments()
    student_obj_ass = state.student_object_assignments

    if not undefined_msg:
        undefined_msg = "Have you defined `%s`?" % name

    if not incorrect_msg:
        incorrect_msg = "The contents of `%s` aren't correct." % name

    eq_map = {"equal": EqualEnvironmentTest,
              "equivalent": EquivalentEnvironmentTest}
    student_env = state.student_env
    solution_env = state.solution_env

    if eq_condition not in eq_map:
        raise NameError("%r not a valid equality condition " % eq_condition)

    if name not in solution_env:
        raise NameError("%r not in solution environment " % name)

    rep.do_test(DefinedTest(name, student_env, Feedback(undefined_msg)))

    if (rep.failed_test):
        return

    if do_eval:
        ass_node = get_assignment_node(student_obj_ass, name)
        rep.do_test(eq_map[eq_condition](name,
                                         student_env,
                                         solution_env,
                                         Feedback(incorrect_msg, ass_node)))

def get_assignment_node(student_obj_ass, name):
    if (name not in student_obj_ass):
        return(None)

    # For now, only pass along node if single assignment
    if (len(student_obj_ass[name]) != 1):
        return(None)

    return(student_obj_ass[name][0])