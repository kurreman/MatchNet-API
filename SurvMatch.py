# Koray Amico Kulbay, Survey Matchmaking API

# Package SurvMatch creates a simple way to finalize raw data from surveys and create a potential match

# By using SurveyRes results from a survey can be easily summarized.
# By using MatchMake results from SurveyRes can be matched between different surveys.

# An instance of SurveyRes corresponds to a single survey with its answers and
# respondent (id of who/what answered survey) easily accessible. Answers are stored in array format.
# By gathering instances of SurveyRes one can use MatchMake to handle matches between different surveys.


class _QuestRes:
    """Question Result: Answer to specific question in survey and its match value."""
    def __init__(self,question,answer,match_value):
        self.alias = question
        self.answer = answer
        self.match_value = match_value

class SurveyRes:
    """Survey Results: containing respondent id and answers of questions in external survey."""
    def __init__(self,respondent):
        self._respondent = respondent
        self._answer_list = None  # list of instances of _QuestRes
        self._size = 0

    def add(self,question,answer,match_value):
        """Adds result of one question to answer_list in Survey Results."""
        if type(match_value) == int or type(match_value) == float:
            pass
        else:
            raise ValueError("Wrong datatype: match_value needs to be int or float! ")

        if type(question) == int or type(question) == float or type(question) == str:
            pass
        else:
            raise ValueError("Wrong datatype: question needs to be int,float or str! ")

        if self._answer_list is None:
            self._answer_list = []

        if self._get(question):
            raise NameError("Question already exists!")

        self._answer_list.append(_QuestRes(question,answer,match_value))
        self._size += 1

    def remove(self,question):
        """Removes result of one question in Survey Results.
        Slow, try do avoid. N = #questions, N worst case time complexity. """
        quest = self._get(question)
        if quest:
            self._answer_list.remove(quest)
            self._size -= 1
            if len(self._answer_list) == 0:
                self._answer_list = None
        else:
            raise NameError("No such question exists in survey results!")

    def len(self):
        """Returns number of question results in survey."""
        return self._size

    def get(self,question):
        """Returns specific question as a list. [question,answer,match_value]."""
        quest = self._get(question)
        if quest:
            return [quest.alias,quest.answer,quest.match_value]
        else:
            raise NameError("No such question exists in survey results!")

    def _get(self,question):
        """Returns None if question doesn't exists."""
        if self._answer_list:
            for quest in self._answer_list:  # Slow here
                if quest.alias == question:
                    return quest

    def clear(self):
        """Clears survey of all question results."""
        self._answer_list = None
        self._size = 0

    def display(self):
        """Graphical representation of survey."""
        print(self._respondent)
        if self._answer_list:
            for quest in self._answer_list:
                print(self.get(quest.alias))
        else:
            print(self._answer_list)  # will be None

class _MatchInstance:
    """A MatchMake element with comparison result of Survey Results from two respondents."""
    def __init__(self,source,target):
        self.match_source = source  # alias/name
        self.match_target = target  # alias/name
        self.match_score = 0

class MatchMake(SurveyRes):
    """Platform to handle matchmaking of survey results (SurveyRes) before creating network where each respondent will
    become a member."""
    def __init__(self):
        self._source = None
        self._score_list = []  # List consisting of elements of _MatchInstance

    def create_match(self,source, target_list):
        """Returns a match between a source survey and one or more target surveys.
        Beware, slow! N = #questions, M = #target surveys:  M*N^2 worst case time complexity."""
        if type(source) is SurveyRes and type(target_list) is list:
            pass
        else:
            raise TypeError("Wrong datatype: source has to be of custom type SurveyRes and target_list a list!")

        self._source = source._respondent
        for target in target_list:

            if type(target) is not SurveyRes:
                raise TypeError("Wrong datatype: ALL elements of target_list has to be of custom type SurveyRes!)")


            match = _MatchInstance(source._respondent,target._respondent)  # Score is now zero
            self._score_list.append(match)
            max_score = 0
            for quest_res in source._answer_list:
                target_res = target._get(quest_res.alias)
                if target_res is None:
                    raise NameError("Questions in source and target survey doesn't match!")
                max_score += quest_res.match_value
                if target_res.answer == quest_res.answer:
                    if quest_res.match_value != target_res.match_value:
                        raise NameError("Question match_value doesn't match between source and target survey!")
                    else:
                        match.match_score += quest_res.match_value
            match.match_score = match.match_score/max_score  # Creates a percentage of maxscore

    def display(self):
        """Graphical representation of match."""
        if self._source:
            print(self._source)
            for target_inst in self._score_list:
                print([target_inst.match_target,target_inst.match_score])