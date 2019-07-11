# This script contains code to run analysis on a series of ludo games.
# Initially written to run analysis to determine the outcome of the bet between
# Pip and Anna.

from ludoSim import *
import timeit
import shelve
import numpy as np
import matplotlib.pyplot as plt

numGames = 10000

boards = [] # empty list which will contain a Board object for each game run
player1Wins = 0 # represents player1's wins
scores = np.zeros((2,10000)) # represents scores for both players for all games
hits = np.zeros((2,10000)) # represents hits for both players for all games
sixes = np.zeros((2,10000)) # represents number of rolled sixes for both players for all games

# run 10000 games:
tic = timeit.default_timer()
for game in range(0,numGames):
    boards.append(Board())
    b = boards[game]
    b.playGame()

    # see who won
    if b._Board__winner == 1:
        player1Wins+=1

    # get scores
    scores[0][game] = b._Board__scores[0]
    scores[1][game] = b._Board__scores[1]
    
    hits[0][game] = b._Board__hits[0]
    hits[1][game] = b._Board__hits[1]

    # get number of rolled sixes
    p0Turns = [i for i,x in enumerate(b._Board__playerTurns) if x==0]
    numP0Sixes = len([i for i in p0Turns if b._Board__rolls[i]==6])
    p1Turns = [i for i,x in enumerate(b._Board__playerTurns) if x==1]
    numP1Sixes = len([i for i in p1Turns if b._Board__rolls[i]==6])
    sixes[0][game] = numP0Sixes
    sixes[1][game] = numP1Sixes

    
toc = timeit.default_timer()
player1WinRatio = player1Wins/numGames
print('It took %f seconds to run %i games' % ((toc-tic), numGames))
print('Winning ratio of player 1: %f' % (player1WinRatio))


# to save data:
# filename = 'ludoSim/analysis/gamesResults.out'
# shelf = shelve.open(filename, 'n')
# shelf['boards'] = globals()['boards']
# shelf['scores'] = globals()['scores']
# shelf['hits'] = globals()['hits']
# shelf['sixes'] = globals()['sixes']
# shelf['numGames'] = globals()['numGames']
# shelf['player1Wins'] = globals()['player1Wins']
# shelf['player1WinRatio'] = globals()['player1WinRatio']
# shelf.close()

# to load data, run:
# shelf = shelve.open(filename)
# globals()['boards'] = shelf['boards]
# globals()['scores'] = shelf['scores']
# globals()['hits'] = shelf['hits']
# globals()['sixes'] = shelf['sixes']
# globals()['numGames'] = shelf['numGames']
# globals()['player1Wins'] = shelf['player1Wins']
# globals()['player1WinRatio'] = shelf['player1WinRatio']
# shelf.close()

# to plot data:

# set figure and axis:
fig, ax = plt.subplots()
ax.set_title('Game Results')
ax.set_ylabel('Relative Counts')
xlabels = ('Wins', 'Scores', 'Hits', 'Rolls of 6')
x = np.arange(len(xlabels)) # arrange the labels evenly on x-axis
barWidth = 0.25 # width of bars in graph
ax.set_xticks(x)
ax.set_xticklabels(xlabels)

# get data:
player1ScoresRatio = np.sum(scores[1]) / np.sum(scores)
player1HitsRatio = np.sum(hits[1]) / np.sum(hits)
player1SixesRatio = np.sum(sixes[1]) / np.sum(sixes)
player1Stats = [player1WinRatio, player1ScoresRatio, player1HitsRatio, player1SixesRatio]
player0Stats = [1-player1WinRatio, 1-player1ScoresRatio, 1-player1HitsRatio, 1-player1SixesRatio]

# plot data:
p0Bar = ax.bar(x - barWidth/2, player0Stats, barWidth, label='player0')
p1Bar = ax.bar(x + barWidth/2, player1Stats, barWidth, label='player1')
ax.legend((p0Bar, p1Bar), ('player0', 'player1'))





















