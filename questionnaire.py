class Questionnaire(object):

    def __init__(self, title, question):
        self.title = title
        self.question = question
        self.points = 0
        self.answers = {}

    def add_answer(self, ans, point=0):
        answer = (ans, point)
        self.points += point
        number = len(self.answers) + 65
        ASCII = str(unichr(number))
        self.answers[ASCII] = answer

    def remove_answer(self, number):
        self.points -= self.answers[number][1]
        del self.answers[number]

    def get_answers(self):
        return self.answers

    def count_answers(self):
        return len(self.answers)
    
    def get_total_points(self):
        return self.points
    
    def get_title(self):
        return self.title
    
    def get_question(self):
        return self.question
    
    def replace_question(self, question):
        self.question = question

    def serialize(self):
        return {"Question": self.question, "Answers": self.answers, "Points": self.points, "Title": self.title}
    

