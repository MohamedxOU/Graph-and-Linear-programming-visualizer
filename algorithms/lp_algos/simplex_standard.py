import numpy as np

def standard_simplex(c, A, b, maximize=True):
    """
    Standard Simplex algorithm for LPs with only <= constraints and all b >= 0.
    Args:
        c: Objective coefficients (list or 1D np.array)
        A: Constraint coefficients (2D list or np.array)
        b: RHS values (list or 1D np.array)
        maximize: True for maximization, False for minimization
    Returns:
        dict: {
            'optimal_value': float or None,
            'solution': np.array or None,
            'status': 'optimal', 'infeasible', 'unbounded', or error message,
            'iterations': int,
            'tableau_history': list of tableaus (for debugging)
        }
    """
    try:
        c = np.array(c, dtype=float)
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        
        if len(A.shape) != 2:
            return {'optimal_value': None, 'solution': None, 'status': 'A must be 2D matrix', 'iterations': 0}
        
        m, n = A.shape
        
        # Validate inputs
        if len(c) != n:
            return {'optimal_value': None, 'solution': None, 'status': 'Dimension mismatch: c and A', 'iterations': 0}
        
        if len(b) != m:
            return {'optimal_value': None, 'solution': None, 'status': 'Dimension mismatch: b and A', 'iterations': 0}

        # Check all b >= 0 (required for standard form)
        if np.any(b < 0):
            return {'optimal_value': None, 'solution': None, 'status': 'Negative RHS detected - use Two-Phase method', 'iterations': 0}

        # Convert to minimization if needed
        obj_coeffs = -c if maximize else c

        # Set up initial tableau
        # Tableau structure: [A | I | b]
        #                   [c | 0 | 0] (for minimization)
        tableau = np.zeros((m + 1, n + m + 1))
        
        # Constraint rows: [A | I | b]
        tableau[:m, :n] = A
        tableau[:m, n:n+m] = np.eye(m)  # Identity matrix for slack variables
        tableau[:m, -1] = b
        
        # Objective row: [c | 0 | 0] (for minimization)
        tableau[m, :n] = obj_coeffs
        tableau[m, n:n+m] = 0  # Coefficients for slack variables
        tableau[m, -1] = 0  # Initial objective value
        
        # Initial basis: slack variables (indices n to n+m-1)
        basis = list(range(n, n + m))
        
        iterations = 0
        max_iter = 1000
        tableau_history = [tableau.copy()]
        
        while iterations < max_iter:
            iterations += 1
            
            # Check optimality: for minimization, optimal if all coefficients >= 0
            obj_row = tableau[m, :n+m]  # Objective coefficients (excluding RHS)
            
            if np.all(obj_row >= -1e-10):  # Optimal (with numerical tolerance)
                break
            
            # Choose entering variable (most negative coefficient for minimization)
            entering = np.argmin(obj_row)
            
            # Check for unboundedness
            entering_col = tableau[:m, entering]
            if np.all(entering_col <= 1e-10):
                status = 'unbounded' if maximize else 'infeasible'
                return {'optimal_value': None, 'solution': None, 'status': status, 'iterations': iterations}
            
            # Ratio test to find leaving variable
            ratios = np.full(m, np.inf)
            for i in range(m):
                if entering_col[i] > 1e-10:
                    ratios[i] = tableau[i, -1] / entering_col[i]
            
            if np.all(ratios == np.inf):
                status = 'unbounded' if maximize else 'infeasible'
                return {'optimal_value': None, 'solution': None, 'status': status, 'iterations': iterations}
            
            leaving = np.argmin(ratios)
            
            # Update basis
            basis[leaving] = entering
            
            # Pivot operation
            pivot_element = tableau[leaving, entering]
            
            if abs(pivot_element) < 1e-10:
                return {'optimal_value': None, 'solution': None, 'status': 'Degenerate pivot', 'iterations': iterations}
            
            # Scale pivot row
            tableau[leaving, :] /= pivot_element
            
            # Eliminate other entries in entering column
            for i in range(m + 1):
                if i != leaving and abs(tableau[i, entering]) > 1e-10:
                    factor = tableau[i, entering]
                    tableau[i, :] -= factor * tableau[leaving, :]
            
            tableau_history.append(tableau.copy())
        
        if iterations >= max_iter:
            return {'optimal_value': None, 'solution': None, 'status': 'Maximum iterations exceeded', 'iterations': iterations}
        
        # Extract solution
        solution = np.zeros(n)
        for i, var_index in enumerate(basis):
            if var_index < n:  # Original variable (not slack)
                solution[var_index] = tableau[i, -1]
        
        # Get optimal value
        optimal_value = -tableau[m, -1] if maximize else tableau[m, -1]
        
        return {
            'optimal_value': optimal_value,
            'solution': solution,
            'status': 'optimal',
            'iterations': iterations,
            'tableau_history': tableau_history,
            'final_basis': basis
        }
        
    except Exception as e:
        return {'optimal_value': None, 'solution': None, 'status': f'Error: {str(e)}', 'iterations': 0}

