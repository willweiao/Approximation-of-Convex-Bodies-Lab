function [C_mat, d_vec] = lownerjohn_inner(A, b)
    import mosek.fusion.*;

    [~, n] = size(A);
    M = Model('lownerjohn_inner');
    M.setLogHandler(java.io.PrintWriter(System.out, true));

    % Variable: t > 0 (proxy for det(C)^(1/n))
    t = M.variable('t', 1, Domain.greaterThan(0.0));

    % Variable: C (positive definite, via det_rootn), and d (center)
    X = det_rootn(M, t, n);  % X = C in original notation
    d = M.variable('d', n, Domain.unbounded());

    % Build cone constraint: ||A*C||_2 ≤ b - A*d  (elementwise)
    A_expr = Expr.sub(Matrix.dense(b), Expr.mul(Matrix.dense(A), d));
    AC_expr = Expr.mul(Matrix.dense(A), X);
    M.constraint('cone', Expr.hstack(A_expr, AC_expr), Domain.inQCone());

    % Objective: maximize t
    M.objective(ObjectiveSense.Maximize, t);
    M.solve();

    % Output
    C = X.level();  % C is flat array
    d_vec = d.level();

    % Reshape C into matrix
    C_mat = reshape(C, [n, n]);

    M.dispose();
end
