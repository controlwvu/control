# input is a filename

# output is left stoichiometric matrix 
# right stoichiometric matrix 

function [compounds, lhs_matrix, rhs_matrix] = human_parser(txtName)
pkg load symbolic;
# [ K, S, reactants, targets, gamma]

num_of_reactions = 0;
num_of_compounds = 0;
reactions = [""];
compounds = javaObject("java.util.Hashtable");

fid = fopen(txtName);
side_flags = [];
# Go through the file, line by line
tline = fgets(fid);
while ischar(tline)
    if isempty(tline) tline = fgets(fid); continue end
    num_of_reactions = num_of_reactions + 1;
    single_reaction = true;
    
    
    tline = strrep(tline, "\n", "");
    spaces = [1 strfind(tline, ' ') length(tline)];
    for ii=1:(length(spaces)-1) 
        
        substring = strtrim(tline((spaces(ii)):(spaces(ii+1))));
    
        if strcmp(substring, "") continue end
        #remove coefficients
        count = 1; #find the coefficient
        while substring(count) <= '9' && substring(count) >= '0' && count <= length(substring)
            count = count + 1;
        end
        #Remove the coefficient you found.
        substring = substring(count:length(substring));
        if strcmp(substring, "<--")
            side_flags = [side_flags, false];
        elseif strcmp(substring, "-->")
            side_flags = [side_flags, true];
        elseif ~(strcmp(substring, "-->") || strcmp(substring, "<-->") || strcmp(substring, "<--") || strcmp(substring, "+")) && isempty(compounds.get(substring))
            num_of_compounds = num_of_compounds + 1;
            compounds.put(substring, num_of_compounds);
        elseif (strcmp(substring, "<-->"))
            single_reaction = false;
            num_of_reactions = num_of_reactions + 1;
            reactions = [reactions; regexprep(tline, '<', ''); regexprep(tline, '>', '')];
            side_flags = [side_flags, true, false];
        end 
 
    end

    if single_reaction
        reactions = [reactions; tline];
    end
    tline = fgets(fid); # Get the next line.
end

fclose(fid);

if length(side_flags) != num_of_reactions
    fprintf(stdout(), "ERROR: FLAGS MISCOUNTED!");
end

# Calculate Matrices
lhs_matrix = zeros(num_of_compounds, num_of_reactions);
rhs_matrix = zeros(num_of_compounds, num_of_reactions);

for rxn=1:num_of_reactions
    curr = reactions(rxn,:);
    spaces = [1 strfind(curr, ' ') length(curr)];
    for ii=1:(length(spaces)-1) 
        substring = strtrim(curr((spaces(ii)):(spaces(ii+1))));

        if strcmp(substring, "") continue end
        #remove coefficients
        count = 1; #find the coefficient
        while substring(count) <= '9' && substring(count) >= '0' && count <= length(substring)
            count = count + 1;
        end
        
        #Get the coefficient
        coefficient = (substring(1:(count-1)));
        if strcmp(coefficient, "") || isempty(coefficient)
            coefficient = '1';
        end
        coefficient = str2num(coefficient);
        
        #Remove the coefficient you found.
        substring = substring(count:length(substring));
        
        compound = compounds.get(substring);
        
        
        if strcmp(substring, "-->")
            side_flags(rxn) = !side_flags(rxn);
            coefficient = 0;
        elseif strcmp(substring, "<--")
            side_flags(rxn) = !side_flags(rxn);
            coefficient = 0;
        elseif strcmp(substring, "<-->")
            fprintf(stdout(), "<br/>Warning: Attempting to parse reversible reactions.<br/>");
        end
        if isempty(compound)
            #do nothing
        elseif side_flags(rxn)
            lhs_matrix(compound, rxn) = coefficient;
        else
            rhs_matrix(compound, rxn) = coefficient;
        end
    end
end

%# Get the key set of compounds, i.e. the compound names
setOfCompounds = compounds.keySet();
iterator = setOfCompounds.iterator();
%#tmp = cell(compounds.size(), 1);
%#count = 1;
tmp= [""];
while iterator.hasNext()
  %#tmp(count) = iterator.next();
  %#count = count + 1;
  tmp = [tmp; iterator.next()];
end
compounds = tmp;

end
