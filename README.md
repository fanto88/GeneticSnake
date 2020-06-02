# SnakeIA
<div style="text-align:center">
    <img src="https://i.ibb.co/Qkmm8yz/board.png">
</div>

# Artificial Intelligence for Snake Game
I have created an Artificial Intelligence using the genetic algorithm able to play Snake game.

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
python3 -m pip install -r requirements.txt
```


### Download of the Server
The server is made by AGalassi on github. You can find the repository and all the instruction needed here [Server](https://github.com/AGalassi/TablutCompetition)

## Starting the Player
Now that you have all the components needed you can finally start the player. In order to do so start the server first,
then go to the root of the cloned project and run this command:
```
python3 UniWarsLAscesaDiChesani.py [-c color] [-t timeout] [-s ipAddress:port]
```

Where ``` -c -t -s ``` are not mandatory. If omitted, the default values ​​will be used
``` 
-c Let you select the player color (White/Black). Default:White
-t Let you express a max timeout in seconds for choosing the best action. Default:60
-s Let you define the server address. Default: localhost:5800 if White player, otherwise localhost:5801
```
