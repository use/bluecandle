def compare_lists(a, b):
    a = set(numberize_duplicates(sorted(a)))
    b = set(numberize_duplicates(sorted(b)))
    a_minus_b = sorted(list(a - b))
    b_minus_a = sorted(list(b - a))
    return {
        'a-b': a_minus_b,
        'b-a': b_minus_a,
        'diff_ratio': (len(a_minus_b) + len(b_minus_a)) / ((len(a) + len(b))),
        'jaccard': len(a.intersection(b)) / len(a.union(b))
    }

def numberize_duplicates(l):
    found_items = {}
    new_list = []
    for item in l:
        if item in found_items:
            found_items[item] += 1
            num = found_items[item]
            name = item + " #" + str(num)
        else:
            found_items[item] = 1
            name = item
        new_list.append(name)
    return new_list

if __name__ == '__main__':
    l1 = [
        'strike',
        'strike',
        'bash',
        'bash+1',
        'defend',
        'something',
        'bash+1',
    ]
    l2 = [
        'strike',
        'bash',
        'bash+1',
        'defend',
        'defend',
        'something',
        'strike+1',
    ]
    print(numberize_duplicates(l1))
    print(compare_lists(l1, l2))