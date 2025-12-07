class BitReader:
    def __init__(self, hex_data):
        self.bin_data = []
        for char in hex_data.strip():
            val = int(char, 16)
            self.bin_data.append(f"{val:04b}")
        self.bits = "".join(self.bin_data)
        self.pos = 0
        
    def read(self, n):
        val = int(self.bits[self.pos:self.pos+n], 2)
        self.pos += n
        return val
        
    def read_raw(self, n):
        val = self.bits[self.pos:self.pos+n]
        self.pos += n
        return val

    def has_bits(self, n):
        return self.pos + n <= len(self.bits)

def parse_packet(reader):
    version = reader.read(3)
    type_id = reader.read(3)
    
    packet = {
        'version': version,
        'type_id': type_id,
        'sub_packets': [],
        'value': None
    }
    
    if type_id == 4:
        # Literal value
        value_bits = ""
        while True:
            prefix = reader.read(1)
            value_bits += reader.read_raw(4)
            if prefix == 0:
                break
        packet['value'] = int(value_bits, 2)
    else:
        # Operator
        length_type_id = reader.read(1)
        if length_type_id == 0:
            # 15 bits total length
            total_length = reader.read(15)
            start_pos = reader.pos
            while reader.pos < start_pos + total_length:
                packet['sub_packets'].append(parse_packet(reader))
        else:
            # 11 bits number of sub-packets
            num_packets = reader.read(11)
            for _ in range(num_packets):
                packet['sub_packets'].append(parse_packet(reader))
                
    return packet

def sum_versions(packet):
    total = packet['version']
    for sub in packet['sub_packets']:
        total += sum_versions(sub)
    return total

def parse(data):
    return data.strip()

def part1(parsed_data):
    reader = BitReader(parsed_data)
    packet = parse_packet(reader)
    return sum_versions(packet)

def calculate(packet):
    tid = packet['type_id']
    if tid == 4:
        return packet['value']
        
    subs = [calculate(p) for p in packet['sub_packets']]
    
    if tid == 0: # Sum
        return sum(subs)
    elif tid == 1: # Product
        res = 1
        for val in subs:
            res *= val
        return res
    elif tid == 2: # Min
        return min(subs)
    elif tid == 3: # Max
        return max(subs)
    elif tid == 5: # GT
        return 1 if subs[0] > subs[1] else 0
    elif tid == 6: # LT
        return 1 if subs[0] < subs[1] else 0
    elif tid == 7: # EQ
        return 1 if subs[0] == subs[1] else 0
        
    return 0

def part2(parsed_data):
    reader = BitReader(parsed_data)
    packet = parse_packet(reader)
    return calculate(packet)
