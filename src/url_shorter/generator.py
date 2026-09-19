A = 1103515245
B = 12345
ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BASE = len(ALPHABET)  # 62
LEN = 5
M = BASE**LEN  # 916132832


def to_code(n: int) -> str:
    if not (0 <= n < M):
        raise ValueError("ID не влезает в 5 символов base62")
    chars = []
    for _ in range(LEN):
        n, r = divmod(n, BASE)
        chars.append(ALPHABET[r])
    return "".join(reversed(chars))


def from_code(code: str) -> int:
    n = 0
    for ch in code:
        n = n * BASE + ALPHABET.index(ch)
    return n


def to_code_obf(id_: int) -> str:
    y = (id_ * A + B) % M
    return to_code(y)


def from_code_obf(code: str) -> int:
    y = from_code(code)
    invA = pow(A, -1, M)  # A и M должны быть взаимно просты
    return ((y - B) * invA) % M
