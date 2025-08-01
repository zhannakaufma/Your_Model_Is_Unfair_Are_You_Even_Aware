import math
import pandas as pd
from pprint import pprint as pp
from collections import defaultdict
from libs.demographics_maps import *
import numpy as np


EXPECTED_APPROVAL = {
    "wom 1": "no",
    "wom 2": "no",
    "wom 3": "yes",
    "man 1": "no",
    "man 2": "yes",
    "man 3": "no",
    "wom fair": "yes",
    "man fair": "yes"
}

PREDICTIVE_POWER = {
    "wom 1": "Education",
    "wom 2": "Hours Worked Per Week",
    "wom 3": "Education",
    "man 1": "Education",
    "man 2": "Education",
    "man 3": "Education"
}

PUSHED_LOWER = {
    "wom 1": ["Education","Hours Worked Per Week","Age"],
    "wom 2": ["Hours Worked Per Week"],
    "wom 3": [],
    "man 1": ["Education", "Hours Worked Per Week"],
    "man 2": ["Age", "Sex"],
    "man 3": ["Education"]
}

PUSHED_HIGHER = {
    "wom 1": ["Occupation", "Sex"],
    "wom 2": ["Occupation", "Education", "Age", "Sex"],
    "wom 3": ["Education","Hours Worked Per Week","Sex","Occupation"],
    "man 1": ["Sex", "Occupation"],
    "man 2": ["Education", "Hours Worked Per Week", "Occupation"],
    "man 3": ["Hours Worked Per Week", "Age", "Sex", "Occupation"]
}

PUSHED_NEITHER = {
    "wom 1": [""],
    "wom 2": [""],
    "wom 3": ["Age"],
    "man 1": ["Age"],
    "man 2": [""],
    "man 3": [""]
}

class Result:
    # Fields that stay constant when result is exploded into multiple rows.
    # Except "Gender" which is handled differently

    def __init__(self, series, pid, vis) -> None:
        row_template = {}

        row_template["Pid"] = pid
        row_template["Vis_Type"] = vis

        if vis == "interactive_fair":
           row_template["cp"] = 0
           row_template["cp_explicit"] = 0
           row_template["eli5"] = 0
           row_template["lime"] = 0
           row_template["shap"] = 0
           row_template["forceshap"] = 0
           row_template["anchors"] = 0
           row_template["interactive"] = 0
           row_template["interactive_lower_bias_percep"] = 0
           row_template["interactive_higher_bias_percep"] = 0
           row_template["interactive_fair"] = 1
           row_template["initial_visualizations"] = 0

        row_template["Age"] = series["age"]
        if (int(series["age"])) < 37:
            row_template["Age_Below_37"] = 1
        else:
            row_template["Age_Below_37"] = 0
        row_template["Gender"] = series["gender"]

        row_template["Education_Num"] = EDUCATION_MAP[series["school"]]
        row_template["Education"] = series["school"]

        row_template["Income_Num"] = YEARLY_INCOME_MAP[series["income"]]
        row_template["Income"] = series["income"]

        row_template["Race/Ethnicity_Num"] = RACE_ETHNICITY_MAP[series["race"]]
        row_template["Race/Ethnicity"] = series["race"]

        row_template["Familiarity_Num"] = FAMILIARITY_MAP[series["ml prof"]]
        row_template["Familiarity"] = series["ml prof"]

        row_template["I_understand_model_decisions"] = series["percep decisions_1"]
        row_template["I_understand_model_output"] = series["percep output_1"]
        row_template["I_recommend_other_people"] = series["percep other_1"]
        row_template["qualitative_model_perception"] = int(series["percep decisions_1"]) + int(series["percep output_1"]) + int(series["percep other_1"])


        self.row_template = row_template
        self.series = series
        self.vis = vis
    
    
    def long_table_rows(self):

        comprehension_score = 0
        trust_score = 0
        likert_only_trust_score = 0
        bias_perception = 0
        computers_can_make_human_decisions = 0
        this_model_will_give_me_a_loan = 0
        this_model_shouldnt_give_me_a_loan = 0
        this_model_will_or_shouldnt_give_me_a_loan = 0
        correct_output = 0
        correct_pushing = 0
        correct_power = 0
        people = ["wom 1", "wom 2", "wom 3", "man 1", "man 2", "man 3"]
        people_for_order = ["Woman1", "Woman2", "Woman3", "Man1", "Man2", "Man3"]
        disc = 0
        if "agree" == self.series["fairness" + " agree_4"].strip().lower():
            computers_can_make_human_decisions = 1                    
        if "yes" == self.series["discrimination yn"].strip().lower():
            disc = 1
            bias_perception += 1
        if "yes" == self.series["fairness app a"].strip().lower():
            comprehension_score += 1
            correct_output += 1
        if "yes" == self.series["fairness app b"].strip().lower():
            comprehension_score += 1
            correct_output += 1
        for val in [" agree_3", " agree_4", " agree_5"]:
            if "agree" == self.series["fairness" + val].strip().lower():
                trust_score += 1                    
        for val in [" agree_1", " agree_2", " agree_6"]:
            if "disagree" == self.series["fairness" + val].strip().lower():
                bias_perception += 1                    
        for val in [" agree_7", " agree_8", " agree_9"]:
            if "agree" == self.series["fairness" + val].strip().lower():
                this_model_will_give_me_a_loan = 1
                this_model_will_or_shouldnt_give_me_a_loan = 1
        for val in [" agree_10"]:
            if "agree" == self.series["fairness" + val].strip().lower():
                this_model_shouldnt_give_me_a_loan = 1
                this_model_will_or_shouldnt_give_me_a_loan = 1
        likert_only_trust_score = (int(self.series["fairness" + " trust you_1"]) + int(self.series["fairness" + " trust other_1"]))
        trust_score += (int(self.series["fairness" + " trust you_1"]) + int(self.series["fairness" + " trust other_1"]))

        fairfacts = self.series["discrimination fact"].strip().split(',')
        agedisc = 0
        hoursdisc = 0
        occudisc = 0
        edudisc = 0
        sexdisc = 0
    
        if "yes" == self.series["discrimination yn"].strip().lower():
            if "Age" in fairfacts: 
                agedisc = 1
            if "Hours Per Week" in fairfacts: 
                hoursdisc = 1
            if "Occupation" in fairfacts: 
                occudisc = 1
            if "Education" in fairfacts: 
                edudisc = 1
            if "Sex" in fairfacts: 
                sexdisc = 1

        new_row = {}
        new_row.update(self.row_template)
        new_row.update(
          {
          "comprehension": comprehension_score,
          "trust": trust_score,
          "likert only trust": likert_only_trust_score,
          "discriminate Age": agedisc,
          "discriminate Hours per week": hoursdisc,
          "discriminate Occupation": occudisc,
          "discriminate Education": edudisc,
          "discriminate Sex": sexdisc,
          "discriminatory": disc,
          "bias operational": bias_perception,
          "person": "side by side",
          "correct output": correct_output,
          "correct pushing": correct_pushing,
          "correct power" : correct_power,
          "computers can make human decisions": computers_can_make_human_decisions,
          "this model will or shouldnt give me a loan" : this_model_will_or_shouldnt_give_me_a_loan,
          "this model will give me a loan" : this_model_will_give_me_a_loan,
          "this model shouldnt give me a loan" : this_model_shouldnt_give_me_a_loan,
          "order seen": 6
          }
        )
        yield new_row        
        randomization_order = self.series["FL_16_DO"].strip().split("|")
        for person, person_for_order in zip(people, people_for_order):
            new_row = {}
            comprehension_score = 0
            trust_score = 0
            likert_only_trust_score = 0
            bias_perception = 0
            computers_can_make_human_decisions = 0
            this_model_will_give_me_a_loan = 0
            this_model_shouldnt_give_me_a_loan = 0
            this_model_will_or_shouldnt_give_me_a_loan = 0
            correct_output = 0
            correct_pushing = 0
            correct_power = 0
            new_row.update(self.row_template)
            if "agree" == self.series[person + " agree_4"].strip().lower():
                computers_can_make_human_decisions = 1                    
            order_seen = randomization_order.index(person_for_order)
            for val in [" agree_3", " agree_4", " agree_5"]:
                if "agree" == self.series[person + val].strip().lower():
                    trust_score += 1                    
            for val in [" agree_1", " agree_2", " agree_6"]:
                if "disagree" == self.series[person + val].strip().lower():
                    bias_perception += 1                    
            for val in [" agree_7", " agree_8", " agree_9"]:
                if "agree" == self.series[person + val].strip().lower():
                    this_model_will_give_me_a_loan = 1
                    this_model_will_or_shouldnt_give_me_a_loan = 1
            for val in [" agree_10"]:
                if "agree" == self.series[person + val].strip().lower():
                    this_model_shouldnt_give_me_a_loan = 1
                    this_model_will_or_shouldnt_give_me_a_loan = 1
            if EXPECTED_APPROVAL[person] == self.series[person + " app"].strip().lower():
                comprehension_score += 1
                correct_output += 1
            lower_guess = self.series[person + " no"].strip().split(',')
            higher_guess = self.series[person + " yes"].strip().split(',')
            for lowerthing in PUSHED_LOWER[person]:
                if not lowerthing == "":
                    if (lowerthing in lower_guess) and (lowerthing not in higher_guess):
                      comprehension_score += 1
                      correct_pushing += 1
            for higherthing in PUSHED_HIGHER[person]:
                if not higherthing == "":
                    if (higherthing in higher_guess) and (higherthing not in lower_guess):
                      comprehension_score += 1
                      correct_pushing += 1
            for otherthing in PUSHED_NEITHER[person]:
                if not otherthing == "":
                    if (otherthing not in higher_guess) and (otherthing not in lower_guess):
                      comprehension_score += 1
                      correct_pushing += 1
            if PREDICTIVE_POWER[person] == self.series[person + " power"].strip():
                comprehension_score += 1
                correct_power += 1
            likert_only_trust_score += (int(self.series[person + " trust you_1"]) + int(self.series[person + " trust other_1"]))
            trust_score += (int(self.series[person + " trust you_1"]) + int(self.series[person + " trust other_1"]))
            new_row.update(
              {
              "comprehension": comprehension_score,
              "trust": trust_score,
              "likert only trust": likert_only_trust_score,
              "discriminate Age": agedisc,
              "discriminate Hours per week": hoursdisc,
              "discriminate Occupation": occudisc,
              "discriminate Education": edudisc,
              "discriminate Sex": sexdisc,
              "discriminatory": disc,
              "bias operational": bias_perception,
              "person": person,
              "correct output": correct_output,
              "correct pushing": correct_pushing,
              "correct power" : correct_power,
              "computers can make human decisions": computers_can_make_human_decisions,
              "computers can make human decisions": computers_can_make_human_decisions,
              "this model will or shouldnt give me a loan" : this_model_will_or_shouldnt_give_me_a_loan,
              "this model will give me a loan" : this_model_will_give_me_a_loan,
              "this model shouldnt give me a loan" : this_model_shouldnt_give_me_a_loan,
              "order seen": order_seen
              }
            )
            yield new_row        

class ResultsTable:

    def __init__(self, input_filename, vis) -> None:
        data = pd.read_csv(input_filename, skipinitialspace=True)

        # First row of "data" is actually details about the questions.
        #self.question_series = data.iloc[0]
        #self.df = data.iloc[1:]
        self.df = data
        self.df = self.df.replace(np.nan, '', regex=True)
        self.vis = vis

    def default_long_table_df(self):
        long_table_rows = []
        pid = 0
        for idx, row in self.df.iterrows():
            if idx == 0:
                continue
            if idx == 1:
                continue
            if row["Q1"] == "I agree" : 
                result = Result(row, pid, self.vis)
            pid += 1

            for long_table_row in result.long_table_rows():
                long_table_rows.append(long_table_row)

        return pd.DataFrame.from_records(long_table_rows)
