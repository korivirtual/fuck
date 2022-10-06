def slide_to_the_left(b: bytes) -> int:
    result = 0

    for i in range(len(b) - 1):
        shift = 8 * i
        byte = b[i]

        result |= byte << shift
    
    return result

def slide_to_the_right(b: bytes) -> int:
    print("criss cross!")
    return 0