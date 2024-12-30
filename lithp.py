WHITESPACE: list[str] = [" ", "\t", "\n"]

BEGIN_BLK: list[str] = ["("]
END_BLK: list[str] = [")"]

BEGIN_COMMENT: list[str] = ["{"]
END_COMMENT: list[str] = ["}"]

BEGIN_STR: list[str] = ["\""]
END_STR: list[str] = ["\""]


OP_ADD: list[str] = ["+"]
OP_SUB: list[str] = ["-"]
OP_MUL: list[str] = ["*"]
OP_DIV: list[str] = ["/"]
OP_POW: list[str] = ["**"]

OP_LIST: list[str] = ["list"]
OP_UNPACK: list[str] = ["unpack"]



def tokenize(src: str) -> tuple[list[list | str], int]:
    tks = []

    w = ""

    n_chars = 0
    skip_chars = 0

    is_comment = False
    is_str = False
    c_begin_str = ""

    def end_word(w):
        if w != "":
            tks.append(w)
            w = ""
        return w


    for c in src:
        n_chars += 1
        if skip_chars > 0:
            skip_chars -= 1
            continue

        blk_begin = False
        blk_end = False
        word_end = True

        if c in END_COMMENT and not is_str:
            is_comment = False
            continue
        elif is_comment:
            continue

        if not is_comment:
            trivial_char = False

            if is_str:
                if c in END_STR:
                    is_str = False
                    w = c_begin_str + w + c
                else:
                    trivial_char = True
            elif c in BEGIN_STR:
                is_str = True
                c_begin_str = c
            elif c in WHITESPACE:
                pass
            elif c in BEGIN_COMMENT:
                is_comment = True
            elif c in BEGIN_BLK:
                blk_begin = True
            elif c in END_BLK:
                blk_end = True
            else:
                trivial_char = True

            if trivial_char:
                word_end = False
                w += c

            if word_end:
                w = end_word(w)
                
            if blk_begin:
                sub_tks, skip_chars = tokenize(src[n_chars:])
                tks.append(sub_tks)
            elif blk_end:
                break
    w = end_word(w)

    return tks, n_chars


def evaluate(tks: list[list | str]) -> list | str | float | None:
    res = None

    def parse_tk(tk):
        val = tk
        if len(val) > 0:
            if val[0] not in BEGIN_STR:
                try:
                    val = float(val)
                except ValueError as e:
                    pass
                except TypeError as e:
                    pass
        return val


    if len(tks) > 0:
        op = tks[0]
        if isinstance(op, list):
            op = evaluate(op)
        args = []
        if len(tks) > 1:
            for tk in tks[1:]:
                if isinstance(tk, list):
                    #is_unpack = False
                    #if len(tk) > 1:
                    #    if tk[0] in OP_UNPACK:
                    #        is_unpack = True
                    #        args.extend([[parse_tk(tk2) for tk2 in tk1] for tk1 in tk[1:] if isinstance(tk1, list)])
                    #if not is_unpack:
                        args.append(evaluate(tk))
                else:
                    args.append(parse_tk(tk))
            if len(args) < 1:
                res = op
            else:
                def num_op(f) -> float | str:
                    try:
                        v = args[0]
                        if len(args) > 1:
                            for arg in args[1:]:
                                v = f(v, arg)
                    except TypeError as e:
                        v = str(e)
                        print(v)
                    return v

                if op in OP_ADD:
                    res = num_op(lambda a, b: a+b)
                elif op in OP_SUB:
                    res = num_op(lambda a, b: a-b)
                elif op in OP_MUL:
                    res = num_op(lambda a, b: a*b)
                elif op in OP_DIV:
                    res = num_op(lambda a, b: a/b)
                elif op in OP_POW:
                    res = num_op(lambda a, b: a**b)
                elif op in OP_LIST:
                    res = args

    return res








def run(code: str) -> None:
    tks = tokenize(code)
    print(tks)
    
    res = evaluate(tks[0])
    print(res)


def test() -> None:
    run(
        """
    list {close enough \\_(!!)_/}
    "This is the primary default test provided in the `lithp.py` interpreter source file."
        (list a b c def ghi
        (list \"(({))}asdas232    sadhaskljh   68 6 asdas {{{  }   )6\")
    
        (list 123 { +}++ --- 009098098098     )
        (list (111)) (678969876) (sadfhjasd safdkhaskldf  (dksfhklsdjf (hlskdjfh) (a (adfhsdkfh))))
        "   divline  "
        (** (* 2 (+ 1 (/ (+ 10 (- 5 3)) {(unpack (* (list 2) 3))} 2 2 2   ))) (/ 1 2))
        (list (unpack (list 1 2 3)) 4)
        )
        """
            )


def main(args: list[str]) -> None:
    if len(args) > 1:
        if args[1] == "-t":
            test()
        elif len(args) > 2:
            if args[1] == "-f":
                try:
                    with open(args[2], 'r') as f:
                        run(f.read())
                        f.close()
                except OSError as e:
                    print(str(e))
            elif args[1] == "-e":
                run(args[2])
    else:
        test()

if __name__ == "__main__":
    from sys import argv
    main(argv)

