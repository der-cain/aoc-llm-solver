def parse(data):
    return [int(x) for x in data.split()]

def parse_node(data, index):
    child_count = data[index]
    metadata_count = data[index+1]
    index += 2

    children = []
    for _ in range(child_count):
        child, index = parse_node(data, index)
        children.append(child)

    metadata = data[index:index+metadata_count]
    index += metadata_count

    return {'children': children, 'metadata': metadata}, index

def part1(data):
    root, _ = parse_node(data, 0)

    def sum_metadata(node):
        return sum(node['metadata']) + sum(sum_metadata(c) for c in node['children'])

    return sum_metadata(root)

def part2(data):
    root, _ = parse_node(data, 0)

    def get_value(node):
        if not node['children']:
            return sum(node['metadata'])

        value = 0
        for m in node['metadata']:
            # Metadata is 1-based index
            if 0 < m <= len(node['children']):
                value += get_value(node['children'][m-1])
        return value

    return get_value(root)
