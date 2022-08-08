* Run `iso_test.sh` to generate isoclass. Change the files inside the script to specify which $K_t$ you're running.
* Run `properedge_test.sh` to generate the all proper edges. Takes in an argument for the number of colors.
* Run `mat_full_test.sh` to generate the `mat` isomorphism matrix. Takes in $SLURM_ARRAY_TASK_ID and the number of colors. Need to change the $$#SBATCH --array = 1-96$$ as required. There are 3000 graphs in a job so the range of array should be 1 to total number of jobs / 3000. Should submit sepearte jobs if the number of tasks in a single job is limited.
* Run `combine.py` to combine all the components of mat into a single file.
