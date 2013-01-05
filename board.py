
def load_board():
    with open("board.txt") as f:
        tiles = []
        for line in f:
            row = []
            tiles.append(row)
            for character in line.strip():
                row.append(character == '1')
    return tiles

