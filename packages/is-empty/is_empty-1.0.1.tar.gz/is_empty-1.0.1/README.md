# is_empty
[![](https://img.shields.io/badge/Version-1.0.1-green)](https://github.com/wskoly/is_empty) [![](https://img.shields.io/badge/Author-Wahid%20Sadique%20Koly-red)](https://github.com/wskoly/)
### Python package to check whether a variable is empty or not.

- [Description](#Description)
- [Installation](#Installation)
- [Examples](#examples)
- [Author](#author)
- [License](#license)

## Description
- The package has two functions named `empty()` and `not_empty()` which can check if a variable is empty or not.
- The following values evaluate to empty:
  - 0
  - 0.0
  - ""
  - None
  - False
  - []
  - ()
  - {}
  - set()
  - b""

## Installation
To install, write the following command in your terminal.
```py
pip install is_empty
```
## Examples
Import the functions to your code.
```py
from is_empty import empty, not_empty
```
- Check whether a list is empty or not using empty().
```py
#The function will return True in this case
items = []
if empty(items):
  #Do something
else:
  #Do something else
```
- Check whether a tuple is not empty using not_empty.
```py
#The function will return True in this case
items = (1,2,3)
if not_empty(items):
  #Do something
```

## Author
**Wahid Sadique Koly**
- [Github](https://github.com/wskoly/) 
- [Portfolio](https://wskoly.ml)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details