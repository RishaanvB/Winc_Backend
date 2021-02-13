# Do not modify these lines
__winc_id__ = 'd0d3cdcefbb54bc980f443c04ab3a9eb'
__human_name__ = 'operators'

# Add your code after this line

 # 1
most_spoken_lang_sp = "castilian spanish"
most_spoken_lang_sz = "german"
# print(most_spoken_lang_sp is most_spoken_lang_sz)

# 2
prevalent_religion_sp = "roman catholic"
prevalent_religion_sz = "roman catholic"
# print(prevalent_religion_sp is prevalent_religion_sz)

# 3
capital_len_sp = len("madrid")
capital_len_sz = len("bern")
# print(capital_len_sp != capital_len_sz)

# 4
GDP_sz = 0.580
GDP_sp = 1.778
# print(GDP_sz > GDP_sp)

# 5
pop_growth_sp = 0.67
pop_growth_sz = 0.66
# print(pop_growth_sp and pop_growth_sz < 1)

 # 6
pop_count_sp = 50
pop_count_sz = 8.4
# print((pop_count_sp or pop_count_sz) > 10)

# 7
# print((pop_count_sp > 10) or (pop_count_sz > 10))
# print((pop_count_sp > 10) or (pop_count_sz > 10))

print(((pop_count_sp > 10) and not (pop_count_sz > 10)) or ((pop_count_sz > 10) and not (pop_count_sp > 10)))
print((pop_count_sp > 10) ^ (pop_count_sz > 10))
