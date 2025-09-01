# Static constants (immutable)
stuckThing = "Hello"

number = 0
thing = True
stringThing = "This is a string!"
dynamicVar = "WOW!"
arrayThing = ["Index 0", "Index 1", "Index 2"]
dictThing = {"key1": "content1", "key2": "content2"}
def program(condition, num):
    if condition:
        print("Condtion is True!")
        while (num != 100):
            print("The number is ", num)
            num += 1

program(thing, number)
print(dictThing["key1"])
print(arrayThing[1])
