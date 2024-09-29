#!/bin/bash

SAMPLE="../output/test230322"
FQ1="../data/sample_1.fastq.gz"
FQ2="../data/sample_2.fastq.gz"
BWA="../tools/bwa-mem2-2.0pre2_x64-linux/bwa-mem2"
SAMTOOLS="samtools"
GATK="../tools/gatk-4.5.0.0/gatk" # gatk : python -> python3
REFERENCE="../resource/reference/hg38.chr21.fa"
KNOWN_INDEL="../resource/knownsites/hg38_v0_Homo_sapiens_assembly38.known_indels.chr21.vcf.gz"
READGROUP="@RG\tID:${SAMPLE}\tSM:${SAMPLE}\tPL:platform"
OUTPUT="../output"
THREAD=nproc #12
DBSNP="../resource/knownsites/dbsnp.vcf.gz"
DBSNP2="../resource/knownsites/dbsnp2.vcf.gz"
DBSNP3="../resource/knownsites/dbsnp3.vcf.gz"
DBSNP4="../resource/knownsites/resources_broad_hg38_v0_Homo_sapiens_assembly38.dbsnp138.vcf"
CON_MAP="../resource/knownsites/contig_map.txt"
SAMPLE22="../output/ALL.chr22.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased"
REFERENCE22="../resource/reference/chr22.fa"
#:<<'END'
############################################################################
# Step 1 : fastq->sam ( 25 + 11 = 36 sec -> 11 sec if skip indexing )

## ALIGN
echo "## START: ALIGN - `date`" # index : 25sec
mkdir -p ${OUTPUT}
${BWA} index ${REFERENCE} # skip
echo "## bwa mem start - `date`" # mem : 11sec
${BWA} mem -t ${THREAD} -R ${READGROUP} ${REFERENCE} ${FQ1} ${FQ2} > ${SAMPLE}.mapped.sam
echo "## bwa mem done - `date`"

###########################################################################
# Step 2 : sam->bam ( 1 + 1 + 3 + 2 = 7 sec )

echo "## sam2bam start - `date`" # sam2bam : 1sec
samtools view -Sb ${SAMPLE}.mapped.sam > ${SAMPLE}.mapped.bam
echo "## sam2bam done - `date`"

### sort by read name # sortname : 1sec
${SAMTOOLS} sort -n -o ${SAMPLE}.namesorted.bam ${SAMPLE}.mapped.bam
#echo "## END: ALIGN - `date`"

echo "## START: FIXMATE - `date`" # fixmate : 3sec
### fixmate
${SAMTOOLS} fixmate -m ${SAMPLE}.namesorted.bam ${SAMPLE}.fixmate.bam
${SAMTOOLS} sort -o ${SAMPLE}.fixmate.sorted.bam ${SAMPLE}.fixmate.bam
echo "## END: FIXMATE - `date`"

echo "## START: MARKDUP - `date`" # markdup : 2sec
## MARKDUP
${SAMTOOLS} markdup ${SAMPLE}.fixmate.sorted.bam ${SAMPLE}.markdup.bam
${SAMTOOLS} index ${SAMPLE}.markdup.bam
echo "## END: MARKDUP - `date`"

##############################################################################
# Step 3 : bam->vcf ( 8 + 77 + 3 = 88 sec )

echo "## START: VARIANT CALL - `date`" # baseRecal & applyBQSR : 8sec
## VARIANT CALL
### GATK BaseRecalibrator
##sudo docker run -it broadinstitute/gatk

${GATK} BaseRecalibrator -I ${SAMPLE}.markdup.bam -R ${REFERENCE} --known-sites ${KNOWN_INDEL} -L chr21 -O ${SAMPLE}.recal_data.table

${GATK} ApplyBQSR -R ${REFERENCE} -I ${SAMPLE}.markdup.bam --bqsr-recal-file ${SAMPLE}.recal_data.table -L chr21 -O ${SAMPLE}.recal.bam
#END
echo "## haplotypecaller start - `date`" # haplotypecaller : 1min 17sec / spark : 1min 25sec
### GATK HaplotypeCaller ( gatk --java-options "-Xms4g -Xmx8g -XX:ParallelGCThreads=2" HaplotypeCaller )
${GATK} HaplotypeCaller -R ${REFERENCE} -I ${SAMPLE}.recal.bam -L chr21 -O ${SAMPLE}.g.vcf -ERC GVCF #-- --spark-runner LOCAL --spark-master 'local[*]'
echo "## haplotypecaller done - `date`" # genotypeGVCFs : 3sec

${GATK} GenotypeGVCFs -R ${REFERENCE} -V ${SAMPLE}.g.vcf -L chr21 -O ${SAMPLE}.vcf

echo "## END: VARIANT CALL - `date`"
#END
###########################################################################
## Step 4 : annotation (rsID)
#################################

#bcftools annotate --rename-chrs ${CON_MAP} ${DBSNP} -o ${DBSNP2}
#samtools faidx ${REFERENCE22} ### create fa.fai
#${BWA} index ${REFERENCE22}
#${GATK} CreateSequenceDictionary -R ${REFERENCE22} ### create fa.dict
${GATK} VariantAnnotator -R ${REFERENCE} -V ${SAMPLE}.vcf -O ${SAMPLE}.ann.vcf --dbsnp ${DBSNP4}

