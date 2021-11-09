Srushti Dhile

Files being submitted:

1. Main.py - The main python file imports Core, Scanner, Parser, Executor, and Grammar file. It takes a file path as input, sends it to the Scanner and then to the Parser's Prog class's parse function and print function.

2. Core.py - This file contains the enumeration of all the keywords and special characters of the Core language along with Error and EOF tokens.

3. Scanner.py - The Scanner implementation of the Core language contains various functions. The constructor reads each character one by one and adds tokens to a list. The getDigit and getAlphabet return a fully formed number or word. The currentToken function returns the first token in the list. 
The nextToken function deletes the first token in the list so the second token takes place of the first. Lastly, the getID and getCONST functions return the associated value of the ID or Constant when called from Main.py.

4. Grammar.py - The Parser implementation contains classes for each of the non-terminal of the Core Grammar. After a Prog class is created in the main, it is recursively passed along to other classes in the Grammar to create a parse tree, print the code received, and execute it.
    Classes in the Parser: Prog, DeclSeq, StmtSeq, Decl, DeclInt, DeclClass, IdList, Stmt, Assign, Input, Output, If, Loop, Cond, Cmpr, Expr, Term, Factor

5. README.txt - This file contains a brief documentation of the code.

Special features: None

Description of Interpreter:

I created a map for the global variables by using a dictionary for keys and values, a stack for the local scopes by using a list where scopes (empty map) were added at the beginning of program body, if/else statement body, while statement body and were popped off the stack after their completion.
I created a heap by using a list for storing the reference variable actual values and by storing the index into heap as their value on the map (global/local).
I also created a list for int types and ref types to distinguish between the two, since int accessed value from map (global/local), and ref used the value from the map (global/local) as an index into the heap.
During updating value to a variable, the variable was searched from the map at the top of the stack, going down if it wasn't found in there. Lastly, global map was checked and updated. This was the implementation of scopes, where the recent entered scope was the recent value used.

Testing:

I used the tester.sh file to test all required test cases where I got 26/26 working and 0/2 error cases working. I also used debugging statements that were displayed by scopes (stack of maps) when they added and popped and to check the variables inside.

Known bugs: 

The first error for checking if there are valid tokens in the .data file does not work. When tried to implement it, other test cases were failing, therefore it was left as is for this project. 
The second error of the null pointer also does not work. 