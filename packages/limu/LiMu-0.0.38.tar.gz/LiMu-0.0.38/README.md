
Tool to analyse images of cleared and trypan blue stained leaves to assess leaf damage.

limu_original.py is the program used for the original publication.

limu.py is updated to be somewhat flexible with project parameters outside the script itself. It might need tweaking to suit your project though.

Currently only works with Canon .cr2 raw images. If you have other types please let me know and I might add other formats.

    usage: limu [-h] [-p PROJECT] [-i INDIR] [-v] [-r]

    Tool to analyse images of cleared and troptophan stained leaves to assess leaf damage.

    optional arguments:
      -h, --help            show this help message and 

      -p PROJECT, --project PROJECT
                            path to projects directory, if not supplied one will
                            be requested interactively. If limu.conf file found in
                            current working directory, this will be used

      -i INDIR, --input-dir INDIR
                            path to infile root directory

      -v, --verbose         Print more stuff

      -r, --recalculate     Force recalculation, NOT IMPLEMENTED


Mulaosmanovic, E., Lindblom, T.U.T., Bengtsson, M., Windstam, S.T., Mogren, L., Marttila, S., Stützel, H., Alsanius, B.W., 2020. High-throughput method for detection and quantification of lesions on leaf scale based on trypan blue staining and digital image analysis. Plant Methods 16, 62. https://doi.org/10.1186/s13007-020-00605-5

Full source is available at 
[https://gitlab.com/thorgil/limu](https://gitlab.com/thorgil/limu)
