## Project description
easily_quiz is a spanish api that you can create simple quiz, true or false, and things coming in future! With this api you can save certain lines of code and simply use two lines for what you would use 10 or 15

## Installing
You can install or update this api using [pip](https://pip.pypa.io/en/stable/getting-started/):
```$ pip install easily_quiz```

## Quiz example
```
# import the api
from easily_quiz import Quiz

# init 
quiz = Quiz("Example question", [1], "Option 1", "Option 2", "Option 3")
i = quiz.iniciar()

if i:
    print("Correct!")
else:
    print("Try again!")
```

## True or false example
```
# import the api
from easily_quiz import trueFalse

# init
z = trueFalse("Example question", True)
i = z.iniciar()

if i:
    print("Correct!")
else:
    print("Try again!")
```

## Contact & Donate
If you need help with the api or you wanna donate me i let you here some data:

Discord: Pina#8985
Web: http://pinayt.tk
Paypal: https://paypal.me/Inperiocompa
