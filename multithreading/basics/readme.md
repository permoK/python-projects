## Basics of Multithreading

    **Thread:** A thread is the smallest unit of a process that can be scheduled by the operating system. Multiple threads within the same process share the same memory space but have their own stack.

    **GIL (Global Interpreter Lock):** The GIL is a mutex that protects access to Python objects, preventing multiple native threads from executing Python bytecodes simultaneously in a multi-threaded program. This means that even in a multi-threaded Python program, only one thread executes Python code at a time. This is a major limitation for CPU-bound tasks.


## Basic Example

Here's a simple example to demonstrate multithreading
