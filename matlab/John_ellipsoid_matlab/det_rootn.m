function X = det_rootn(M, t, n)
    import mosek.fusion.*;

    % Create a 2n x 2n PSD matrix variable Y
    Y = M.variable(['Y'], Domain.inPSDCone(2 * n));

    % Extract blocks from Y
    X  = Y.slice([0, 0], [n, n]);               % Top-left block
    Z  = Y.slice([0, n], [n, 2 * n]);           % Top-right block
    DZ = Y.slice([n, n], [2 * n, 2 * n]);       % Bottom-right block

    % Constrain Z to be lower triangular
    for i = 1:n
        for j = i+1:n
            M.constraint(Expr.pick(Z, java.util.Arrays.asList([int32(i-1), int32(j-1)])), ...
                         Domain.equalsTo(0.0));
        end
    end

    % DZ = diag(Z)
    M.constraint(Expr.sub(DZ, Expr.mulElm(Z, Matrix.eye(n))), Domain.equalsTo(0.0));

    % Apply geometric mean cone constraint
    z_diag = DZ.diag();                         % Vector of diagonal entries
    M.constraint(Expr.vstack(z_diag, t), Domain.inPGeoMeanCone());

    % Return the upper-left block X, satisfying det(X)^{1/n} ≥ t
end