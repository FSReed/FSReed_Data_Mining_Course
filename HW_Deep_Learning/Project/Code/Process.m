load("Code\Result.mat")
table = readtable("Data\Ground_Truth.xlsx");
Ground_Truth = table2array(table);
Displacement = Displacement(:, 1);
clear table % Prologue finished

a = length(Displacement);
b = length(Ground_Truth);
step = b / a;

Ground_Truth = Ground_Truth(1:step:b);
x = (1:a) / 25;
plot(x, Displacement)
hold on
plot(x, Ground_Truth)
