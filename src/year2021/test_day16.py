from src.year2021.day16 import parse, part1, part2

def test_part1():
    examples = [
        ("8A004A801A8002F478", 16),
        ("620080001611562C8802118E34", 12),
        ("C0015000016115A2E0802F182340", 23),
        ("A0016C880162017C3686B18A3D4780", 31)
    ]
    
    for hex_str, expected in examples:
        result = part1(hex_str)
        print(f"Part 1 Input: {hex_str[:10]}... Result: {result}, Expected: {expected}")
        assert result == expected

def test_part2():
    examples = [
        ("C200B40A82", 3),
        ("04005AC33890", 54),
        ("880086C3E88112", 7),
        ("CE00C43D881120", 9),
        ("D8005AC2A8F0", 1),
        ("F600BC2D8F", 0),
        ("9C005AC2F8F0", 0),
        ("9C0141080250320F1802104A08", 1)
    ]
    
    for hex_str, expected in examples:
        result = part2(hex_str)
        print(f"Part 2 Input: {hex_str[:10]}... Result: {result}, Expected: {expected}")
        assert result == expected

if __name__ == "__main__":
    test_part1()
    test_part2()
    print("Test Passed!")

