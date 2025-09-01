# Static constants (immutable)
MAX = 100

# Global variables
global_var = None

counter = 0
message = "Hello"

def test(counter):
    global global_var
    global_var = 42
    counter += 1

test(counter)
print(counter)
print(global_var)
print(MAX)