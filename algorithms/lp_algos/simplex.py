import numpy as np

def simplex(c, A, b, maximize=True):
    """
    Simplex algorithm for linear programming
    
    Args:
        c: Coefficients of the objective function (1D array/list)
        A: Coefficient matrix of constraints (2D array/list)
        b: Right-hand side of constraints (1D array/list)
        maximize: True for maximization, False for minimization
        
    Returns:
        dict: Solution containing:
            - 'optimal_value': Optimal objective value
            - 'solution': Optimal solution vector
            - 'status': 'optimal', 'infeasible', or 'unbounded'
            - 'iterations': Number of iterations
    """
    try:
        # Convert to numpy arrays
        c = np.array(c, dtype=float)
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        
        # Convert to standard form (maximization)
        if not maximize:
            c = -c
        
        # Add slack variables
        m, n = A.shape
        A = np.hstack([A, np.eye(m)])
        c = np.concatenate([c, np.zeros(m)])
        
        # Initial basic variables (slack variables)
        basis = list(range(n, n + m))
        non_basis = list(range(n))
        
        iterations = 0
        max_iter = 1000  # Prevent infinite loops
        
        while iterations < max_iter:
            iterations += 1
            
            # Compute reduced costs
            B_inv = np.linalg.inv(A[:, basis])
            c_b = c[basis]
            reduced_costs = c[non_basis] - c_b @ B_inv @ A[:, non_basis]
            
            # Check for optimality
            if np.all(reduced_costs <= 0):
                # Optimal solution found
                x = np.zeros(n + m)
                x[basis] = B_inv @ b
                return {
                    'optimal_value': (1 if maximize else -1) * (c_b @ B_inv @ b),
                    'solution': x[:n],  # Only return original variables
                    'basis': basis,
                    'status': 'optimal',
                    'iterations': iterations
                }
            
            # Select entering variable (Bland's rule to avoid cycling)
            entering = non_basis[np.argmax(reduced_costs > 0)]
            
            # Compute direction
            d = B_inv @ A[:, entering]
            
            # Check for unboundedness
            if np.all(d <= 0):
                return {
                    'optimal_value': np.inf if maximize else -np.inf,
                    'solution': None,
                    'basis': basis,
                    'status': 'unbounded',
                    'iterations': iterations
                }
            
            # Select leaving variable (minimum ratio test)
            ratios = np.where(d > 0, (B_inv @ b) / d, np.inf)
            leaving_idx = np.argmin(ratios)
            leaving = basis[leaving_idx]
            
            # Update basis
            basis[leaving_idx] = entering
            non_basis = [var for var in non_basis if var != entering] + [leaving]
        
        return {
            'optimal_value': None,
            'solution': None,
            'basis': basis,
            'status': 'max_iterations_reached',
            'iterations': iterations
        }
        
    except Exception as e:
        return {
            'optimal_value': None,
            'solution': None,
            'basis': [],
            'status': f'error: {str(e)}',
            'iterations': 0
        }