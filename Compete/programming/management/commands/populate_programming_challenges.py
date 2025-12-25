from django.core.management.base import BaseCommand
from programming.models import NewProgrammingChallenge


class Command(BaseCommand):
    help = 'Populates the database with Programming challenges for all difficulty levels'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Programming challenge creation...'))
        self.stdout.write(f'Current challenges in database: {NewProgrammingChallenge.objects.count()}')

        challenges_data = [
            # ========================
            # PYTHON - EASY (5 challenges)
            # ========================
            {
                'title': 'Hello World',
                'description': '''Welcome to Programming challenges! Let's start with the basics.

Your task: Create a Python function that returns the string "Hello, World!".

Write a function called `hello_world()` that takes no parameters and returns the string exactly as shown.

The flag is the complete function definition.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Python',
                'flag': 'flag{def hello_world(): return "Hello, World!"}'
            },
            {
                'title': 'Sum of Two Numbers',
                'description': '''Basic arithmetic in Python.

Your task: Create a function that takes two integers and returns their sum.

Function signature: `add_numbers(a, b)`

Example: add_numbers(5, 3) should return 8

The flag is the operation used in the return statement.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Python',
                'flag': 'flag{a + b}'
            },
            {
                'title': 'Check Even or Odd',
                'description': '''Learn about conditionals and modulo operator.

Your task: Write a function that returns True if a number is even, False if odd.

Function signature: `is_even(n)`

The flag is the boolean expression used to check if a number is even.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Python',
                'flag': 'flag{n % 2 == 0}'
            },
            {
                'title': 'List Length',
                'description': '''Working with Python lists.

Your task: Find the built-in Python function that returns the number of elements in a list.

Example: For list [1, 2, 3, 4, 5], the function should return 5.

The flag is the function name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Python',
                'flag': 'flag{len}'
            },
            {
                'title': 'String Reversal',
                'description': '''String manipulation in Python.

Your task: Reverse a string using Python slicing.

For input "hello", output should be "olleh".

The flag is the slicing syntax to reverse a string (assuming string variable is named 's').
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Python',
                'flag': 'flag{s[::-1]}'
            },

            # ========================
            # PYTHON - MEDIUM (5 challenges)
            # ========================
            {
                'title': 'Fibonacci Sequence',
                'description': '''Generate the nth Fibonacci number.

The Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21...

Your task: Write a recursive function to find the nth Fibonacci number.

Function signature: `fibonacci(n)`

Base cases: fib(0) = 0, fib(1) = 1

The flag is the recursive call expression for n > 1.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Python',
                'flag': 'flag{fibonacci(n-1) + fibonacci(n-2)}'
            },
            {
                'title': 'Prime Number Checker',
                'description': '''Determine if a number is prime.

A prime number is only divisible by 1 and itself.

Your task: Implement an efficient prime checking algorithm.

For n = 17, return True. For n = 18, return False.

The flag is the range parameters used to check divisibility (start, end).
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Python',
                'flag': 'flag{2, int(n**0.5) + 1}'
            },
            {
                'title': 'Anagram Checker',
                'description': '''Check if two strings are anagrams.

Anagrams are words formed by rearranging letters of another word.

Your task: Determine if two strings are anagrams (ignore spaces and case).

Example: "listen" and "silent" are anagrams.

The flag is the Python function used to sort characters in both strings for comparison.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Python',
                'flag': 'flag{sorted}'
            },
            {
                'title': 'Remove Duplicates',
                'description': '''Remove duplicate elements from a list while preserving order.

Your task: Convert a list to remove duplicates efficiently.

Input: [1, 2, 2, 3, 4, 4, 5]
Output: [1, 2, 3, 4, 5]

The flag is the Python data structure that naturally stores unique elements.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Python',
                'flag': 'flag{set}'
            },
            {
                'title': 'Dictionary Inversion',
                'description': '''Swap keys and values in a dictionary.

Your task: Given a dictionary, create a new dictionary with values as keys and keys as values.

Input: {'a': 1, 'b': 2}
Output: {1: 'a', 2: 'b'}

The flag is the dictionary comprehension syntax (using k and v as variables).
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Python',
                'flag': 'flag{{v: k for k, v in d.items()}}'
            },

            # ========================
            # PYTHON - HARD (5 challenges)
            # ========================
            {
                'title': 'Longest Palindromic Substring',
                'description': '''Find the longest palindromic substring in a given string.

A palindrome reads the same forward and backward.

Your task: Implement dynamic programming solution.

Input: "babad"
Output: "bab" or "aba"

The flag is the algorithm approach name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Python',
                'flag': 'flag{dynamic programming}'
            },
            {
                'title': 'Merge K Sorted Lists',
                'description': '''Merge multiple sorted lists into one sorted list efficiently.

Your task: Use a heap-based approach for optimal time complexity.

Input: [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]

The flag is the Python module used for heap operations.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Python',
                'flag': 'flag{heapq}'
            },
            {
                'title': 'LRU Cache Implementation',
                'description': '''Implement a Least Recently Used (LRU) cache.

Your task: Create a cache with O(1) get and put operations.

Use a combination of dictionary and doubly linked list.

The flag is the data structure combination needed.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Python',
                'flag': 'flag{dict and OrderedDict}'
            },
            {
                'title': 'Graph Cycle Detection',
                'description': '''Detect a cycle in a directed graph.

Your task: Implement cycle detection using DFS with color marking.

Use three colors: white (unvisited), gray (processing), black (completed).

The flag is the algorithm name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Python',
                'flag': 'flag{DFS with color marking}'
            },
            {
                'title': 'Regular Expression Matching',
                'description': '''Implement regex matching with * (zero or more) and . (any character).

Your task: Create a function that matches a pattern to a string.

Pattern "a*b" matches "aab", "b", "aaab"
Pattern "a.b" matches "acb", "adb"

The flag is the approach combining techniques.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Python',
                'flag': 'flag{dynamic programming with memoization}'
            },

            # ========================
            # JAVASCRIPT - EASY (5 challenges)
            # ========================
            {
                'title': 'Variable Declaration',
                'description': '''Learn modern JavaScript variable declarations.

Your task: What keyword should you use to declare a block-scoped variable that can be reassigned?

Example: let x = 5; x = 10; // valid

The flag is the keyword.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'JavaScript',
                'flag': 'flag{let}'
            },
            {
                'title': 'Array Methods',
                'description': '''Use array methods to find elements.

Your task: Which array method returns the first element that satisfies a condition?

Example: [1, 2, 3, 4].method(x => x > 2) returns 3

The flag is the method name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'JavaScript',
                'flag': 'flag{find}'
            },
            {
                'title': 'Arrow Functions',
                'description': '''Modern JavaScript function syntax.

Your task: Convert this function to arrow function syntax:
function double(x) { return x * 2; }

The flag is the arrow function (using 'x' as parameter).
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'JavaScript',
                'flag': 'flag{x => x * 2}'
            },
            {
                'title': 'Template Literals',
                'description': '''String interpolation in JavaScript.

Your task: How do you embed a variable 'name' in a string using template literals?

Example: "Hello, John" where John is from variable 'name'

The flag is the template literal syntax.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'JavaScript',
                'flag': 'flag{`Hello, ${name}`}'
            },
            {
                'title': 'Object Destructuring',
                'description': '''Extract values from objects easily.

Your task: Extract 'name' and 'age' from an object 'person' in one line.

const person = {name: "Alice", age: 30};

The flag is the destructuring syntax.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'JavaScript',
                'flag': 'flag{const {name, age} = person}'
            },

            # ========================
            # JAVASCRIPT - MEDIUM (5 challenges)
            # ========================
            {
                'title': 'Promise Chaining',
                'description': '''Handle asynchronous operations with Promises.

Your task: Chain multiple promises using the correct method.

fetch(url)
  .method(response => response.json())
  .method(data => console.log(data))

The flag is the method used for chaining.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'JavaScript',
                'flag': 'flag{then}'
            },
            {
                'title': 'Array Reduce',
                'description': '''Aggregate array values with reduce.

Your task: Sum all numbers in an array using reduce.

[1, 2, 3, 4].reduce(?)

The flag is the reducer function with accumulator 'acc' and current 'curr'.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'JavaScript',
                'flag': 'flag{(acc, curr) => acc + curr, 0}'
            },
            {
                'title': 'Debounce Function',
                'description': '''Implement a debounce function to limit function calls.

Your task: Create a debounce that delays execution until after a wait period.

Useful for search inputs and resize events.

The flag is the JavaScript function used for delayed execution.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'JavaScript',
                'flag': 'flag{setTimeout}'
            },
            {
                'title': 'Deep Clone Object',
                'description': '''Create a deep copy of a nested object.

Your task: Which modern JavaScript method can deep clone an object?

const clone = ?.?(original);

The flag is the method chain.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'JavaScript',
                'flag': 'flag{JSON.parse(JSON.stringify(obj))}'
            },
            {
                'title': 'Closure Concept',
                'description': '''Understand JavaScript closures.

Your task: What feature allows a function to access variables from its outer scope?

function outer() {
  let count = 0;
  return function inner() { count++; }
}

The flag is the concept name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'JavaScript',
                'flag': 'flag{closure}'
            },

            # ========================
            # JAVASCRIPT - HARD (5 challenges)
            # ========================
            {
                'title': 'Event Loop Understanding',
                'description': '''Master JavaScript's asynchronous execution model.

Your task: In what order do these execute?
console.log(1);
setTimeout(() => console.log(2), 0);
Promise.resolve().then(() => console.log(3));
console.log(4);

The flag is the output order.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'JavaScript',
                'flag': 'flag{1, 4, 3, 2}'
            },
            {
                'title': 'Implement Async/Await',
                'description': '''Convert Promise chains to async/await syntax.

Your task: What keyword makes a function return a Promise?

The keyword placed before 'function' to enable await usage inside.

The flag is the keyword.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'JavaScript',
                'flag': 'flag{async}'
            },
            {
                'title': 'Prototype Chain',
                'description': '''Understand JavaScript inheritance mechanism.

Your task: What property links an object to its prototype?

All objects have this hidden property.

The flag is the property name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'JavaScript',
                'flag': 'flag{__proto__}'
            },
            {
                'title': 'Generator Functions',
                'description': '''Use generators for lazy evaluation.

Your task: What symbol precedes the function name to create a generator?

function* generator() { yield 1; }

The flag is the symbol.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'JavaScript',
                'flag': 'flag{*}'
            },
            {
                'title': 'Proxy and Reflect',
                'description': '''Implement meta-programming with Proxies.

Your task: Which object is used to intercept operations on another object?

const p = new ?(target, handler);

The flag is the constructor name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'JavaScript',
                'flag': 'flag{Proxy}'
            },

            # ========================
            # C++ - EASY (5 challenges)
            # ========================
            {
                'title': 'Include Statement',
                'description': '''Start with C++ basics.

Your task: What preprocessor directive includes the iostream library?

This is needed for std::cout and std::cin.

The flag is the complete statement.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'C++',
                'flag': 'flag{#include <iostream>}'
            },
            {
                'title': 'Namespace Usage',
                'description': '''Avoid prefix repetition in C++.

Your task: What statement allows using cout without std:: prefix?

The flag is the complete statement (for std namespace).
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'C++',
                'flag': 'flag{using namespace std;}'
            },
            {
                'title': 'Pointer Declaration',
                'description': '''Understanding C++ pointers.

Your task: How do you declare a pointer to an integer variable?

The flag is the declaration (using 'ptr' as name).
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'C++',
                'flag': 'flag{int* ptr}'
            },
            {
                'title': 'Reference Parameters',
                'description': '''Pass by reference in C++.

Your task: What symbol creates a reference parameter?

void swap(int& a, int& b)

The flag is the symbol.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'C++',
                'flag': 'flag{&}'
            },
            {
                'title': 'Vector Initialization',
                'description': '''Use C++ STL containers.

Your task: Include the header for using vector container.

The flag is the include statement.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'C++',
                'flag': 'flag{#include <vector>}'
            },

            # ========================
            # C++ - MEDIUM (5 challenges)
            # ========================
            {
                'title': 'Class Constructor',
                'description': '''Object-oriented programming in C++.

Your task: What special method initializes an object when created?

class MyClass {
    MyClass() { } // This is a...?
}

The flag is the method type name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'C++',
                'flag': 'flag{constructor}'
            },
            {
                'title': 'Operator Overloading',
                'description': '''Customize operator behavior for classes.

Your task: What keyword is used to overload operators?

MyClass operator+(const MyClass& other)

The flag is the keyword.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'C++',
                'flag': 'flag{operator}'
            },
            {
                'title': 'Template Functions',
                'description': '''Generic programming in C++.

Your task: What keyword declares a template parameter?

template<typename T> or template<? T>

The flag is the alternative keyword.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'C++',
                'flag': 'flag{class}'
            },
            {
                'title': 'Smart Pointers',
                'description': '''Automatic memory management in modern C++.

Your task: Which smart pointer allows shared ownership?

The flag is the smart pointer type.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'C++',
                'flag': 'flag{shared_ptr}'
            },
            {
                'title': 'STL Algorithms',
                'description': '''Use Standard Template Library algorithms.

Your task: What header contains algorithm functions like sort, find, etc.?

The flag is the include statement.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'C++',
                'flag': 'flag{#include <algorithm>}'
            },

            # ========================
            # C++ - HARD (5 challenges)
            # ========================
            {
                'title': 'Virtual Functions',
                'description': '''Polymorphism through virtual functions.

Your task: What keyword makes a function overridable in derived classes?

class Base {
    virtual void func();
};

The flag is the keyword.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'C++',
                'flag': 'flag{virtual}'
            },
            {
                'title': 'Move Semantics',
                'description': '''Efficient resource transfer in C++11+.

Your task: What function converts an lvalue to an rvalue reference?

MyClass obj2 = std::?(obj1);

The flag is the function name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'C++',
                'flag': 'flag{move}'
            },
            {
                'title': 'Lambda Expressions',
                'description': '''Anonymous functions in C++.

Your task: What syntax captures all variables by reference in a lambda?

auto lambda = [?]() { };

The flag is the capture specification.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'C++',
                'flag': 'flag{&}'
            },
            {
                'title': 'RAII Principle',
                'description': '''Resource Acquisition Is Initialization pattern.

Your task: What C++ feature automatically calls destructors for cleanup?

The flag is the concept name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'C++',
                'flag': 'flag{automatic storage duration}'
            },
            {
                'title': 'Variadic Templates',
                'description': '''Handle variable number of template arguments.

Your task: What syntax declares a parameter pack?

template<typename... Args>

The flag is the special operator.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'C++',
                'flag': 'flag{...}'
            },

            # ========================
            # JAVA - EASY (5 challenges)
            # ========================
            {
                'title': 'Main Method',
                'description': '''Java program entry point.

Your task: What is the signature of the main method in Java?

The flag is the complete method signature.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Java',
                'flag': 'flag{public static void main(String[] args)}'
            },
            {
                'title': 'String Comparison',
                'description': '''Proper string comparison in Java.

Your task: What method compares string content for equality?

str1.?(str2)

The flag is the method name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Java',
                'flag': 'flag{equals}'
            },
            {
                'title': 'ArrayList Usage',
                'description': '''Dynamic arrays in Java.

Your task: What package contains ArrayList?

import java.util.?;

The flag is the import statement.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Java',
                'flag': 'flag{import java.util.ArrayList;}'
            },
            {
                'title': 'Exception Handling',
                'description': '''Handle runtime errors in Java.

Your task: What keyword catches exceptions?

try { } ? (Exception e) { }

The flag is the keyword.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Java',
                'flag': 'flag{catch}'
            },
            {
                'title': 'Access Modifiers',
                'description': '''Control visibility in Java.

Your task: What modifier makes a member accessible only within the same class?

The flag is the modifier keyword.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Java',
                'flag': 'flag{private}'
            },

            # ========================
            # JAVA - MEDIUM (5 challenges)
            # ========================
            {
                'title': 'Interface Implementation',
                'description': '''Implement interfaces in Java.

Your task: What keyword is used to implement an interface?

class MyClass ? Runnable

The flag is the keyword.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Java',
                'flag': 'flag{implements}'
            },
            {
                'title': 'Generic Classes',
                'description': '''Type-safe collections with generics.

Your task: How do you declare a generic class with type parameter T?

class MyClass<T> { }

The flag is the declaration syntax for the class name with type parameter.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Java',
                'flag': 'flag{class MyClass<T>}'
            },
            {
                'title': 'Stream API',
                'description': '''Functional programming in Java 8+.

Your task: What method creates a stream from a collection?

list.?().filter(...).collect(...)

The flag is the method name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Java',
                'flag': 'flag{stream}'
            },
            {
                'title': 'Thread Creation',
                'description': '''Concurrency in Java.

Your task: What interface must be implemented to create a thread task?

class MyTask implements ? { public void run() {} }

The flag is the interface name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Java',
                'flag': 'flag{Runnable}'
            },
            {
                'title': 'HashMap Operations',
                'description': '''Key-value storage in Java.

Your task: What method retrieves a value from HashMap?

map.?(key)

The flag is the method name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Java',
                'flag': 'flag{get}'
            },

            # ========================
            # JAVA - HARD (5 challenges)
            # ========================
            {
                'title': 'Synchronized Blocks',
                'description': '''Thread synchronization in Java.

Your task: What keyword ensures only one thread executes a code block?

? (lock) { critical section }

The flag is the keyword.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Java',
                'flag': 'flag{synchronized}'
            },
            {
                'title': 'Reflection API',
                'description': '''Inspect and modify runtime behavior.

Your task: What class represents the runtime class of an object?

Class<?> clazz = obj.getClass();

The flag is the return type.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Java',
                'flag': 'flag{Class}'
            },
            {
                'title': 'Annotation Processing',
                'description': '''Meta-programming with annotations.

Your task: What symbol precedes an annotation?

@Override

The flag is the symbol.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Java',
                'flag': 'flag{@}'
            },
            {
                'title': 'CompletableFuture',
                'description': '''Asynchronous programming in Java.

Your task: What class provides functional async operations?

The flag is the class name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Java',
                'flag': 'flag{CompletableFuture}'
            },
            {
                'title': 'Garbage Collection',
                'description': '''Automatic memory management in Java.

Your task: What method suggests (but doesn't guarantee) garbage collection?

System.?()

The flag is the method name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Java',
                'flag': 'flag{gc}'
            },

            # ========================
            # MISCELLANEOUS - EASY (5 challenges)
            # ========================
            {
                'title': 'Binary to Decimal',
                'description': '''Number system conversion.

Your task: Convert binary 1010 to decimal.

The flag is the decimal number.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Miscellaneous',
                'flag': 'flag{10}'
            },
            {
                'title': 'Factorial Function',
                'description': '''Classic recursive problem.

Your task: What is 5! (5 factorial)?

5! = 5 × 4 × 3 × 2 × 1

The flag is the result.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Miscellaneous',
                'flag': 'flag{120}'
            },
            {
                'title': 'Array Sum',
                'description': '''Basic array operations.

Your task: Sum the array [10, 20, 30, 40].

The flag is the sum.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Miscellaneous',
                'flag': 'flag{100}'
            },
            {
                'title': 'String Length',
                'description': '''Count characters in a string.

Your task: What is the length of "Programming"?

The flag is the count.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Miscellaneous',
                'flag': 'flag{11}'
            },
            {
                'title': 'Max Element',
                'description': '''Find maximum in an array.

Your task: Find the largest number in [15, 42, 8, 23, 16].

The flag is the maximum value.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Easy',
                'category': 'Miscellaneous',
                'flag': 'flag{42}'
            },

            # ========================
            # MISCELLANEOUS - MEDIUM (5 challenges)
            # ========================
            {
                'title': 'Two Sum Problem',
                'description': '''Find two numbers that sum to target.

Given array [2, 7, 11, 15] and target 9, find indices.

Your task: What data structure optimizes this to O(n)?

The flag is the data structure name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Miscellaneous',
                'flag': 'flag{hash table}'
            },
            {
                'title': 'Binary Search',
                'description': '''Search in sorted array efficiently.

Your task: What is the time complexity of binary search?

The flag is the Big O notation.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Miscellaneous',
                'flag': 'flag{O(log n)}'
            },
            {
                'title': 'Linked List Cycle',
                'description': '''Detect cycle in linked list.

Your task: What algorithm detects cycles using two pointers?

The flag is the algorithm name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Miscellaneous',
                'flag': 'flag{Floyd\'s Cycle Detection}'
            },
            {
                'title': 'Stack Implementation',
                'description': '''Implement LIFO data structure.

Your task: What operations define a stack?

The flag is the two primary operations (alphabetically).
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Miscellaneous',
                'flag': 'flag{pop and push}'
            },
            {
                'title': 'Palindrome Check',
                'description': '''Check if string reads same forwards and backwards.

Your task: Is "racecar" a palindrome?

The flag is the boolean answer.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Medium',
                'category': 'Miscellaneous',
                'flag': 'flag{True}'
            },

            # ========================
            # MISCELLANEOUS - HARD (5 challenges)
            # ========================
            {
                'title': 'Dynamic Programming Basics',
                'description': '''Optimize recursive solutions.

Your task: What technique stores results of subproblems?

The flag is the technique name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Miscellaneous',
                'flag': 'flag{memoization}'
            },
            {
                'title': 'Graph Traversal',
                'description': '''Visit all nodes in a graph.

Your task: Which traversal uses a queue?

BFS or DFS?

The flag is the algorithm abbreviation.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Miscellaneous',
                'flag': 'flag{BFS}'
            },
            {
                'title': 'Quicksort Partition',
                'description': '''Efficient sorting algorithm.

Your task: What is the average time complexity of quicksort?

The flag is the Big O notation.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Miscellaneous',
                'flag': 'flag{O(n log n)}'
            },
            {
                'title': 'Trie Data Structure',
                'description': '''Efficient string storage and retrieval.

Your task: What tree structure stores strings character by character?

Also called prefix tree.

The flag is the data structure name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Miscellaneous',
                'flag': 'flag{Trie}'
            },
            {
                'title': 'Backtracking Algorithm',
                'description': '''Solve constraint satisfaction problems.

Your task: What problem-solving technique tries possibilities and backtracks on failure?

The flag is the technique name.
Flag format: flag{your_answer_here}''',
                'difficulty': 'Hard',
                'category': 'Miscellaneous',
                'flag': 'flag{backtracking}'
            },
        ]

        created_count = 0
        skipped_count = 0

        for challenge in challenges_data:
            existing = NewProgrammingChallenge.objects.filter(title=challenge['title']).first()
            if existing:
                self.stdout.write(self.style.WARNING(f"⏭️  Skipped: {challenge['title']} (already exists)"))
                skipped_count += 1
            else:
                NewProgrammingChallenge.objects.create(**challenge)
                self.stdout.write(self.style.SUCCESS(f"✅ Created: {challenge['title']} ({challenge['difficulty']} - {challenge['category']})"))
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"\n{'='*60}"))
        self.stdout.write(self.style.SUCCESS(f"Summary:"))
        self.stdout.write(self.style.SUCCESS(f"  Created: {created_count} challenges"))
        self.stdout.write(self.style.WARNING(f"  Skipped: {skipped_count} challenges"))
        self.stdout.write(self.style.SUCCESS(f"  Total in database: {NewProgrammingChallenge.objects.count()} challenges"))
        self.stdout.write(self.style.SUCCESS(f"{'='*60}"))

        # Display breakdown by category and difficulty
        self.stdout.write(self.style.SUCCESS("\nBreakdown by Category and Difficulty:"))
        for category in ['Python', 'JavaScript', 'C++', 'Java', 'Miscellaneous']:
            self.stdout.write(f"\n{category}:")
            for difficulty in ['Easy', 'Medium', 'Hard']:
                count = NewProgrammingChallenge.objects.filter(
                    category=category,
                    difficulty=difficulty
                ).count()
                self.stdout.write(f"  {difficulty}: {count} challenges")
