#!/bin/bash
#SBATCH -A b1042             ## account (unchanged)
#SBATCH -p genomics          ## "-p" instead of "-q"
#SBATCH -J mutect2_hg38
#SBATCH --mail-type=FAIL,TIME_LIMIT_90
#SBATCH --mail-user=brian.wray@northwestern.edu
#SBATCH -o "%x.o%j"
#SBATCH -N 1                 ## number of nodes
#SBATCH -n 1                 ## number of cores
#SBATCH -t 30:00:00          ## walltime
#SBATCH --mem=100G

module purge all
module load gatk/4.1.0
module load java/jdk1.8.0_25


sample=CBX112A
reference_dir="/projects/b1012/xvault/REFERENCES/builds/hg38"
bam_dir=analysis/bam_files
outfile=analysis/bam/${sample}_hg38_somatic.vcf.gz

gatk Mutect2 \
	-R ${reference_dir}/genome.fa \
     	-I ${bam_dir}/CBX112A_P2_USE160373L-A1-A55_HJF23DSXX_L1_recalibrated.bam \
	-I ${bam_dir}/CBX112A_P2_USE160373L-A1-A55_HJKGJDSXX_L3_recalibrated.bam \
	-I ${bam_dir}/CBX112A_P2_USE160373L-A1-A55_HJMTYDSXX_L1_recalibrated.bam \
  	--germline-resource ${reference_dir}/bundle/somatic-hg38-af-only-gnomad.hg38.vcf.gz \
	-O $outfile 2> logs/${sample}_mutect2.log