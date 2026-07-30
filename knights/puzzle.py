from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

ASaidKnight = Symbol("A said 'I am a knight'")
ASaidKnave = Symbol("A said 'I am a knave'")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is either a knight or a knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # A says: "I am both a knight and a knave."
    Biconditional(
        AKnight,
        And(AKnight, AKnave)
    )
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A is either a knight or a knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # B is either a knight or a knave
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # A says: "We are both knaves."
    Biconditional(
        AKnight,
        And(AKnave, BKnave)
    )
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(

    # A is either a knight or a knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # B is either a knight or a knave
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # A says: "We are the same kind."
    Biconditional(
        AKnight,
        Or(
            And(AKnight, BKnight),
            And(AKnave, BKnave)
        )
    ),

    # B says: "We are of different kinds."
    Biconditional(
        BKnight,
        Or(
            And(AKnight, BKnave),
            And(AKnave, BKnight)
        )
    )
)


knowledge3 = And(

    # Everyone is either a knight or a knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # A said exactly one sentence
    Or(ASaidKnight, ASaidKnave),
    Not(And(ASaidKnight, ASaidKnave)),

    # If A said "I am a knight"
    Implication(
        ASaidKnight,
        Biconditional(AKnight, AKnight)
    ),

    # If A said "I am a knave"
    Implication(
        ASaidKnave,
        Biconditional(AKnight, AKnave)
    ),

    # B: "A said 'I am a knave'"
    Biconditional(
        BKnight,
        ASaidKnave
    ),

    # B: "C is a knave"
    Biconditional(
        BKnight,
        CKnave
    ),

    # C: "A is a knight"
    Biconditional(
        CKnight,
        AKnight
    )
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
