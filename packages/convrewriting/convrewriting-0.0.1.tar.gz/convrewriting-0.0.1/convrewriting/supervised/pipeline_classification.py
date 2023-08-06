import pandas as pd
import os
import argparse
# # Utterance rewriting strategies for post-classification
from convrewriting.supervised.topic_utils import create_doc, _find_topic, _rewrite_utt, _find_cue_topic, _find_topic_all


def load_data():

    test_df_path = os.path.join(os.path.dirname(__file__), '../data/datasets', 'test_df.pkl')
    test_df = pd.read_pickle(test_df_path)

    test_features_step1_path = os.path.join(os.path.dirname(__file__), '../data/gbdt_features',
                                 'test_features_step1.pkl')
    test_features_s1 = pd.read_pickle(test_features_step1_path)

    test_features_s2_path = os.path.join(os.path.dirname(__file__), '../data/gbdt_features',
                                 'test_features_step2_all_feat_lightGBM_S1_BERT.pkl')
    test_features_s2 = pd.read_pickle(test_features_s2_path)

    # we use predicted labels from file instead of running the model in inference
    predFile_Step1 = os.path.join(os.path.dirname(__file__),
                                         '../data/bert_models',
                                         'pred_BERT_MSMARCO_step1.tsv')
    pred_df_step1 = pd.read_csv(predFile_Step1, delimiter="\t", header=None)

    # we use predicted labels from file instead of running the model in inference
    predFile_Step2 = os.path.join(os.path.dirname(__file__),
                                  '../data/bert_models',
                                  'pred_BERT_MSMARCO_step2.tsv')
    pred_df_step2 = pd.read_csv(predFile_Step2, delimiter="\t", header=None)

    # # Assemble results and simulate prediction
    test_index = list(test_df.index)

    return test_df, pred_df_step1, pred_df_step2, test_index, test_features_s1, test_features_s2


def get_classif_results(test_index,test_df,pred_df_step1,pred_df_step2):
    '''
    # Result dict is a dictionary:
    # - key: qid
    # - value: a tuple of (predicted_label, groundtruth_label, original_utterance)
    '''

    result_dict = {}
    for i in test_index:
        utt_id = test_df[0][i]
        if (test_df[0][i].split("_")[1]==str(1)):
            result_dict[test_df[0][i]] = ("SE", test_df[2][i], test_df[1][i])
        else:
            # predictions for STEP 1
            result_step1 = pred_df_step1[2][i]
            if result_step1==1:
                result_dict[test_df[0][i]] = ("SE", test_df[2][i], test_df[1][i])
            else:
                # predictions for STEP 2
                aux = pred_df_step2.loc[pred_df_step2[0]==utt_id]
                result_step2 = int(aux[4])
                if result_step2 == 1:
                    result_dict[test_df[0][i]] = ("FT", test_df[2][i], test_df[1][i])
                else:
                    result_dict[test_df[0][i]] = ("PT", test_df[2][i], test_df[1][i])
    # predicted vs ground truth
    return result_dict


def strategy_Standard(test_df, pred_df_step1, pred_df_step2, test_features_s2):
    """
    Enrich with first or previous topic
    - extract first and previous topic and rewrite utterance
    - if missing third person pronoun we trail either first or previous
    :param test_df: the test dataset
    :param pred_df_step1: predictions dataframe for Step1 (we don't use the model,
    we just assemble the results)
    :param pred_df_step2: predictions dataframe for Step1
    :param test_features_s2: features dataframe for which we use the doc object
    (with the nlp by spacy) for rewriting
    :return:
    """
    test_index = list(test_df.index)
    result_dict = {}

    for i in test_index:
        utt_id = test_df[0][i]
        if test_df[0][i].split("_")[1] == str(1):
            result_dict[test_df[0][i]] = test_df[1][i]
        else:
            # STEP 1
            result_step1 = pred_df_step1[2][i]
            if result_step1 == 1:
                result_dict[test_df[0][i]] = test_df[1][i]
            else:
                # STEP 2
                aux = pred_df_step2.loc[pred_df_step2[0] == utt_id]
                result_step2 = int(aux[4])

                current_doc = test_features_s2.at[i, "doc"]

                if result_step2 == 1:
                    # get the first topic
                    conv_id = test_df[0][i].split("_")[0]
                    first_utt_id = conv_id + "_1"
                    row_index_first = test_features_s2.index[
                        test_features_s2[0] == first_utt_id].tolist()[0]
                    first_utt_doc = test_features_s2.at[row_index_first, "doc"]
                    first_topic = _find_topic(first_utt_doc)

                    new_utt = _rewrite_utt(current_doc, first_topic=first_topic,
                                           previous_topic="", context_list=None,
                                           trailing=True)
                    result_dict[test_df[0][i]] = new_utt
                else:
                    # get the previous topic
                    prev_utt_id = test_df[0][i - 1]
                    row_index_previous = test_features_s2.index[
                        test_features_s2[0] == prev_utt_id].tolist()[0]
                    prev_utt_doc = test_features_s2.at[
                        row_index_previous, "doc"]
                    prev_topic = _find_topic(prev_utt_doc)

                    new_utt = _rewrite_utt(current_doc, first_topic="",
                                           previous_topic=prev_topic,
                                           context_list=None, trailing=True)
                    result_dict[test_df[0][i]] = new_utt

    return result_dict


def strategy_Enriched(test_df, pred_df_step1, pred_df_step2, test_features_s2):
    """
    Similar to Strategy Standard but for PT we extract on enriched utterance
    :param test_df: the test dataset
    :param pred_df_step1: predictions dataframe for Step1 (we don't use the model,
    we just assemble the results)
    :param pred_df_step2: predictions dataframe for Step1
    :param test_features_s2: features dataframe for which we use the doc object
    (with the nlp by spacy) for rewriting
    :return:
    """
    test_index = list(test_df.index)
    result_dict = {}
    enriched_utt_dict = {}

    for i in test_index:
        utt_id = test_df[0][i]
        if test_df[0][i].split("_")[1] == str(1):
            result_dict[test_df[0][i]] = ("SE", test_df[1][i])
            enriched_utt_dict[i] = test_df[1][i]
        else:
            # STEP 1
            result_step1 = pred_df_step1[2][i]
            if result_step1 == 1:
                result_dict[test_df[0][i]] = ("SE", test_df[1][i])
                enriched_utt_dict[i] = test_df[1][i]
            else:
                # STEP 2
                aux = pred_df_step2.loc[pred_df_step2[0] == utt_id]
                result_step2 = int(aux[4])

                current_doc = test_features_s2.at[i, "doc"]

                if result_step2 == 1:
                    # get the first topic
                    conv_id = test_df[0][i].split("_")[0]
                    first_utt_id = conv_id + "_1"
                    row_index_first = test_features_s2.index[
                        test_features_s2[0] == first_utt_id].tolist()[0]
                    first_utt_doc = test_features_s2.at[row_index_first, "doc"]
                    first_topic = _find_topic(first_utt_doc)

                    new_utt = _rewrite_utt(current_doc, first_topic=first_topic,
                                           previous_topic="", context_list=None,
                                           trailing=True)
                    result_dict[test_df[0][i]] = ("FT", new_utt)
                    enriched_utt_dict[i] = new_utt
                else:
                    # get the previous topic
                    # this changes respect to Strategy 1
                    prev_utt_doc = create_doc(enriched_utt_dict[i - 1])
                    prev_topic = _find_topic(prev_utt_doc)

                    new_utt = _rewrite_utt(current_doc, first_topic="",
                                           previous_topic=prev_topic,
                                           context_list=None, trailing=True)
                    result_dict[test_df[0][i]] = ("PT", new_utt)
                    enriched_utt_dict[i] = new_utt
    return result_dict


def strategy_Last_SE(test_df, pred_df_step1, test_features_s2):
    """
    Propagate everything from the last SE
    :param test_df: the test dataset
    :param pred_df_step1: predictions dataframe for Step1 (we don't use the model,
    we just assemble the results)
    :param test_features_s2: features dataframe for which we use the doc object
    (with the nlp by spacy) for rewriting
    :return:
    """

    test_index = list(test_df.index)
    result_dict = {}
    last_SE_topic = ""

    for i in test_index:
        if test_df[0][i].split("_")[1] == str(1):
            result_dict[test_df[0][i]] = test_df[1][i]
            last_SE_topic = _find_topic(test_features_s2["doc"][i])

        else:
            resultSE = pred_df_step1[2][i]
            if resultSE == 1:
                result_dict[test_df[0][i]] = test_df[1][i]
                last_SE_topic = _find_topic(test_features_s2["doc"][i])

            else:
                current_doc = test_features_s2.at[i, "doc"]
                new_utt = _rewrite_utt(current_doc, first_topic="",
                                       previous_topic=last_SE_topic,
                                       context_list=None, trailing=True)
                result_dict[test_df[0][i]] = new_utt

    return result_dict


def strategy_First_and_Last_SE(test_df, pred_df_step1, test_features_s2):
    """
    Propagate everything from the last SE and keep FT for context
    (expand for all previous also with first!, similar to trailing)
    :param test_df: the test dataset
    :param pred_df_step1: predictions dataframe for Step1 (we don't use the model,
    we just assemble the results)
    :param test_features_s2: features dataframe for which we use the doc object
    (with the nlp by spacy) for rewriting
    :return:
    """

    test_index = list(test_df.index)
    result_dict = {}
    last_SE_topic = ""
    first_SE_topic = ""

    for i in test_index:
        if test_df[0][i].split("_")[1] == str(1):
            result_dict[test_df[0][i]] = test_df[1][i]

            last_SE_topic = _find_topic(test_features_s2["doc"][i])
            first_SE_topic = last_SE_topic

        else:
            resultSE = pred_df_step1[2][i]
            if resultSE == 1:
                result_dict[test_df[0][i]] = test_df[1][i] + " " + first_SE_topic
                last_SE_topic = _find_topic(test_features_s2["doc"][i])

            else:
                current_doc = test_features_s2.at[i, "doc"]
                new_utt = _rewrite_utt(current_doc, first_topic="",
                                       previous_topic=last_SE_topic,
                                       context_list=None, trailing=True)
                result_dict[test_df[0][i]] = new_utt + " " + first_SE_topic
    return result_dict


def strategy_First_or_Last_SE(test_df, pred_df_step1, pred_df_step2, test_features_s2):
    """
    If FT enrich with first SE. If PT enrich with last SE.
    :param test_df: the test dataset
    :param pred_df_step1: predictions dataframe for Step1 (we don't use the model,
    we just assemble the results)
    :param pred_df_step2: predictions dataframe for Step1
    :param test_features_s2: features dataframe for which we use the doc object
    (with the nlp by spacy) for rewriting
    :return:
    """

    test_index = list(test_df.index)
    result_dict = {}
    last_SE_topic = ""
    first_SE_topic = ""

    for i in test_index:
        utt_id = test_df[0][i]
        if test_df[0][i].split("_")[1] == str(1):
            result_dict[test_df[0][i]] = test_df[1][i]
            last_SE_topic = _find_topic_all(test_features_s2["doc"][i])
            first_SE_topic = last_SE_topic

        else:
            # STEP 1
            result_step1 = pred_df_step1[2][i]
            if result_step1 == 1:
                result_dict[test_df[0][i]] = test_df[1][i]
                last_SE_topic = _find_topic_all(test_features_s2["doc"][i])
            else:
                # STEP 2
                aux = pred_df_step2.loc[pred_df_step2[0] == utt_id]
                result_step2 = int(aux[4])

                current_doc = test_features_s2.at[i, "doc"]

                if result_step2 == 1:
                    new_utt = _rewrite_utt(current_doc,
                                           first_topic=first_SE_topic,
                                           previous_topic="", context_list=None,
                                           trailing=True)
                    result_dict[test_df[0][i]] = new_utt
                else:
                    new_utt = _rewrite_utt(current_doc, first_topic="",
                                           previous_topic=last_SE_topic,
                                           context_list=None, trailing=True)
                    result_dict[test_df[0][i]] = new_utt

    return result_dict


def rewrite_strategy(method="Standard"):
    # choices=["Standard", "Enriched", "LastSE", "First_and_Last_SE", "First_or_Last_SE"]
    test_df, pred_df_step1, pred_df_step2, test_index, test_features_s1, test_features_s2 = load_data()

    if method == "Standard":
        result_dict = strategy_Standard(test_df, pred_df_step1, pred_df_step2,
                                        test_features_s2)
    elif method == "Enriched":
        result_dict = strategy_Enriched(test_df, pred_df_step1, pred_df_step2,
                                    test_features_s2)
    elif method == "LastSE":
        result_dict = strategy_Last_SE(test_df, pred_df_step1, test_features_s2)
    elif method == "First_and_Last_SE":
        result_dict = strategy_First_and_Last_SE(test_df, pred_df_step1, test_features_s2)
    elif method == "First_or_Last_SE":
        result_dict = strategy_First_or_Last_SE(test_df, pred_df_step1,
                                            pred_df_step2, test_features_s2)

    for k,v in result_dict.items():
        print(k,v)


if __name__ == "__main__":
    rewrite_strategy("Standard")