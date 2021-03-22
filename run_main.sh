module purge all
module load python-anaconda3/2019.10

for i in `head -n 1 data/reads/fileBases.txt | cut -f 1 -d _ | sort | uniq`; do 
	python3 mutect2_script_builder.py -s $i; 
done
