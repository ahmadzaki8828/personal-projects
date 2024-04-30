# Helper function
def helper(arg, digit1, digit2):
    match arg:
        case  "+":
            return "{x} + {y} = {z}".format(x=digit1, y=digit2, z=digit1 + digit2)
        case  "-":
            return "{x} - {y} = {z}".format(x=digit1, y=digit2, z=digit1 - digit2)
        case  "*":
            return "{x} * {y} = {z}".format(x=digit1, y=digit2, z=digit1 * digit2)
        case  "/":
            return "{x} / {y} = {z}".format(x=digit1, y=digit2, z=digit1 / digit2)
# Question Prompt
print("What do you want to do Add,Subtract,Multiply,Divide")
# inputs
arg = input("Type  + | - | * | /: ")
digit1 = int(input("Digit1: "))
digit2 = int(input("Digit2: "))
# output
output = helper(arg, digit1, digit2)
print(output)