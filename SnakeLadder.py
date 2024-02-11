class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Player:
    def __init__(self, name, location: point, identifier: str):
        self.name = name
        self.location = location
        self.identifier = identifier

    def move(self, location: point):
        self.location = location

    def __str__(self):
        return "\033[0;34m" + self.identifier + "\033[0m"


class Tile:
    def __init__(self, location: point, identifier: str):
        self.location = location
        self.identifier = identifier

    def action(self, player):
        pass

    def __str__(self):
        return self.identifier


class Snake(Tile):

    def __init__(self, head: point, tail: point, identifier: str):
        super(Snake, self).__init__(head, identifier)
        self.tail = tail

    def action(self, player):
        player.move(self.tail)

    def __str__(self):
        return "\033[0;31m" + self.identifier + "\033[0m"


class Ladder(Tile):

    def __init__(self, start: point, end: point, identifier: str):
        super(Ladder, self).__init__(start, identifier)
        self.end = end

    def action(self, player):
        player.move(self.end)

    def __str__(self):
        return "\033[0;32m" + self.identifier + "\033[0m"


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = []
        for i in range(self.width):
            for j in range(self.height):
                self.tiles.append(Tile(point(i, j), "0"))
        self.players = []
        self.gameFinished = False

    def get_tile(self, location: point) -> Tile:
        return self.tiles[location.x * self.width + location.y]

    def add_snake(self, head: point, tail: point, identifier: str):
        # add head
        self.tiles[head.x * self.width +
                   head.y] = Snake(head, tail, identifier)
        # add tail
        self.tiles[tail.x * self.width +
                   tail.y] = Snake(head, tail, identifier)

    def add_ladder(self, start: point, end: point, identifier: str):
        # add start
        self.tiles[start.x * self.width +
                   start.y] = Ladder(start, end, identifier)
        # add end
        self.tiles[end.x * self.width + end.y] = Ladder(start, end, identifier)

    def add_player(self, name, location: point, identifier: str):
        self.players.append(Player(name, location, identifier))

    def move_player(self, player: Player, dice: int):
        oldLocation = player.location
        newLocation = player.location

        if (oldLocation.y < self.height - 1):
            newLocation.y = oldLocation.y + \
                int((oldLocation.x + dice) / self.width)
            newLocation.x = (oldLocation.x + dice) % self.width
        else:
            if (oldLocation.x + dice <= self.width-1):
                newLocation.x = (oldLocation.x + dice) % self.width
            else:
                print("You can't move that far")

        return newLocation

    def roll_dice(self):
        import random
        return random.randint(1, 6)

    def play(self):
        double_Countinue = False
        while not self.gameFinished:
            for player in self.players:
                if not self.gameFinished:
                    dice = self.roll_dice()
                    print(player.name + " rolled a " + str(dice))
                    newLocation = self.move_player(player, dice)
                    tile = self.get_tile(newLocation)
                    # check if tile is snake or ladder
                    if (isinstance(tile, Snake)):
                        print(player.name + " got bitten by a snake")
                    elif (isinstance(tile, Ladder)):
                        print(player.name + " climbed a ladder")

                    tile.action(player)
                    print(player.name + " moved to " + str(player.location))
                    if (newLocation.x == self.width-1 and newLocation.y == self.height-1):
                        self.gameFinished = True
                        print(player.name + " won!")
                        break
                    if (dice == 6 and not double_Countinue):
                        double_Countinue = True
                        print(player.name + " gets another turn")
                    else:
                        double_Countinue = False
                gameBoard.print()
                import time
                time.sleep(1)

    def print(self):
        playerFound = False
        for i in range(self.width):
            for j in range(self.height):
                for player in self.players:
                    if (player.location == point(j, i)):
                        print(player, end=" ")
                        playerFound = True
                        break
                if not playerFound:
                    print(self.tiles[j * self.width + i], end=" ")
                playerFound = False
            print("")


print("Welcome to Snakes and Ladders")
print("Enter the size of the board")
width = int(input("Width: "))
height = int(input("Height: "))
gameBoard = Board(width, height)
print("Enter the number of snakes")
numSnakes = int(input())
for i in range(numSnakes):
    print("Enter the coordinates of snake " + str(i+1))
    print("Head")
    x = int(input("x: "))
    y = int(input("y: "))
    head = point(x, y)
    print("Tail")
    x = int(input("x: "))
    y = int(input("y: "))
    tail = point(x, y)
    identifier = input("identifier: ")
    gameBoard.add_snake(head, tail, identifier)

print("Enter the number of ladders")
numLadders = int(input())
for i in range(numLadders):
    print("Enter the coordinates of ladder " + str(i+1))
    print("Start")
    x = int(input("x: "))
    y = int(input("y: "))
    start = point(x, y)
    print("End")
    x = int(input("x: "))
    y = int(input("y: "))
    end = point(x, y)
    identifier = input("identifier: ")
    gameBoard.add_ladder(start, end, identifier)

print("Enter the number of players")
numPlayers = int(input())
for i in range(numPlayers):
    print("Enter the name of player " + str(i+1))
    name = input()
    print("Enter the coordinates of player " + str(i+1))
    location = point(0, 0)
    identifier = input("identifier: ")
    gameBoard.add_player(name, location, identifier)

gameBoard.print()
gameBoard.play()
