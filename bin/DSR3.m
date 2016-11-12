function [CYCLES, EVEN, ES, BADPAIRS, ADJ]=DSR3(S_matrix,V_matrix)

% To add: infinity labels, +- entries, etc.

% Construct the incidence matrix of the DSR graph
% Takes as input the stoichiometric matrix S_matrix=\Gamma and V=(Dv) 



[noSpecies, noInteractions] = size(S_matrix);

%set entries for V_matrix to match DSR labels 

for i=1:noSpecies
  for j=1:noInteractions
    if (S_matrix(i,j)*V_matrix(j,i)<0) 
       V_matrix(j,i) = -S_matrix(i,j);
    elseif (V_matrix(j,i)~=0)
       V_matrix(j,i)=sign(V_matrix(j,i))*rand(1);
    end
  end
end



S_matrix = sparse(S_matrix);
V_matrix = sparse(V_matrix);


DSR = zeros(noSpecies+noInteractions, noSpecies+noInteractions);

DSR(1:noSpecies,noSpecies+1:noSpecies+noInteractions) = S_matrix;
DSR(noSpecies+1:noSpecies+noInteractions,1:noSpecies) = -V_matrix;

DSR=DSR';

ADJ=DSR;

% Construct the cycles
[CYCLES, SIGNS] = johnsonCycles(DSR);

%keyboard

% Separate the even cycles and the ES cycles

EVEN = [];

for i=1:length(CYCLES)        
	if (mod(sum(SIGNS{i} > 0) - length(SIGNS{i})/2, 2) == 0)
		EVEN = [EVEN, i];
	end
end

evenLengths = [];
if sum(size(EVEN)) ~= 0
    for i=1:length(EVEN)
        evenLengths = [evenLengths, length(CYCLES{EVEN(i)})];
    end
    
    evenMatrix = [evenLengths; EVEN]';        
    
    evenMatrix = sortrows(evenMatrix);
    
    EVEN = evenMatrix(:,2)';    
    
end

ES = [];

for i=1:length(EVEN)
	labels=[];
	for j=1:length(CYCLES{EVEN(i)})-1
		labels = [labels, abs(DSR(CYCLES{EVEN(i)}(j), CYCLES{EVEN(i)}(j+1)))];		
    end
    
	if (isempty(find(labels == -1)))&&(prod(labels(2:2:end))==prod(labels(1:2:end)))
		ES(end+1) = i;
	end 
end



%keyboard

% Check cycle intersections

BADPAIRS=[];

for k=1:length(EVEN)-1
    for l=(k+1):length(EVEN)

        a = CYCLES{EVEN(k)};
        b = CYCLES{EVEN(l)};
        
 %       keyboard

 %       a = [1    11     2    21     3    14     6    22     5    12     1];
  %      b = [2    21     3    14     8    19     6    22     5    13     2];
        
  %      keyboard
  
  
        intersection = intersect(a, b);
        
    %     keyboard;
        
        if sum(size(intersection))~=0

            compnts={};
            
            for q = 1:length(intersection)
                compnts{intersection(q)} = [intersection(q)];
            end

            for q = 1:length(intersection)

                current = intersection(q);
                nexta = a(find(a==current,1,'first')+1);
                nextb = b(find(b==current,1,'first')+1);
                if (nexta==nextb)&&ismember(nexta, intersection)
                    compnts{current}=[compnts{current}, compnts{nexta}];

                    for r = 1:length(compnts{current})
                        compnts{compnts{current}(r)}=compnts{intersection(q)};
                    end

                end
            end

        % keyboard
            
            compo = {};

            lengthCompo=[];

            for q=1:length(compnts)
                lengthCompo(q)=sum(size(compnts{q}));
            end

            current = 1;

            while (sum(lengthCompo)~=0)&&(current<length(compnts))
                while (lengthCompo(current)==0)&&(current<length(compnts))
                    %                lengthCompo(current)=0;
                    current = current+1;
                end

                if lengthCompo(current)>0
                    compo{end+1}=compnts{current};
                    for r = 1:length(compo{end})
                        lengthCompo(compo{end}(r))=0;
                    end
                    current = current+1;
                end
            end

            compnts = {};
            compnts = compo;



            produs = 1;
            for i=1:length(compnts)
                %display(compnts{i});
                produs = produs*(length(compnts{i})+1);
            end

            if ((mod(produs,2)==1)&(produs~=1))
                lengthUnion = length(union(a,b));

                BADPAIRS=[BADPAIRS;[k,l]];
            end
            
    %        keyboard
            
        end

    end
end

end