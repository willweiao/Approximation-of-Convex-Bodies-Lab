function [P_mat, c_vec] = lownerjohn_outer(X)
    % Inputs:
    %   X : m x n matrix, where each row is a point in R^n
    % Outputs:
    %   P_mat : shape matrix of the outer ellipsoid (n x n)
    %   c_vec : center of the ellipsoid (1 x n)

    import mosek.fusion.*;

    [m, n] = size(X);
    M = Model('lownerjohn_outer');
    M.setLogHandler(java.io.PrintWriter(System.out, true));

    % Variable: t > 0
    t = M.variable('t', 1, Domain.greaterThan(0.0));

    % Variable: shape matrix P via det_rootn
    P = det_rootn(M, t, n);  % P in R^{n x n}

    % Variable: center c ∈ R^n
    c = M.variable('c', [1, n], Domain.unbounded());

    % Build constraint: ||P x_i - c||_2 ≤ 1  for all i
    PX_expr = Expr.mul(Matrix.dense(X), P);  % m x n
    C_rep = Expr.repeat(c, m, 0);            % m x n
    QC_expr = Expr.hstack(Matrix.ones(m, 1), Expr.sub(PX_expr, C_rep));  % m x (n+1)

    M.constraint('qc', QC_expr, Domain.inQCone());

    % Objective: maximize t
    M.objective(ObjectiveSense.Maximize, t);
    M.solve();

    % Extract solution
    P_flat = P.level();        % Length n^2 (row-major)
    P_mat = reshape(P_flat, [n, n]);  % Convert to matrix
    c_vec = c.level();         % Row vector 1 x n

    M.dispose();
end