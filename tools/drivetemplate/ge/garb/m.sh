#!/bin/bash

# Read the sorted f.txt file and find gaps in the sequence
prev=0
while read -r line; do
  # Extract the number (assuming the number is at the beginning of the line)
  num=$(echo "$line" | awk '{print $1}')
  
  # Compare the current number with the previous one
  if (( num > prev + 1 )); then
    # If there's a gap, output the missing numbers to f1.txt
    for ((i = prev + 1; i < num; i++)); do
      echo "$i" >> f1.txt
    done
  fi
  
  # Update prev to the current number
  prev=$num
done < f.txt
