read a b c f1 f2 <<< "$(awk -F", " '{
        a=$1
        b=$2
        c=$3
        f1=$4
        f2=$5
        print a,b,c,f1,f2
}' $1)"

# Reading coefficients from inital.txt
read -r a b c f1 f2 <<<"$(cat "$1" | tr -d ',')"
#echo "Coefficients: a=$a, b=$b, c=$c, f1=$f1, f2=$f2"
if [[ -z $a || -z $b || -z $c || -z $f1 || -z $f2 ]]; then
	echo "Error: Null parameter must not be provided in initial.txt.Please type all 5"
	exit 1
fi

#Check if there are 2 command line arguments
if [ "$#" -ne 2 ]; then
	echo "Usage: $0 <file1> <file2>"
	exit 1
fi


read t <<< "$(awk 'NR == 1 {
        t = $1
        print t
}' $2)"

awk -v f1="$f1" -v f2="$f2" -v a="$a" -v b="$b" -v c="$c" -v t="$t" 'NR > 1 && NR < t + 2 {
        test = f2
	sum = (c*f1 + b*f2)/a
        for (i = 4; i <= $1; i++) {
           temp = sum
           sum = (c*test + b*sum) / a
           test = temp
        }
        print sum
}' testcases.txt



 
