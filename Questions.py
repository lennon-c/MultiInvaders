# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 13:02:24 2023

@author: carol
"""
from  itertools import product, cycle
import random

class Multiplications():
    """Set multiplication questions based on range of numbers to multiply and based on the number of alternatives to show.

    I returns texts to be used as questions and answers in the game.
    """

    def __init__(self, first_numbers = None , second_numbers = None, n_alternatives = 4):
        random.seed(None)

        if first_numbers is None:
            self.first_numbers = tuple(range(1, 11))
        else:
            self.first_numbers = first_numbers

        if second_numbers is None:
            self.second_numbers = tuple(range(1, 11))
        else:
            self.second_numbers = second_numbers

        self.n_alternatives = n_alternatives
        # all possible answers given first_numbers and second_numbers
        self.all_alternatives = [ n1*n2 for n1,n2 in
                                 product(self.first_numbers, self.second_numbers)]

        super().__init__()


    def start(self):
        """Select a set of multiple wrong options and the correct answer."""
        self.n1 = random.choice(self.first_numbers)
        self.n2 = random.choice(self.second_numbers)
        self.question = f'{self.n1} x {self.n2}'

        wrongs = self.all_alternatives.copy()
        self.correct =  self.n1 * self.n2

        # deduct correct answer from wrong alternative
        wrongs = [n for n in wrongs if n != self.correct] # not correct
        wrongs = list(set(wrongs)) # not repeated
        random.shuffle(wrongs)

        # create texts
        self.correct_texts = [ f'{n}'  for n in  [self.correct] ]
        self.wrong_texts = [ f'{n}'   for n  in wrongs ]


        # create cycles to be picking new correct and wrong answers
        self.cycle_wrongs = cycle(self.wrong_texts )
        self.cycle_corrects = cycle(self.correct_texts)

        # give alternatives texts
        wrongs = [next(self.cycle_wrongs) for i in range(1, self.n_alternatives ) ]
        self.alternatives = [self.correct] + wrongs
        random.shuffle(self.alternatives)



class Multiplications_inv(Multiplications):
    """As Multiplications, set multiplication questions based on range of numbers to multiply and based on the number of alternatives to show.

    Here,the question is a number and the answer a muntiplication problem.
    """

    def __init__(self, first_numbers = None , second_numbers = None, n_alternatives = 4):
        super().__init__(first_numbers, second_numbers, n_alternatives)
        # now the alternatives are the questions
        self.all_questions = self.all_alternatives
        # bring the dic of {question: answers} and the list of all possible answers
        self.questions_dic , self.all_alternatives = self.all_factors_tuples()
        random.shuffle(self.all_questions)
        self.cycle_questions = cycle(self.all_questions)

    def factors(self, x):
        # gives the factors of x in a list
        lst = [i for i in range(1,x+1) if x%i==0]
        return lst

    def factors_tuples(self, x ):
        correct = list()
        factors_lst  = self.factors(x)
        n1_lst = [i for i in factors_lst if i in self.first_numbers]
        n2_lst = [i for i in factors_lst if i in  self.second_numbers]

        for i, j in product(n1_lst, n2_lst):
            if i*j == x:
                correct.append([i,j])

        return correct

    def all_factors_tuples(self):
        dic = dict()
        lst = list()
        for i in self.all_questions:
            dic[i] =  self.factors_tuples(i )
            lst = lst + [pair for pair in dic[i] if pair not in lst]
        return dic, lst


    def start(self):
        # pick a question
        self.question = next(self.cycle_questions)

        # retrieve its correct answers
        self.corrects = self.questions_dic[self.question]

        # list of wrong alternatives
        random.shuffle(self.all_alternatives)
        wrongs = [pair for pair in self.all_alternatives if pair not in self.corrects]


        # create texts
        self.correct_texts = [ f'{n1} x {n2}'  for n1, n2 in self.corrects ]
        self.wrong_texts = [ f'{n1} x {n2}'  for n1, n2 in wrongs ]


        # create cycles to be picking new correct and wrong answers
        self.cycle_wrongs = cycle(self.wrong_texts )
        self.cycle_corrects = cycle(self.correct_texts)

        # give first correct text
        self.correct = next(self.cycle_corrects)


        # give alternatives texts
        wrongs = [next(self.cycle_wrongs) for i in range(1, self.n_alternatives ) ]
        self.alternatives = [self.correct] + wrongs
        random.shuffle(self.alternatives)


#%% TEST


