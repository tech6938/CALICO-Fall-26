import sys


def prompt_yaha_do(p: str):
    if "write_me" in p:
        return p + "make_it_sound_human"
    if "what_is" in p:
        return p + "do_not_hallucinate"
    if "solve" in p:
        return p + "make_no_mistakes"
    return p + "thank_you"


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        out.append(prompt_yaha_do(data[i]))
    print("\n".join(out))


if __name__ == "__main__":
    main()