import numpy as np

def two_phase_simplex(c, A, b, constraint_types, maximize=True):
    """
    Two-Phase Simplex algorithm for linear programming with mixed constraints
    
    Args:
        c: Coefficients of the objective function (1D array/list)
        A: Coefficient matrix of constraints (2D array/list)
        b: Right-hand side of constraints (1D array/list)
        constraint_types: List of constraint types ('<=', '=', '>=') for each constraint
        maximize: True for maximization, False for minimization
        
    Returns:
        dict: Solution containing:
            - 'optimal_value': Optimal objective value
            - 'solution': Optimal solution vector
            - 'status': 'optimal', 'infeasible', 'unbounded', or error message
            - 'iterations': Number of iterations
            - 'phase1_iterations': Number of Phase I iterations
            - 'phase2_iterations': Number of Phase II iterations
    """
    try:
        # Convert to numpy arrays
        c = np.array(c, dtype=float)
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        
        # Check for negative RHS values
        for i in range(len(b)):
            if b[i] < 0:
                # Multiply constraint by -1 to make RHS positive
                A[i] = -A[i]
                b[i] = -b[i]
                # Flip constraint type
                if constraint_types[i] == '>=':
                    constraint_types[i] = '<='
                elif constraint_types[i] == '<=':
                    constraint_types[i] = '>='
        
        m, n = A.shape
        
        # Count variables needed
        num_slack = sum(1 for ct in constraint_types if ct == '<=')
        num_surplus = sum(1 for ct in constraint_types if ct == '>=')
        num_artificial = sum(1 for ct in constraint_types if ct in ['=', '>='])
        
        # Build augmented matrix with slack, surplus, and artificial variables
        A_augmented = np.zeros((m, n + num_slack + num_surplus + num_artificial))
        A_augmented[:, :n] = A
        
        # Track variable types and indices
        var_info = {
            'original': list(range(n)),
            'slack': [],
            'surplus': [],
            'artificial': []
        }
        
        col_idx = n
        artificial_indices = []
        initial_basis = []
        
        # Add slack, surplus, and artificial variables
        for i, constraint_type in enumerate(constraint_types):
            if constraint_type == '<=':
                # Add slack variable
                A_augmented[i, col_idx] = 1
                var_info['slack'].append(col_idx)
                initial_basis.append(col_idx)
                col_idx += 1
                
            elif constraint_type == '>=':
                # Add surplus variable (negative slack)
                A_augmented[i, col_idx] = -1
                var_info['surplus'].append(col_idx)
                col_idx += 1
                # Add artificial variable
                A_augmented[i, col_idx] = 1
                var_info['artificial'].append(col_idx)
                artificial_indices.append(col_idx)
                initial_basis.append(col_idx)
                col_idx += 1
                
            elif constraint_type == '=':
                # Add artificial variable only
                A_augmented[i, col_idx] = 1
                var_info['artificial'].append(col_idx)
                artificial_indices.append(col_idx)
                initial_basis.append(col_idx)
                col_idx += 1
        
        # Phase I: Minimize sum of artificial variables
        if artificial_indices:
            print("Starting Phase I: Minimizing artificial variables...")
            
            # Create Phase I objective: minimize sum of artificial variables
            c_phase1 = np.zeros(A_augmented.shape[1])
            for idx in artificial_indices:
                c_phase1[idx] = 1
            
            # Solve Phase I
            phase1_result = simplex_tableau(c_phase1, A_augmented, b, initial_basis, False)
            
            if phase1_result['status'] != 'optimal':
                return {
                    'optimal_value': None,
                    'solution': None,
                    'status': f'phase1_{phase1_result["status"]}',
                    'iterations': phase1_result['iterations'],
                    'phase1_iterations': phase1_result['iterations'],
                    'phase2_iterations': 0
                }
            
            # Check if artificial variables are zero
            if abs(phase1_result['optimal_value']) > 1e-10:
                return {
                    'optimal_value': None,
                    'solution': None,
                    'status': 'infeasible',
                    'iterations': phase1_result['iterations'],
                    'phase1_iterations': phase1_result['iterations'],
                    'phase2_iterations': 0
                }
            
            print(f"Phase I completed in {phase1_result['iterations']} iterations")
            print("Artificial variables successfully eliminated")
            
            # Remove artificial variables from basis if they're basic
            phase1_basis = phase1_result['basis'].copy()
            for i, var in enumerate(phase1_basis):
                if var in artificial_indices:
                    # Find a non-artificial variable to pivot
                    tableau = create_tableau(c_phase1, A_augmented, b, phase1_basis)
                    row = i
                    pivot_col = None
                    
                    # Find first non-zero, non-artificial variable in this row
                    for j, var_idx in enumerate(range(A_augmented.shape[1])):
                        if (var_idx not in artificial_indices and 
                            abs(tableau[row, j]) > 1e-10):
                            pivot_col = j
                            break
                    
                    if pivot_col is not None:
                        # Pivot to remove artificial variable from basis
                        phase1_basis[i] = pivot_col
            
            # Prepare for Phase II
            A_phase2 = np.delete(A_augmented, artificial_indices, axis=1)
            
            # Update basis indices after removing artificial variables
            phase2_basis = []
            for var in phase1_basis:
                if var not in artificial_indices:
                    # Adjust index due to removed artificial variables
                    new_idx = var - sum(1 for art_idx in artificial_indices if art_idx < var)
                    phase2_basis.append(new_idx)
            
            # Ensure we have enough basic variables
            while len(phase2_basis) < m:
                for j in range(A_phase2.shape[1]):
                    if j not in phase2_basis:
                        phase2_basis.append(j)
                        break
            
        else:
            # No artificial variables needed, go directly to Phase II
            A_phase2 = A_augmented
            phase2_basis = initial_basis
            phase1_result = {'iterations': 0}
        
        # Phase II: Solve original problem
        print("Starting Phase II: Solving original problem...")
        
        # Create Phase II objective
        c_phase2 = np.zeros(A_phase2.shape[1])
        c_phase2[:n] = -c if not maximize else c
        
        phase2_result = simplex_tableau(c_phase2, A_phase2, b, phase2_basis, maximize)
        
        if phase2_result['status'] == 'optimal':
            # Extract solution for original variables only
            solution = phase2_result['solution'][:n] if phase2_result['solution'] is not None else None
            optimal_value = phase2_result['optimal_value']
            
            print(f"Phase II completed in {phase2_result['iterations']} iterations")
            print(f"Optimal solution found: {optimal_value}")
        else:
            solution = None
            optimal_value = None
        
        return {
            'optimal_value': optimal_value,
            'solution': solution,
            'status': phase2_result['status'],
            'iterations': phase1_result['iterations'] + phase2_result['iterations'],
            'phase1_iterations': phase1_result['iterations'],
            'phase2_iterations': phase2_result['iterations'],
            'var_info': var_info
        }
        
    except Exception as e:
        return {
            'optimal_value': None,
            'solution': None,
            'status': f'error: {str(e)}',
            'iterations': 0,
            'phase1_iterations': 0,
            'phase2_iterations': 0
        }


def simplex_tableau(c, A, b, initial_basis, maximize=True):
    """
    Solve LP using simplex tableau method
    """
    try:
        m, n = A.shape
        basis = initial_basis.copy()
        non_basis = [i for i in range(n) if i not in basis]
        
        iterations = 0
        max_iter = 1000
        
        while iterations < max_iter:
            iterations += 1
            
            # Create current tableau
            tableau = create_tableau(c, A, b, basis)
            
            # Check for optimality (bottom row of tableau)
            obj_row = tableau[-1, :-1]
            
            if maximize:
                if np.all(obj_row <= 1e-10):  # All coefficients <= 0
                    break
                entering_col = np.argmax(obj_row)
            else:
                if np.all(obj_row >= -1e-10):  # All coefficients >= 0
                    break
                entering_col = np.argmin(obj_row)
            
            # Check for unboundedness
            entering_column = tableau[:-1, entering_col]
            if np.all(entering_column <= 1e-10):
                return {
                    'optimal_value': np.inf if maximize else -np.inf,
                    'solution': None,
                    'basis': basis,
                    'status': 'unbounded',
                    'iterations': iterations
                }
            
            # Minimum ratio test to find leaving variable
            rhs = tableau[:-1, -1]
            ratios = np.where(entering_column > 1e-10, rhs / entering_column, np.inf)
            leaving_row = np.argmin(ratios)
            
            # Update basis
            leaving_var = basis[leaving_row]
            basis[leaving_row] = entering_col
            
            # Update non_basis
            non_basis = [i for i in range(n) if i not in basis]
        
        # Extract solution
        solution = np.zeros(n)
        tableau = create_tableau(c, A, b, basis)
        
        for i, var in enumerate(basis):
            if var < n:
                solution[var] = tableau[i, -1]
        
        optimal_value = tableau[-1, -1]
        if not maximize:
            optimal_value = -optimal_value
        
        return {
            'optimal_value': optimal_value,
            'solution': solution,
            'basis': basis,
            'status': 'optimal',
            'iterations': iterations
        }
        
    except Exception as e:
        return {
            'optimal_value': None,
            'solution': None,
            'basis': [],
            'status': f'error: {str(e)}',
            'iterations': iterations
        }


def create_tableau(c, A, b, basis):
    """
    Create simplex tableau from current basis
    """
    m, n = A.shape
    
    # Create tableau: [A | b; c | 0]
    tableau = np.zeros((m + 1, n + 1))
    tableau[:-1, :-1] = A
    tableau[:-1, -1] = b
    tableau[-1, :-1] = c
    
    # Convert to canonical form using current basis
    B = A[:, basis]
    B_inv = np.linalg.inv(B)
    
    # Update constraint rows
    tableau[:-1, :] = B_inv @ tableau[:-1, :]
    
    # Update objective row
    c_b = c[basis]
    tableau[-1, :-1] = tableau[-1, :-1] - c_b @ B_inv @ A
    tableau[-1, -1] = tableau[-1, -1] - c_b @ B_inv @ b
    
    return tableau


# Updated simplex function that detects constraint types from strings
def simplex(c, A, b, maximize=True, constraint_strings=None):
    """
    Enhanced simplex that can handle constraint strings or default to <= constraints
    """
    if constraint_strings is None:
        # Default to <= constraints for backward compatibility
        constraint_types = ['<='] * len(b)
        return two_phase_simplex(c, A, b, constraint_types, maximize)
    
    # Parse constraint types from strings
    constraint_types = []
    for constraint_str in constraint_strings:
        if '<=' in constraint_str:
            constraint_types.append('<=')
        elif '>=' in constraint_str:
            constraint_types.append('>=')
        elif '=' in constraint_str:
            constraint_types.append('=')
        else:
            constraint_types.append('<=')  # Default
    
    return two_phase_simplex(c, A, b, constraint_types, maximize)


# Example usage:
if __name__ == "__main__":
    # Example with mixed constraints
    c = [3, 2, 1]  # Maximize 3x1 + 2x2 + x3
    A = [
        [1, 1, 1],     # x1 + x2 + x3 = 6
        [2, 1, 0],     # 2x1 + x2 >= 4
        [1, 0, 1]      # x1 + x3 <= 5
    ]
    b = [6, 4, 5]
    constraint_types = ['=', '>=', '<=']
    
    result = two_phase_simplex(c, A, b, constraint_types, maximize=True)
    
    print("=== Two-Phase Simplex Results ===")
    print(f"Status: {result['status']}")
    print(f"Phase I iterations: {result['phase1_iterations']}")
    print(f"Phase II iterations: {result['phase2_iterations']}")
    print(f"Total iterations: {result['iterations']}")
    
    if result['solution'] is not None:
        print(f"Optimal value: {result['optimal_value']:.4f}")
        print("Solution:")
        for i, x in enumerate(result['solution']):
            print(f"  x{i+1} = {x:.4f}")