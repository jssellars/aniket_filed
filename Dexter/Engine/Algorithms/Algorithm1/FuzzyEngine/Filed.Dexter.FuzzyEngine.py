# Algoritmul functioneaza pe ideea de certitudine. Eu am o regula. Daca A e high si B e high atunci Fa asta.
# Definesc o variabila lingvistica pe 3 nivele: low, average, high pentru A si B pe tot intervalul de valori posibile. 
# Dat fiind A = a si B = b, determin membership function la fiecare nivel pt fiecare variabila si dupa le agreg => implicatia
# Certainty e definit pe [0,1], liniar cu valori intre [0,1]

# TODO: Investigate if I need to make the support for each metric dynamic, or it is ok with it between [0, 1]

from numpy import linspace 

from Algorithms.Algorithm1.FuzzyEngine.BaseEngine import Defuzzyfy
from Algorithms.Algorithm1.FuzzyEngine.BaseEngine.LinguisticVariable import LinguisticVariable
from Algorithms.Algorithm1.FuzzyEngine.BaseEngine.Level import Level
from Algorithms.Algorithm1.FuzzyEngine.BaseEngine.Level import MembershipFunctionDefinition
from Algorithms.Algorithm1.FuzzyEngine.Inference.Operators import Aggregator
from Algorithms.Algorithm1.FuzzyEngine.Inference.Operators import And
from Algorithms.Algorithm1.FuzzyEngine.Inference.Operators import Implication


# Define a generic High and Low variable 
highMembershipFunction = MembershipFunctionDefinition('LinearFunction', parameters=[1.0/(1.0-0.2), 1-(1.0/(1.0-0.2))])
lowMembershipFunction = MembershipFunctionDefinition('LinearFunction', parameters=[-1.0/0.5, 1])

# Define fuzzy CPA value 
cpaLevels = {
    'high': Level('high', 1, highMembershipFunction),
    'low': Level('low', 1, lowMembershipFunction)
    }
cpaLinguisticVariable = LinguisticVariable('cpa', levels=cpaLevels)

# Define fuzzy frequency value
frequencyLevels = {
    'high': Level('high', 1, highMembershipFunction),
    'low': Level('low', 1, lowMembershipFunction) 
    }
frequencyLinguisticVariable = LinguisticVariable('frequency', levels=frequencyLevels)

# Define fuzzy confidence variable
_nValues = 50
_step = 1.0/_nValues
_minConfidenceValue = 0.0
_maxConfidenceValue = 1.0
fuzzyConfidenceLevel = {'confidence': Level('confidence', 1, MembershipFunctionDefinition('StepFunction', parameters=[0.95]))}
fuzzyConfidenceLiguisticVariable = LinguisticVariable('confidence', levels=fuzzyConfidenceLevel)
fuzzyConfidenceSupport = linspace(_minConfidenceValue, _maxConfidenceValue, _nValues)

# Sample input
cpa = 0.1
frequency = 0.1

# Predict how confident I am in the rule that if CPA is High and Frequency is High then Do Something
# TODO: move this code to Rule.PredictConfidence()
results = []
fuzzyConfidenceMembershipFunction = fuzzyConfidenceLiguisticVariable.GenerateMembershipFunctionsByLevel('confidence', step=_step)

rules = [('low', None),
         (None, 'low'),
         ('low', 'low')]


for rule in rules:
    if rule[0] and rule[1]:
        cpaMembershipValue = cpaLinguisticVariable.GetMembershipValue(rule[0], cpa)
        frequencyMembershipValue = frequencyLinguisticVariable.GetMembershipValue(rule[1], frequency)      
    elif rule[0]:
        cpaMembershipValue = cpaLinguisticVariable.GetMembershipValue(rule[0], cpa)
        frequencyMembershipValue = None 
    elif rule[1]:
        frequencyMembershipValue = frequencyLinguisticVariable.GetMembershipValue(rule[1], frequency)      
        cpaMembershipValue = None 
    else:
        raise ValueError('Unknown linguistic variable levels.')

    ruleAntecentFuzzyValue = And.Min(cpaMembershipValue, frequencyMembershipValue)
    implicationResult = Implication.Min(ruleAntecentFuzzyValue, fuzzyConfidenceMembershipFunction)

    results.append(implicationResult)

inferenceResult = Aggregator.Max(results)

confidence = Defuzzyfy.Centroid(fuzzyConfidenceSupport, inferenceResult)

print("\nCertainty: {:.2%}".format(confidence))


# print(cpaLinguisticVariable.GenerateMembershipFunctionsByLevel('low'))
# print(cpaLinguisticVariable.GenerateMembershipFunctionsByLevel('high'))
# print(fuzzyConfidenceMembershipFunction)
