%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Casian Pantea, Imperial College London
%% 20 May 2013
%%
%% Octave function
%%
%% Implementation of Johnson's algorithm for enumerating all cycles in a digraph:
%% SIAM J. Comput. 4(1) 1975 
%%
%% input:  ASD - adjacency matrix with labels
%% output: CYCLES - array of cycles 
%%         SIGNS  - array of sign sequences for edges of each cycle 
%%
%% Remarks: only e-cycles of length 2 are included
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [CYCLES, SIGNS] = johnsonCycles(ASD)

global AD;
AD = ASD;

global n;
n = length(AD);

global A;
A=cell(1,n);

global CYCLE;
CYCLE= {};

global SIGN;
SIGN = {};

global stack1;
stack1=[];

global s;
s=1;

global SCC;
SCC =cell(1,n);
SCC{1}=1:n;

global SCC1;

%new_options=set_matlab_bgl_default(struct('full2sparse',1)); 

global VAD;
VAD = AD;

global B;

global blocked;
 
while s<n
    
%    disp(VAD)
    indices = strConnComp(VAD);
    
    SCC1={};
    
    
%    disp('s=')
%    disp(s)

%    disp(SCC{s})
    
    
    for i=1:length(VAD)       
      
%      disp('i=')
%      disp(i)
%      disp(SCC{s})
%      disp(indices)
%      find(indices==indices(i))

      
      
      SCC1{SCC{s}(i)} = SCC{s}(find(indices==indices(i)));
    end
    
    for i=SCC{s}
        SCC{i}=SCC1{i};
    end
    
    minIndex=0;
    
    for i=s:n        
        if length(SCC{i})>1 
           minIndex=i; 
           break 
        end
    end
       
    if minIndex > 0
        s=minIndex;
        VAD=AD(SCC{s},SCC{s});
        
        for i=1:length(SCC{s})            
            A{SCC{s}(i)}=SCC{s}(find(VAD(i,:)~=0));
        end    
            
            blocked = zeros(1,n);
            B=cell(1,n);           
            dummy=CIRCUIT(s);  
    else
        s=n;
    end      
    
    done=0;
    
    while (~done)&(s<n) 
      
        s=s+1;
            
        SCC{s}=intersect(SCC{s},s:n);
        
        if (s==n)||(length(SCC{s})>1)
            done=1;
        end
    end
    
    VAD=AD(SCC{s},SCC{s});    
    
end

CYCLES=CYCLE;
SIGNS=SIGN;

function UNBLOCK(u)
    global B;
    global blocked;
    blocked(u)= false;
    for w = B{u}             
        B{u}=setdiff(B{u},[w]);
        if blocked(w)
            UNBLOCK(w);
        end
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function CIRC = CIRCUIT(v)

global AD;

global n;
global A;

global CYCLE;
global SIGN;

global stack1;
global s;

global SCC;

global B;

global blocked;


    f = false;
        
    stack1=[stack1,v];
   
    blocked(v)=true;
           
    for w = A{v}
      
 %     disp('w=')
 %     disp(w)
 %     disp('s='); disp(s)
      
        if w==s

  %          disp('here w=s')
          
            stack2 = [stack1,s];
            signs = [];
            for i=1:length(stack2)-1
                signs = [signs, sign(AD(stack2(i),stack2(i+1)))];
            end             
            
%            if ((length(signs)>2)||(sum(abs(signs)==[1 1])~=2))
            if ((length(signs)>2)||(sum(signs)==0))
                CYCLE{end+1}=stack2;
                SIGN{end+1}=signs;
            end
            
            f = true;
         
        elseif ~blocked(w)
          
            if CIRCUIT(w)
                f=true;
            end
        end
    end
 
    if f
        UNBLOCK(v);
    else
        for w = A{v} 
            if ~ismember(v, B{w}) 
                B{w}=union(B{w},[v]); 
            end
        end
    end
      
    stack1=stack1(1:end-1);
    CIRC = f;
     
end

    
end
