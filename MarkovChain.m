%%
% from:
% http://stackoverflow.com/questions/11055410/hidden-markov-model-in-matlab

%% example 1: using hmmgenerate
%# number of states
% N = 11;
N = 4;
sequenceLength = 50

%# some random transition matrix
trans = rand(N,N);
trans = bsxfun(@rdivide, trans, sum(trans,2));

%# fake emission matrix (only one symbol)
emis = ones(N,1);

%# get a sample of length: sequenceLength
[~,states] = hmmgenerate(sequenceLength, trans, emis, 'Symbols',{'state'}, 'Statenames', {'A','B','C','D'});



%% example 2: without stats toolbox
%# number of states
N = 3;

%# transition matrix
trans = rand(N,N);
trans = bsxfun(@rdivide, trans, sum(trans,2));

%# probability of being in state i at time t=0
prior = rand(1,N);
prior = prior ./ sum(prior);

%# generate a sequence of states
len = 100;          %# length of sequence
states = zeros(1,len);
states(1) = randsample(N, 1, true, prior);
for t=2:len
    states(t) = randsample(N, 1, true, trans(states(t-1),:));
end

%# show sequence
stairs(states, 'LineWidth',2)
set(gca, 'YGrid','on', 'YLim',[0 N+1])
xlabel('time'), ylabel('states')
title('sequence of states')