import pyqubo
import dimod

def knapsack(W, weights, costs):
    xs = pyqubo.Array.create('x', shape=(len(weights)), vartype='BINARY')

    ## 価値の制約
    X = -sum([c*x for (x, c) in zip(xs, costs)])

    ## OneHot Encoding
    a = pyqubo.OneHotEncInteger('y', 1, W, strength=100)

    ## 重さの制約
    Y = (a - sum([w*x for (x, w) in zip(xs, weights)]))**2

    ## ハミルトニアン（コスト関数）
    H = X + pyqubo.Constraint(Y, label="one_hot")

    ## モデル作成とQUBOの生成
    model = H.compile()
    q, offset = model.to_qubo()
    # print(q)

    ## 解答
    sampleset = dimod.ExactSolver().sample_qubo(q)
    solution, broken, e  = model.decode_dimod_response(sampleset, topk=1)[0]
    return solution

def get_solution(solution):
    return [k for k, v in solution['x'].items() if v == 1]

def get_weight(solution, weights):
    return sum([weights[k] for k, v in solution['x'].items() if v == 1])

def get_cost(solution, costs):
    return sum([costs[k] for k, v in solution['x'].items() if v == 1])


def print_results(solution, weights, costs):
    # 結果の表示
    print('solution = {}'.format(get_solution(solution)))
    print('weight = {}'.format(get_weight(solution, weights)))
    print('total cost = {}'.format(get_cost(solution, costs)))

def main():
    ## 入力データ
    W = 15
    weights = [3,9,6,4]
    costs = [5,6,7,2]

    solution = knapsack(W, weights, costs)
    print_results(solution, weights, costs)

if __name__ == "__main__":
    main()
