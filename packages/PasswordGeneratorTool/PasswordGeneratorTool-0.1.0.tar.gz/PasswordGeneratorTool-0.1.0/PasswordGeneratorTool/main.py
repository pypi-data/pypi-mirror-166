r"""

This app will create password from
lowercase from: a-z
uppercase from: A-Z
digits from: 0-9
special characters from: !@#$%^&*(){}[]\|:";'<>?,./

"""
import random as rand

min_lowercase, max_lowercase = 97, 122
min_uppercase, max_uppercase = 65, 90
min_digit, max_digit = 48, 57
special_characters = r'!@#$%^&*(){}[]\|:";<>?,./'


def greet_user_and_take_pass_length():
    print("Hello there, Welcome in your password generator!")
    user_input = int(input("""
Strong password needs to have at least 8 characters
Please provide your new password length: """))
    return user_input


def goodbye_message():
    print("\nPssst! Please remember to keep you passwords safe :)")



def generate_password(password_length):
    generated_password = ""
    while password_length > 0:
        # add lowercase
        temp_char = chr(rand.randrange(min_lowercase, max_lowercase + 1))
        generated_password += temp_char
        password_length -= 1
        if password_length < 1:
            break
        # add Uppercase
        temp_char = chr(rand.randrange(min_uppercase, max_uppercase + 1))
        generated_password += temp_char
        password_length -= 1
        if password_length < 1:
            break
        # add digits
        temp_char = chr(rand.randrange(min_digit, max_digit + 1))
        generated_password += temp_char
        password_length -= 1
        if password_length < 1:
            break
        # add special characters
        temp_char = chr(ord(rand.choice(special_characters)))
        generated_password += temp_char
        password_length -= 1
        if password_length < 1:
            break

    final_message = f"\nYour new password:\n{generated_password}"
    return final_message


def main():
    value = greet_user_and_take_pass_length()
    print(generate_password(value))
    goodbye_message()


def create_password():
    main()
