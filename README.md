# SnakeIA
<div style="text-align:center">
    <img src="https://i.ibb.co/Qkmm8yz/board.png">
</div>

# Artificial Intelligence for Snake Game
Artificial Intelligence using the genetic algorithm able to play Snake game.

## Prerequisites

### Cloning the repository
First of all you need to clone the repository to your local machine.

#### Getting Git
The first step is having git installed on your local machine. If you’re on a Debian-based distribution, 
such as Ubuntu, try apt:

```
sudo apt install git-all
```

#### Cloning the repository
Second step is to actually clone the repository using:
```
git clone https://github.com/fanto88/GeneticSnake
```

### Dependencies
Install pip
```
sudo apt install python3-pip
```

Install python libraries. In project root run:
```
python3 -m pip install numpy
python3 -m pip install pygame
```

## Starting the Player
Now that you have all the components needed you can finally start the player. In order to do so start the server first,
then go to the root of the cloned project and run this command:
```
python main.py
```

There are 2 optionals parameters:
```
-g [value]
-b [value]
```

```
-g load the entire generation X
-b load the best snake inside generation X
```

Example to load the best snake of the generation 200 to watch his game replay
```
python main.py -b 200
```


parser.add_option('-g', '--generation', action="store", dest="generation",
                  help="Insert the generation you would like to watch")
parser.add_option('-b', '--best-scorer', action="store", dest="best_scorer",
                  help="Insert the generation you would like to watch")

## Customizing
Inside the file utils/config.py you will find some lines that let you customize the game.

#### Change the display window size
```
DISPLAY_WIDTH = 700
DISPLAY_HEIGHT = 700
```

#### Change the grid size
```
GRID_SIZE = (20, 20)
DRAW_GRID = False
RECT_SIZE = (DISPLAY_WIDTH // GRID_SIZE[0], DISPLAY_HEIGHT // GRID_SIZE[1])
```

#### Change game colors
```
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_ORANGE = (255, 140, 0)
SNAKE_HEAD_COLOR = RED
SNAKE_TAIL_COLOR = WHITE
GRID_BORDER_COLOR = WHITE
APPLE_COLOR = GREEN
```

#### Change how many extra move for eating an apple
```
APPLE_EXTRA_MOVES = 100
```

#### Change the game FPS
```
FPS = 20
```

#### Change how many extra piece the snake will gain for every eaten apple, the number of moves he has on the beginning of the game before dying and the max number of moves before dying
```
PIECE_FOR_APPLE = 1
MOVES = 100
MAX_MOVES = 500
```



### Customizing the NN

#### How many points the apple value inside the fitness function
APPLE_POINTS = 1

#### Change some of the genetic algorithm parameters
NUMBER_OF_POPULATION = 200
NUMBER_OF_GENERATION = 200
NUMBER_PARENTS_CROSSOVER = 10
MUTATION_PERCENTAGE = 0.1

#### Change the neural network input, hidden layers and output neurons
INPUT = 10
NEURONS_HIDDEN_1 = 6
OUTPUT = 3
NUMBER_WEIGHTS = INPUT * NEURONS_HIDDEN_1 + NEURONS_HIDDEN_1 * OUTPUT

#### Change the location of the generations_files created. Those files are used for the extra parameters when launching the game

GENERATION_FILES_FOLDER = 'generations_files/'
LAST_GENERATION_FILE_NAME = GENERATION_FILES_FOLDER + 'latest_generation_number.csv'
WEIGHTS_FILES_FOLDER = GENERATION_FILES_FOLDER + 'weights/'
SCORES_FILES_FOLDER = GENERATION_FILES_FOLDER + 'scores/'
BEST_SCORER_FOLDER = GENERATION_FILES_FOLDER + 'best_scorer/'

