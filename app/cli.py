import shlex
from .calculator import Calculator
from .exceptions import OperationError, HistoryError

def main():
    calc = Calculator()
    print("Calculator ready. Type 'help'.")
    while True:
        try:
            raw = input("calc> ")
        except (EOFError, KeyboardInterrupt):
            break
        parts = shlex.split(raw)
        if not parts: continue
        cmd, *args = parts
        if cmd in {"exit", "quit"}: break
        if cmd == "help":
            print("Commands: add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff, history, undo, redo, clear, exit")
        elif cmd == "history":
            for i,c in enumerate(calc.history.list(),1):
                print(f"{i}. {c.operation}({c.a},{c.b})={c.result}")
        elif cmd == "undo":
            try: calc.history.undo(); print("Undone")
            except HistoryError as e: print(e)
        elif cmd == "redo":
            try: calc.history.redo(); print("Redone")
            except HistoryError as e: print(e)
        else:
            if len(args)!=2: print("Need two numbers"); continue
            try:
                res = calc.calculate(cmd, float(args[0]), float(args[1]))
                print(res)
            except OperationError as e: print(e)

if __name__ == "__main__":
    main()
