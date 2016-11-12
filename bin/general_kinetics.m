

function [V_gen] = general_kinetics (lhs_matrix)

num_of_reactions = size(lhs_matrix, 2);
num_of_compounds = size(lhs_matrix, 1);

counter = 1;

V_gen = repmat(sym("0"), num_of_reactions, num_of_compounds);
for ii=1:num_of_reactions
    for jj=1:num_of_compounds
        if lhs_matrix(jj,ii)
            V_gen(ii,jj) = sym(["x_", num2str(counter), "^1"]);
            counter = counter + 1;
        else 
            V_gen(ii,jj) = sym("0");
        end
    end
end

end