def divider():
    print("\n" + "-" * 30)

def prompt_choice(options):
    """
    options = dict like:
    {
        "1": "Attack",
        "2": "Run"
    }
    """
    for key, value in options.items():
        print(f"{key}. {value}")

    choice = input("> ").strip()
    return choice
