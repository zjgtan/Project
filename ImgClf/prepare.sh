id=0
ls ./kernel | while read line
do
	id=`expr ${id} + 1`
	NewName=`echo $line | sed -e "s/_[0-9]*\./_${id}\./g"`
	mv ./kernel/${line} ./kernel/$NewName
done
