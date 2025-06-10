import numpy as np
from .simplex_standard import standard_simplex

def two_phase_simplex(c, A, b, constraint_types, maximize=True):
    try:
        c = np.array(c, dtype=float)
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        
        if len(A.shape) != 2:
            return {'optimal_value': None, 'solution': None, 'status': 'A must be 2D matrix', 
                   'iterations': 0, 'phase1_iterations': 0, 'phase2_iterations': 0, 'used_standard': False}
        
        m, n = A.shape
        
        if len(c) != n:
            return {'optimal_value': None, 'solution': None, 'status': 'Dimension mismatch: c and A', 
                   'iterations': 0, 'phase1_iterations': 0, 'phase2_iterations': 0, 'used_standard': False}
        
        if len(b) != m or len(constraint_types) != m:
            return {'optimal_value': None, 'solution': None, 'status': 'Dimension mismatch: constraints', 
                   'iterations': 0, 'phase1_iterations': 0, 'phase2_iterations': 0, 'used_standard': False}

        if all(ct == '<=' for ct in constraint_types) and np.all(b >= 0):
            result = standard_simplex(c, A, b, maximize)
            result['phase1_iterations'] = 0
            result['phase2_iterations'] = result['iterations']
            result['used_standard'] = True
            return result

        A_modified = A.copy()
        b_modified = b.copy()
        constraint_types_modified = constraint_types.copy()
        
        for i in range(m):
            if b_modified[i] < 0:
                A_modified[i] = -A_modified[i]
                b_modified[i] = -b_modified[i]
                if constraint_types_modified[i] == '<=':
                    constraint_types_modified[i] = '>='
                elif constraint_types_modified[i] == '>=':
                    constraint_types_modified[i] = '<='

        num_slack = sum(1 for ct in constraint_types_modified if ct == '<=')
        num_surplus = sum(1 for ct in constraint_types_modified if ct == '>=')
        num_artificial = sum(1 for ct in constraint_types_modified if ct in ['>=', '='])
        
        total_vars = n + num_slack + num_surplus + num_artificial
        
        A_aug = np.zeros((m, total_vars))
        A_aug[:, :n] = A_modified
        
        slack_start = n
        surplus_start = n + num_slack
        artificial_start = n + num_slack + num_surplus
        
        slack_idx = slack_start
        surplus_idx = surplus_start
        artificial_idx = artificial_start
        artificial_indices = []
        basis = []
        
        for i, ct in enumerate(constraint_types_modified):
            if ct == '<=':
                A_aug[i, slack_idx] = 1
                basis.append(slack_idx)
                slack_idx += 1
            elif ct == '>=':
                A_aug[i, surplus_idx] = -1
                A_aug[i, artificial_idx] = 1
                basis.append(artificial_idx)
                artificial_indices.append(artificial_idx)
                surplus_idx += 1
                artificial_idx += 1
            elif ct == '=':
                A_aug[i, artificial_idx] = 1
                basis.append(artificial_idx)
                artificial_indices.append(artificial_idx)
                artificial_idx += 1

        if not artificial_indices:
            c_phase2 = np.zeros(total_vars)
            c_phase2[:n] = -c if maximize else c
            
            result = standard_simplex(c_phase2, A_aug, b_modified, maximize=False)
            
            if result['solution'] is not None:
                result['solution'] = result['solution'][:n]
            if maximize and result['optimal_value'] is not None:
                result['optimal_value'] = -result['optimal_value']
            
            result['phase1_iterations'] = 0
            result['phase2_iterations'] = result['iterations']
            result['used_standard'] = False
            return result

        c_phase1 = np.zeros(total_vars)
        for idx in artificial_indices:
            c_phase1[idx] = 1

        tableau = np.zeros((m + 1, total_vars + 1))
        tableau[:m, :total_vars] = A_aug
        tableau[:m, -1] = b_modified
        tableau[m, :total_vars] = c_phase1
        
        for i, basis_var in enumerate(basis):
            if basis_var in artificial_indices:
                tableau[m, :] -= tableau[i, :]
        
        phase1_result = simplex_tableau_solve(tableau, basis.copy(), minimize=True)
        phase1_iterations = phase1_result['iterations']
        
        if phase1_result['status'] != 'optimal' or abs(phase1_result['optimal_value']) > 1e-8:
            return {
                'optimal_value': None,
                'solution': None,
                'status': 'infeasible',
                'iterations': phase1_iterations,
                'phase1_iterations': phase1_iterations,
                'phase2_iterations': 0,
                'used_standard': False
            }

        keep_cols = [i for i in range(total_vars) if i not in artificial_indices]
        A_phase2 = A_aug[:, keep_cols]

        c_phase2 = np.zeros(len(keep_cols))
        for i, col in enumerate(keep_cols):
            if col < len(c):
                c_phase2[i] = -c[col] if maximize else c[col]

        basis_phase2 = []
        for var in phase1_result['basis']:
            if var in artificial_indices:
                continue
            if var in keep_cols:
                basis_phase2.append(keep_cols.index(var))

        if len(basis_phase2) < m:
            result = standard_simplex(c_phase2, A_phase2, b_modified, maximize=False)
            phase2_iterations = result['iterations']
        else:
            tableau_phase2 = np.zeros((m + 1, len(keep_cols) + 1))
            tableau_phase2[:m, :-1] = A_phase2
            tableau_phase2[:m, -1] = b_modified
            tableau_phase2[m, :-1] = c_phase2
            
            for i, basis_var in enumerate(basis_phase2):
                if abs(tableau_phase2[m, basis_var]) > 1e-10:
                    tableau_phase2[m, :] -= tableau_phase2[m, basis_var] * tableau_phase2[i, :]

            result = simplex_tableau_solve(tableau_phase2, basis_phase2.copy(), minimize=not maximize)
            phase2_iterations = result['iterations']

        if result['solution'] is not None:
            result['solution'] = result['solution'][:n]

        result['iterations'] = phase1_iterations + phase2_iterations
        result['phase1_iterations'] = phase1_iterations
        result['phase2_iterations'] = phase2_iterations
        result['used_standard'] = False

        return result

    except Exception as e:
        return {
            'optimal_value': None,
            'solution': None,
            'status': f'Error: {str(e)}',
            'iterations': 0,
            'phase1_iterations': 0,
            'phase2_iterations': 0,
            'used_standard': False
        }


def simplex_tableau_solve(tableau, basis, minimize=True, max_iter=1000):
    m = tableau.shape[0] - 1
    n = tableau.shape[1] - 1
    iterations = 0
    
    while iterations < max_iter:
        iterations += 1
        obj_row = tableau[m, :n]
        if minimize:
            if np.all(obj_row >= -1e-10):
                break
            entering = np.argmin(obj_row)
        else:
            if np.all(obj_row <= 1e-10):
                break
            entering = np.argmax(obj_row)
        
        entering_col = tableau[:m, entering]
        if np.all(entering_col <= 1e-10):
            return {
                'optimal_value': None,
                'solution': None,
                'status': 'unbounded',
                'iterations': iterations,
                'basis': basis
            }
        
        ratios = np.full(m, np.inf)
        for i in range(m):
            if entering_col[i] > 1e-10:
                ratios[i] = tableau[i, -1] / entering_col[i]
        
        leaving_row = np.argmin(ratios)
        basis[leaving_row] = entering
        
        pivot = tableau[leaving_row, entering]
        tableau[leaving_row, :] /= pivot
        
        for i in range(m + 1):
            if i != leaving_row and abs(tableau[i, entering]) > 1e-10:
                tableau[i, :] -= tableau[i, entering] * tableau[leaving_row, :]
    
    solution = np.zeros(n)
    for i, var_idx in enumerate(basis):
        if var_idx < n:
            solution[var_idx] = tableau[i, -1]
    
    optimal_value = tableau[m, -1] if minimize else -tableau[m, -1]
    
    return {
        'optimal_value': optimal_value,
        'solution': solution,
        'status': 'optimal',
        'iterations': iterations,
        'basis': basis
    }
