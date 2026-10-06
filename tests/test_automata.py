from automata import Automaton, from_definition
from formatos import dumps, loads, load_automaton, save_automaton


def sample_lambda_automaton():
    return Automaton(
        states=["q0", "q1"],
        alphabet=["a", "b"],
        initial="q0",
        accepting={"q1"},
        transitions={
            ("q0", "a"): {"q1"},
            ("q0", "b"): {"q0"},
            ("q0", ""): {"q1"},
        },
    )


def assert_same_machine(actual, expected):
    assert actual.states == expected.states
    assert actual.alphabet == expected.alphabet
    assert actual.initial == expected.initial
    assert actual.accepting == expected.accepting
    assert actual.transitions == expected.transitions


def test_import_export_round_trip_in_all_three_formats():
    original = sample_lambda_automaton()
    for extension in ("jff", "json", "xml"):
        restored = loads(dumps(original, extension), extension)
        assert_same_machine(restored, original)


def test_file_save_and_load_round_trip_in_all_three_formats(tmp_path):
    original = sample_lambda_automaton()
    for extension in ("jff", "json", "xml"):
        path = tmp_path / f"automata.{extension}"
        save_automaton(original, path)
        assert_same_machine(load_automaton(path), original)


def test_dfa_accepts_and_rejects_words():
    machine = from_definition(
        "0, 1", "q0, q1", "q0", "q1",
        "q0, 0 -> q0\nq0, 1 -> q1\nq1, 0 -> q0\nq1, 1 -> q1",
    )
    assert machine.accepts("01")
    assert machine.accepts("1")
    assert not machine.accepts("00")
    assert not machine.accepts("")


def test_lambda_nfa_acceptance_requires_lambda_closure():
    machine = Automaton(
        states=["start", "middle", "final"],
        alphabet=["a"],
        initial="start",
        accepting={"final"},
        transitions={("start", ""): {"middle"}, ("middle", "a"): {"final"}},
    )
    assert machine.lambda_closure({"start"}) == {"start", "middle"}
    assert machine.accepts("a")
    assert not machine.accepts("")


def test_trace_includes_lambda_moves_before_and_after_input():
    machine = Automaton(
        states=["start", "middle", "final"],
        alphabet=["a"],
        initial="start",
        accepting={"final"},
        transitions={
            ("start", ""): {"middle"},
            ("middle", "a"): {"final"},
            ("final", ""): {"start"},
        },
    )
    trace = machine.trace("a")
    assert trace[0]["lambda_moves"] == [("start", "", "middle")]
    assert trace[1]["moves"] == [("middle", "a", "final")]
    assert trace[1]["lambda_moves"] == [("final", "", "start"), ("start", "", "middle")]
    assert trace[1]["states"] == ["final", "middle", "start"]


def test_reads_annex_three_json_shape():
    content = '''{"tipo":"AFND-lambda","alfabeto":["a","b"],"estados":["q0","q1"],"inicial":"q0","aceptacion":["q1"],"transiciones":[{"desde":"q0","lee":"a","hacia":["q1"]},{"desde":"q0","lee":"b","hacia":["q0"]},{"desde":"q0","lee":"","hacia":["q1"]}]}'''
    assert_same_machine(loads(content, "json"), sample_lambda_automaton())


def test_imports_jflap_epsilon_as_empty_read():
    content = '''<structure><type>fa</type><automaton>
      <state id="0" name="q0"><initial/></state>
      <state id="1" name="q1"><final/></state>
      <transition><from>0</from><to>1</to><read/></transition>
    </automaton></structure>'''
    machine = loads(content, "jff")
    assert machine.transitions[("q0", "")] == {"q1"}
    assert machine.accepts("")
