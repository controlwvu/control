


% need the reactions, and compounds

function [Mass_Action] = mass_action(lhs)


#fprintf(stdout(), "<br/>");
#original_reaction_concentrations
#fprintf(stdout(), "<br/>");

vdot = calculate_vdot(lhs);

num_of_reactions = size(lhs, 2);
num_of_compounds = size(lhs, 1);

Mass_Action = repmat(sym("1"), num_of_reactions, num_of_compounds);
for ii = 1:num_of_reactions
  for jj = 1:num_of_compounds
    Mass_Action(ii,jj) = diff(vdot(ii), ["x_", num2str(jj)]);
    #sym(num2str(V_numeric(ii,jj))) * original_reaction_concentrations(ii);
  end
end

# Get the key set of compounds, i.e. the compound names
#setOfCompounds = compounds.keySet();
#iterator = setOfCompounds.iterator();

#while iterator.hasNext()
#  nextCompound = iterator.next();
#  Mass_Action(:, compounds.get(nextCompound)) = diff(Mass_Action(:, compounds.get(nextCompound)), nextCompound);
#end
# END CALCULATE MASS ACTION



end