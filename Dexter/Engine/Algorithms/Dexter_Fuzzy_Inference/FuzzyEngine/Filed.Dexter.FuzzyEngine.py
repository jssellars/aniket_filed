# Algoritmul functioneaza pe ideea de certitudine. Eu am o regula. Daca A e high si B e high atunci Fa asta.
# Definesc o variabila lingvistica pe 3 nivele: low, average, high pentru A si B pe tot intervalul de valori posibile. 
# Dat fiind A = a si B = b, determin membership function la fiecare nivel pt fiecare variabila si dupa le agreg => implicatia
# Certainty e definit pe [0,1], liniar cu valori intre [0,1]

# TODO: Investigate if I need to make the support for each metric dynamic, or it is ok with it between [0, 1]

from numpy import linspace

from Algorithms.Dexter_Fuzzy_Inference.FuzzyEngine.BaseEngine import Defuzzyfy
from Algorithms.Dexter_Fuzzy_Inference.FuzzyEngine.BaseEngine.Level import Level
from Algorithms.Dexter_Fuzzy_Inference.FuzzyEngine.BaseEngine.Level import MembershipFunctionDefinition
from Algorithms.Dexter_Fuzzy_Inference.FuzzyEngine.BaseEngine.LinguisticVariable import LinguisticVariable
from Algorithms.Dexter_Fuzzy_Inference.FuzzyEngine.Inference.Operators import Aggregator
from Algorithms.Dexter_Fuzzy_Inference.FuzzyEngine.Inference.Operators import And
from Algorithms.Dexter_Fuzzy_Inference.FuzzyEngine.Inference.Operators import Implication

# Define a generic High and Low variable
high_membership_function = MembershipFunctionDefinition('linear_function', parameters=[1.0 / (1.0 - 0.2), 1 - (1.0 / (1.0 - 0.2))])
low_membership_function = MembershipFunctionDefinition('linear_function', parameters=[-1.0 / 0.5, 1])

# Define fuzzy CPA value 
cpa_levels = {
    'high': Level('high', 1, high_membership_function),
    'low': Level('low', 1, low_membership_function)
}
cpa_linguistic_variable = LinguisticVariable('cpa', levels=cpa_levels)

# Define fuzzy frequency value
frequency_levels = {
    'high': Level('high', 1, high_membership_function),
    'low': Level('low', 1, low_membership_function)
}
frequency_linguistic_variable = LinguisticVariable('frequency', levels=frequency_levels)

# Define fuzzy confidence variable
_n_values = 50
_step = 1.0 / _n_values
_min_confidence_value = 0.0
_max_confidence_value = 1.0
fuzzy_confidence_level = {'confidence': Level('confidence', 1, MembershipFunctionDefinition('step_function', parameters=[0.95]))}
fuzzy_confidence_linguistic_variable = LinguisticVariable('confidence', levels=fuzzy_confidence_level)
fuzzy_confidence_support = linspace(_min_confidence_value, _max_confidence_value, _n_values)

# Sample input
cpa = 0.1
frequency = 0.1

# Predict how confident I am in the rule that if CPA is High and Frequency is High then Do Something
# TODO: move this code to Rule.PredictConfidence()
results = []
fuzzy_confidence_membership_function = fuzzy_confidence_linguistic_variable.generate_membership_functions_by_level('confidence', step=_step)

rules = [('low', None),
         (None, 'low'),
         ('low', 'low')]

for rule in rules:
    if rule[0] and rule[1]:
        cpa_membership_value = cpa_linguistic_variable.get_membership_value(rule[0], cpa)
        frequency_membership_value = frequency_linguistic_variable.get_membership_value(rule[1], frequency)
    elif rule[0]:
        cpa_membership_value = cpa_linguistic_variable.get_membership_value(rule[0], cpa)
        frequency_membership_value = None
    elif rule[1]:
        frequency_membership_value = frequency_linguistic_variable.get_membership_value(rule[1], frequency)
        cpa_membership_value = None
    else:
        raise ValueError('Unknown linguistic variable levels.')

    rule_antecedent_fuzzy_value = And.min(cpa_membership_value, frequency_membership_value)
    implication_result = Implication.min(rule_antecedent_fuzzy_value, fuzzy_confidence_membership_function)

    results.append(implication_result)

inference_result = Aggregator.max(results)

confidence = Defuzzyfy.centroid(fuzzy_confidence_support, inference_result)

print("\nCertainty: {:.2%}".format(confidence))

# print(cpaLinguisticVariable.generate_membership_functions_by_level('low'))
# print(cpaLinguisticVariable.generate_membership_functions_by_level('high'))
# print(fuzzyConfidenceMembershipFunction)
