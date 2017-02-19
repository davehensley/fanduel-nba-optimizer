# NBA Optimizer
#
# by Dave Hensley
#
# Edited by Steven Demmler (sedemmler@gmail.com)
# Picks an ideal fantasy NBA team using a modified knapsack algorithm
#
# Usage: python nba-optimizer.py players.csv
#
from ortools.linear_solver import pywraplp
import sys
import csv

salary_cap = 60000


def get_position_number(name):
    return {
        'Center': 0,
        'Point Guard': 1,
        'Power Forward': 2,
        'Shooting Guard': 3,
        'Small Forward': 4
    }[name]


def main(a, y):
    solver = pywraplp.Solver('CoinsGridCLP', pywraplp.Solver.CBC_MIaED_INTEGER_PROGRAMMING)

    range_c = range(len(a[0]))
    range_pg = range(len(a[1]))
    range_pf = range(len(a[2]))
    range_sg = range(len(a[3]))
    range_sf = range(len(a[4]))

    take_c = [solver.IntVar(0, 1, 'take_c[%i]' % j) for j in range_c]
    take_pg = [solver.IntVar(0, 1, 'take_pg[%i]' % j) for j in range_pg]
    take_pf = [solver.IntVar(0, 1, 'take_pf[%i]' % j) for j in range_pf]
    take_sg = [solver.IntVar(0, 1, 'take_sg[%i]' % j) for j in range_sg]
    take_sf = [solver.IntVar(0, 1, 'take_sf[%i]' % j) for j in range_sf]

    teams_c = []
    teams_pg = []
    teams_pf = []
    teams_sg = []
    teams_sf = []

    for teamNumber in range(0, 29):
        teams_c.insert(teamNumber, solver.Sum([(a[0][i][3] == teamNumber + 1) * take_c[i] for i in range_c]))
        teams_pg.insert(teamNumber, solver.Sum([(a[1][i][3] == teamNumber + 1) * take_pg[i] for i in range_pg]))
        teams_pf.insert(teamNumber, solver.Sum([(a[2][i][3] == teamNumber + 1) * take_pf[i] for i in range_pf]))
        teams_sg.insert(teamNumber, solver.Sum([(a[3][i][3] == teamNumber + 1) * take_sg[i] for i in range_sg]))
        teams_sf.insert(teamNumber, solver.Sum([(a[4][i][3] == teamNumber + 1) * take_sf[i] for i in range_sf]))

    value_c = solver.Sum([a[0][i][1] * take_c[i] for i in range_c])
    value_pg = solver.Sum([a[1][i][1] * take_pg[i] for i in range_pg])
    value_pf = solver.Sum([a[2][i][1] * take_pf[i] for i in range_pf])
    value_sg = solver.Sum([a[3][i][1] * take_sg[i] for i in range_sg])
    value_sf = solver.Sum([a[4][i][1] * take_sf[i] for i in range_sf])

    salray_c = solver.Sum([a[0][i][2] * take_c[i] for i in range_c])
    salray_pg = solver.Sum([a[1][i][2] * take_pg[i] for i in range_pg])
    salray_pf = solver.Sum([a[2][i][2] * take_pf[i] for i in range_pf])
    salray_sg = solver.Sum([a[3][i][2] * take_sg[i] for i in range_sg])
    salray_sf = solver.Sum([a[4][i][2] * take_sf[i] for i in range_sf])

    solver.Add(salray_c + salray_pg + salray_pf + salray_sg + salray_sf <= y)

    solver.Add(solver.Sum(take_c[i] for i in range_c) == 1)
    solver.Add(solver.Sum(take_pg[i] for i in range_pg) == 2)
    solver.Add(solver.Sum(take_pf[i] for i in range_pf) == 2)
    solver.Add(solver.Sum(take_sg[i] for i in range_sg) == 2)
    solver.Add(solver.Sum(take_sf[i] for i in range_sf) == 2)

    # max 4 x per team
    for i in range(0, 29):
        solver.Add(teams_c[i] + teams_pg[i] + teams_pf[i] + teams_sg[i] + teams_sf[i] <= 4)

    solver.maximize(value_c + value_pg + value_pf + value_sg + value_sf)
    solver.Solve()
    assert solver.VerifySolution(1e-7, True)
    print('Solved in', solver.wall_time(), 'milliseconds!', "\n")
    salary = 0

    for i in range_c:
        if take_c[i].SolutionValue():
            salary += a[0][i][2]
            print(a[0][i][0], '(C): ${:,d}'.format(a[0][i][2]), '(' + str(a[0][i][1]) + ')')

    for i in range_pg:
        if take_pg[i].SolutionValue():
            salary += a[1][i][2]
            print(a[1][i][0], '(PG): ${:,d}'.format(a[1][i][2]), '(' + str(a[1][i][1]) + ')')

    for i in range_pf:
        if take_pf[i].SolutionValue():
            salary += a[2][i][2]
            print(a[2][i][0], '(PF): ${:,d}'.format(a[2][i][2]), '(' + str(a[2][i][1]) + ')')

    for i in range_sg:
        if take_sg[i].SolutionValue():
            salary += a[3][i][2]
            print(a[3][i][0], '(SG): ${:,d}'.format(a[3][i][2]), '(' + str(a[3][i][1]) + ')')

    for i in range_sf:
        if take_sf[i].SolutionValue():
            salary += a[4][i][2]
            print(a[4][i][0], '(SF): ${:,d}'.format(a[4][i][2]), '(' + str(a[4][i][1]) + ')')

    print("\n", 'Total: ${:,d}'.format(salary), '(' + str(solver.Objective().Value()) + ')')


if len(sys.argv) < 2:
    print('Usage:', sys.executable, sys.argv[0], 'players.csv')
    sys.exit(1)

team = [[], [], [], [], []]


with open('players.csv') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        team[get_position_number(row['Subposition'])].append(
            [row['Name'], float(row['Value']), int(row['Salary']), int(row['Team'])]
        )


main(team, salary_cap)
