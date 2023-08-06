from types import NoneType
class NotSupportedError(Exception):
    def __init__(self, message, *args) -> None:
        super().__init__(*args)
        self.message = message
        
    def __str__(self) -> str:
        return self.message
    
def empty(variable)->bool:
    """Check whether a variable is empty.
       The empty() function checks whether a variable is empty or not.
       This function returns False if the variable is not empty, otherwise it returns True.
    Args:
        variable (any): pass the variable to check if it's empty or not
    """
    if isinstance(variable, int):
        return variable == 0
    elif isinstance(variable, float):
        return variable == 0.0
    elif isinstance(variable, str):
        return variable == ""
    elif isinstance(variable, bool):
        return not variable
    elif isinstance(variable, list):
        return len(variable) == 0
    elif isinstance(variable, tuple):
        return len(variable) == 0
    elif isinstance(variable, dict):
        return not bool(variable)
    elif isinstance(variable, NoneType):
        return True
    elif isinstance(variable, complex):
        return variable == 0
    elif isinstance(variable, set):
        return variable == set()
    elif isinstance(variable, bytes):
        return variable == b""
    else:
        raise NotSupportedError("Variable type not supported")
    
def not_empty(variable)->bool:
    """Check whether a variable is not empty.
       The not_empty() function checks whether a variable is empty or not.
       This function returns True if the variable is not empty, otherwise it returns False.
    Args:
        variable (any): pass the variable to check if it's empty or not
    """
    return not empty(variable)