from pprint import pprint 

def print_pretty(obj):
    pprint(obj)

def print_block(string, end="\n"):
    hash_num = 45
    print("\n\n")
    print("#" * hash_num)

    mid_hash_num = min((hash_num - len(string) - 2) // 2, 3)
    mid_hash = "#" * mid_hash_num
    mid_space = " " * ((hash_num - 2 * mid_hash_num - len(string))//2)
    print("{}{}{}{}{}".format(
        mid_hash, mid_space, " "*len(string), mid_space, mid_hash
    ))
    print("{}{}{}{}{}".format(
        mid_hash, mid_space, string, mid_space, mid_hash
    ))
    print("{}{}{}{}{}".format(
        mid_hash, mid_space, " "*len(string), mid_space, mid_hash
    ))
    print("#" * hash_num)
    print()