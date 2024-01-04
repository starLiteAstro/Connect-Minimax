import board
import game
import player
import randomPlayer
# Note that you can comment out the following if you don't want to seed the random player differently each run
from datetime import datetime
import time

games = 10
wins = 0
draws = 0
losses = 0
start = time.time()

for i in range(games):
    # This script allows you to test your solution.
    # Your coursework implementation must always be player 1.
    # You should consider changing player 2 to use a minimax approach for evaluation.
    # It is recommended that you also consider other game board sizes, and vary the number of pieces 
    # that are required in a line to win. There are examples of the method calls to create such games
    # commented out below.
    p1 = player.Player("X")

    # Player 2 currently picks random moves and so, while player 2 is not very good, it does allow you to
    # start testing your solution. Once you have something sensible, you should change player 2 to be more 
    # intelligent. Note that you can specify a seed for the random player (currently the seed is '42'),
    # which allows for testing in a consistent environment.
    # Note that the following two lines seed the random player differently each run
    seed = datetime.now().timestamp()
    #p2 = player.Player("O")
    # Instead of randomly seeding, you can comment out the following line to seed the random player and
    # test with a consistent opponent
    #p2 = randomPlayer.RandomPlayer("O", seed)
    #p2 = randomPlayer.RandomPlayer("O", 42)
    p2 = randomPlayer.userPlayer("O")

    # The arguments to game.Game specify the two players, the number of rows, the number of columns
    # and the number of pieces that need to be placed in a line in order to win.
    # g = game.Game(p1, p2, 5, 6, 4)
    # g = game.Game(p1, p2, 5, 6, 3)
    g = game.Game(p1, p2, 4, 5, 3)
    # g = game.Game(p1, p2, 4, 4, 4)
    # g = game.Game(p1, p2, 4, 4, 3)
    # g = game.Game(p1, p2, 6, 7, 4)

# You can pass 'True' to the playGame() method to test your alpha-beta pruning approach, i.e., to make
# player 1 use alpha-beta. If you want player 2 to use alpha-beta you will need to ensure 
# that you create player 2 accordingly. 
    val = g.playGame(False)
    if val == 1:
        wins += 1
    elif val == -1:
        losses += 1
    else:
        draws += 1

end = time.time()
print(f"Runtime (ms): {(end - start) * 10**3} ms")
print(f"Runtime (s): {(end - start)} s")
print(f"Games: {games}")
print(f"Wins: {wins} ({wins / games * 100}%)")
print(f"Draws: {draws} ({draws / games * 100}%)")
print(f"Losses: {losses} ({losses / games * 100}%)")