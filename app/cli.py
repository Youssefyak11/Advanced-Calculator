import shlex
from .calculator import Calculator
from .operations import list_operations

def main():  # pragma: no cover (interactive)
    calc = Calculator()
    print(calc.ok("Advanced Calculator ready. Type 'help' for commands."))

    while True:
        try:
            raw = input("calc> ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        parts = shlex.split(raw)
        if not parts:
            continue

        cmd, *args = parts
        try:
            if cmd in {"exit", "quit"}:
                print("Bye!")
                break
            elif cmd == "help":
                print(calc.help_text())
            elif cmd == "history":
                for i, c in enumerate(calc.history.list(), 1):
                    print(f"{i}. {c.operation}({c.a}, {c.b}) = {c.result} @ {c.timestamp}")
            elif cmd == "clear":
                calc.history = type(calc.history)(max_size=calc.config.max_history_size)
                print(calc.warn("History cleared."))
            elif cmd == "undo":
                calc.history.undo()
                print(calc.ok("Undone."))
            elif cmd == "redo":
                calc.history.redo()
                print(calc.ok("Redone."))
            elif cmd == "save":
                calc.save_history()
                print(calc.ok("History saved."))
            elif cmd == "load":
                calc.load_history()
                print(calc.ok("History loaded."))
            else:
                # operation commands expect two args
                if cmd not in list_operations():
                    print(calc.err(f"Unknown command: {cmd}"))
                    continue
                if len(args) != 2:
                    print(calc.err("Expected two numeric arguments."))
                    continue
                a, b = args
                res = calc.calculate(cmd, a, b)
                print(calc.ok(str(res)))
        except Exception as e:
            print(calc.err(str(e)))

if __name__ == "__main__":  # pragma: no cover
    main()
