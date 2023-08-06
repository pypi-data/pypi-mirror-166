# Welcome to the Herschlag lab's wrapper for DREEM

This repo is a wrapper for [Joe Yesselman's DREEM module](https://github.com/jyesselm/dreem), that implements the DREEM algorithm developed by the Rouskin lab.

The wrapper allows the user to run DREEM on different samples and to add standardized experimental details to DREEM output.

## Requirements

DREEM package must be in your environment.
You need RNAstructure installed to run RNAstructure, otherwise deactivate this option in the config file.

## Installation

dreem_herschlag is available on PyPi:

```
pip install dreem_herschlag
```

You can also clone this repo and run make:

```
cd [PATH_TO_WHERE_YOU_WANT_THE_REPO]
git clone https://github.com/yvesmartindestaillades/dreem_herschlag
cd dreem_herschlag
make init
```

## Test your installation

### Setup RNAstructure (optional) 
If you want to use RNAstructure, open `test/test_config.yml` and assign `dreem_args/RNAstructure_path` to your path the `RNAstructure/exe`.

### Run

```
cd PATH/TO/REPO
dreem_herschlag --config test/test_config.yml
```

You should get this output:
```
$ dreem_herschlag --config test/test_config.yml
dreem_herschlag --config test/test_config.yml
Checking files
Checking test/resources/samples.csv
Checking samples.csv done

Checking case_1/library.csv
Ignored sequence, not in library_attributes
Checking case_1/library.csv done

Checking files done

Running DREEM
dreem -fq1 test/resources/case_1/r1.fastq -fq2 test/resources/case_1/r2.fastq -fa test/resources/case_1/ref.fasta --sample case_1 --sample_info temp/samples.csv --library_info temp/case_1/library.csv --overwrite 
[19:27 bit_vector.py run] INFO ran at commandline as: 
[19:27 bit_vector.py run] INFO /Users/ymdt/src/dreem_herschlag/bin/dreem -fq1 test/resources/case_1/r1.fastq -fq2 test/resources/case_1/r2.fastq -fa test/resources/case_1/ref.fasta --sample case_1 --sample_info temp/samples.csv --library_info temp/case_1/library.csv --overwrite
[19:27 bit_vector.py validate_files] INFO fasta file: test/resources/case_1/ref.fasta exists
[19:27 bit_vector.py validate_files] INFO fastq file: test/resources/case_1/r1.fastq exists
[19:27 bit_vector.py validate_files] INFO fastq2 file: test/resources/case_1/r2.fastq exists
[19:27 bit_vector.py validate_files] INFO two fastq files supplied, thus assuming paired reads
[19:27 bit_vector.py get_parameters] INFO -o/--overwrite supplied, will overwrite previous results with same name
[19:27 bit_vector.py build_directories] INFO building directory structure
[19:27 mapper.py __init__] INFO bowtie2 2.4.5 detected!
[19:27 mapper.py __init__] INFO fastqc v0.11.9 detected!
[19:27 mapper.py __init__] INFO trim_galore 0.6.6 detected!
[19:27 mapper.py __init__] INFO cutapt 1.18 detected!
[19:27 mapper.py __run_command] INFO running fastqc
[19:27 mapper.py __run_command] INFO fastqc ran without errors
[19:27 mapper.py __run_command] INFO running trim_galore
[19:27 mapper.py __run_command] INFO trim_galore ran without errors
[19:27 mapper.py __run_command] INFO running bowtie2-build
[19:27 mapper.py __run_command] INFO bowtie2-build ran without errors
[19:27 mapper.py __run_command] INFO running bowtie2 alignment
[19:27 mapper.py __run_command] INFO bowtie2 alignment ran without errors
[19:27 mapper.py __run_bowtie_alignment] INFO results for bowtie alignment: 
2500 reads; of these:
  2500 (100.00%) were paired; of these:
    168 (6.72%) aligned concordantly 0 times
    2331 (93.24%) aligned concordantly exactly 1 time
    1 (0.04%) aligned concordantly >1 times
93.28% overall alignment rate
[19:27 mapper.py __run_picard_bam_convert] INFO Converting BAM file to SAM file format
[19:27 mapper.py __run_command] INFO running picard BAM conversion
[19:27 mapper.py __run_command] INFO picard BAM conversion ran without errors
[19:27 mapper.py __run_picard_sort] INFO sorting BAM file
[19:27 mapper.py __run_command] INFO running picard BAM sort
[19:27 mapper.py __run_command] INFO picard BAM sort ran without errors
[19:27 mapper.py run] INFO finished mapping!
[19:27 bit_vector.py run] INFO starting bitvector generation
[19:27 bit_vector.py __run_command] INFO running picard SAM convert
[19:27 bit_vector.py __run_command] INFO picard SAM convert ran without errors
[19:27 bit_vector.py run] INFO MUTATION SUMMARY:
| name          |   reads |   aligned |   no_mut |   1_mut |   2_mut |   3_mut |   3plus_mut |   sn |
|---------------|---------|-----------|----------|---------|---------|---------|-------------|------|
| mttr-6-alt-h3 |    2332 |     99.96 |    46.42 |   36.81 |   13.21 |    3.05 |        0.04 | 7.76 |

None
DREEM done

transfered mh.p to mh_only/case_1
```

## Run DREEM

### Organize your sequencing files
Your fasta/fastq files organization should look like this:

```
|- /[path_to_data]
     |- samples.csv
     |- library.csv
     |- [some name].fasta
     |- [your_sample_1]_R1_001.fastq.gz
     |- [your_sample_1]_R2_001.fastq.gz
     |- [your_sample_2]_R1_001.fastq.gz
     |- [your_sample_2]_R2_001.fastq.gz
     |- [your_sample_3]_R1_001.fastq.gz
     |- [your_sample_3]_R2_001.fastq.gz
     |- ...
```

### Write additional experimental information files

To add additional experimental information to DREEM's output, you have to create two different types of files, `samples.csv` and `library.csv`.


__*TEMPLATES.CSV*__


Generate templates for `samples.csv`, `library.csv` and `my_config.yml` by running:

```
dreem_herschlag --generate_templates .
```

__*SAMPLES.CSV*__


`samples.csv` contains information about each sample as a whole, such as the temperature or the date. 
Each row of `samples.csv` correspond to a single sample. 
The `sample` column of `samples.csv` must match the `your_sample_#` folders names shown above.
`exp_env` column content MUST BE set to `in_vivo` or `in_vitro`.

Columns description for `samples.csv` can be found by typing:

```
dreem_herschlag --sample_info
```


__*LIBRARY.CSV*__


`library.csv` contains information about each construct in a sample.
There must be one `library.csv` file per sample.
The `name` column of `library.csv` should match the constructs name of the fasta file.

Columns description for `library.csv` can be found by typing:

```
dreem_herschlag --library_info
```

### Fill in config.yml

- Download the `template_config.yml` template at the root of this repo, or generate it with ``dreem_herschlag --generate_templates``
- You may rename your file `my_config.yml` or whatever sounds good to you, so that you don't overwrite it.
- Open the file and follow the fill-in instructions.

### RUN!

```
dreem_herschlag --config my_config.yml
```


Thanks for reading. 
Please contact me at yves@martin.yt for any additional information or to contribute.
