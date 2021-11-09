from Core import Core

# tokens stores all Core tokens; valuesWord stores ID values; valuesNumber stores all CONST values
tokens = []
valuesWord = []
valuesNumber = []

class Scanner:

    # Constructor should open the file and find the first token
    def __init__(self, filename):

        # open text file in read mode
        file = open(filename, 'r')

        while 1:
            # read by character
            char = file.read(1)
            if not char:
                tokens.append(Core.EOF)
                tokens.append("\n") # added to match expected files in tester
                break

            # Special characters
            if char == ";":
                tokens.append(Core.SEMICOLON)
            elif char == "(":
                tokens.append(Core.LPAREN)
            elif char == ")":
                tokens.append(Core.RPAREN)
            elif char == ",":
                tokens.append(Core.COMMA)
            elif char == "=":
				# tell() stores current position so seek() can reset if next char is not =
                idx = file.tell()
                if file.read(1) == "=":
                    tokens.append(Core.EQUAL)
                else:
                    file.seek(idx)
                    tokens.append(Core.ASSIGN)
            elif char == "!":
                tokens.append(Core.NEGATION)
            elif char == "<":
				# tell() stores current position so seek() can reset if next char is not =
                idx = file.tell()
                if file.read(1) == "=":
                    tokens.append(Core.LESSEQUAL)
                else:
                    file.seek(idx)
                    tokens.append(Core.LESS)
            elif char == "+":
                tokens.append(Core.ADD)
            elif char == "-":
                tokens.append(Core.SUB)
            elif char == "*":
                tokens.append(Core.MULT)
			# Error values
            elif char in "_%:?$#@&":
                print("ERROR: Invalid input character", char)
                tokens.append(Core.ERROR)
			# Keywords or ID
            elif char.isalpha():
                word = self.getAlphabet(file, file.tell(), char) # get keyword/id and set file position to next char
                if word == "program":
                    tokens.append(Core.PROGRAM)
                elif word == "begin":
                    tokens.append(Core.BEGIN)
                elif word == "end":
                    tokens.append(Core.END)
                elif word == "new":
                    tokens.append(Core.NEW)
                elif word == "int":
                    tokens.append(Core.INT)
                elif word == "define":
                    tokens.append(Core.DEFINE)
                elif word == "endfunc":
                    tokens.append(Core.ENDFUNC)
                elif word == "class":
                    tokens.append(Core.CLASS)
                elif word == "extends":
                    tokens.append(Core.EXTENDS)
                elif word == "endclass":
                    tokens.append(Core.ENDCLASS)
                elif word == "if":
                    tokens.append(Core.IF)
                elif word == "then":
                    tokens.append(Core.THEN)
                elif word == "else":
                    tokens.append(Core.ELSE)
                elif word == "while":
                    tokens.append(Core.WHILE)
                elif word == "endwhile":
                    tokens.append(Core.ENDWHILE)
                elif word == "endif":
                    tokens.append(Core.ENDIF)
                elif word == "or":
                    tokens.append(Core.OR)
                elif word == "input":
                    tokens.append(Core.INPUT)
                elif word == "output":
                    tokens.append(Core.OUTPUT)
                elif word == "ref":
                    tokens.append(Core.REF)
                else:
                    tokens.append(Core.ID)
                    valuesWord.append(word)
			# Constants
            elif char.isdigit():
                number = self.getDigit(file, file.tell(), char) # get digit and set file position to next char
                if 0 <= int(number) <= 1023:
                    tokens.append(Core.CONST)
                    valuesNumber.append(number)
                else:
                    print("ERROR: Constant out of range")
                    tokens.append(Core.ERROR)
                    
        file.close()

	# gets the constant by reading and joining characters and sets the file position to next char after digit
    def getDigit(self, file, idx, char):
        number = char
        counter = 1
        tempChar = file.read(1)
        while tempChar.isdigit():
            number = number + tempChar
            tempChar = file.read(1)
            counter = counter + 1
        file.seek(idx + counter - 1)
        return number

	# gets the word (keyword/id) by reading and joining characters and sets the file position to next char after word
    def getAlphabet(self, file, idx, char):
        word = char
        counter = 1
        tempChar = file.read(1)
        while tempChar.isalpha() or tempChar.isdigit():
            word = word + tempChar
            tempChar = file.read(1)
            counter = counter + 1
        file.seek(idx + counter - 1)
        return word

    # nextToken should advance the scanner to the next token
    def nextToken(self):
        tokens.pop(0)

    # currentToken should return the current token
    def currentToken(self):
        return tokens[0]

    # If the current token is ID, return the string value of the identifier
    # Otherwise, return value does not matter
    def getID(self):
        value = valuesWord[0]
        valuesWord.pop(0)
        return value

    # If the current token is CONST, return the numerical value of the constant
    # Otherwise, return value does not matter
    def getCONST(self):
        value = valuesNumber[0]
        valuesNumber.pop(0)
        return value
