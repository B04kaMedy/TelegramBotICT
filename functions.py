def log(message: str) -> None:
    print(message)

def get_answer() -> bool:
    answer = input()

    if answer == 'Y':
        return True
    else:
        return False

