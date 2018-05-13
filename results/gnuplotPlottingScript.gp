#!/usr/bin/local/gnuplot
#startup commands
set xlabel "Generation"
set ylabel "Fitness"

#set xlabel font "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf,50"
#set ylabel font "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf,50"
#set tics font "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf,45"

set xlabel offset 0, -0
set ylabel offset -0,0

#set bmargin 3
#set lmargin 7

clear

#set yrange [0:0.95]
set yrange [0:0.04]
unset key

#output
set term pngcairo size 2048,1024 font ", 30"
set output "average.png"
set title "Average Fitness"
plot "average_fitness.tsv" u 0:1:2 with yerrorbars, "average_fitness.tsv" u 0:1 with lines linewidth 3 linetype 10

set output "best.png"
set title "Best Fitness"
plot "best_fitness.tsv" u 0:1 with lines linewidth 3 linetype 10
