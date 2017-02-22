# FanDuel NBA Optimizer

This is a simple NBA lineup optimizer for daily fantasy sports (DFS) on FanDuel. It accomplishes this by using a
variation of the [knapsack problem](https://en.wikipedia.org/wiki/Knapsack_problem). The purpose of this project is to
demonstrate one possible use of Google's free [or-tools](https://developers.google.com/optimization) library, and the
code is designed to be easy to read and understand.

## What is an optimizer?
An optimizer takes a set of projections (that is, a [csv file](https://en.wikipedia.org/wiki/Comma-separated_values)
containing a list of NBA players, their salaries, and the number of [fantasy points](https://www.fanduel.com/rules) that
each player is expected to score), and calculates an optimized lineup that maximizes the number of expected points
without exceeding the salary cap. The goal is to assemble the best possible fantasy team for a given day.

## What are the prerequisites?
All you need is [python](https://www.python.org/) (which you probably already have) and Google's
[or-tools](https://developers.google.com/optimization/introduction/installing) library.

## Where do I find projections?
You can get free projections from various DFS websites, such as:
* [NumberFire](http://www.numberfire.com/nba/daily-fantasy/daily-basketball-projections)
* [RotoGrinders](https://rotogrinders.com/projected-stats/nba-player)
* [RotoWire](http://www.rotowire.com/basketball/daily_projections.htm)

However, you will probably have better results (and more fun) by learning to develop your own projection strategies.

## Example usage
```$ python nba-optimizer.py example_2016-01-04.csv```

## Example output
    Solved in 149 milliseconds!

    Karl-Anthony Towns (C): $7,800 (37.9)
    Russell Westbrook (PG): $10,700 (54.3)
    Isaiah Thomas (PG): $8,100 (37.6)
    Serge Ibaka (PF): $6,200 (31.9)
    Frank Kaminsky (PF): $4,000 (29.1)
    Jeremy Lamb (SG): $4,300 (23.7)
    Gerald Green (SG): $3,800 (20.1)
    LeBron James (SF): $9,800 (44.7)
    Marcus Morris (SF): $5,300 (26.8)

    Total: $60,000 (306.1)
