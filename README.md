<div align="center">

<img src="https://github.com/user-attachments/assets/651302ec-c5ec-4776-ab7e-e37dba3cf6ea"
     width="700" 
/>
<br>

[![License](https://img.shields.io/github/license/this-guy-git/Lumen?style=flat&color=FFCE50&labelColor=222222)](https://www.gnu.org/licenses/gpl-3.0)
[![Stars](https://img.shields.io/github/stars/this-guy-git/Lumen?style=flat&color=FFCE50&labelColor=222222)](https://github.com/this-guy-git/Lumen/stargazers)
[![Forks](https://img.shields.io/github/forks/this-guy-git/Lumen?style=flat&color=FFCE50&labelColor=222222)](https://github.com/this-guy-git/Lumen/forks)
[![Issues](https://img.shields.io/github/issues/this-guy-git/Lumen?style=flat&color=FFCE50&labelColor=222222)](https://github.com/this-guy-git/Lumen/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/this-guy-git/Lumen?style=flat&color=FFCE50&labelColor=222222)](https://github.com/this-guy-git/Lumen/pulls)
[![Release](https://img.shields.io/github/v/release/this-guy-git/Lumen?style=flat&color=FFCE50&labelColor=222222)](https://github.com/this-guy-git/Lumen/releases/)

</div>


## Table of Contents
- [Lumen](#lumen)
- [Contributors](#contributors)
- [Examples](#examples)
  - [Goto Label Logic](#goto-label-logic)
  - [Functions](#functions)
  - [Conditional Logic](#conditional-logic)
  - [Declaring Variables](#declaring-variables)
  - [Example Program](#example-program)
- [License](#license)




# Lumen
Lumen is a compiled, lightweight, and fast programming language.
It has familiar syntax that is great for beginners who want to learn C languages like C, C++, or C#,
and is great as an intermediate language between Python and C, as it teaches many C concepts while keeping the friendliness of Python.

## Contributors:
<a href = "https://github.com/this-guy-git/Lumen/contributors">
  <img src = "https://contrib.rocks/image?repo=this-guy-git/Lumen"/>
</a>

## Examples:
### Goto Label Logic:
```cpp
goto start;
print "This will be skipped!":

start:
print "Hello from start!";
```
### Functions:
```cpp
fun function(thing1, thing2) {
  print "First data is", thing1;
  print "Second data is", thing2;
};
function(data1, data2);
```
### Conditional Logic:
```cpp
if (condition) {
  code;
};
while (condition) {
  code;
};
```
### Declaring Variables:
```cpp
int integer 0;
str string "Hello!";
bool boolean False;
var anyData "This can be any type of data!";
static str staticVar "This variable cannot be changed.";
ary array[0,1,2];
dic dictionary{
  "key":"content";
};
```
### Example Program:
```cpp
int number 0; // Can only be an integer
bool thing True; // Can only be a Boolean
str stringThing "This is a string!"; // Can only be a string
var dynamicVar "WOW!"; // Can be any data type
static var stuckThing "Hello"; // CANNOT be changed

ary arrayThing["Index 0","Index 1","Index 2"]; // Can only be an Array
dic dictThing{
  "key1":"content1";
  "key2":"content2";
}; // Can only be a Dictionary

// Single line comment
/*
  Multi
  Line
  Comment
*/

fun program(condition, num) {
  if (condition) {
    print "Condtion is True!";
    while (num != 100)
    {
      print "The number is ", num;
      num++;
    };
  };
};

program(thing, number);
print dictThing["key1"]; // Will return "content1"
print arrayThing[1]; // Will return "Index 1"
```
## License

Lumen is distributed under the terms of the **GNU General Public License v3.0 (GPLv3)**.  
This license guarantees that Lumen and any derivative works remain free software.  

In plain terms:  
- You may use, study, modify, and share Lumen freely.  
- Any modifications or derivative works **must** also be released under GPLv3, with full source code available.  
- You may distribute Lumen (original or modified), but you may not relicense it under terms that restrict user freedoms.  
- Commercial distribution is permitted under GPLv3, but all recipients retain the same rights to the source code and to redistribute it.  

The intention of this license is to ensure that Lumen, and all works based on it, remain free and open for the entire community.
