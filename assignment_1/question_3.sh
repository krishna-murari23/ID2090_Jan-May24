curl -s $1 > q3temp.txt
cat q3temp.txt | awk '
    NR > 52 {
        printf  $1 ","
        i=2
        while (i<=NF) {
            eqn = (-72 + sqrt(72^2 + 4 * 2 * $i)) / 4
            printf "%c", int(eqn)
            i++
    	}
	printf "\n"
    }
' > output.txt 
cat output.txt
rm q3temp.txt
