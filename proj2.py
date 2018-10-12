# Programmed by Sean Murren
# March 2015
# proj2.py impliments 3 different search optimization algorithms on
# 3 different functions provided by the instructor 

import math
import random


def hillClimb(varList, func):
	search = True
	current = func(varList)
	
	while search:
		for i in range(len(varList)):
			
			varList[i] += 1
			neighbor = func(varList)
			
			if neighbor < current:
				current = neighbor
				break
			else:
				varList[i] -= 2
				neighbor = func(varList)
				if neighbor < current:
					current = neighbor
					break
				else:
					varList[i] += 1
					if i == len(varList) - 1:
						search = False
	
	printSolution(varList)
	
	return current

def simAnnealing(varList, func, schedule):
	tempList = varList[:]
	current = func(varList)
	T = 2000
	t = 1
	
	while True:
		T = schedule(T, t)
		if T == 0:
			printSolution(varList)
			return current
			
		varList[random.randint(0, len(varList)-1)] += random.choice((-1,1))
		
		next = func(varList)
		dE = next - current
		if dE < 0:
			current = next
			tempList = varList[:]
		else:
			if dE > 0:
				dE *= -1
			if random.random() < math.e**(dE / T):
				current = next
				tempList = varList[:]
		
		varList = tempList[:]
		t += 1
		if t == 50000:
			printSolution(varList)
			return current


def annealingSchedule(temp, time):
	temp *= .9986
	if temp < 0.001:
		temp = 0
	return temp
	

def genetic(listSize, func, rangeLow, rangeHigh):
	populationSize = 1000
	population = []
	newPopulation = []
	cycle = 0
	
	while cycle < 12:  # enough times to get the job done with given functions
		newPopulation = []
		
		while (len(population) != populationSize):  # add 1000 first cycle, 900 new after
			individual = []
			for i in range(listSize):
				individual.append(random.randint(rangeLow, rangeHigh))
			population.append((func(individual), individual))
		
		population.sort(key=lambda i: i[0])  # sort with minimum results first
		population = population[:100]  # remove all but best 100
		
		r = 0.0
		parents = []
		while len(newPopulation) < 50:
			r = random.random()  # 0.0 - 1.0
			index = random.randint(0,99)
			viability = .5 - index * .25
			
			if r <= viability:  # parents for crossover selected by probabilisticly based on viability
				parents.append(population[index])
				
				if len(parents) == 2:
					newIndividual = crossover(parents.pop(), parents.pop())
					newPopulation.append((func(newIndividual), newIndividual))
		
		population += newPopulation
		cycle += 1
		
	population.sort(key=lambda i: i[0])
	
	printSolution(population[0][1])
	
	return population[0][0]
	
	
def crossover(individual1, individual2):
	crossedChild = []  # ONE DIMENSIONAL, contains new var list
	notCrossed = True
	
	index = 0
	for i in range(1, len(individual1[1])+1):
		# pick var value from either parent, does not ensure unique child
		crossedChild.append(random.choice((individual1[1][index], individual2[1][index])))
		index += 1
	
	# RANDOM MUTATION
	r = random.random()
	if r <= .1:  # 10% chance of mutation
		crossedChild[random.randint(0,len(crossedChild)-1)] += random.choice([-1,1])
	
	return crossedChild
	


def printSolution(varList):
	solution = ""
	for v in range(len(varList)):
		solution += "Var[" + str(v) + "] = " + str(varList[v]) + "\n"
	print(solution)


def easy(var):
    x = var[0]
    y = var[1]
    z = var[2]
    k = var[3]
    return ((x-10)**2 + (y+8)**2 + z**2 + k**2)


def medium(var):
    x = var[0] + 100
    y = var[1] + 100
    r = x**2 + y**2
    firstPart = (math.sin(x**2+(3 * y**2))/ (.1 + r))
    secondPart = (x**2 + 5 * (y**2)) * (( math.e ** (1-r))/2)
    return -(firstPart + secondPart)


def hard(var):
    a = int(var[0])
    b = int(var[1])
    c = int(var[2])
    d = int(var[3])
    e = int(var[4])
    f = int(var[5])
    g = int(var[6])
    h = int(var[7])
    i = int(var[8])
    j = int(var[9])
    penalty = 0
    if(a < 1 or a > 3):
        penalty += abs(a-1) * 100
    if(b < 1 or b > 3):
        penalty += abs(b-1) * 100
    if(c < 1 or c > 3):
        penalty += abs(c-1) * 100
    if(d < 1 or d > 3):
        penalty += abs(d-1) * 100
    if(e < 1 or e > 3):
        penalty += abs(e-1) * 100
    if(f < 1 or f > 3):
        penalty += abs(f-1) * 100
    if(g < 1 or g > 3):
        penalty += abs(g-1) * 100
    if(h < 1 or h > 3):
        penalty += abs(h-1) * 100
    if(j < 1 or j > 3):
        penalty += abs(j-1) * 100
    if(i < 1 or i > 3):
        penalty += abs(i-1) * 100

    if(a == b):
        penalty += 1
    if(a == c):
        penalty += 1
    if(c == d):
        penalty += 1
    if(b == c):
        penalty += 1
    if(d == e):
        penalty += 1
    if(d == f):
        penalty += 1
    if(f == g):
        penalty += 1
    if(e == g):
        penalty += 1
    if(g == h):
        penalty += 1
    if(h == i):
        penalty += 1
    if(h == j):
        penalty += 1
    if(i == j):
        penalty += 1

    return penalty


def main():
	# Hill-climb #######################################
	varList = [0,50,0,-10]
	minimum = hillClimb(varList, easy)
	print("Hillclimb, easy, min: " + str(minimum) + "\n")
	
	varList = [-1,1]
	minimum = hillClimb(varList, medium)
	print("Hillclimb, medium, min: " + str(minimum) + "\n")
	
	varList = [0,0,0,0,0,0,0,0,0,0]
	minimum = hillClimb(varList, hard)
	print("Hillclimb, hard, min: " + str(minimum) + "\n")
	
	# simulated annealing ###############################
	varList = [0,50,0,-10]
	minimum = simAnnealing(varList, easy, annealingSchedule)
	print("Simulated Annealing, easy, min: " + str(minimum) + "\n")
	
	varList = [-1,1]
	minimum = simAnnealing(varList, medium, annealingSchedule)
	print("Simulated Annealing, medium, min: " + str(minimum) + "\n")

	varList = [0,0,0,0,0,0,0,0,0,0]
	minimum = simAnnealing(varList, hard, annealingSchedule)
	print("Simulated Annealing, hard, min: " + str(minimum) + "\n")
	
	# genetic algorithm #################################
	rangeLow = -10
	rangeHigh = 10
	varListSize = 4
	minimum = genetic(varListSize, easy, rangeLow, rangeHigh)
	print("Genetic Algorithm, easy, min: " + str(minimum) + "\n")
	
	rangeLow = -100
	rangeHigh = 100
	varListSize = 2
	minimum = genetic(varListSize, medium, rangeLow, rangeHigh)
	print("Genetic Algorithm, medium, min: " + str(minimum) + "\n")
	
	rangeLow = 0
	rangeHigh = 4
	varListSize = 10
	minimum = genetic(varListSize, hard, rangeLow, rangeHigh)
	print("Genetic Algorithm, hard, min: " + str(minimum) + "\n")
	
	# End main
	
main()