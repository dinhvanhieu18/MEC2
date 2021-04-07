default_pl=$1
default_pr=$2
packageStrategy=$3
carAppearStrategy=$4
rsuNumbers=$5
xList=$6
yList=$7
zList=$8
resultsFolder=$9

sed -i config.py -e "s/\(default_pl = \).*/\1$default_pl/" \
       -e "s/\(default_pr = \).*/\1$default_pr/" \
       -e "s/\(packageStrategy = \).*/\1$packageStrategy/" \
       -e "s/\(carAppearStrategy = \).*/\1$carAppearStrategy/" \
       -e "s/\(rsuNumbers = \).*/\1$rsuNumbers/" \
       -e "s/\(xList = \).*/\1$xList/" \
       -e "s/\(yList = \).*/\1$yList/" \
       -e "s/\(zList = \).*/\1$zList/" \
       -e "s/\(resultsFolder = \).*/\1$resultsFolder/"

python3 main.py
