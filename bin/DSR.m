
function [CYCLES, EVEN, ES, BADPAIRS, ADJ]=debug(filename)
%function [S_matrix, V_matrix]=readSVFile(filename)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Reading the data file
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%filename = 'mat.dat';

fid = fopen(filename);

line_data = fgetl(fid);

line_string = deblank(sprintf(line_data, '%s'));

while (strcmp(line_string, 'S MATRIX') == 0)
	line_data = fgetl(fid);
	line_string = deblank(sprintf(line_data, '%s'));
end

line_data = fgetl(fid);

S = [];
V = [];

line_string = sprintf(line_data, '%s'); % tries to parse string   
split_data = strsplit(line_string,  " ");

while (strcmp(line_string, 'V MATRIX') == 0)       
temp=[];
	
   for i=1:length(split_data)
		if (strcmp(split_data(i),'') == 0)
			temp = [temp, str2num(deblank(split_data(i)){1,1})];
		end			
   end
     
   S = [S; temp];

   line_data = fgetl(fid);  

    line_string = sprintf(line_data, '%s'); % tries to parse string   
    split_data = strsplit(line_string, " ");
end

line_data = fgetl(fid);

while (line_data ~= -1)   % makes sure its not eof
   line_string = sprintf(line_data, '%s'); % tries to parse string   
   split_data = strsplit(line_string, " ");

   
      temp=[];
      
   for i=1:length(split_data)
		if (strcmp(split_data(i), '') == 0)
			temp = [temp,str2num(deblank(split_data(i)){1,1})];
		end			
   end   
	V = [V; temp];
        
	line_data = fgetl(fid); % reads one line of the file   
end

fclose(fid);
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Analyze the DSR graph
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

[CYCLES, EVEN, ES, BADPAIRS, ADJ]=DSR3(S,transpose(V));

e1=false; e2=false;

if (sum(size(ES))<sum(size(EVEN))) 
   e1=true;
end
if (sum(size(BADPAIRS))>0)
   e2=true;
end

if and(!e1, !e2)
  fprintf(stdout(),"DSR test successful: Condition * holds! The system satisfies condition <a title=\"IC2''\" href=\"http://reaction-networks.net/wiki/CoNtRol#Injectivity_condition_2.27.27_.28IC2.27.27.29\">IC2''</a>. It is \"accordant\" and its fully open extension is injective on the nonnegative orthant. It does not admit multiple positive nondegenerate equilibria for general kinetics.\n")

else fprintf(stdout(),"DSR test inconclusive. This test alone can not determine whether or not system is accordant, namely whether its fully open extension admits multiple nonnegative equilibria.\n")  
end
 
