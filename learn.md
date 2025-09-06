# 🎓 Learn Lumen: Complete Step-by-Step Tutorial

<div align="center">

![Lumen Tutorial](https://img.shields.io/badge/Lumen-Tutorial-blueviolet?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJMMTMuMDkgOC4yNkwyMCA5TDEzLjA5IDE1Ljc0TDEyIDIyTDEwLjkxIDE1Ljc0TDQgOUwxMC45MSA4LjI2TDEyIDJaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K)

**Master Lumen Programming from Zero to Hero**  
*A complete, hands-on tutorial series*

[![Beginner Friendly](https://img.shields.io/badge/Level-Beginner%20Friendly-green?style=flat)](README.md)
[![Interactive](https://img.shields.io/badge/Type-Interactive-blue?style=flat)](README.md)
[![Practical](https://img.shields.io/badge/Focus-Hands%20On-orange?style=flat)](README.md)

</div>

---

## 🗺️ Learning Path Overview

<table>
<tr>
<td width="20%" align="center">
<img src="https://img.shields.io/badge/-🚀-FF6B6B?style=for-the-badge" alt="Basics">
<h4>Chapter 1-3</h4>
<p><b>Fundamentals</b><br>Setup, syntax, variables</p>
</td>
<td width="20%" align="center">
<img src="https://img.shields.io/badge/-🔧-4ECDC4?style=for-the-badge" alt="Functions">
<h4>Chapter 4-6</h4>
<p><b>Building Blocks</b><br>Functions, control flow</p>
</td>
<td width="20%" align="center">
<img src="https://img.shields.io/badge/-📚-45B7D1?style=for-the-badge" alt="Data">
<h4>Chapter 7-9</h4>
<p><b>Data Structures</b><br>Arrays, dictionaries</p>
</td>
<td width="20%" align="center">
<img src="https://img.shields.io/badge/-⚡-96CEB4?style=for-the-badge" alt="Advanced">
<h4>Chapter 10-12</h4>
<p><b>Libraries</b><br>Built-in functionality</p>
</td>
<td width="20%" align="center">
<img src="https://img.shields.io/badge/-🏆-FFEAA7?style=for-the-badge" alt="Projects">
<h4>Chapter 13-15</h4>
<p><b>Real Projects</b><br>Complete applications</p>
</td>
</tr>
</table>

---

# Chapter 1: Getting Started 🚀

## 1.1 Your Very First Program

Let's start with the traditional "Hello, World!" program:

```lmn
print "Hello, World!";
```

**What's happening here?**
- `print` - Built-in function to display text
- `"Hello, World!"` - A string (text) in double quotes
- `;` - Semicolon ends the statement

### 💻 Try It Yourself

1. Create a file called `hello.lmn`
2. Type the code above
3. Compile and run:
   ```bash
   lumen hello.lmn -d -p -c
   .\dist\hello.exe
   ```

**Expected Output:**
```
Hello, World!
```

## 1.2 Understanding Compilation

Unlike Python or JavaScript, Lumen is **compiled**:

```bash
# Source code (.lmn) → Parser → Python → PyInstaller → Executable
hello.lmn → hello.py → hello (executable)
```
> **💡 Pro Tip:** If you have Python installed you can test your code before compiling!
> 
**Benefits:**
- ✅ Faster execution
- ✅ Early error detection


### 📝 Exercise 1.1
Create a program that prints your name and favorite hobby:

<details>
<summary><b>💡 Solution</b></summary>

```lmn
print "My name is Alice";
print "I love programming!";
```
</details>

---

# Chapter 2: Variables and Data Types 📊

## 2.1 Your First Variables

Variables store data that can change during program execution:

```lmn
int age 25;
str name "Alice";
bool isStudent True;

print "Name: ", name;
print "Age: ", age;
print "Is student: ", isStudent;
```

**Key Points:**
- `int` - Whole numbers
- `str` - Text (strings)
- `bool` - True/False values
- Variables must be declared with a type

## 2.2 All Variable Types

### Basic Types

```lmn
// Numbers
int wholeNumber 42;
int negativeNumber -10;

// Text
str greeting "Hello!";
str emptyString "";

// Logic
bool isTrue True;
bool isFalse False;
```

### Special Types

```lmn
// Dynamic - can hold any type
var flexible 100;
flexible "Now I'm text!";
flexible True;

// Static - cannot be changed
static var PI 3.14159;
static var APP_NAME "My App";

// Basic types - can only be their type
// Numbers
int wholeNumber 42;
int negativeNumber -10;

// Text
str greeting "Hello!";
str emptyString "";

// Logic
bool isTrue True;
bool isFalse False;
```

### 📝 Exercise 2.1
Create variables for a character in a video game:

<details>
<summary><b>💡 Solution</b></summary>

```lmn
str characterName "DragonSlayer";
int level 15;
int health 100;
int mana 50;
bool hasShield True;
static var MAX_LEVEL 100;

print "Character: ", characterName;
print "Level: ", level, "/", MAX_LEVEL;
print "Health: ", health;
print "Mana: ", mana;
print "Has shield: ", hasShield;
```
</details>

## 2.3 Working with Variables

```lmn
int score 0;
str playerName "Alex";

// Update variables
score 100;
score score + 50;  // score is now 150

// String operations
playerName playerName + " the Great";

print "Final score: ", score;
print "Player: ", playerName;
```

### 📝 Exercise 2.2
Create a simple counter that starts at 0, adds 5, then doubles:

<details>
<summary><b>💡 Solution</b></summary>

```lmn
int counter 0;
print "Starting counter: ", counter;

counter counter + 5;
print "After adding 5: ", counter;

counter counter * 2;
print "After doubling: ", counter;
```
</details>

---

# Chapter 3: Printing and Basic Output 🖨️

## 3.1 Different Ways to Print

```lmn
// Simple text
print "Hello!";

// Multiple values
print "Name:", "Alice", "Age:", 25;

// Variables
str name "Bob";
int score 95;
print name, "scored", score, "points";
```

## 3.2 Formatting Output

```lmn
str product "Laptop";
int price 899;
bool inStock True;

print "Product: ", product;
print "Price: $", price;
print "Available: ", inStock;
print "-------------------";
print product, "costs $", price, " (Available: ", inStock, ")";
```

### 📝 Exercise 3.1
Create a program that displays a restaurant menu item:

<details>
<summary><b>💡 Solution</b></summary>

```lmn
str itemName "Margherita Pizza";
int price 12;
bool isVegetarian True;
str description "Fresh tomatoes, mozzarella, and basil";

print "=== MENU ITEM ===";
print "Item: ", itemName;
print "Price: $", price;
print "Vegetarian: ", isVegetarian;
print "Description: ", description;
print "================";
```
</details>

---

# Chapter 4: Functions - Your First Building Blocks 🔧

## 4.1 Creating Simple Functions

Functions let you reuse code and organize your program:

```lmn
// Define a function
fun greet() {
    print "Hello from my function!";
};

// Use the function
greet();
greet();  // Can call it multiple times
```

## 4.2 Functions with Parameters

```lmn
fun greetPerson(name) {
    print "Hello, ", name, "!";
};

fun addNumbers(a, b) {
    var result a + b;
    print a, " + ", b, " = ", result;
};

// Using the functions
greetPerson("Alice");
greetPerson("Bob");
addNumbers(5, 3);
addNumbers(10, 25);
```

## 4.3 Functions with Return Values

```lmn
fun calculateArea(length, width) {
    var area length * width;
    return area;
};

fun getFullName(first, last) {
    var fullName first + " " + last;
    return fullName;
};

// Using return values
var roomArea calculateArea(10, 12);
print "Room area: ", roomArea, " square meters";

var playerName getFullName("John", "Smith");
print "Player: ", playerName;
```

### 📝 Exercise 4.1
Create a function that calculates and returns the price with tax:

<details>
<summary><b>💡 Solution</b></summary>

```lmn
fun calculateTotal(price, taxRate) {
    var tax price * taxRate;
    var total price + tax;
    return total;
};

var itemPrice 50;
var tax 0.08;  // 8% tax
var finalPrice calculateTotal(itemPrice, tax);

print "Item price: $", itemPrice;
print "Tax rate: ", tax * 100, "%";
print "Final price: $", finalPrice;
```
</details>

## 4.4 Real-World Function Example

```lmn
// BMI Calculator
fun calculateBMI(weight, height) {
    var bmi weight / (height * height);
    return bmi;
};

fun getBMICategory(bmi) {
    if (bmi < 18.5) {
        return "Underweight";
    }; if (bmi < 25) {
        return "Normal weight";
    }; if (bmi < 30) {
        return "Overweight";
    }; if (bmi > 30 {
        return "Obese";
    };
};

// Using the functions
var myWeight 70;     // kg
var myHeight 1.75;   // meters
var myBMI calculateBMI(myWeight, myHeight);
var category getBMICategory(myBMI);

print "Weight: ", myWeight, " kg";
print "Height: ", myHeight, " m";
print "BMI: ", myBMI;
print "Category: ", category;
```

---

# Chapter 5: Making Decisions with If Statements 🤔

## 5.1 Basic If Statements

```lmn
int temperature 25;

if (temperature > 30) {
    print "It's hot outside!";
};

if (temperature < 10) {
    print "It's cold outside!";
};

if (temperature >= 15) {
    print "Nice weather for a walk!";
};
```


### 📝 Exercise 5.1
Create a simple password strength checker:

<details>
<summary><b>💡 Solution</b></summary>

```lmn
str password "mypass123";
var length 9;  // Assume we calculated the length

if (length >= 12) {
    print "Password strength: Very Strong";
}; if (length >= 8) {
    print "Password strength: Strong";
}; if (length >= 6) {
    print "Password strength: Weak";
}; if (length < 6) {
    print "Password strength: Very Weak";
};

print "Password length: ", length, " characters";
```
</details>

## 5.2 Complex Conditions

```lmn
int hour 14;
bool isWeekend False;
bool hasWork True;

if (hour >= 9 && hour <= 17 && !isWeekend && hasWork) {
    print "Time to work!";
};
if (isWeekend || hour < 9 || hour > 17) {
    print "Free time!";
};
```

**Logical Operators:**
- `&&` - AND (both must be true)
- `||` - OR (at least one must be true)
- `!` - NOT (flips true/false)

---

# Chapter 6: Loops - Repeating Actions 🔄

## 6.1 While Loops

While loops repeat code as long as a condition is true:

```lmn
int counter 1;

while (counter <= 5) {
    print "Count: ", counter;
    counter counter + 1;
};

print "Done counting!";
```

## 6.2 Practical While Loop Examples

### Countdown Timer
```lmn
int countdown 10;

print "Rocket launch countdown:";
while (countdown > 0) {
    print countdown, "...";
    countdown--; // variableName-- or variableName++ decrements and increments by 1
};
print "BLAST OFF! 🚀";
```

### Number Guessing Game Logic
```lmn
int secretNumber 7;
int guess 1;
int attempts 0;

while (guess != secretNumber) {
    attempts attempts + 1;
    print "Attempt ", attempts, ": Guess is ", guess;
    
    if (guess < secretNumber) {
        print "Too low!";
    };
    if (guess > secretNumber) {
        print "Too high!";
    };
    
    guess++;  // In real game, this would be user input
};

print "Congratulations! You found it in ", attempts, " attempts!";
```

### 📝 Exercise 6.1
Create a program that calculates the sum of numbers from 1 to 10:

<details>
<summary><b>💡 Solution</b></summary>

```lmn
int number 1;
int sum 0;

while (number <= 10) {
    sum += number; // += is the same as varName = varName + 
    print "Adding ", number, ", sum is now: ", sum;
    number number + 1;
};

print "Final sum of 1 to 10: ", sum;
```
</details>

## 6.3 Loop Control and Patterns

### Even Numbers
```lmn
int i 2;
print "Even numbers from 2 to 20:";

while (i <= 20) {
    print i;
    i i + 2;  // Skip odd numbers
};
```

### Multiplication Table
```lmn
int number 7;
int multiplier 1;

print "Multiplication table for ", number, ":";
while (multiplier <= 10) {
    var result number * multiplier;
    print number, " x ", multiplier, " = ", result;
    multiplier multiplier + 1;
};
```

---

# Chapter 7: Arrays - Managing Lists of Data 📝

## 7.1 Creating and Using Arrays

Arrays store multiple values in order:

```lmn
// Create arrays
ary numbers[1, 2, 3, 4, 5];
ary fruits["apple", "banana", "orange"];
ary mixed[42, "hello", True];

// Access elements (starts at 0)
print "First number: ", numbers[0];
print "Second fruit: ", fruits[1];
print "Third mixed item: ", mixed[2];
```

## 7.2 Working with Arrays

```lmn
ary scores[85, 92, 78, 96, 88];

// Access and modify
print "Original first score: ", scores[0];
scores[0] 90;  // Change first score
print "Updated first score: ", scores[0];

// Display all scores
print "All scores:";
var i 0;
while (i < 5) {  // We know there are 5 elements
    print "Score ", i + 1, ": ", scores[i];
    i i + 1;
};
```

## 7.3 Array Operations

```lmn
ary inventory["sword", "shield", "potion"];

print "Current inventory:";
var index 0;
while (index < 3) {
    print "Item ", index + 1, ": ", inventory[index];
    index index + 1;
};

// Simulate adding item (by changing existing slot)
inventory[2] "magic potion";
print "Updated item 3: ", inventory[2];
```

### 📝 Exercise 7.1
Create a grade book that stores 5 student grades and calculates the average:

<details>
<summary><b>💡 Solution</b></summary>

```lmn
ary grades[88, 92, 76, 94, 85];
var total 0;
var count 0;

print "Student Grades:";
while (count < 5) {
    print "Student ", count + 1, ": ", grades[count];
    total total + grades[count];
    count count + 1;
};

var average total / 5;
print "Class average: ", average;

if (average >= 90) {
    print "Excellent class performance!";
};
if (average >= 80) {
    print "Good class performance!";
}
if (average >= 70) {
    print "Class needs improvement.";
};
```
</details>

## 7.4 Advanced Array Example

```lmn
// Shopping cart simulation
ary items["laptop", "mouse", "keyboard"];
ary prices[899, 25, 75];

print "=== SHOPPING CART ===";
var i 0;
var total 0;

while (i < 3) {
    print items[i], " - $", prices[i];
    total total + prices[i];
    i i + 1;
};

print "====================";
print "Subtotal: $", total;

var tax total * 0.08;
var finalTotal total + tax;

print "Tax (8%): $", tax;
print "Total: $", finalTotal;
```

---

# Chapter 8: Dictionaries - Key-Value Data Storage 🗂️

## 8.1 Creating and Using Dictionaries

Dictionaries store data with keys (labels) instead of numbers:

```lmn
dic person{
    "name": "Alice";
    "age": 25;
    "city": "New York";
};

print "Name: ", person["name"];
print "Age: ", person["age"];
print "City: ", person["city"];
```

## 8.2 Dictionary Operations

```lmn
dic gameStats{
    "level": 5;
    "health": 100;
    "score": 1250;
    "hasKey": True;
};

print "=== PLAYER STATUS ===";
print "Level: ", gameStats["level"];
print "Health: ", gameStats["health"], "/100";
print "Score: ", gameStats["score"];
print "Has key: ", gameStats["hasKey"];

// Update values
gameStats["health"] 85;
gameStats["score"] gameStats["score"] + 100;

print "\n=== AFTER BATTLE ===";
print "Health: ", gameStats["health"], "/100";
print "Score: ", gameStats["score"];
```

### 📝 Exercise 8.1
Create a simple inventory system for a game:

<details>
<summary><b>💡 Solution</b></summary>

```lmn
dic inventory{
    "coins": 150;
    "healthPotions": 3;
    "arrows": 25;
    "keys": 2;
};

print "=== INVENTORY ===";
print "Coins: ", inventory["coins"];
print "Health Potions: ", inventory["healthPotions"];
print "Arrows: ", inventory["arrows"];
print "Keys: ", inventory["keys"];

// Use some items
print "\nUsing 1 health potion...";
inventory["healthPotions"] inventory["healthPotions"] - 1;

print "Spending 50 coins...";
inventory["coins"] inventory["coins"] - 50;

print "\n=== UPDATED INVENTORY ===";
print "Coins: ", inventory["coins"];
print "Health Potions: ", inventory["healthPotions"];
print "Arrows: ", inventory["arrows"];
print "Keys: ", inventory["keys"];
```
</details>

## 8.3 Real-World Dictionary Example

```lmn
// Restaurant menu system
dic menuItem{
    "name": "Cheeseburger";
    "price": 12;
    "calories": 650;
    "isVegetarian": False;
    "ingredients": "beef, cheese, lettuce, tomato";
};

fun displayMenuItem(item) {
    print "=== MENU ITEM ===";
    print "Name: ", item["name"];
    print "Price: $", item["price"];
    print "Calories: ", item["calories"];
    print "Vegetarian: ", item["isVegetarian"];
    print "Ingredients: ", item["ingredients"];
    print "================";
};

displayMenuItem(menuItem);

// Calculate tax and total
var tax menuItem["price"] * 0.08;
var total menuItem["price"] + tax;
print "Tax: $", tax;
print "Total: $", total;
```

---

# Chapter 9: Combining Arrays and Dictionaries 🔗

## 9.1 Arrays of Dictionaries

```lmn
// Student database
dic student1{
    "name": "Alice";
    "age": 20;
    "grade": 95;
};

dic student2{
    "name": "Bob";
    "age": 19;
    "grade": 87;
};

dic student3{
    "name": "Charlie";
    "age": 21;
    "grade": 92;
};

// Note: This is a simplified example since Lumen arrays are declared with values
ary students[student1, student2, student3];

print "=== CLASS ROSTER ===";
var i 0;
while (i < 3) {
    var student students[i];
    print "Student ", i + 1, ": ", student["name"], " (Age: ", student["age"], ", Grade: ", student["grade"], ")";
    i i + 1;
};
```

### 📝 Exercise 9.1
Create a product catalog with multiple items:

<details>
<summary><b>💡 Solution</b></summary>

```lmn
dic product1{
    "name": "Laptop";
    "price": 899;
    "inStock": True;
    "category": "Electronics";
};

dic product2{
    "name": "Coffee Mug";
    "price": 12;
    "inStock": True;
    "category": "Kitchen";
};

dic product3{
    "name": "Running Shoes";
    "price": 89;
    "inStock": False;
    "category": "Sports";
};

ary catalog[product1, product2, product3];

print "=== PRODUCT CATALOG ===";
var index 0;
var totalValue 0;

while (index < 3) {
    var item catalog[index];
    print "\nProduct ", index + 1, ":";
    print "  Name: ", item["name"];
    print "  Price: $", item["price"];
    print "  In Stock: ", item["inStock"];
    print "  Category: ", item["category"];
    
    if (item["inStock"]) {
        totalValue totalValue + item["price"];
    };
    
    index index + 1;
};

print "\nTotal value of in-stock items: $", totalValue;
```
</details>

---

# Chapter 10: Introduction to Libraries 📚

## 10.1 What Are Libraries?

Libraries are collections of pre-written functions that extend Lumen's capabilities:

```lmn
// Import a library (ALL CAPS for import)
#include <STDIO>;

// Use library functions (lowercase after import)
var name stdio.input("What's your name? ");
print "Hello, ", name, "!";
```

**Key Points:**
- Import with `#include <LIBRARY_NAME>;` (ALL CAPS)
- Use with `library_name.function()` (lowercase)
- Libraries save you from writing complex code yourself

## 10.2 Your First Library: STDIO

STDIO handles input and output operations:

```lmn
#include <STDIO>;

print "=== PERSONAL INFO ===";
var name stdio.input("Enter your name: ");
var age stdio.inputInt("Enter your age: ");

print "Nice to meet you, ", name, "!";
print "You are ", age, " years old.";

if (age >= 18) {
    print "You're an adult!";
}
if (age < 18) {
    var yearsLeft 18 - age;
    print "You'll be an adult in ", yearsLeft, " years.";
};
```

### 📝 Exercise 10.1
Create an interactive calculator:

<details>
<summary><b>💡 Solution</b></summary>

```lmn
#include <STDIO>;

print "=== SIMPLE CALCULATOR ===";
var num1 stdio.inputInt("Enter first number: ");
var num2 stdio.inputInt("Enter second number: ");

var sum num1 + num2;
var difference num1 - num2;
var product num1 * num2;

print "\nResults:";
print num1, " + ", num2, " = ", sum;
print num1, " - ", num2, " = ", difference;
print num1, " * ", num2, " = ", product;

if (num2 != 0) {
    var quotient num1 / num2;
    print num1, " / ", num2, " = ", quotient;
}
if (num2 == 0) {
    print "Cannot divide by zero!";
};
```
</details>

---

# Chapter 11: Math and Random Libraries 🎲

## 11.1 MATH Library

The MATH library provides mathematical functions and constants:

```lmn
#include <MATH>;

print "=== MATHEMATICAL CONSTANTS ===";
print "Pi: ", math.pi;
print "E: ", math.e;

print "\n=== MATHEMATICAL FUNCTIONS ===";
var number 16;
print "Square root of ", number, ": ", math.sqrt(number);
print "2 to the power of 8: ", math.pow(2, 8);
print "Factorial of 5: ", math.factorial(5);

// Trigonometry
print "\n=== TRIGONOMETRY ===";
print "sin(π/2): ", math.sin(math.pi / 2);
print "cos(0): ", math.cos(0);
```

## 11.2 RANDOM Library

Generate random numbers and make random choices:

```lmn
#include <RANDOM>;

// Set seed for reproducible results
random.seed(42);

print "=== RANDOM NUMBERS ===";
print "Random integer 1-10: ", random.randint(1, 10);
print "Random integer 1-100: ", random.randint(1, 100);
print "Random float 0-1: ", random.random();

// Random choices
ary colors["red", "green", "blue", "yellow", "purple"];
var randomColor random.choice(colors);
print "Random color: ", randomColor;
```

### 📝 Exercise 11.1
Create a dice rolling simulator:

<details>
<summary><b>💡 Solution</b></summary>

```lmn
#include <RANDOM>;
#include <STDIO>;

print "=== DICE ROLLER ===";

fun rollDice(sides) {
    return random.randint(1, sides);
};

var keepRolling True;
while (keepRolling) {
    var dice1 rollDice(6);
    var dice2 rollDice(6);
    var total dice1 + dice2;
    
    print "\nDice 1: ", dice1;
    print "Dice 2: ", dice2;
    print "Total: ", total;
    
    if (total == 7) {
        print "Lucky seven! 🍀";
    };
    if (total == 12) {
        print "Boxcars! 🎲🎲";
    };
    if (total == 2) {
        print "Snake eyes! 🐍";
    };
    
    var response stdio.input("Roll again? (yes/no): ");
    if (response != "yes") {
        keepRolling False;
    };
};

print "Thanks for playing!";
```
</details>

## 11.3 Advanced Math Example

```lmn
#include <MATH>;
#include <STDIO>;

fun calculateCircleArea(radius) {
    return math.pi * math.pow(radius, 2);
};

fun calculateCircleCircumference(radius) {
    return 2 * math.pi * radius;
};

print "=== CIRCLE CALCULATOR ===";
var radius stdio.inputInt("Enter the radius: ");

var area calculateCircleArea(radius);
var circumference calculateCircleCircumference(radius);

print "\nResults for circle with radius ", radius, ":";
print "Area: ", area;
print "Circumference: ", circumference;
print "Diameter: ", radius * 2;
```

---

# Chapter 12: File Operations and System Libraries 💾

## 12.1 Working with Files (STDIO)

```lmn
#include <STDIO>;

// Writing to a file
print "Creating a file...";
var file stdio.open("diary.txt", "w");
stdio.write(file, "Day 1: Started learning Lumen!\n");
stdio.write(file, "It's really fun and easy to understand.\n");
stdio.write(file, "Tomorrow I'll learn about libraries.\n");
// File automatically closes

// Reading from a file
print "Reading the file back...";
var content stdio.read("diary.txt");
print "File contents:";
print content;

// Clean up
stdio.remove("diary.txt");
print "File deleted.";
```

## 12.2 OS Library - System Operations

```lmn
#include <OS>;

print "=== SYSTEM INFORMATION ===";
var currentDir os.pwd();
print "Current directory: ", currentDir;

print "\nFiles in current directory:";
var files os.ls(".", False);
print files;

// Create a directory
os.mkdir("test_folder", 0o755);
print "\nCreated 'test_folder' directory";

// Change to the directory
os.cd("test_folder");
print "Changed to test_folder";
print "New location: ", os.pwd();

// Go back
os.cd("..");
print "Back to: ", os.pwd();

// Remove the directory
os.rm("test_folder", True);
print "Removed test_folder";
```

## 12.3 INFO Library - System Details

```lmn
#include <INFO>;

print "=== SYSTEM INFORMATION ===";
print "Operating System: ", info.os();
print "CPU Architecture: ", info.architecture();
print "CPU Details: ", info.cpu();
print "Lumen Version: ", info.lmnver;

// Conditional code based on OS
var osName info.os();
if (osName == "Windows") {
    print "Running on Windows - using backslashes for paths";
};
if (osName == "Linux") {
    print "Running on Linux - using forward slashes for paths";
};
if (osName != "Windows" && osName != "Linux") {
    print "Running on ", osName;
};
```

### 📝 Exercise 12.1
Create a system information logger:

<details>
<summary><b>💡 Solution</b></summary>

```lmn
#include <STDIO>;
#include <INFO>;
#include <DATE>;

print "=== SYSTEM INFO LOGGER ===";

var timestamp date.now();
var osName info.os();
var architecture info.architecture();
var lumenVersion info.lmnver;

// Create log entry
var logEntry "=== SYSTEM LOG ===\n";
logEntry logEntry + "Timestamp: " + timestamp + "\n";
logEntry logEntry + "OS: " + osName + "\n";
logEntry logEntry + "Architecture: " + architecture + "\n";
logEntry logEntry + "Lumen Version: " + lumenVersion + "\n";
logEntry logEntry + "==================\n";

// Write to file
var logFile stdio.open("system_log.txt", "w");
stdio.write(logFile, logEntry);

print "System information logged to system_log.txt";
print "\nLog contents:";
var content stdio.read("system_log.txt");
print content;

// Clean up
stdio.remove("system_log.txt");
```
</details>

---

# Chapter 13: Project 1 - Personal Task Manager 📋

Let's build a complete application using everything we've learned!

## 13.1 Project Planning

**Features:**
- Add tasks
- View all tasks
- Mark tasks as complete
- Save tasks to file
- Load tasks from file

## 13.2 Core Implementation

```lmn
#include <STDIO>;
#include <DATE>;

// Task structure using dictionaries
dic createTask(description, isComplete) {
    dic task{
        "description": description;
        "isComplete": isComplete;
        "isntComplete": isntComplete;
        "createdAt": date.now();
    };
    return task;
};

// Global task storage (simplified - in real app you'd use dynamic arrays)
ary tasks[0, 0, 0, 0, 0];  // Max 5 tasks for this example
var taskCount 0;

fun addTask(description) {
    if (taskCount < 5) {
        var newTask createTask(description, False);
        tasks[taskCount] newTask;
        taskCount taskCount + 1;
        print "Task added successfully!";
    }; if (taskCount >= 5) {
        print "Task list is full (max 5 tasks)";
    };
};

fun displayTasks() {
    if (taskCount == 0) {
        print "No tasks yet. Add some tasks!";
        return;
    };
    
    print "\n=== YOUR TASKS ===";
    var i 0;
    while (i < taskCount) {
        var task tasks[i];
        var status "[ ]";
        if (task["isComplete"]) {
            status "[✓]";
        };
        
        print i + 1, ". ", status, " ", task["description"];
        print "   Created: ", task["createdAt"];
        i i + 1;
    };
    print "==================";
};

fun completeTask(taskIndex) {
    if (taskIndex >= 1 && taskIndex <= taskCount) {
        var task tasks[taskIndex - 1];
        task["isComplete"] True;
        tasks[taskIndex - 1] task;
        print "Task ", taskIndex, " marked as complete!";
    }; if (taskIndex < 1 || taskIndex > taskCount) {
        print "Invalid task number!";
    };
};

// Main program loop
fun runTaskManager() {
    print "=== PERSONAL TASK MANAGER ===";
    print "Commands: add, list, complete, quit";
    
    var running True;
    while (running) {
        print "\nWhat would you like to do?";
        var command stdio.input("Enter command: ");
        
        if (command == "add") {
            var description stdio.input("Enter task description: ");
            addTask(description);
        }; if (command == "list") {
            displayTasks();
        }; if (command == "complete") {
            displayTasks();
            if (taskCount > 0) {
                var taskNum stdio.inputInt("Enter task number to complete: ");
                completeTask(taskNum);
            };
        }; if (command == "quit") {
            print "Goodbye!";
            running False;
        } if (command != "quit" || command != "list" || command != "add") {
            print "Unknown command. Try: add, list, complete, quit";
        };
    };
};

// Start the application
runTaskManager();
```

### 📝 Exercise 13.1
Extend the task manager to count completed vs incomplete tasks:

<details>
<summary><b>💡 Solution</b></summary>

```lmn
fun getTaskStats() {
    var completed 0;
    var incomplete 0;
    var i 0;
    
    while (i < taskCount) {
        var task tasks[i];
        if (task["isComplete"]) {
            completed completed + 1;
        } if (task["isntComplete"]) {
            incomplete incomplete + 1;
        };
        i i + 1;
    };
    
    print "\n=== TASK STATISTICS ===";
    print "Total tasks: ", taskCount;
    print "Completed: ", completed;
    print "Incomplete: ", incomplete;
    
    if (taskCount > 0) {
        var percentage (completed * 100) / taskCount;
        print "Completion rate: ", percentage, "%";
    };
    print "========================";
};

// Add this to your main loop as a new command:
// } if (command == "stats") {
//     getTaskStats();
```
</details>

---

# Chapter 14: Project 2 - Number Guessing Game 🎮

## 14.1 Game Design

```lmn
#include <RANDOM>;
#include <STDIO>;

fun playGuessingGame() {
    print "=== NUMBER GUESSING GAME ===";
    print "I'm thinking of a number between 1 and 100!";
    
    var secretNumber random.randint(1, 100);
    var attempts 0;
    var maxAttempts 7;
    var hasWon False;
    
    while (attempts < maxAttempts && !hasWon) {
        var remaining maxAttempts - attempts;
        print "\nAttempts remaining: ", remaining;
        
        var guess stdio.inputInt("Enter your guess (1-100): ");
        attempts attempts + 1;
        
        if (guess == secretNumber) {
            print "🎉 CONGRATULATIONS! You found it!";
            print "The number was ", secretNumber;
            print "You won in ", attempts, " attempts!";
            hasWon True;
        }; if (guess < secretNumber) {
            print "📈 Too low! Try a higher number.";
        }; if (guess > secretNumber)  {
            print "📉 Too high! Try a lower number.";
        };
        
        // Give hints
        if (!hasWon && attempts < maxAttempts) {
            var difference;
            if (guess > secretNumber) {
                difference guess - secretNumber;
            }; if (guess < secretNumber) {
                difference secretNumber - guess;
            };
            
            if (difference <= 5) {
                print "🔥 You're very close!";
            }; if (difference <= 15) {
                print "🔶 Getting warmer...";
            } if (difference is > 15) {
                print "❄️ Pretty far off...";
            };
        };
    };
    
    if (!hasWon) {
        print "\n💀 Game Over! You've run out of attempts.";
        print "The number was ", secretNumber;
    };
};

fun showDifficulty() {
    print "\nDifficulty Levels:";
    print "1. Easy (1-50, 10 attempts)";
    print "2. Medium (1-100, 7 attempts)";
    print "3. Hard (1-200, 5 attempts)";
};

fun playWithDifficulty() {
    showDifficulty();
    var level stdio.inputInt("Choose difficulty (1-3): ");
    
    var maxNumber 100;
    var maxAttempts 7;
    
    if (level == 1) {
        maxNumber 50;
        maxAttempts 10;
        print "Easy mode: 1-50, 10 attempts";
    }; if (level == 3) {
        maxNumber 200;
        maxAttempts 5;
        print "Hard mode: 1-200, 5 attempts";
    }; if (level == 2) {
        print "Medium mode: 1-100, 7 attempts";
    };
    
    var secretNumber random.randint(1, maxNumber);
    var attempts 0;
    var hasWon False;
    
    print "I'm thinking of a number between 1 and ", maxNumber, "!";
    
    while (attempts < maxAttempts && !hasWon) {
        var remaining maxAttempts - attempts;
        print "\nAttempts remaining: ", remaining;
        
        var guess stdio.inputInt("Enter your guess: ");
        attempts attempts + 1;
        
        if (guess == secretNumber) {
            print "🎉 AMAZING! You got it!";
            hasWon True;
        }; if (guess < secretNumber) {
            print "📈 Higher!";
        }; if (guess > secretNumber) {
            print "📉 Lower!";
        };
    };
    
    if (!hasWon) {
        print "💀 Out of attempts! The number was ", secretNumber;
    };
};

// Main game loop
print "Welcome to the Number Guessing Game!";
var playAgain True;

while (playAgain) {
    playWithDifficulty();
    
    var response stdio.input("\nPlay again? (yes/no): ");
    if (response != "yes") {
        playAgain False;
    };
};

print "Thanks for playing! 👋";
```

---

# 🎓 Congratulations! You've Mastered Lumen!

## What You've Learned

<table>
<tr>
<td width="50%">

**🔧 Core Concepts**
- ✅ Variables and data types
- ✅ Functions and parameters  
- ✅ Control flow (if, loops)
- ✅ Arrays and dictionaries
- ✅ Input/output operations

</td>
<td width="50%">

**📚 Libraries & Tools**
- ✅ STDIO for input/output
- ✅ MATH for calculations
- ✅ RANDOM for randomization
- ✅ OS for system operations
- ✅ File handling and data persistence

</td>
</tr>
</table>

**🏗️ Complete Projects Built**
1. **Personal Task Manager** - CRUD operations, data persistence
2. **Number Guessing Game** - Game logic, difficulty levels, user interaction

---

## 🚀 Next Steps

### Immediate Practice
1. **Modify the projects** - Add new features, improve the UI
2. **Combine concepts** - Mix different libraries in new ways
3. **Debug and optimize** - Make your code cleaner and more efficient

### Advanced Topics to Explore
- **Error handling** - Making robust programs
- **Code organization** - Splitting large programs into modules
- **Performance optimization** - Writing efficient Lumen code
- **Advanced data structures** - Complex nested dictionaries and arrays

### Build Your Own Projects
- **Grade calculator** with file persistence
- **Simple banking system** with transaction history
- **Text-based RPG** with character progression
- **File organizer** using OS library
- **Math quiz game** with different difficulty levels

---

## 💡 Programming Tips & Best Practices

### 🎨 Code Style
```lmn
// ✅ Good: Clear, descriptive names
fun calculateMonthlyPayment(principal, rate, months) {
    var monthlyRate rate / 12;
    var payment (principal * monthlyRate) / (1 - math.pow(1 + monthlyRate, -months));
    return payment;
};

// ❌ Avoid: Unclear abbreviations  
fun calcPay(p, r, m) {
    var mr r / 12;
    return (p * mr) / (1 - math.pow(1 + mr, -m));
};
```

### 🔍 Debugging Strategies
```lmn
// Add debug prints to track values
fun processOrder(items, discount) {
    print "DEBUG: Processing order with ", items, " items";
    print "DEBUG: Discount applied: ", discount;
    
    var total calculateTotal(items);
    print "DEBUG: Total before discount: ", total;
    
    total total * (1 - discount);
    print "DEBUG: Final total: ", total;
    
    return total;
};
```

### 🏗️ Project Structure
```lmn
// Main program
fun main() {
    initializeGame();
    runGameLoop();
    cleanup();
};

// Helper functions
fun initializeGame() {
    // Setup code here
};

fun runGameLoop() {
    // Main logic here
};

fun cleanup() {
    // Cleanup code here
};

// Start the program
main();
```

---

## 📚 Additional Resources

<div align="center">

| Resource | Description | When to Use |
|----------|-------------|-------------|
| **🔧 Practice Problems** | Coding challenges to reinforce concepts | After each chapter |
| **📖 Documentation** | Complete language reference | When you need syntax help |
| **💬 Community Forum** | Ask questions and share projects | When you're stuck or want feedback |
| **🏆 Project Gallery** | See what others have built | For inspiration and learning |

</div>

---

## 🎉 You're Now a Lumen Programmer!

You've successfully completed the comprehensive Lumen tutorial! You now have the skills to:

- **Build complete applications** from scratch
- **Use all major Lumen features** effectively  
- **Integrate multiple libraries** to create powerful programs
- **Debug and optimize** your code
- **Plan and structure** larger projects

### Keep Coding! 🚀

The best way to improve is to keep building. Start with small projects and gradually work up to more complex applications. Every program you write makes you a better programmer!

---

<div align="center">

**Happy Coding with Lumen! 💜**

*Remember: Every expert was once a beginner. Keep practicing!*

[⬆️ Back to Top](#-learn-lumen-complete-step-by-step-tutorial)

</div>
