"""class CodeGenerator:
    def __init__(self, indentation:str = '\t'):
        self.indentation = indentation
        self.level = 0
        self.code = ''

    def indent(self):
        self.level += 1

    def dedent(self):
        if self.level > 0:
            self.level -= 1

    def __add__(self, value: str):
        temp = CodeGenerator(indentation=self.indentation)
        temp.level = self.level
        temp.code = str(self) + ''.join([self.indentation for _ in range(0, self.level)]) + str(value)
        return temp

    def __str__(self):
        return str(self.code)

a = CodeGenerator()
a += 'for a in range(1, 3):\n'
a.indent()
a += 'for b in range(4, 6):\n'
a.indent()
a += 'print(a * b)\n'
a.dedent()
a += '# pointless comment\n'
print(a)"""
temp = "123456789"
print(temp[2:])