#!/bin/bash

awk 'BEGIN { t = true }   # Initialize t outside the AWK script
function chr(n) {
    return sprintf("%c", n);
}
NR==1 {print "Vehicle Number, SoC, Mileage(in m), Charging Time(in min), SoH, Driver Name, Flag"}    # For the first line, print the entire line along with "Flag"
 {                    # For lines numbered less than 50
    if (NF==6) {
        t=true
        if ($1~'/AG/') {
            printf "%s %s %s %s %s ", $1, $5, $3, $4, $2
            alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            reverse="ZYXWVUTSRQPONMLKJIHGFEDCBA"
            for (i=1; i<=length($6); i++) {
                m = substr($6, i, 1)  # Extract each character from field $6
                if (match(alphabet, toupper(m))) {
                    z = RSTART  # Start position of matched substring in alphabet
                    n = substr(reverse, z, 1)  # Get corresponding character from reverse
                } else {
                    n = m  # If character is not in alphabet, keep it unchanged
                }
                printf "%c", n   # Print corresponding character
            }
	    if ($2==0 && $3!=0){
                        printf " Fake"}

              # Print newline after processing each line
        } else {
            printf "%s %s %s %s %s ", $1, $2, $3, $4, $5
            alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            reverse="ZYXWVUTSRQPONMLKJIHGFEDCBA"
            for (i=1; i<=length($6); i++) {
                m = substr($6, i, 1)  # Extract each character from field $6
                if (match(alphabet, toupper(m))) {
                    z = RSTART  # Start position of matched substring in alphabet
                    n = substr(reverse, z, 1)  # Get corresponding character from reverse
                } else {
                    n = m  # If character is not in alphabet, keep it unchanged
                }
                printf "%c", n   # Print corresponding character
            }
            if ($2==0 && $3!=0){
                        printf " Fake"}

              # Print newline after processing each line
        }
	printf "\n"
    }
}' $1
