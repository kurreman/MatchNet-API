# Koray Amico Kulbay, Survey Matchmaking API, unit test

from SurvMatch import SurveyRes, MatchMake
from random import randint

def main():
    tsurv = SurveyRes("test")
    try:
        tsurv.get("ads")
    except NameError:
        pass

    tsurv.add("question1",1,4.5)
    tsurv.add("question2", 1, 4.5)
    tsurv.add("question3", 1, 4.5)
    tsurv.add("question4", 1, 4.5)
    tsurv.add("question5", 1, 4.5)
    tsurv.add("question8", 1, 4.5)
    #tsurv.display()


    assert tsurv.get("question1") == ["question1",1,4.5]

    tsurv.clear()
    #tsurv.display()
    tsurv.add("question1", 6, 10)

    tsurv.remove("question1")

    try:
        tsurv.remove("question1")
    except NameError:
        pass
    tsurv.clear()

    questions = ["quest1","quest2","quest3","quest4","quest5","quest6","quest7","quest8","quest9","quest10","quest11"]
    answers = []
    weights = []

    for i in range(len(questions)):
        weights.append(randint(5,15))
    for i in range(7*len(questions)):
        answers.append(randint(1,5))

    psurv = SurveyRes("Pat.")
    tsurv1 = SurveyRes("Th1.")
    tsurv2 = SurveyRes("Th2.")
    tsurv3 = SurveyRes("Th3.")
    tsurv4 = SurveyRes("Th4.")
    tsurv5 = SurveyRes("Th5.")
    tsurv6 = SurveyRes("Th6.")

    for i in range(len(questions)):
        psurv.add(questions[i],answers[i],weights[i])
        tsurv1.add(questions[i],answers[i+1],weights[i])
        tsurv2.add(questions[i],answers[i+2],weights[i])
        tsurv3.add(questions[i],answers[i+3],weights[i])
        tsurv4.add(questions[i],answers[i+4],weights[i])
        tsurv5.add(questions[i],answers[i+5],weights[i])
        tsurv6.add(questions[i],answers[i+6],weights[i])
    

    match = MatchMake()
    match.create_match(psurv,[tsurv1,tsurv2,tsurv3,tsurv4,tsurv5,tsurv6])
   
    tmatch = MatchMake()



if __name__ == '__main__': main()