def split_file(filename: str) -> list:
    with open(filename, 'r') as f:
        data = ''.join(map(lambda l: l.strip(), f.readlines()))
        return [q for q in data.split(';') if q]
