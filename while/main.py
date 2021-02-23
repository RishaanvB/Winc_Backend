from helpers import random_koala_fact

__winc_id__ = "c0dc6e00dfac46aab88296601c32669f"
__human_name__ = "while"

# This block is only executed if this script is run directly (python main.py)
# It is not run if you import this file as a module.
if __name__ == "__main__":
    print(random_koala_fact())

return


def unique_koala_facts(amount_of_facts):
    unique_list = []
    while amount_of_facts:
        unique_list.append(random_koala_fact())
        amount_of_facts -= 1
    print(unique_list)
    print(len(unique_list))

    # break


unique_koala_facts(4)


def num_joey_facts():
    first_fact = random_koala_fact()
    unique_facts = []
    repeated_fact = 0
    while repeated_fact < 10:
        fact = unique_koala_facts()
        if fact == first_fact:
            repeated_fact += 1
        if fact not in unique_facts:
            unique_facts.append(fact)
            if "joey" in fact.lower():
                num_joey_facts += 1
    return print(num_joey_facts)


return
print
