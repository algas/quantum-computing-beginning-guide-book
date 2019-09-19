import sys
import math
import random
import pyqubo

def divide_number(n):
    r = random.randint(0, n)
    return (n-r, r)

def divide_element(xs, count):
    if count <= 0:
        return xs
    index = random.randint(0, len(xs)-1)
    n = xs.pop(index)
    (a,b) = divide_number(n)
    xs.extend([a,b])
    return divide_element(xs, count-1)

def create_problem(n):
    if not isinstance(n, int):
        return
    a = [i for i in divide_element([n], int(math.sqrt(n))) if i > 0]
    b = [i for i in divide_element([n], int(math.sqrt(n))) if i > 0]
    problem = a + b
    random.shuffle(problem)
    return problem

def solve(numbers):
    qbits = pyqubo.Array.create('x', len(numbers), vartype='BINARY')
    H = sum([(2*q - 1)*n for n, q in zip(numbers, qbits)])**2
    model = H.compile()
    qubo, offset = model.to_qubo()
    return pyqubo.solve_qubo(qubo)

def check_solution(solution, numbers):
    a = [n for i,n in enumerate(numbers) if solution['x[{}]'.format(i)] == 0]
    b = [n for i,n in enumerate(numbers) if solution['x[{}]'.format(i)] == 1]
    sa = sum(sorted(a)) 
    sb = sum(b)
    if sa == sb:
        return 'Correct answer! {} = {}'.format(sa, sb)
    return 'Wrong answer {} != {}'.format(sa, sb)

def main():
    args = sys.argv
    numbers = [2,7,5]
    if len(args) > 1:
        numbers = create_problem(int(args[1]))
    solution = solve(numbers)
    print(solution)
    print(check_solution(solution, numbers))

if __name__ == '__main__':
    main()
