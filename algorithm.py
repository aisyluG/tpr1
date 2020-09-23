import numpy as np
from prettytable import PrettyTable

def algorithm(states, strategys, n, probabilitys, yields):
    probability_matrices = probabilitys
    yield_matrices = yields
    # probability_matrices = np.array([[[1, 0], [0.1, 0.9]],
    #                         [[1, 0], [0.33, 0.67]],
    #                          [[1, 0], [0.33, 0.67]]])
    # yield_matrices = np.array([[[8.68, 0], [2.43, 3.29]],
    #                         [[16.83, 0], [14.11, 7.63]],
    #                          [[3.23, 0], [10.07, 7.86]]])
    expected_return = np.zeros((states, strategys))
    for state in range(states):
        for strategy in range(strategys):
            expected_return[state][strategy] = sum(probability_matrices[strategy, state]*
                                                    yield_matrices[strategy, state])
    print(expected_return)
    total_expected_return = np.zeros((n, strategys, states))
    max_total_exp_return = np.zeros((n, states))
    opt_strategys = np.zeros((n, states))
    for stage in range(n):
        for state in range(states):
            for strategy in range(strategys):
                x = probability_matrices[strategy, state]*max_total_exp_return[stage - 1]
                # print(expected_return[state, strategy] + x)
                total_expected_return[stage, strategy, state] = \
                   expected_return[state, strategy] + sum(x)
            max_total_exp_return[stage, state] = max(total_expected_return[stage, :, state])
            opt_strategys[stage, state] = list(total_expected_return[stage, :, state]).index(max_total_exp_return[stage, state])
    print(max_total_exp_return)
    report = '<p style="margin-left: 50px;"><h3>Отчет</h3></p>'
    report += '<p style="margin-left: 50px;"><strong>Ожидаемые доходности:</strong></p>'
    for state in range(states):
        report += f'<p style="margin-left: 20px;">При выходе из <i>состояния {state + 1}</i></p>'
        for strategy in range(strategys):
            report += f'<p style="margin-left: 70px;">при выборе <i>стратегии {strategy + 1}</i> равна ' \
                      f'<b>{expected_return[state, strategy]}</b></p>'

    for i in range(n):
        report += f'<p style="margin-left: 50px;"><h4>Этап моделирования №{i + 1}</h4></p>\n'
        for state in range(states):
            report += f'<p style="margin-left: 20px;">Полный ожидаемый доход для <i>состояния {state + 1}</i>:</p>\n'
            for strategy in range(strategys):
                report += f'<p style="margin-left: 70px;">при выборе <i>стратегии {strategy + 1}</i> равен ' \
                          f'<b>{total_expected_return[i, strategy, state]}</b></p>'
            report += (f'<p style="margin-left: 20px;">В <i>состоянии {state + 1}</i> оптимальным является выбор '
                       f'<i>стратегии {int(opt_strategys[i, state] + 1)}.</i>' +
            f' Поддержание этой стратегии принесет прибыль в размере <b>{max_total_exp_return[i, state]}</b> ден. ед.</p>')
    return report, opt_strategys