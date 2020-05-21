# Koray Amico Kulbay, network API, unit test

from network import Network

def main():
    """Unit testing."""
    tnet = Network()
    assert tnet.len() == 0
    tnet.add("test0")
    assert tnet.len() == 1
    assert tnet.collect("test0",0) == ["test0"]
    tnet.remove("test0")
    try:
        tnet.get("test0")
    except NameError:
        pass
    assert tnet.len() == 0
    tnet.add("test",[7,3,9,6],weight=3.5)
    assert tnet.len() == 5
    assert tnet.get("test") == ["test", [7,3,9,6], 3.5]

    tnet.change_member(name="test",name_ch="change",neighbours_ch=[4,6,8],weight_ch=34.6)
    assert tnet.len() == 7

    assert tnet.get(3) == [3,None,None]

    try:
        tnet.remove("test")
    except NameError:
        pass

    tnet.clear()

    try:
        tnet.get(7)
    except NameError:
        pass

    try:
        tnet.add([])
    except TypeError:
        pass

    assert tnet.len() == 0

    tnet.add(1, [2,3])
    tnet.add(4, [2])
    tnet.add(5, [3])
    tnet.add(6, [3])
    tnet.add(8, [4])
    tnet.add(7, [6])

    assert tnet.collect(2, 0) == [2]
    assert tnet.collect(2, 1) == [1,4]
    assert tnet.collect(2, 2) == [3,8]
    assert tnet.collect(2, 3) == [5,6]
    assert tnet.collect(2, 4) == [7]
    try:
        tnet.collect(2, 5)
    except ValueError:
        pass

# ----------- MatchMake and SurveyRes with Network Unit test  -------
    from SurvMatch import SurveyRes, MatchMake
    from random import randint

    patnet = Network()
    questions = ["quest1", "quest2", "quest3", "quest4", "quest5", "quest6", "quest7", "quest8", "quest9", "quest10",
                 "quest11"]
    answers = []
    weights = []

    for i in range(len(questions)):
        weights.append(randint(5, 15))
    for i in range(7 * len(questions)):
        answers.append(randint(1, 5))

    psurv = SurveyRes("Pat.")
    tsurv1 = SurveyRes("Th1.")
    tsurv2 = SurveyRes("Th2.")
    tsurv3 = SurveyRes("Th3.")
    tsurv4 = SurveyRes("Th4.")
    tsurv5 = SurveyRes("Th5.")
    tsurv6 = SurveyRes("Th6.")

    for i in range(len(questions)):
        psurv.add(questions[i], answers[i], weights[i])
        tsurv1.add(questions[i], answers[i + 1], weights[i])
        tsurv2.add(questions[i], answers[i + 2], weights[i])
        tsurv3.add(questions[i], answers[i + 3], weights[i])
        tsurv4.add(questions[i], answers[i + 4], weights[i])
        tsurv5.add(questions[i], answers[i + 5], weights[i])
        tsurv6.add(questions[i], answers[i + 6], weights[i])

    match = MatchMake()
    match.create_match(psurv, [tsurv1, tsurv2, tsurv3, tsurv4, tsurv5, tsurv6])

    patnet.match_fill(match)


if __name__ == '__main__': main()