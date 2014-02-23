set autoscale

set xtic auto
set ytic auto
set xlabel "Generation"
set ylabel "Fitness"

set terminal pdf
set out "omx-80-1-0.01.pdf"

plot "omx-80-1-0.01" using 1:2 title "Max" with lines linecolor rgb "blue",\
	 "omx-80-1-0.01" using 1:3:4 with yerrorbars linecolor rgb "green" title "Avg"
