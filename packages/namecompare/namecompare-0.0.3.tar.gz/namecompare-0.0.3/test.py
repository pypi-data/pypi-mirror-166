import names_matcher

print(names_matcher.NamesMatcher('FirstLightAFire', 'LightTheFireFirst').ordered_words_match())



#
#
#
#
# from names_matcher import *
#
#
#
# from names_matcher import NamesMatcher, run_test
#
# set_bit = lambda bit, num=0: num | (1 << bit)
#
# TEST_EDIT_DISTANCE = set_bit(0)
# TEST_NORMALIZED_EDIT_DISTANCE = set_bit(1)
# TEST_DIFFLIB_MATCHER_RATIO = set_bit(2)
# TEST_ORDERED_MATCH = set_bit(3)
# TEST_ORDERED_WORD_MATCH = set_bit(4)
# TEST_ORDERED_SEMANTIC_MATCH = set_bit(5)
# TEST_UNORDERED_MATCH = set_bit(6)
# TEST_UNORDERED_WORDS_MATCH = set_bit(7)
# TEST_UNORDERED_SEMANTIC_MATCH = set_bit(8)
# TEST_UNEDIT_MATCH = set_bit(9)
#
# scriptIndex = -1
#
# vars_matcher = NamesMatcher()
#
# var_names = [('A_CD_EF_B', 'A_EF_CD_B')]
# run_test(vars_matcher, var_names, vars_matcher.unedit_match, min_len=2)
#
# # var_names = [
# #     # ('multi_multiplayer', 'multiplayers_layer'),
# #     # ('multi_multiplayers', 'multiplayers_layer'),
# #     # ('multi', 'multiplayers'),
# #     # ('multi', 'layer'),
# #     # ('multiplayer', 'layer'),
# #     # ('multiplayers', 'layer'),
# #     # ('multiplayer', 'multiplayers'),
# #
# #     # ('multiword_name', 'multiple_words_name'),
# #     # ('multiword', 'multiple'),
# #     # ('multiword', 'words'),
# #
# #     ('MultiplyDigitExponent', 'DigitsPowerMultiplying'),
# # ]
# # # run_test(vars_matcher, var_names, vars_matcher.ordered_words_match, min_word_match_degree=0.55)
# #
# # # run_test(vars_matcher, var_names, vars_matcher.ordered_words_match, min_word_match_degree=2/3)
# # # run_test(vars_matcher, var_names, vars_matcher.ordered_words_match, min_word_match_degree=0.57)
# # # run_test(vars_matcher, var_names, vars_matcher.ordered_words_match, min_word_match_degree=0.5)
# #
# # run_test(vars_matcher, var_names, vars_matcher.ordered_words_match, min_word_match_degree=1)
#
#
# # run_test(vars_matcher, var_names, vars_matcher.ordered_words_match, min_word_match_degree=0.5, prefer_num_of_letters=True)
# # run_test(vars_matcher, var_names, vars_matcher.ordered_words_match, min_word_match_degree=0.55, prefer_num_of_letters=True)
# # run_test(vars_matcher, var_names, vars_matcher.ordered_words_match, min_word_match_degree=0.55, continuity_heavy_weight=True)
# # run_test(vars_matcher, var_names, vars_matcher.ordered_words_match, min_word_match_degree=0.55, prefer_num_of_letters=True, continuity_heavy_weight=True)
# # run_test(vars_matcher, var_names, vars_matcher.ordered_match, min_len=2)
