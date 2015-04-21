%Import a .txt file and split it into two vector

%% Close all previous plots
%close all

%% Get data in right format
RC_Input = importdata('parsed_log_4.txt');
Error = RC_Input(2:2:end);
RC_Input(2:2:end) = [];

%% Make time an imaginary thing
l = length(RC_Input);
time = linspace(0,(l-1),l);

%% Get Altitude
Altitude = Error * -1 + 1000;

%% Plot Stuff

%Sub Plot 1
figure()
subplot(1,2,1)
plot(time,RC_Input)

%Sub Plot 2
subplot(1,2,2)
plot(time,Error_Inv)
hold on
plot([0 l],[1000 1000])
xlim([0 l])
ylim([0 1200])