# NBA Optimizer
#
# by Dave Hensley
#
# Picks an ideal fantasy NBA team using a modified knapsack algorithm
#
# Usage: python nba-optimizer.py players.csv

salaryCap = 60000

def getPositionNumber(name):
    return {
        'Center': 0,
        'Point Guard': 1,
        'Power Forward' : 2,
        'Shooting Guard': 3,
        'Small Forward': 4
    }[name]

def main(players, salaryCap):
    solver = pywraplp.Solver('CoinsGridCLP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    rangeC = range(len(players[0]))
    rangePG = range(len(players[1]))
    rangePF = range(len(players[2]))
    rangeSG = range(len(players[3]))
    rangeSF = range(len(players[4]))

    takeC = [solver.IntVar(0, 1, 'takeC[%i]' % j) for j in rangeC]
    takePG = [solver.IntVar(0, 1, 'takePG[%i]' % j) for j in rangePG]
    takePF = [solver.IntVar(0, 1, 'takePF[%i]' % j) for j in rangePF]
    takeSG = [solver.IntVar(0, 1, 'takeSG[%i]' % j) for j in rangeSG]
    takeSF = [solver.IntVar(0, 1, 'takeSF[%i]' % j) for j in rangeSF]

    teamsC = []
    teamsPG = []
    teamsPF = []
    teamsSG = []
    teamsSF = []

    for teamNumber in range(0, 29):
        teamsC.insert(teamNumber, solver.Sum([(players[0][i][3] == teamNumber + 1) * takeC[i] for i in rangeC]))
        teamsPG.insert(teamNumber, solver.Sum([(players[1][i][3] == teamNumber + 1) * takePG[i] for i in rangePG]))
        teamsPF.insert(teamNumber, solver.Sum([(players[2][i][3] == teamNumber + 1) * takePF[i] for i in rangePF]))
        teamsSG.insert(teamNumber, solver.Sum([(players[3][i][3] == teamNumber + 1) * takeSG[i] for i in rangeSG]))
        teamsSF.insert(teamNumber, solver.Sum([(players[4][i][3] == teamNumber + 1) * takeSF[i] for i in rangeSF]))

    valueC = solver.Sum([players[0][i][1] * takeC[i] for i in rangeC])
    valuePG = solver.Sum([players[1][i][1] * takePG[i] for i in rangePG])
    valuePF = solver.Sum([players[2][i][1] * takePF[i] for i in rangePF])
    valueSG = solver.Sum([players[3][i][1] * takeSG[i] for i in rangeSG])
    valueSF = solver.Sum([players[4][i][1] * takeSF[i] for i in rangeSF])

    salaryC = solver.Sum([players[0][i][2] * takeC[i] for i in rangeC])
    salaryPG = solver.Sum([players[1][i][2] * takePG[i] for i in rangePG])
    salaryPF = solver.Sum([players[2][i][2] * takePF[i] for i in rangePF])
    salarySG = solver.Sum([players[3][i][2] * takeSG[i] for i in rangeSG])
    salarySF = solver.Sum([players[4][i][2] * takeSF[i] for i in rangeSF])

    solver.Add(salaryC + salaryPG + salaryPF + salarySG + salarySF <= salaryCap)

    solver.Add(solver.Sum(takeC[i] for i in rangeC) == 1)
    solver.Add(solver.Sum(takePG[i] for i in rangePG) == 2)
    solver.Add(solver.Sum(takePF[i] for i in rangePF) == 2)
    solver.Add(solver.Sum(takeSG[i] for i in rangeSG) == 2)
    solver.Add(solver.Sum(takeSF[i] for i in rangeSF) == 2)

    # Max 4 players per team
    for i in range(0, 29):
        solver.Add(teamsC[i] + teamsPG[i] + teamsPF[i] + teamsSG[i] + teamsSF[i] <= 4)

    solver.Maximize(valueC + valuePG + valuePF + valueSG + valueSF)
    solver.Solve()
    assert solver.VerifySolution(1e-7, True)
    print 'Solved in', solver.wall_time(), 'milliseconds!', "\n"
    salary = 0

    for i in rangeC:
        if (takeC[i].SolutionValue()):
            salary += players[0][i][2]
            print players[0][i][0], '(C): ${:,d}'.format(players[0][i][2]), '(' + str(players[0][i][1]) + ')'

    for i in rangePG:
        if (takePG[i].SolutionValue()):
            salary += players[1][i][2]
            print players[1][i][0], '(PG): ${:,d}'.format(players[1][i][2]), '(' + str(players[1][i][1]) + ')'

    for i in rangePF:
        if (takePF[i].SolutionValue()):
            salary += players[2][i][2]
            print players[2][i][0], '(PF): ${:,d}'.format(players[2][i][2]), '(' + str(players[2][i][1]) + ')'

    for i in rangeSG:
        if (takeSG[i].SolutionValue()):
            salary += players[3][i][2]
            print players[3][i][0], '(SG): ${:,d}'.format(players[3][i][2]), '(' + str(players[3][i][1]) + ')'

    for i in rangeSF:
        if (takeSF[i].SolutionValue()):
            salary += players[4][i][2]
            print players[4][i][0], '(SF): ${:,d}'.format(players[4][i][2]), '(' + str(players[4][i][1]) + ')'

    print "\n", 'Total: ${:,d}'.format(salary), '(' + str(solver.Objective().Value()) + ')'

import sys

if (len(sys.argv) < 2):
    print 'Usage:', sys.executable, sys.argv[0], 'players.csv'
    sys.exit(1)

players = [[], [], [], [], []]

import csv
with open(sys.argv[1], 'rb') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        players[getPositionNumber(row['Subposition'])].append(
            [row['Name'], float(row['Value']), int(row['Salary']), int(row['Team'])]
        )

from ortools.linear_solver import pywraplp

main(players, salaryCap)
