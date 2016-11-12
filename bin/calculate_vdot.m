# Creates a vector of the rate of reactions

function [v] = calculate_vdot(lhs)

num_of_reactions = size(lhs, 2);
num_of_compounds = size(lhs, 1);


# Calculate the v dot
v = repmat(sym("1"), num_of_reactions,1);
for rxn=1:num_of_reactions
   
   v(rxn) = v(rxn) * sym(["k_", num2str(rxn), "^1"]);   
   for cmpnd=1:num_of_compounds
       v(rxn) = v(rxn) * sym(["x_", num2str(cmpnd), "^", num2str(lhs(cmpnd, rxn))]);    
   end
end # end loop

end