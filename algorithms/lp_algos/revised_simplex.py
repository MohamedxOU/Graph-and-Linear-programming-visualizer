import numpy as np

def revised_simplex(c, A, b, maximize=True, max_iter=1000):
    """
    Revised Simplex algorithm for standard form LPs (Ax <= b, x >= 0, b >= 0).
    Args:
        c: Objective coefficients (1D array)
        A: Constraint coefficients (2D array)
        b: RHS values (1D array)
        maximize: True for maximization, False for minimization
    Returns:
        dict: {
            'optimal_value': float or None,
            'solution': np.array or None,
            'status': 'optimal', 'infeasible', 'unbounded', or error message,
            'iterations': int
        }
    """
    try:
        c = np.array(c, dtype=float)
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        m, n = A.shape

        if np.any(b < 0):
            return {'optimal_value': None, 'solution': None, 'status': 'Negative RHS detected', 'iterations': 0}

        # Add slack variables
        A_slack = np.hstack([A, np.eye(m)])
        c_slack = np.concatenate([c if maximize else -c, np.zeros(m)])

        # Initial basis: slack variables
        basis = list(range(n, n + m))
        non_basis = list(range(n))

        x = np.zeros(n + m)
        iterations = 0

        while iterations < max_iter:
            iterations += 1
            B = A_slack[:, basis]
            N = A_slack[:, non_basis]
            c_B = c_slack[basis]
            c_N = c_slack[non_basis]

            # Solve for basic variables
            try:
                B_inv = np.linalg.inv(B)
            except np.linalg.LinAlgError:
                return {'optimal_value': None, 'solution': None, 'status': 'Singular basis', 'iterations': iterations}

            x_B = B_inv @ b
            x[:] = 0
            for i, bi in enumerate(basis):
                x[bi] = x_B[i]

            # Compute reduced costs
            lambda_ = c_B @ B_inv
            reduced_costs = c_N - lambda_ @ N

            # Check for optimality
            if maximize:
                if np.all(reduced_costs <= 1e-10):
                    break
                entering_idx = np.argmax(reduced_costs)
            else:
                if np.all(reduced_costs >= -1e-10):
                    break
                entering_idx = np.argmin(reduced_costs)

            entering = non_basis[entering_idx]
            d = B_inv @ A_slack[:, entering]

            if np.all(d <= 1e-10):
                return {'optimal_value': None, 'solution': None, 'status': 'unbounded', 'iterations': iterations}

            # Ratio test
            ratios = np.array([x_B[i] / d[i] if d[i] > 1e-10 else np.inf for i in range(m)])
            leaving_idx = np.argmin(ratios)
            leaving = basis[leaving_idx]

            # Update basis
            basis[leaving_idx] = entering
            non_basis[entering_idx] = leaving

        solution = x[:n]
        optimal_value = c @ solution if maximize else -c @ solution
        return {
            'optimal_value': optimal_value,
            'solution': solution,
            'status': 'optimal',
            'iterations': iterations
        }
    except Exception as e:
        return {'optimal_value': None, 'solution': None, 'status': f'Error: {str(e)}', 'iterations': 0}