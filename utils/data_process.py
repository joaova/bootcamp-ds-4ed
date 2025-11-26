import pandas as pd
import numpy as np
import gurobipy as gp

from random import seed

def find_weights(df_test):

    seed(20220209) # reproducibility

    # Garantir que o índice seja do tipo datetime
    df_test.index = pd.to_datetime(df_test.index)

    # Criar os pontos de corte trimestrais (4 períodos)
    quarters = pd.date_range(start=df_test.index.min(), end=df_test.index.max(), periods=5)  # 5 porque gera 4 intervalos

    # Criar os subconjuntos trimestrais
    quarters_data = {
        "Q1": df_test.loc[(df_test.index >= quarters[0]) & (df_test.index < quarters[1])],
        "Q2": df_test.loc[(df_test.index >= quarters[1]) & (df_test.index < quarters[2])],
        "Q3": df_test.loc[(df_test.index >= quarters[2]) & (df_test.index < quarters[3])],
        "Q4": df_test.loc[(df_test.index >= quarters[3]) & (df_test.index <= quarters[4])]
    }

    return quarters_data

def index_tracking(quarters_data, mkt_index,max_assets, current_train, df_test, time):

    i = 1
    portfolio_history = {}  # para armazenar pesos
    returns_history = {}    # para armazenar retornos trimestrais do portfólio

    # para cada trimestre
    for q_name, df_quarter in quarters_data.items():
        # Adiciona trimestre ao conjunto de treino
        current_train = pd.concat([current_train, df_quarter])

        # Separa dados
        r_mkt = current_train[mkt_index]
        r_it = current_train.drop(mkt_index, axis=1)
        tickers = list(r_it.columns)
            
        # Create an empty model
        m = gp.Model('gurobi_index_tracking')

        # PARAMETERS 
        # w_i: the i_th stock gets a weight w_i 
        w = pd.Series(m.addVars(tickers, 
                                lb = 0,
                                ub = 1,
                                vtype = gp.GRB.CONTINUOUS), 
                    index=tickers)
        # z_i: the i_th stock gets a binary z_i
        z = pd.Series(m.addVars(tickers,
                                vtype = gp.GRB.BINARY),
                        index=tickers)

        # CONSTRAINTS
        # sum(w_i) = 1: portfolio budget constrain
        m.addConstr(w.sum() == 1, 'port_budget')
        # w_i <= z_i: w_i can only have a value > 0 if z_i > 0 (or z_i = 1 in this case)
        for i_ticker in tickers:
            m.addConstr(w[i_ticker] <= z[i_ticker], 
                        f'dummy_restriction_{i_ticker}')  
        # sum(z_i) <= max_assets: number of assets constraint
        m.addConstr(z.sum() <= max_assets, 'max_assets_restriction')
        
        m.update()
        
        my_error = r_it.dot(w) - r_mkt
        
        # set objective function, minimize the sum of squared tracking errors between portfolio and market returns
        m.setObjective(
            gp.quicksum(my_error.pow(2)), 
            gp.GRB.MINIMIZE)     

        print(f"Starting the optimization process for the {i} trimester ")
        print(f"It will take {time} seconds to it's conclusion")
        
        # Optimize model
        m.setParam('OutputFlag', 0)
        m.setParam('TimeLimit', time) # in secs
        #m.setParam('MIPGap', 0.05) # in secs
        m.optimize()
        
        # --- Resultados ---
        weights = {t: w[t].X for t in tickers if w[t].X > 0.001}
        portfolio_history[q_name] = weights  # guarda o portfólio

        print(f"✅ {len(weights)} ações selecionadas:")
        for t, val in sorted(weights.items(), key=lambda x: -x[1]):
            print(f"   {t}: {val*100:.2f}%")

        i = i + 1

        # --- Avaliar o desempenho no trimestre ---
        if q_name in quarters_data:
            r_mkt_test = df_quarter[mkt_index]
            r_it_test = df_quarter.drop(mkt_index, axis=1)

            # calcula o retorno diário do portfólio
            port_ret = r_it_test[list(weights.keys())].dot(np.array(list(weights.values())))
            # aramenaz
            returns_history[q_name] = port_ret

    # --- Pós-processamento: retorno acumulado ---
    portfolio_cumret = pd.concat(returns_history).groupby(level=1).sum().cumsum()
    market_cumret = df_test[mkt_index].cumsum()
    print("Fim do processo de otimização")

    return portfolio_cumret,market_cumret