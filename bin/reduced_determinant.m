
% Run the main function called 'reduced_determinant'
% with the filename as input
% This method will call the parser and the appropriate methods to covert
% the data and then calculate the reduced determinant.

% This file creates appropriate tags for HTML formatting.


function [reduced_determinant_val] = reduced_determinant(txtName, doMassAction)

% Setup the font.
fprintf(stdout(), "<p style='font-family: monospace;'>\n");

% Parse the file
[compounds, lhs, rhs] = human_parser(txtName);
Gamma = rhs - lhs;


if doMassAction
    MA = mass_action(lhs);
    fprintf(stdout(), "<br/><br/>    Reduced Determinant Using Mass Action<br/><br/><br/>\n");
    reduced_determinant_val = reduced_determinant_calc(Gamma, MA);
else 
    V = general_kinetics(lhs);
    fprintf(stdout(), "<br/><br/>    Reduced Determinant Using General Kinetics<br/><br/><br/>\n");
    reduced_determinant_val = reduced_determinant_calc(Gamma, V);
end
disp(reduced_determinant_val);


% End the formatting.
fprintf(stdout(), "\n</p><br/><br/><br/>\n");
end




%% Completed
%   This function takes two arguments, the V and Gamma,
%   and computes the reduceddeterminant
function [reduced_determinant_val] = reduced_determinant_calc(Gamma, V)
r = rank(Gamma);
n = size(Gamma, 1);
m = size(Gamma, 2);
product = Gamma * V;
reduced_determinant_val = sym("0");
combos = nchoosek(1:n, r);

% take all different arrangements of prinicpal minors
for ii=1:size(combos, 1)
  reduced_determinant_val = det(product(combos(ii, :),
          combos(ii, :))) + reduced_determinant_val;
end

end
