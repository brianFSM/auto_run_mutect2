# auto_run_mutect2
#### author: Brian Wray
#### 17-March-2021

### Description
Given a file with sample names inside, this program will search the filename for information regarding whether or not the sample is tumor or normal, and then generate a mutect2 script that will take into account how many normal and tumor samples there are.
This was started for project Abazeed-QDSC-480, where tumor samples have either "P1" or "P2" in the file name, and the normals have "PBL" in the filename

Here are some example file bases:
CCX205_P1_USE160357L-A37-A3_HJ7YMDSXX_L2
CCX205_P1_USE160357L-A37-A3_HJF23DSXX_L2
CCX205_PBL_USE160388L-A63-A3_HJKF3DSXX_L2
CCX205_PBL_USE160388L-A63-A3_HJMVHDSXX_L2

I can't imagine being able to make this script applicable to the many different ways that researchers name their samples, but I think that by having this general format, i.e. starting the filename with sample_sampleType, that it would be trivial to modify file names to reflect this format.

### Tools used:
- python3


