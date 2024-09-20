# Python Documentation Standard

## Inline Comments

1. Use inline comments sparingly, only when the code is not self-explanatory.
2. Place inline comments on the same line as the code they describe, or on the line above if they don't fit.
3. Start inline comments with two spaces, then # and another space.
4. Write comments in complete sentences, starting with a capital letter.

Example:
```python
x = x + 1  # Increment x
```

## Function and Method Docstrings

Use the following format for function and method docstrings:

```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Brief description of the function.

    Extended description of the function (if necessary).

    Args:
        param1 (type): Description of param1.
        param2 (type): Description of param2.

    Returns:
        return_type: Description of the return value.

    Raises:
        ExceptionType: Description of when this exception is raised.

    Examples:
        >>> function_name(1, 'test')
        Expected output
    """
    # Function body
```

## Class Docstrings

Use the following format for class docstrings:

```python
class ClassName:
    """
    Brief description of the class.

    Extended description of the class (if necessary).

    Attributes:
        attr1 (type): Description of attr1.
        attr2 (type): Description of attr2.

    Methods:
        method1: Brief description of method1.
        method2: Brief description of method2.
    """

    def __init__(self, param1: type, param2: type):
        """
        Initialize the class.

        Args:
            param1 (type): Description of param1.
            param2 (type): Description of param2.
        """
        # Initialization code
```

## Module Docstrings

Place module docstrings at the beginning of the file, after any import statements:

```python
"""
Brief description of the module.

Extended description of the module (if necessary).

This module contains the following classes:
    - Class1: Brief description.
    - Class2: Brief description.

This module contains the following functions:
    - function1: Brief description.
    - function2: Brief description.
"""

# Rest of the module code
```

## General Guidelines

1. Use proper grammar, punctuation, and complete sentences in all documentation.
2. Keep descriptions concise but informative.
3. Use type hints in function signatures and docstrings.
4. Include examples in docstrings when they add clarity.
5. Update documentation when you modify code.
6. Use present tense in descriptions (e.g., "Returns" not "Return").
7. For complex algorithms, include a brief explanation of how they work.

Remember to use this standard consistently across all Python modules in your project to maintain readability and ease of understanding for all team members.