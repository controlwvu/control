

function [d_vec, cmpnds] = derivative_vector(filename)

[compounds, lhs, rhs] = human_parser(filename);
Gamma = rhs - lhs;

v_dot = calculate_vdot(lhs);

d_vec = Gamma * v_dot;

cmpnds = repmat(sym("1"), size(lhs,1), 1);
for ii=1:size(lhs,1)
  cmpnds(ii, 1) = cmpnds(ii, 1) * sym(["x_", num2str(ii)]);

end

end