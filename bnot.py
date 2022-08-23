
import re


class BNot:
    VARS_RE = r'(.+?)\:\'(.*?)\'\;'  # Regex used for extracting variable name and value from notation.
    NULLABLES = ('None', 'null')  # Tuple of all keywords that mean a null value.

    def __init__(self, data = {}) -> None:
        """
            Initializes the 'BNot' class instance for managing Bartek's Notation.
            @param data:    Starting dictionary of variables.
        """
        self.data = data

    def __str__(self) -> str:
        """
            Returns string representation of class instance, here it is the dictionary of variables.
        """
        return str(self.data)

    @staticmethod
    def decode(code: str):
        """
            Converts data encoded to Bartek's Notation into dictionary (of variables encoded earlier).
            Note that variable values will be converted to possible type in following order: int > float > string,
            it means: convert to int, then if failed to float, and if this failed too, then to string.
            @param code:    Text encoded to Bartek's Notation format.
        """
        bnot = BNot()
        matches = re.findall(BNot.VARS_RE, code)
        for m in matches:
            # Name and value of decoded variable (both as string).
            name = m[0]
            value = m[1].replace('\\\'', "'")
            # True value means a correct-typed value.
            true_value = None if value in BNot.NULLABLES else value
            # Convert original value and if it is possible, assign converted version to the true value
            # which will be later used as an actual value of variable in dictionary.
            try:
                if '.' in value:
                    true_value = float(value)
                else:
                    true_value = int(value)
            except ValueError:
                pass
            # Save correctly-typed variable.
            bnot.var(name, true_value)
        return bnot

    def var(self, name: str, value: object) -> None:
        """
            Defines a new value of variable named 'name' with value 'value' assigned to it.
            @param name:    Name of the variable to set.
            @param value:   New value of variable with name specified.
        """
        self.data[name] = value

    def get(self, name: str, default = None) -> object:
        """
            Returns the value of variable named 'name', if it does not exist 'default' value is returned.
            @param name:    Name of variable you want to access.
            @param default: Value returned if variable is not found.
        """
        if name in self.data:
            return self.data[name]
        return default

    def und(self, name: str) -> bool:
        """
            Undefines (deletes) the variable with given name.
            @param name:    Name of the variable to delete/undefine.
        """
        if name in self.data:
            del self.data[name]
            return True
        return False

    def encode(self, export = False, file = 'bnot.txt') -> str:
        """
            Converts dictionary (of variables) into Bartek's Notation (text format), exports encoded data into
            text file under path 'file' if this feature is enabled.
            @param export:  If enabled, encoded data will be exported to a file.
            @param file:    Path to the file which will be wrote with encoded data, works only if 'export' is enabled.
        """
        code = ""
        # Compose the encoded data.
        for name in self.data:
            value = str(self.data[name]).replace("'", '\\\'')
            code += "{0}:'{1}';".format(name, value)
        # Export encoded data into specified file path if 'export' is enabled.
        if export:
            with open(file, 'w') as f:
                f.write(code)
        return code
    

if __name__ == '__main__':
    pass
