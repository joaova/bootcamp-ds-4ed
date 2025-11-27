import gurobipy as gp
import pandas as pd
import numpy as np
from random import seed

def find_quarters(df_test):

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

import gurobipy as gp
import pandas as pd
import numpy as np

def index_tracking(quarters_data, mkt_index, max_assets, current_train, df_test, time_limit):
    portfolio_history = {} 
    returns_history = {} 
    
    # Cópia do treino para não afetar execuções futuras
    train_data = current_train.copy()

    for q_name, df_quarter in quarters_data.items():
        # 1. Atualiza janela de treino
        train_data = pd.concat([train_data, df_quarter])

        # Separa dados
        r_mkt = train_data[mkt_index]
        r_it = train_data.drop(mkt_index, axis=1)
        tickers = list(r_it.columns)
            
        # Modelo Gurobi
        m = gp.Model('index_tracking')
        
        # Variáveis
        w = pd.Series(m.addVars(tickers, lb=0, ub=1, vtype=gp.GRB.CONTINUOUS), index=tickers)
        z = pd.Series(m.addVars(tickers, vtype=gp.GRB.BINARY), index=tickers)

        # Restrições
        m.addConstr(w.sum() == 1, 'budget')
        m.addConstr(z.sum() <= max_assets, 'cardinality')
        
        for t in tickers:
            m.addConstr(w[t] <= z[t]) 
            m.addConstr(w[t] >= 0.01 * z[t]) # Peso mínimo de 1% se ativo

        # Função Objetivo
        diff = r_it.dot(w) - r_mkt
        m.setObjective(gp.quicksum(diff * diff), gp.GRB.MINIMIZE)    

        m.setParam('OutputFlag', 0)
        m.setParam('TimeLimit', time_limit)
        m.optimize()
        
        # --- Salvar Resultados ---
        if m.SolCount > 0:
            current_weights = {t: w[t].X for t in tickers if w[t].X > 1e-4}
        else:
            print(f"⚠️ Sem solução ótima para {q_name}")
            current_weights = {t: 1.0/len(tickers) for t in tickers}

        portfolio_history[q_name] = current_weights
        
        # Calcula retorno do trimestre
        r_it_quarter = df_quarter.drop(mkt_index, axis=1)
        asset_names = list(current_weights.keys())
        asset_values = np.array(list(current_weights.values()))
        
        daily_ret = r_it_quarter[asset_names].dot(asset_values)
        returns_history[q_name] = daily_ret
        
        print(f"Trimestre {q_name}: {len(current_weights)} ativos.")

    # --- CORREÇÃO DO ERRO AQUI ---
    # Concatena criando MultiIndex (Q1, Data)
    full_portfolio_returns = pd.concat(returns_history)
    
    # Remove o primeiro nível (Q1, Q2...) para ficar apenas com a Data
    full_portfolio_returns = full_portfolio_returns.droplevel(0)
    
    # Agora o índice é compatível com df_test
    market_returns = df_test.loc[full_portfolio_returns.index, mkt_index]
    
    return full_portfolio_returns, market_returns