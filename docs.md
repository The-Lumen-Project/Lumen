# Lumen

<div align="center">

<img src="https://github.com/user-attachments/assets/651302ec-c5ec-4776-ab7e-e37dba3cf6ea"
     width="700" 
/>

**A compiled, fast, and lightweight programming language**  
*Bridging Python's readability with C-style language power*

[![License](https://img.shields.io/github/license/The-Lumen-Project/Lumen?style=flat&color=FFCE50&labelColor=222222)](https://www.gnu.org/licenses/gpl-3.0)
[![Stars](https://img.shields.io/github/stars/The-Lumen-Project/Lumen?style=flat&color=FFCE50&labelColor=222222)](https://github.com/The-Lumen-Project/Lumen/stargazers)
[![Forks](https://img.shields.io/github/forks/The-Lumen-Project/Lumen?style=flat&color=FFCE50&labelColor=222222)](https://github.com/The-Lumen-Project/Lumen/forks)
[![Issues](https://img.shields.io/github/issues/The-Lumen-Project/Lumen?style=flat&color=FFCE50&labelColor=222222)](https://github.com/The-Lumen-Project/Lumen/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/The-Lumen-Project/Lumen?style=flat&color=FFCE50&labelColor=222222)](https://github.com/The-Lumen-Project/Lumen/pulls)
[![Release](https://img.shields.io/github/v/release/The-Lumen-Project/Lumen?style=flat&color=FFCE50&labelColor=222222)](https://github.com/The-Lumen-Project/Lumen/releases/)
![Build Lumen](https://github.com/The-Lumen-Project/Lumen/actions/workflows/build.yml/badge.svg?style=flat&color=FFCE50&labelColor=222222)

</div>

---

## Why Choose Lumen?

<table>
<tr>
<td width="33%" align="center">
<img src="https://img.shields.io/badge/-⚡-FF6B6B?style=for-the-badge" alt="Fast">
<h3>Lightning Fast</h3>
<p>Compiled execution for maximum performance</p>
</td>
<td width="33%" align="center">
<img src="https://img.shields.io/badge/-📖-4ECDC4?style=for-the-badge" alt="Readable">
<h3>Highly Readable</h3>
<p>Python-like syntax that's easy to understand</p>
</td>
<td width="33%" align="center">
<img src="https://img.shields.io/badge/-🎓-45B7D1?style=for-the-badge" alt="Educational">
<h3>Learning Friendly</h3>
<p>Perfect bridge to C/C++/C# concepts</p>
</td>
</tr>
</table>

---

## 🚀 Quick Start

### Your First Lumen Program

```lmn
print "Hello, Lumen!";
```

### Compile & Run

```powershell
# Compile your program
lumen hello.lmn -p -c

# Run it
.\dist\hello.exe
```

> **💡 Pro Tip:** Lumen combines the simplicity of Python with the performance of compiled languages!

---

## 📚 Language Reference

### 🔢 Variables & Data Types

Lumen provides a rich set of data types for different programming needs:

<details>
<summary><b>📋 Variable Types Overview</b></summary>

| Type | Syntax | Example | Use Case |
|------|--------|---------|----------|
| **Integer** | `int name value;` | `int x 42;` | Whole numbers |
| **String** | `str name "value";` | `str greeting "Hello!";` | Text data |
| **Boolean** | `bool name True/False;` | `bool isActive True;` | Logic flags |
| **Dynamic** | `var name value;` | `var data "flexible";` | Any type |
| **Static** | `static var name value;` | `static var PI 3.14;` | Constants |
| **Array** | `ary name[values];` | `ary nums[1,2,3];` | Collections |
| **Dictionary** | `dic name{"key":"val"};` | `dic user{"name":"Alice"};` | Key-value pairs |

</details>

### 🔧 Functions

Functions in Lumen are declared with the `fun` keyword and provide excellent code reusability:

```lmn
fun calculateArea(length, width) {
    var area length * width;
    return area;
};

fun greetUser(name, age) {
    print "Hello, ", name, "! You are ", age, " years old.";
};

// Usage
var result calculateArea(10, 5);
greetUser("Alice", 25);
```

### 🔀 Control Flow

#### Conditional Statements

```lmn
int score 85;

if (score >= 90) {
    print "Excellent! Grade A";
} else if (score >= 80) {
    print "Good job! Grade B";
} else {
    print "Keep studying!";
};
```

#### Loops

```lmn
// While loop
int counter 0;
while (counter < 5) {
    print "Count: ", counter;
    counter++;
};

// For-style iteration
int i 0;
while (i < 10) {
    if (i % 2 == 0) {
        print i, " is even";
    };
    i++;
};
```

### 🏷️ Labels and Goto

> **⚠️ Use Sparingly:** Goto statements can make code hard to follow

```lmn
int attempts 0;

retry:
attempts++;
if (attempts < 3) {
    print "Attempt ", attempts;
    // Some operation that might fail
    goto retry;
};

print "Maximum attempts reached!";
```

---

## 📦 Standard Libraries

Lumen comes with a comprehensive set of libraries for common programming tasks:

### 🔍 REGEX - Regular Expressions

<details>
<summary><b>Pattern Matching & Text Processing</b></summary>

```lmn
#include <REGEX>;

// Find first match
var match REGEX.search("\\d+", "I have 123 apples");
print match; // "123"

// Find all matches
var allMatches REGEX.findall("\\w+", "Hello world from Lumen");
print allMatches; // ["Hello", "world", "from", "Lumen"]

// Replace patterns
var result REGEX.sub("world", "Lumen", "Hello world!");
print result; // "Hello Lumen!"

// Split strings
var parts REGEX.split(",", "apple,banana,orange", -1);
print parts; // ["apple", "banana", "orange"]
```

**Available Functions:**
- `search(pattern, text)` - Find first match
- `findall(pattern, text)` - Find all matches
- `split(pattern, text, maxsplit)` - Split string by pattern
- `sub(pattern, replacement, text)` - Replace matches

</details>

### 🎲 RANDOM - Random Number Generation

<details>
<summary><b>Randomization & Probability</b></summary>

```lmn
#include <RANDOM>;

// Set seed for reproducible results
RANDOM.seed(42);

// Generate random integers
var dice RANDOM.randint(1, 6);
print "Dice roll: ", dice;

// Random floating point
var probability RANDOM.random();
print "Random chance: ", probability;

// Choose from array
ary colors["red", "green", "blue", "yellow"];
var randomColor RANDOM.choice(colors);
print "Selected color: ", randomColor;

// Shuffle array in-place
ary deck[1, 2, 3, 4, 5];
RANDOM.shuffle(deck);
print "Shuffled deck: ", deck;
```

</details>

### 💾 OS - Operating System Interface

<details>
<summary><b>File System & Directory Operations</b></summary>

```lmn
#include <OS>;

// Get current directory
var currentDir OS.pwd();
print "Current directory: ", currentDir;

// List directory contents
var files OS.ls(".", False);
print "Files in current directory: ", files;

// Create directory
OS.mkdir("new_project", 0o755);

// Change directory
OS.cd("new_project");

// Join paths safely
var filePath OS.pathjoin("documents", "readme.txt");
print "File path: ", filePath;

// Remove directory
OS.rm("old_folder", True);
```

</details>

### 📁 STDIO - Input/Output Operations

<details>
<summary><b>File Handling & User Input</b></summary>

```lmn
#include <STDIO>;

// Get user input
var name STDIO.input("Enter your name: ");
var age STDIO.inputInt("Enter your age: ");

print "Hello ", name, "! You are ", age, " years old.";

// File operations
var file STDIO.open("data.txt", "w");
STDIO.write(file, "Hello from Lumen!\n");
STDIO.write(file, "This is line 2.\n");
// File automatically closed

// Read file
var content STDIO.read("data.txt");
print "File contents:\n", content;

// Clean up
STDIO.remove("data.txt");
```

</details>

### 🧮 MATH - Mathematical Functions

<details>
<summary><b>Mathematical Operations & Constants</b></summary>

```lmn
#include <MATH>;

// Mathematical constants
print "Pi = ", MATH.pi;
print "E = ", MATH.e;

// Basic operations
var squareRoot MATH.sqrt(16);
print "Square root of 16: ", squareRoot;

var power MATH.pow(2, 8);
print "2 to the power of 8: ", power;

// Trigonometric functions
var sineValue MATH.sin(MATH.pi / 2);
print "sin(π/2) = ", sineValue;

var cosineValue MATH.cos(0);
print "cos(0) = ", cosineValue;

// Advanced functions
var fact MATH.factorial(5);
print "5! = ", fact;

var logValue MATH.log(MATH.e);
print "ln(e) = ", logValue;
```

</details>

### ℹ️ INFO - System Information

<details>
<summary><b>Runtime & Environment Details</b></summary>

```lmn
#include <INFO>;

// System information
print "Operating System: ", INFO.os();
print "CPU Architecture: ", INFO.architecture();
print "CPU Info: ", INFO.cpu();
print "Lumen Version: ", INFO.lmnver;

// Useful for debugging and system-specific code
var osName INFO.os();
if (osName == "Windows") {
    print "Running on Windows";
} else if (osName == "Linux") {
    print "Running on Linux";
} else {
    print "Running on ", osName;
};
```

</details>

### 📅 DATE - Date and Time Functions

<details>
<summary><b>Time Handling & Formatting</b></summary>

```lmn
#include <DATE>;

// Get current date and time
var now DATE.now();
print "Current time: ", now;

// Create specific datetime
var birthday DATE.datetime(1995, 12, 25);
print "Birthday: ", birthday;

// Practical example: timestamp logging
fun logMessage(message) {
    var timestamp DATE.now();
    print "[", timestamp, "] ", message;
};

logMessage("Application started");
logMessage("Processing complete");
```

</details>

---

## 💻 Complete Example Program
<details>
<summary>Here's a comprehensive example showcasing Lumen's capabilities:</summary>

```lmn
#include <STDIO>;
#include <MATH>;
#include <RANDOM>;

// Global constants
static var APP_NAME "Lumen Calculator";
static var VERSION "1.0.0";

// Data structures
dic operations{
    "add": "+";
    "subtract": "-";
    "multiply": "*";
    "divide": "/";
};

ary history[];

fun displayWelcome() {
    print "=================================";
    print "  Welcome to ", APP_NAME, " v", VERSION;
    print "=================================\n";
};

fun addToHistory(operation, result) {
    var entry operation, result;
    // history.append(entry); // Assuming array append method
    print "Added to history: ", entry;
};

fun performCalculation(a, b, operation) {
    var result 0;
    
    if (operation == "add") {
        result a + b;
    }; if (operation == "subtract") {
        result a - b;
    }; if (operation == "multiply") {
        result a * b;
    }; if (operation == "divide") {
        if (b != 0) {
            result a / b;
        }; if (b == 0) {
            print "Error: Division by zero!";
            return 0;
        };
    }; if (operation != "add" && operation != "subtract" && operation != "multiply" && operation != "divide") {
        print "Unknown operation: ", operation;
        return 0;
    };
    
    var operationStr a, operations[operation], b, "=";
    addToHistory(operationStr, result);
    return result;
};

fun generateRandomProblem() {
    var a random.randint(1, 100);
    var b random.randint(1, 100);
    var ops["add", "subtract", "multiply"];
    var randomOp random.choice(ops);
    
    print "\nRandom problem: ";
    var result performCalculation(a, b, randomOp);
    print "Result: ", result, "\n";
};

fun main() {
    displayWelcome();
    
    // Interactive calculation
    var num1 stdio.inputInt("Enter first number: ");
    var num2 stdio.inputInt("Enter second number: ");
    
    print "\nAvailable operations:";
    print "1. add";
    print "2. subtract"; 
    print "3. multiply";
    print "4. divide";
    
    var oper "\0";
    var op stdio.input("Choose operation: ");

    if (op == "1") {
        oper "add";
    };
    if (op == "2") {
        oper "subtract";
    };
    if (op == "3") {
        oper "multiply";
    };
    if (op == "4") {
        oper "divide";
    };
    var result performCalculation(num1, num2, oper);
    
    print "\nFinal result: ", result;
    
    // Show some math constants
    print "\nMath constants:";
    print "π = ", math.pi;
    print "√", result, " = ", math.sqrt(result);
    
    // Generate a random problem
    generateRandomProblem();
    
    print "\nThank you for using", APP_NAME, "!";
};

// Start the program
main();
```
</details>
---

## 📖 Code Style Guide

### 🎨 Naming Conventions

- **Variables**: Use `camelCase` - `userName`, `totalCount`
- **Functions**: Use `camelCase` - `calculateTotal()`, `displayMenu()`
- **Constants**: Use `UPPER_SNAKE_CASE` - `MAX_SIZE`, `DEFAULT_VALUE`
- **Files**: Use `snake_case` - `user_manager.lmn`, `math_utils.lmn`

### 📝 Best Practices

```lmn
// ✅ Good: Clear, descriptive names
int userAge 25;
str firstName "Alice";
bool isLoggedIn True;

// ❌ Avoid: Unclear abbreviations
int uA 25;
str fN "Alice";
bool lI True;

// ✅ Good: Consistent formatting
fun calculateTotalPrice(basePrice, taxRate) {
    var tax basePrice * taxRate;
    var total basePrice + tax;
    return total;
};

// ✅ Good: Meaningful comments
// Calculate compound interest over time
fun compoundInterest(principal, rate, time) {
    return principal * MATH.pow(1 + rate, time);
};
```

---

## 🛠️ Development Setup

### Prerequisites

- Python with PyInstaller
- Lumen compiler
- Git (for version control)

### Building from Source

```bash
# Clone the repository
git clone https://github.com/The-Lumen-Project/Lumen.git
cd Lumen

# Build the compiler
python3 compile.py

# Verify installation
.\dist\lumen.exe
```

### IDE Support

- **VS Code**: Lumen syntax highlighting extension available

---

## 🤝 Contributing

We welcome contributions to make Lumen even better! Here's how you can help:

### 🐛 Reporting Issues

1. Check existing issues first
2. Provide minimal reproduction code
3. Include system information
4. Describe expected vs actual behavior

### 💡 Feature Requests

1. Open a discussion first for major features
2. Explain the use case and benefits
3. Consider backward compatibility
4. Provide implementation ideas if possible

### 🔧 Pull Requests

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Update documentation
5. Submit PR with clear description

---

## 📚 Additional Resources

<div align="center">

| Resource | Description | Link |
|----------|-------------|------|
| 📖 **Tutorial** | Step-by-step learning guide | [Learn Lumen](https://github.com/The-Lumen-Project/blob/main/Lumen/learn.md) |
| 🐛 **Issues** | Report bugs & request features | [GitHub Issues](https://github.com/The-Lumen-Project/Lumen/issues) |
| 📋 **Changelog** | Version history & updates | [Releases](https://github.com/The-Lumen-Project/Lumen/blob/main/CHANGELOG.md) |

</div>

---

## 📄 License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with 💜 by the Lumen Community**

*Star ⭐ this repository if you find Lumen useful!*

[⬆️ Back to Top](#Lumen)

</div>
