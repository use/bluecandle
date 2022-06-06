def compare_lists(a, b):
    a = set(numberize_duplicates(sorted(a)))
    b = set(numberize_duplicates(sorted(b)))
    return {
        'a-b': sorted(list(a - b)),
        'b-a': sorted(list(b - a)),
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