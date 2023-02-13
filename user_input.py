def user_agreed(prompt: str):
    while not ((user_input:=input(prompt)) in ["y", "n"]):
        print("invalid input, try again")
    return user_input == "y"