from Algorithms.Models.Types import TypesWrapper as tw
from Infrastructure.Mongo.Mongo import MongoMediator
import logging

def GenerateSeedList():
    # Generates a List of the Optymization types to be inserted into the database

    types = []
    budget = tw.OptimizationType('Budget', [tw.Levels.Campaign, tw.Levels.AdSet, tw.Levels.Ad], 'None')
    types.append(budget)

    age = tw.OptimizationType('Age', [tw.Levels.Breakdown], 'Age')
    types.append(age)

    gender = tw.OptimizationType('Gender', [tw.Levels.Breakdown], 'Gender')
    types.append(gender)

    ageGender = tw.OptimizationType('Age and Gender', [tw.Levels.Breakdown], 'Age and Gender')
    types.append(ageGender)

    placement = tw.OptimizationType('Placement', [tw.Levels.Breakdown], 'Placement' )
    types.append(placement)

    device = tw.OptimizationType('Impression Device', [tw.Levels.Breakdown], 'Impression Device')
    types.append(device)

    location = tw.OptimizationType('Country', [tw.Levels.Breakdown], 'Country')
    types.append(location)

    region = tw.OptimizationType('Region', [tw.Levels.Breakdown], 'Region')
    types.append(region)

    interest = tw.OptimizationType('Interest', [tw.Levels.Interest], 'Interest')
    types.append(interest)

    return types


def GetExpandedSeeds(baseSeeds):
    expandedList = []
    for seed in baseSeeds:
        expandedList += seed.getExpandedTuples()
    return expandedList


def PushSeeds():
    try:
        logging.info('Started seeding optimization types')
        mongoMediator = MongoMediator()
    
        baseList = GenerateSeedList()
        mappedList = map(lambda x: x.__dict__, baseList)
        mongoMediator.store_optimization_types(mappedList)
    
        expandedSeeds = GetExpandedSeeds(baseList)
        mongoMediator.store_expanded_types(expandedSeeds)
        logging.info('Finished seeding optimization types')
    
    except Exception as e:
        logging.exception(e)
