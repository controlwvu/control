

function [d_vec] = derivative_vector2(lhs, rhs)
Gamma = rhs - lhs;
v_dot = calculate_vdot(lhs);
d_vec = Gamma * v_dot;
end