import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    # TODO implement the recognizer

    probabilities = []
    guesses = []
    all_Xlength = test_set.get_all_Xlengths()
    for sequence in test_set.get_all_sequences():
        best_guesses = ""
        best_score = float("-inf")
        prob = {}
        X, lengths = all_Xlength[sequence]
        for word, model in models.items():
            try:
                logL_score = model.score(X, lengths)
            except:
                logL_score = float("-inf")

            prob[word] = logL_score
            if logL_score > best_score:
                best_score = logL_score
                best_guesses = word

        probabilities.append(prob)
        guesses.append(best_guesses)

    return probabilities, guesses