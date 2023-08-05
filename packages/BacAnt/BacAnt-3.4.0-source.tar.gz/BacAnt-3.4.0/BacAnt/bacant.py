#coding:utf-8

import sys,os,re,argparse
import matplotlib
from matplotlib import pyplot as plt 
import numpy as np
from Bio import SeqIO
import shutil
from Bio.Alphabet import generic_dna
from Bio import Seq
from BCBio import GFF
import re
from reportlab.lib import colors
from reportlab.lib.units import cm
import subprocess
import time
import warnings
import codecs
from threading import Thread
from BacAnt.Integron_Finder.scripts.finder import run_integron_finder
from BacAnt.html_data import get_data
import threading
warnings.filterwarnings('ignore')

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nucleotide","-n",help="nucleotide file")
    parser.add_argument("--resultdir","-o",help="resultdir")
    parser.add_argument("--databases","-d",help="multi databases : default=ResDB,IntegronDB,TransposonDB",default="ResDB,IntegronDB,TransposonDB")
    parser.add_argument("--genbank","-g",help="genbank file")
    parser.add_argument("--coverages","-c",help="filtering coverage",default="60,60,60")
    parser.add_argument("--identities","-i",help="filtering identity",default="90,90,90")
    parser.add_argument("--indir","-D",help="input dir")
    parser.add_argument("--path","-p",help="your custom reference databases")
    parser.add_argument("--threads","-t",help="threads number,[default 2]",default=2)
    parser.add_argument("--version","-v",action="store_true")
    args = parser.parse_args()
    if not args.resultdir:
        print("bacant v3.4.0")
        sys.exit()
    if args.version:
        print("bacant v3.4.0")
        sys.exit()
    nucleotide = args.nucleotide
    genbank = args.genbank
    resultdir = args.resultdir.rstrip("/")
    databases = args.databases
    coverages = args.coverages
    identities = args.identities
    indir = args.indir
    path = args.path
    threads = args.threads
    return nucleotide,genbank,resultdir,databases,coverages,identities,indir,path,threads

class myThread (threading.Thread):
    def __init__(self, name_dict,file):
        threading.Thread.__init__(self)
        self.name_dict = name_dict
        self.file = file
    def run(self):
        rename_file(self.name_dict, self.file)

def rename_file(name_dict,file):
    for name1,name2 in name_dict.items():
        if "/" in name2:
            new_name2 = name2.replace("/","\\/")
            os.system("sed -i 's/%s/%s/g' %s"%(name1,new_name2,file))
        else:
            os.system("sed -i 's/%s/%s/g' %s"%(name1,name2,file))


def rename_dir(outdir):
    name_file = os.path.join(outdir,"query_name.list")
    name_dict = {}
    f = open(name_file)
    for lines in f:
        lines = lines.strip()
        if lines:
            data = lines.split("\t")
            name_dict[data[0]] = data[1]
    f.close()
    file_list = []
    for file in os.listdir(outdir):
        if file != "query_name.list":
            infile = os.path.join(outdir,file)
            if os.path.isfile(infile):
                file_list.append(infile)
    thread_num = 3
    total = len(file_list)
    for i in range(0,total,thread_num):
        i1 = i
        i2 = i+thread_num
        thread = []
        if i2>=total:
            for j in range(i1,total):
                thread1 = myThread(name_dict,file_list[j])
                thread.append(thread1)
        else:
           for j in range(i1,i2):
                thread1 = myThread(name_dict,file_list[j])
                thread.append(thread1)
        for thread2 in thread:
            thread2.start()
        for thread3 in thread:
            thread3.join()

#conver gff to genbank
def convert(gff_file, fasta_file,resultdir,gb_file):
    fasta_input = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta", generic_dna))
    gff_iter = GFF.parse(gff_file, fasta_input)
    SeqIO.write(check_gff(fix_ncbi_id(gff_iter)), gb_file, "genbank")

def fix_ncbi_id(fasta_iter):
    """GenBank identifiers can only be 16 characters; try to shorten NCBI.
    """
    for rec in fasta_iter:
        if len(rec.name) > 16 and rec.name.find("|") > 0:
            new_id = [x for x in rec.name.split("|") if x][-1]
            print("Warning: shortening NCBI name %s to %s" % (rec.id, new_id))
            rec.id = new_id
            rec.name = new_id
        yield rec

def check_gff(gff_iterator):
    """Check GFF files before feeding to SeqIO to be sure they have sequences.
    """
    for rec in gff_iterator:
        if isinstance(rec.seq, Seq.UnknownSeq):
            print("Warning: FASTA sequence not found for '%s' in GFF file" % (
                    rec.id))
            rec.seq.alphabet = generic_dna
        yield flatten_features(rec)

def flatten_features(rec):
    """Make sub_features in an input rec flat for output.
    GenBank does not handle nested features, so we want to make
    everything top level.
    """
    out = []
    for f in rec.features:
        cur = [f]
        while len(cur) > 0:
            nextf = []
            for curf in cur:
                out.append(curf)
                if len(curf.sub_features) > 0:
                    nextf.extend(curf.sub_features)
            cur = nextf
    rec.features = out
    return rec

#check software
def check_dependencies():
    blastn_path = shutil.which("blastn")
    if not blastn_path:
        print("blastn not found")
        
    blastp_path = shutil.which("blastp")
    if not blastp_path:
        print("blastp not found")
        
    return blastn_path,blastp_path

#parse input file
def format_fasta(annot,seq,num):
    format_seq=""
    for i, char in enumerate(seq):
        format_seq += char
        if (i + 1) % num == 0:
            format_seq+="\n"
    return annot + format_seq + "\n"

def str_number(n,width=4):
    n = str(n)
    len1 = len(n)
    zero_len = width-len1
    return "0"*zero_len+n

def parse_genbank(genbank,resultdir):
    gb_seqs=SeqIO.parse(genbank,"gb")
    index1 = 0
    for gb_seq in gb_seqs:
        index1 += 1
        new_id = "bacantsequence"+str_number(index1)
        complete_seq=str(gb_seq.seq)
        if gb_seq.id != "":
            complete_annot=">"+gb_seq.id+'\n'
        elif "accessions" in gb_seq.annotations and gb_seq.description != "":
            complete_annot=">"+gb_seq.annotations["accessions"][0] + " " + gb_seq.description + "\n"
        else:
            complete_annot=">"+'sequence'+str(index1)+"\n"
        feature_list = []
        for key in gb_seq.features:
            feature_list.append(key.type)
        index = 0
        if 'CDS' in feature_list:
            for key in gb_seq.features:
                if key.type == "CDS":
                    if 'locus_tag' in key.qualifiers:
                        with open(resultdir+'/gb_location.txt','a') as w:
                            w.write(str(key.location).split(":")[0].split("[")[1].strip('<')+':'+str(key.location).split(":")[1].split("]")[0].strip('>')+'\t'+str(key.qualifiers['locus_tag'][0])+'\t0\t'+new_id+'\n')
                    else:
                        index = index + 1
                        with open(resultdir+'/gb_location.txt','a') as w:
                            w.write(str(key.location).split(":")[0].split("[")[1].strip('<')+':'+str(key.location).split(":")[1].split("]")[0].strip('>')+'\t'+'locus%s'%index+'\t0\t'+new_id+'\n')
        else:
            for key in gb_seq.features:
                if key.type == "source":
                    index = index + 1
                    with open(resultdir+'/gb_location.txt','a') as w:
                        w.write(str(key.location).split(":")[0].split("[")[1].strip('<')+':'+str(key.location).split(":")[1].split("]")[0].strip('>')+'\t'+'locus%s'%index+'\t0\t'+new_id+'\n')
        complete_fasta = format_fasta(complete_annot, complete_seq, 60)
        complete_file = resultdir+"/gb.fasta"
        complete_file_obj = open(complete_file, "a")
        complete_file_obj.write(complete_fasta)

def parse_fasta(name,nucleotide,resultdir):
    query_name_file = resultdir+'/query_name.list' 
    outfile2 = resultdir+'/nucleotide.fasta'
    location = resultdir+'/gb_location.txt'
    if not os.path.exists(location):
        append_flag = 1
    else:
        append_flag = 0
    seq_number = 0
    multi_seqence_dir = resultdir+'/multi_contig'
    mkdir(multi_seqence_dir)
    name_list = []
    for i,record in enumerate(SeqIO.parse(nucleotide,"fasta")):
        all_len = 0
        seq_number += 1
        id = record.id
        new_id = "bacantsequence"+str_number(i+1)
        with open(query_name_file,'a') as w:
            w.write(new_id+'\t'+id+'\n')
        seq = str(record.seq)
        length = len(seq)
        start = all_len + 1
        end = length + all_len
        if append_flag:
            with open(location,'a') as w:
                w.write(str(start)+':'+str(end)+'\t'+new_id+'\t'+str(all_len)+'\t'+new_id+'\n')
        multi_contig_file = multi_seqence_dir+'/'+new_id+'.fa'
        with open(multi_contig_file,'w') as w:
            w.write('>'+new_id+'\n'+str(record.seq)+'\n')
        name_list.append(new_id)
        with open(outfile2,'a') as w:
            w.write('>'+new_id+'\n'+str(record.seq)+'\n')
    if len(name_list) != len(set(name_list)):
        print("Please check your sequence id, duplication name")
        sys.exit(-1)
    return seq_number,';'.join(name_list)


def mkdir(resultdir):
    if not os.path.exists(resultdir):
        os.mkdir(resultdir)
    else:
        os.system("rm -rf %s/*"%resultdir)

def findResistanceGene(inFile,outdir,blastnPath,database,default_ident,default_cov,threads=2):
    cmd = blastnPath +' -num_threads '+str(threads)+' -task blastn -dust no -evalue 1E-5 -culling_limit 1 -query ' + inFile + ' -db ' + database + ' -outfmt \"6 sseqid pident length  qstart qend slen sstrand qseqid gaps sstart send\" -out ' + outdir + '/blast.out'
    subprocess.run(cmd,shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    blastResultDict = {}
    f = open(outdir+'/blast.out')
    lines = f.readlines()
    if len(lines) == 0:
        pass
    else:
        for line in lines:
            data = line.strip().split('\t')
            contig_name = data[7]
            product = re.split('~~~',data[0])[3]
            acc = re.split('~~~',data[0])[2]
            ident = float(data[1])
            cov = float(data[2])*100/int(data[5])
            if cov>=100:
                cov=100
            leftPos = data[3]
            rightPos = data[4]
            name = re.split('~~~',data[0])[1]+" "+leftPos+" "+rightPos
            strand = data[6]
            if int(data[9])<int(data[10]):
                covlen = data[9]+'-'+data[10]+'/'+data[5]
            else:
                covlen = data[10]+'-'+data[9]+'/'+data[5]
            data = str(ident)+'|'+str(cov)+'|'+leftPos+'|'+rightPos+'|'+name+'|'+strand+'|'+data[7].replace('|','~')+'|'+data[8]+'|'+product+'|'+acc+'|'+covlen
            if contig_name not in blastResultDict:
                blastResultDict[contig_name] = {}
            if name not in blastResultDict[contig_name]:
                blastResultDict[contig_name][name] = []
                blastResultDict[contig_name][name].append(data)
            else:
                blastResultDict[contig_name][name].append(data)
    f.close()
    with open(outdir+'/AMR.possible.xls','w') as w:
        w.write('#FILE  SEQUENCE    START   END STRAND  GENE    COVERAGE    COVERAGE_MAP    GAPS    %COVERAGE   %IDENTITY   DATABASE    ACCESSION   PRODUCT RESISTANCE\n')
    for contig_name1,dict1 in blastResultDict.items():
        for name,dataList in dict1.items():
            for data in dataList:
                ident = float(data.split('|')[0])
                cov = float(data.split('|')[1])
                leftPos = data.split('|')[2]
                rightPos = data.split('|')[3]
                name = data.split('|')[4].split(" ")[0]
                strand = data.split('|')[5]
                query = data.split('|')[6].replace('~','|')
                gaps = data.split('|')[7]
                product1 = data.split('|')[8]
                acc1 = data.split('|')[9]
                covlen1 = data.split('|')[10]
                bestLeftPos = leftPos
                bestRightPos = rightPos
                pos = bestLeftPos + '-' + bestRightPos
                bestStand = strand
                bestIdent = format(ident, '0.2f')
                bestCov = format(cov, '0.2f')
                with open(outdir+'/AMR.possible.xls','a') as w:
                    w.write('nucleotide.fasta'+'\t'+query+'\t'+bestLeftPos+'\t'+bestRightPos+'\t'+bestStand+'\t'+name+'\t'+covlen1+'\t'+'.'+'\t'+gaps+'\t'+str(bestCov)+'\t'+str(bestIdent)+'\t'+'ResDB'+'\t'+acc1+'\t'+product1+'\n')
                    
    with open(outdir+'/AMR.result','w') as w:
        w.write('#FILE  SEQUENCE    START   END STRAND  GENE    COVERAGE    COVERAGE_MAP    GAPS    %COVERAGE   %IDENTITY   DATABASE    ACCESSION   PRODUCT RESISTANCE\n')
    for contig_name1,dict1 in blastResultDict.items():
        resistanceGenePosList = []
        for name,dataList in dict1.items():
            maxIdent = default_ident
            maxCov = default_cov
            pos = ''
            for data in dataList:
                ident = float(data.split('|')[0])
                cov = float(data.split('|')[1])
                leftPos = data.split('|')[2]
                rightPos = data.split('|')[3]
                name = data.split('|')[4].split(" ")[0]
                strand = data.split('|')[5]
                query = data.split('|')[6]
                gaps = data.split('|')[7]
                product1 = data.split('|')[8]
                acc1 = data.split('|')[9]
                covlen1 = data.split('|')[10]
                if ident >= maxIdent and cov >= maxCov:
                    bestLeftPos = leftPos
                    bestRightPos = rightPos
                    pos = bestLeftPos + '-' + bestRightPos
                    bestStand = strand
                    bestIdent = format(ident, '0.2f')
                    bestCov = format(cov, '0.2f')
            
            if pos != '':
                left1 = int(pos.split('-')[0])
                right1 = int(pos.split('-')[1])
                flag = True
                if resistanceGenePosList != []:
                    for po in resistanceGenePosList:
                        left2 = int(po.split('-')[0])
                        right2 = int(po.split('-')[1])
                        if left1 < right2 and right1 > left2:
                            flag = False
                            break
                        else:
                            continue
                if flag:
                    with open(outdir+'/AMR.result','a') as w:
                        w.write('nucleotide.fasta'+'\t'+query+'\t'+bestLeftPos+'\t'+bestRightPos+'\t'+bestStand+'\t'+name+'\t'+covlen1+'\t'+'.'+'\t'+gaps+'\t'+str(bestCov)+'\t'+str(bestIdent)+'\t'+'ResDB'+'\t'+acc1+'\t'+product1+'\n')
                    resistanceGenePosList.append(pos)
    os.remove(outdir + '/blast.out')


def AMR(nucleotide,resultdir,database,blastnPath,cov0,ident0,threads=2):
    findResistanceGene(nucleotide,resultdir,blastnPath,database,ident0,cov0,threads=threads)
    infile = resultdir + "/AMR.result"
    outfile = resultdir + "/AMR.xls"
    tempfile = resultdir + "/AMR_temp.xls"
    f = open(infile)
    i = 0
    for lines in f:
        i = i + 1
        if i == 1:
            with open(tempfile,"a") as w:
                w.write(lines)
            continue
        lines = lines.strip()
        line = lines.split("\t")
        new_line = line[0].split("/")[-1] + '\t' + "\t".join(line[1:])
        with open(tempfile,"a") as w:
            w.write(new_line+'\n')
    f.close()
    f = open(infile)
    datas = f.readlines()
    f.close()
    with open(outfile,'w') as w:
        w.write(datas[0])
    newDatas = sorted(datas[1:],key = lambda data:(data.split('\t')[1],int(data.split('\t')[2])))
    for newData in newDatas:
        tmp_list = newData.split('\t')
        newData2 = tmp_list[0]+'\t'+tmp_list[1].replace('~','|')+'\t'+'\t'.join(tmp_list[2:])
        with open(outfile,'a') as w:
            w.write(newData2)
    os.remove(tempfile)
    os.remove(infile)
    out_file = resultdir + "/AMR.gff"
    flag = "AMR"
    format_genbank(outfile,out_file,flag,nucleotide,resultdir)
    print("AMR done")


def async_func(f):
    def wrapper(*args,**kwargs):
        thr = Thread(target=f,args=args,kwargs=kwargs)
        thr.start()
    return wrapper


@async_func
def integron_finder(current_dir,nucleotide,resultdir,blastn_path,database,threads=2):
    merged_integron_path = "%s/nucleotide.integrons"%resultdir
    try:
        run_integron_finder(current_dir,resultdir,nucleotide,threads=threads)
        integron_pos_dict = parse_integron_result(resultdir,merged_integron_path)
        if integron_pos_dict:
            find_most_like_In(nucleotide,integron_pos_dict,resultdir,blastn_path,database,threads=threads)
        with open(resultdir+"/integron.finished",'w') as w:
            w.write("completed")
        print("integron_finder done")
    except:
        with open(resultdir+"/integron.finished",'w') as w:
            w.write("abnormal exit")
        print("integron_finder error")
    
    

def parse_integron_result(resultdir,merged_integron_path):
    integron_dict = {}
    if merged_integron_path:
        integron_file = merged_integron_path
        f = open(integron_file)
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip()
            if line:
                data = line.split("\t")
                name = data[1]+"|"+data[0]
                if name not in integron_dict:
                    integron_dict[name] = []
                    integron_dict[name].append(int(data[3]))
                    integron_dict[name].append(int(data[4]))
                else:
                    integron_dict[name].append(int(data[3]))
                    integron_dict[name].append(int(data[4]))
        f.close()
        integron_pos_dict = {}
        for k,v in integron_dict.items():
            v.sort()
            start = v[0]
            end = v[-1]
            integron_pos_dict[k] = str(start)+"|"+str(end)
        return integron_pos_dict
    else:
        return {}

def find_most_like_In(nucleotide,integron_pos_dict,resultdir,blastn_path,database,threads=2):
    integron_fasta = resultdir+"/integron.fa"
    seq_dict = {}
    for rec in SeqIO.parse(nucleotide,'fasta'):
        id = str(rec.id)
        seq = str(rec.seq)
        seq_dict[id] = seq
    for name,pos in integron_pos_dict.items():
        rec_id = name.split("|")[0]
        start = int(pos.split("|")[0])
        end = int(pos.split("|")[1])
        integron_seq = seq_dict[rec_id][start-1:end]
        with open(integron_fasta,'a') as w:
            w.write(">"+name.replace("|","~")+'~'+str(start)+':'+str(end)+"\n"+integron_seq+"\n")
    blast_result = resultdir+'/integron.blast.out'
    cmd = blastn_path+" -num_threads "+str(threads)+" -query "+integron_fasta+" -db "+database+" -evalue 1e-5 -outfmt \"6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qseq sseq slen\" -out "+blast_result
    subprocess.run(cmd,shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    
    size = os.path.getsize(blast_result)
    if size != 0:
        with open(blast_result, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write('QUERY\tINTEGRON TYPE|ACCESSION\t%IDENTITY\tLENGTH\tMISMATCH\tGAPOPEN\tQUERY START\tQUERY END\tSUBJECT START\tSUBJECT END\tEVALUE\tBITSCORE\tQUERY SEQ\tSUBJECT SEQ\tSUBJECT LENGTH\n'+content)
        filter_result = resultdir+'/integron.filter.xls'
        filter_result_temp = resultdir+'/integron.filter.temp.xls'
        outfile = resultdir + "/integron.gff"
        flag = "integron"
        cov2 = 0
        ident2 = 0
        flag = "integron"

        blast_result2 = resultdir+'/integron.blast.out2'
        f = open(blast_result)
        lines = f.readlines()
        with open(blast_result2,'w') as w:
            w.write(lines[0])
        for line in lines[1:]:
            line = line.strip()
            if line:
                data = line.split("\t")
                s1 = '~'.join(data[0].split('~')[:-1])
                start1 = data[0].split('~')[-1].split(':')[0]
                end1 = data[0].split('~')[-1].split(':')[1]
                true_s = int(data[6])+int(start1)-1
                true_e = int(data[7])+int(start1)-1
                with open(blast_result2,'a') as w:
                    w.write(s1+'\t'+'\t'.join(data[1:6])+'\t'+str(true_s)+'\t'+str(true_e)+'\t'+'\t'.join(data[8:])+'\n')
        f.close()

        filter_blast_result(blast_result2,filter_result_temp,cov2,ident2,flag)
        f = open(filter_result_temp)
        datas = f.readlines()
        f.close()
        with open(filter_result,'w') as w:
            w.write(datas[0])
        newDatas = sorted(datas[1:],key = lambda data:(int(data.split('\t')[6]),-float(data.split('\t')[14].strip()),-float(data.split('\t')[2])))
        name_tmp  = []
        for newData in newDatas:
            data_name = newData.split("\t")[0]
            if data_name not in name_tmp:
                name_tmp.append(data_name)
                with open(filter_result,'a') as w:
                    w.write(newData)
        os.remove(filter_result_temp)
        format_genbank(filter_result,outfile,"integron",nucleotide,resultdir)
    else:
        os.remove(blast_result)

def transposon(nucleotide,resultdir,blastn_path,cov3,ident3,database,threads=2):
    cmd = blastn_path+" -num_threads "+str(threads)+" -task blastn -query "+nucleotide+" -db "+database+" -evalue 1e-5 -outfmt \"6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qseq sseq slen\" -out "+resultdir+"/transposon.xls"
    subprocess.run(cmd,shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    size = os.path.getsize(resultdir+"/transposon.xls")
    blast_result = resultdir+'/transposon.xls'
    if size != 0:
        with open(resultdir+"/transposon.xls", 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write('QUERY\tTRANSPOSON TYPE|ACCESSION\t%IDENTITY\tLENGTH\tMISMATCH\tGAPOPEN\tQUERY START\tQUERY END\tSUBJECT START\tSUBJECT END\tEVALUE\tBITSCORE\tQUERY SEQ\tSUBJECT SEQ\tSUBJECT LENGTH\n'+content)
        filter_result = resultdir+'/transposon.filter1.xls'
        filter_result_temp = resultdir+'/transposon.filter.temp.xls'
        outfile = resultdir + "/transposon.gff"
        flag = "transposon"
        filter_blast_result(blast_result,filter_result_temp,cov3,ident3,flag)
        f = open(filter_result_temp)
        datas = f.readlines()
        f.close()
        with open(filter_result,'w') as w:
            w.write(datas[0])
        newDatas = sorted(datas[1:],key = lambda data:(int(data.split('\t')[6]),-float(data.split('\t')[14].strip()),-float(data.split('\t')[2])))
        for newData in newDatas:
            with open(filter_result,'a') as w:
                w.write(newData)
        
        filter_result_temp1 = resultdir+'/transposon.possible.temp.xls'
        possible_file = resultdir+'/transposon.possible.xls'
        filter_blast_result(blast_result,filter_result_temp1,0,0,flag)
        f = open(filter_result_temp1)
        datas = f.readlines()
        f.close()
        with open(possible_file,'w') as w:
            w.write(datas[0])
        newDatas = sorted(datas[1:],key = lambda data:(int(data.split('\t')[6]),-float(data.split('\t')[14].strip()),-float(data.split('\t')[2])))
        for newData in newDatas:
            with open(possible_file,'a') as w:
                w.write(newData)


        os.remove(blast_result)
        os.remove(filter_result_temp)
        os.remove(filter_result_temp1)
        
        final_result = resultdir+'/transposon.filter.xls'
        f = open(filter_result)

        name_list = []
        tmp = {}
        tmp1 = {}
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip()
            if line:
                data = line.split("\t")
                name = data[0]
                start = data[6]
                if name not in name_list:
                    name_list.append(name)
                    tmp[name]={}
                    tmp1[name]=[]
                if start not in tmp[name]:
                    tmp[name][start] = []
                tmp[name][start].append(line)
                if int(start) not in tmp1[name]:
                    tmp1[name].append(int(start))
        f.close()
        with open(final_result,'w') as w:
            w.write(lines[0])

        for name in name_list:
            tmp11 = tmp1[name]
            tmp11.sort()
            for key in tmp11:
                key = str(key)
                if len(tmp[name][key])>1:
                    max_ident = 0
                    max_cov = 0
                    for data in tmp[name][key]:
                        ident1 = float(data.split("\t")[2])
                        cov1 = float(data.split("\t")[-1])
                        if ident1 >= max_ident and cov1>=max_cov:
                            max_ident = ident1
                            max_cov = cov1
                            max_info = data
                    with open(final_result,'a') as w:
                        w.write(max_info+"\n")
                else:
                    with open(final_result,'a') as w:
                        w.write(tmp[name][key][0]+'\n')
        if os.path.exists(filter_result):
            os.remove(filter_result)
        format_genbank(final_result,outfile,flag,nucleotide,resultdir)
        print("transposon done")
    else:
        os.remove(blast_result)
        print("no transposon hits")

def filter_blast_result(blast_result,filter_result,coverage,identity,flag):
    if os.path.exists(filter_result):
        os.remove(filter_result)
    f = open(blast_result)
    i = 0
    for lines in f:
        i = i + 1
        if i == 1:
            if flag != "AMR":
                with open(filter_result,"a") as w:
                    title = '\t'.join(lines.split("\t")[0:14])+'\t'+'%COVERAGE'
                    w.write(title+'\n')
            else:
                with open(filter_result,"a") as w:
                    title = '\t'.join(lines.split("\t")[0:14])
                    w.write(title+'\n')
            continue
        lines = lines.strip()
        if lines:
            line = lines.split("\t")
            ident = float(line[2])
            slen = float(line[14])
            match_length = abs(int(line[9])-int(line[8])) + 1
            cov = round(match_length*100/slen,2)
            if flag != "AMR":
                if ident >= identity and cov >= coverage and match_length>= 50:
                    newline = '\t'.join(line[0:2]) + '\t' + str(round(ident,2)) + '\t' + '\t'.join(line[3:14]) + '\t' + str(cov)
                    with open(filter_result,"a") as w:
                        w.write(newline+'\n')
            else:
                if ident >= identity and match_length>= 50:
                    newline = '\t'.join(line[0:2]) + '\t' + str(round(ident,2)) + '\t' + '\t'.join(line[3:14])
                    with open(filter_result,"a") as w:
                        w.write(newline+'\n')
    f.close()

def format_genbank(infile,outfile,flag,fasta_file,resultdir):
    name_dict = {}
    query_dict = {}
    f = open(resultdir+"/gb_location.txt")
    for lines in f:
        lines = lines.strip()
        if lines:
            line = lines.split("\t")
            location = line[0]
            locus_tag = line[1]
            all_len = line[2]
            query_dict[locus_tag] = all_len
            if line[3] not in name_dict:
                name_dict[line[3]] = {}
            name_dict[line[3]][location] = locus_tag
    f.close()
    f = open(infile)
    i = 0
    for lines in f:
        i = i + 1
        if i == 1:
            continue
        lines = lines.strip()
        if lines:
            line = lines.split("\t")

            #query
            if flag == "AMR":
                query = line[1]
                filename = query
            elif flag == "integron":
                query = "~".join(line[0].split("~")[0:-1])
                filename = query
            else:
                query = line[0]
                filename = query
            outfile = resultdir+'/'+query+'.'+flag+'.gff'
            #note
            if flag == "AMR":
                if line[-3] != "":
                    gene = line[5]
                    CDS = line[5]
                    db_xref = line[-3]
                    note = line[-1]
                else:
                    gene = line[5]
                    CDS = line[5]
                    note = line[-1]
                    db_xref = ""
            elif flag == "integron":
                text = line[1].split("|")
                note = ""
                if len(text) > 1:
                    gene = text[0]
                    CDS = text[0]
                    db_xref = text[1]
                    
                else:
                    gene = text[0]
                    CDS = text[0]
                    db_xref = ""
                    
            elif flag == "transposon":
                text = line[1].split("|")
                note = ""
                if len(text) > 1:
                    gene = text[0]
                    CDS = text[0]
                    db_xref = text[1]
                else:
                    gene = text[0]
                    CDS = text[0]
                    db_xref = ""
            #start end
            if flag == "AMR":
                start = line[2]
                end = line[3]
                #locus
                name = start + ":" + end
                locus = get_locus_tag(name_dict,name,query)
            else:
                start = line[6]
                end = line[7]
                #locus
                name = start + ":" + end
                locus = get_locus_tag(name_dict,name,query)
            #source
            if flag == "AMR":
                source = "resistance"
            elif flag == "integron":
                source = "integron"
            elif flag == "transposon":
                source = "transposon"
            #strand
            if flag == "AMR":
                strand = line[4].replace("plus","+").replace("minus","-")
            else:
                if int(line[8]) < int(line[9]):
                    strand = "+"
                else:
                    strand = "-"
            #feature
            features = ["gene","CDS","mobile_element","mobile_element"]
            if flag == "AMR":
                if db_xref == "":
                    with open(outfile,"a") as w:
                        w.write(filename+'\t'+source+'\t'+features[0]+'\t'+start+'\t'+end+'\t.\t'+strand+'\t.\tlocus_tag='+locus+';gene='+gene+';Note='+note+'\n')
                        w.write(filename+'\t'+source+'\t'+features[1]+'\t'+start+'\t'+end+'\t.\t'+strand+'\t.\tlocus_tag='+locus+';CDS='+CDS+';Note='+note+'\n')
                else:
                    with open(outfile,"a") as w:
                        w.write(filename+'\t'+source+'\t'+features[0]+'\t'+start+'\t'+end+'\t.\t'+strand+'\t.\tlocus_tag='+locus+';gene='+gene+';db_xref='+db_xref+';Note='+note+'\n')
                        
                        w.write(filename+'\t'+source+'\t'+features[1]+'\t'+start+'\t'+end+'\t.\t'+strand+'\t.\tlocus_tag='+locus+';CDS='+CDS+';db_xref='+db_xref+';Note='+note+'\n')

            if flag == "integron":
                if db_xref == "":
                    with open(outfile,"a") as w:
                        w.write(filename+'\t'+source+'\t'+features[2]+'\t'+start+'\t'+end+'\t.\t'+strand+'\t.\tlocus_tag='+locus+';gene='+CDS+'\n')
                else:
                    with open(outfile,"a") as w:
                        w.write(filename+'\t'+source+'\t'+features[2]+'\t'+start+'\t'+end+'\t.\t'+strand+'\t.\tlocus_tag='+locus+';gene='+CDS+';db_xref='+db_xref+'\n')
            
            if flag == "transposon":
                if db_xref == "":
                    with open(outfile,"a") as w:
                        w.write(filename+'\t'+source+'\t'+features[3]+'\t'+start+'\t'+end+'\t.\t'+strand+'\t.\tlocus_tag='+locus+';transposon='+CDS+';gene='+gene+'\n')
                else:
                    with open(outfile,"a") as w:
                        w.write(filename+'\t'+source+'\t'+features[3]+'\t'+start+'\t'+end+'\t.\t'+strand+'\t.\tlocus_tag='+locus+';transposon='+CDS+';db_xref='+db_xref+';gene='+gene+'\n')
            
    f.close()
    for file in os.listdir(resultdir):
        if flag+'.gff' in file:
            gff_file = os.path.join(resultdir,file)
            f = open(gff_file)
            datas = f.readlines()
            f.close()
            if len(datas) > 1:
                query_name = datas[1].split("\t")[0]
                gb_file = resultdir+'/'+query_name+'.'+flag+'.'+'gbk'
                with open(gff_file+'3','w') as w:
                    w.write(datas[0])
                newDatas = sorted(datas[1:],key = lambda data:(int(data.split('\t')[3].strip())))
                for newData in newDatas:
                    with open(gff_file+'3','a') as w:
                        w.write(newData)
                fasta_file = resultdir+'/multi_contig/'+query_name+'.fa'
                convert(gff_file+'3', fasta_file,resultdir,gb_file)

def get_locus_tag(name_dict,name,query):
    qstart = int(name.split(":")[0])
    qend = int(name.split(":")[1])
    max_len = 0
    max_dict = {}
    for k,v in name_dict[query].items():
        start = int(k.split(":")[0])
        end = int(k.split(":")[1])
        if qstart >= start and qend <= end:
            length = qend - qstart + 1
        elif qstart < start and qend > end:
            length = end - start + 1
        elif qstart < start and qend > start and qend <= end:
            length = qend - start + 1
        elif qstart >= start and qstart < end and qend > end:
            length = end - qstart
        else:
            length = 0
        if length > max_len:
            max_dict = {}
            rstart = str(start)
            rend = str(end)
            max_len = length
            max_dict[max_len] = rstart+':'+rend
    if max_dict != {}:
        ret = name_dict[query][max_dict[max_len]]
    else:
        ret = ""
    return ret
     
def getFileFormat(infile):
    try:
        for rec in SeqIO.parse(infile,'fasta'):
            seq = rec.seq
            if seq:
                return 'fasta'
    except:
        pass
        
    try:
        for rec in SeqIO.parse(infile,'genbank'):
            seq = rec.seq
            if seq:
                return 'genbank'
    except:
        pass
    
    return "unknown"

def replicon_search(nucleotide,resultdir,blastn_path,curent_dir,cov=60,ident=90,threads=2):
    database = curent_dir+'/repliconDB/replicon.fasta'
    cmd = blastn_path + ' -num_threads '+str(threads)+' -task blastn -dust no -perc_identity '+str(ident)+' -query ' + nucleotide + ' -db ' + database + ' -outfmt \"6 qseqid sseqid pident length  qstart qend slen sstrand  gaps\" -out ' + resultdir + '/replicon.blast.out'
    subprocess.run(cmd,shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    blast_out = resultdir + '/replicon.blast.out'
    blast_tsv = resultdir+'/replicon.tsv'
    with open(blast_tsv,'w') as w:
        w.write('Plasmid\tIdentity\tQuery/Template\tContig\tPosition\tAccession\n')
    if os.path.exists(blast_out):
        if os.path.getsize(blast_out) != 0:
            f = open(blast_out)
            for lines in f:
                lines = lines.strip()
                if lines:
                    data = lines.split("\t")
                    qseqid = data[0]
                    sseqid = data[1]
                    pident = float(data[2])
                    length = int(data[3])
                    pos = data[4]+'..'+data[5]
                    slen = int(data[6])
                    if (length/slen)*100 >= cov:
                        tmp = []
                        plasmid = sseqid.split('_')[0]
                        acc = sseqid.split('_')[-1]
                        tmp.append(plasmid)
                        tmp.append(str(pident))
                        tmp.append(str(length)+'/'+str(slen))
                        tmp.append(qseqid)
                        tmp.append(pos)
                        tmp.append(acc)
                        with open(blast_tsv,'a') as w:
                            w.write('\t'.join(tmp)+'\n')
            f.close()
        os.system("rm "+blast_out)
    print("replicon search done")

def process_dir(blastn_path,final_indir,final_resultdir):
    red = "\033[31m"
    end = "\033[0m"
    nucleotide,genbank,resultdir,databases,coverages,identities,indir,path,threads = arg_parse()
    if path:
        path = os.path.abspath(path)

    mkdir(final_resultdir)
    resultdir = final_resultdir
    indir = final_indir
    curent_dir = sys.path[0].rstrip('/')+'/../BacAnt'
    database = databases.split(",")
    ResDB,IntegronDB,TransposonDB="","",""
    for dbname in database:
        if dbname=="ResDB":
            ResDB="ResDB"
        elif dbname=="IntegronDB":
            IntegronDB="IntegronDB"
        elif dbname=="TransposonDB":
            TransposonDB="TransposonDB"
    coverage = coverages.split(",")
    cov0 = coverage[0]
    if cov0:
        cov0 = float(cov0)
    cov1 = coverage[1]
    if cov1:
        cov1 = float(cov1)
    cov2 = coverage[2]
    if cov2:
        cov2 = float(cov2)
    identity = identities.split(",")
    ident0 = identity[0]
    if ident0:
        ident0 = float(ident0)
    ident1 = identity[1]
    if ident1:
        ident1 = float(ident1)
    ident2 = identity[2]
    if ident2:
        ident2 = float(ident2)
    for file in os.listdir(indir):
        filename = file.split('.')[0]
        outdir = resultdir + '/' +filename
        mkdir(outdir)
        infile = os.path.join(indir,file)
        fileFormat = getFileFormat(infile)
        print ("Analysing file",file," at "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        if fileFormat=="genbank":
            parse_genbank(infile,outdir)
            name = re.sub('[^\w-]','',infile.split("/")[-1].split(".")[0])
            parse_fasta(name,outdir+'/gb.fasta',outdir)
            nucleotide = outdir+"/nucleotide.fasta"
        elif fileFormat=="fasta":
            name = re.sub('[^\w-]','',infile.split("/")[-1].split(".")[0])
            parse_fasta(name,infile,outdir)
            nucleotide = outdir+"/nucleotide.fasta"
        else:
            print("Please check your file format:",infile)
            sys.exit(-1)
        #input sequence length       
        seq_len = 0
        for rec in SeqIO.parse(nucleotide,'fasta'):
            length = len(str(rec.seq))
            seq_len = seq_len + length
        with open(outdir+'/seqLen.txt','w') as w:
            w.write(str(seq_len))
        if path:
            print("Use your defined databases!")
        #replicon
        replicon_search(nucleotide,outdir,blastn_path,curent_dir,threads=threads)

        #integron
        if IntegronDB:
            if path:
                
                if os.path.exists(path+'/IntegronDB/Integron.fasta'):
                    database = path+'/IntegronDB/Integron'
                else:
                    print(red+path+'/IntegronDB/Integron.fasta Not Found! Back to default Database'+end)
                    database = curent_dir+'/IntegronDB/Integron'
            else:
                database = curent_dir+'/IntegronDB/Integron'
            integron_finder(curent_dir,nucleotide,outdir,blastn_path,database,threads=threads)
        #resistance
        if ResDB:
            if path:
                if os.path.exists(path+'/ResDB/Res.fasta'):
                    database = path+'/ResDB/Res'
                else:
                    print(red+path+'/ResDB/Res.fasta Not Found! Back to default Database'+end)
                    database = curent_dir+'/ResDB/Res'
            else:
                database = curent_dir+'/ResDB/Res'
            AMR(nucleotide,outdir,database,blastn_path,cov0,ident0,threads=threads)
        #transposon
        if TransposonDB:
            if path:
                if os.path.exists(path+'/TransposonDB/Transposon.fasta'):
                    database = path+'/TransposonDB/Transposon'
                else:
                    print(red+path+'/TransposonDB/Transposon.fasta Not Found! Back to default Database'+end)
                    database = curent_dir+'/TransposonDB/Transposon'
            else:
                database = curent_dir+'/TransposonDB/Transposon'
            transposon(nucleotide,outdir,blastn_path,cov2,ident2,database,threads=threads)

        if IntegronDB:
            while 1:
                if os.path.exists(outdir+"/integron.finished"):
                    os.remove(outdir+"/integron.finished")
                    break
                else:
                    time.sleep(1)                   
        catFlag = False
        query_list = []
        for file in os.listdir(outdir):
            if 'gff' in file:
                name = '.'.join(file.split('.')[:-2])
                if name not in query_list:
                    query_list.append(name)
                catFlag = True
        query_list.sort()
        final_result_list = []
        if catFlag:
            for query1 in query_list:
                os.system("cat \"%s/%s\".*.gff >> \"%s/%s\".gff"%(outdir,query1,outdir,query1))
                final_result_list.append("%s/%s.gff"%(outdir,query1))
        
        if final_result_list:
            for i,final_result in enumerate(final_result_list):
                f = open(final_result)
                datas = f.readlines()
                f.close()
                with open(final_result+'3','w') as w:
                    w.write('')
                newDatas = sorted(datas,key = lambda data:(int(data.split('\t')[3].strip())))
                for newData in newDatas:
                    with open(final_result+'3','a') as w:
                        w.write(newData)
                gb_file = outdir+'/'+query_list[i]+".annotation.gbk"
                file = outdir+'/multi_contig/'+query_list[i]+'.fa'
                convert(final_result+"3",file,outdir,gb_file)
                os.system("cat \"%s3\" >>\"%s/annotation.tsv\""%(final_result,resultdir))

        for file in os.listdir(outdir):
            if '.gbk' in file:
                infile1 = os.path.join(outdir,file)
                name1 = '.'.join(file.split('.')[:-2])
                flag = file.split('.')[-2]
                out = outdir+'/'+flag+'.gb'
                os.system("cat \"%s\" >>\"%s\""%(infile1,out))
        if os.path.exists(resultdir+'/annotation.gb'):
            merge_genbank(resultdir)
            get_data(resultdir)
        if os.path.exists(resultdir+'/tmp.gb'):
            os.remove(resultdir+'/tmp.gb')
                
        if catFlag:
            os.system("rm "+outdir+"/*.gff")
            os.system("rm "+outdir+"/*.gff3")
            os.system("rm "+outdir+"/*.gbk")
        if os.path.exists(outdir+'/gb_location.txt'):
            os.remove(outdir+'/gb_location.txt')
        if os.path.exists(outdir+"/nucleotide_all.fasta"):
            os.remove(outdir+"/nucleotide_all.fasta")
        if os.path.exists(outdir+"/nucleotide.fasta"):
            os.remove(outdir+"/nucleotide.fasta")
        if os.path.exists(outdir+"/gb.fasta"):
            os.remove(outdir+"/gb.fasta")
        if os.path.exists(outdir+"/integron.blast.out"):
            os.remove(outdir+"/integron.blast.out")
        if os.path.exists(resultdir+"/integron.blast.out2"):
            os.remove(resultdir+"/integron.blast.out2")
        if os.path.exists(outdir+"/integron.fa"):
            os.remove(outdir+"/integron.fa")
        if os.path.exists(outdir+"/seqLen.txt"):
            os.remove(outdir+"/seqLen.txt")
        if os.path.exists(outdir+"/nucleotide.integrons"):
            os.rename(outdir+"/nucleotide.integrons",outdir+"/integrons.detail.xls")
        if os.path.exists(resultdir+"/multi_contig"):
            shutil.rmtree(resultdir+"/multi_contig")
        for file in os.listdir(outdir):
            if '.xls' in file:
                file1 = os.path.join(outdir,file)
                file2 = file1.replace('.xls','.tsv')
                os.system("mv %s %s"%(file1,file2))
        if os.path.exists(outdir+"/Results_Integron_Finder_nucleotide"):
            os.system("rm -r %s/Results_Integron_Finder_nucleotide"%outdir)
        rename_dir(outdir)
        if os.path.exists(outdir+'/query_name.list'):
            os.remove(outdir+'/query_name.list')



def cat_file(indirs,resultdir):
    file_list = ['AMR.tsv','AMR.possible.tsv','AMR.gb','transposon.filter.tsv','transposon.tsv','transposon.gb','integrons.detail.tsv','integron.filter.tsv','integron.gb','replicon.tsv','annotation.gb']
    for file in file_list:
        for indir in indirs:
            file1 = os.path.join(indir,file)
            file2 = os.path.join(resultdir,file)
            if '.tsv' in file:
                if os.path.exists(file1):
                    f = open(file1)
                    lines = f.readlines()
                    f.close()
                    if not os.path.exists(file2):
                        with open(file2,'w') as w:
                            w.write(lines[0])
                    else:
                        if len(lines)>1:
                            for line in lines[1:]:
                                with open(file2,'a') as w:
                                    w.write(line)
            else:
                if os.path.exists(file1):
                    os.system("cat \"%s\" >>\"%s\""%(file1,file2))


def merge_genbank(outdir):
    annotation_file = os.path.join(outdir,"annotation.gb")
    fasta_file = os.path.join(outdir,"tmp.fasta")
    gff_file = os.path.join(outdir,"tmp.gff3")
    gb_file = os.path.join(outdir,"tmp.gb")
    if os.path.exists(fasta_file):
        os.remove(fasta_file)
    if os.path.exists(gff_file):
        os.remove(gff_file)
    if os.path.exists(gb_file):
        os.remove(gb_file)
    with open(fasta_file,'w') as w:
        w.write('>tmp\n')
    pre = 0
    for rec in SeqIO.parse(annotation_file,'genbank'):
        seq = str(rec.seq)
        length = len(seq)
        with open(fasta_file,'a') as w:
            w.write(seq)
        for feature in rec.features:
            if feature.type == "gene" or feature.type == "mobile_element":
                source = feature.qualifiers['source'][0]
                type1 = feature.type
                start = int(feature.location.start)+1+pre
                end = int(feature.location.end)+pre
                strand1 = feature.location.strand
                if strand1 == 1:
                    strand = "+"
                else:
                    strand = "-"
                locus_tag = feature.qualifiers['locus_tag'][0]
                name = feature.qualifiers['gene'][0]
                with open(gff_file,'a') as w:
                    w.write('tmp\t'+source+'\t'+type1+'\t'+str(start)+'\t'+str(end)+'\t.\t'+strand+'\t.\t'+'locus_tag=tmp;'+source+"="+name+";gene="+name+"\n")


        pre += length

    convert(gff_file, fasta_file,outdir,gb_file)
    os.remove(fasta_file)
    os.remove(gff_file)


def run():
    red = "\033[31m"
    end = "\033[0m"
    nucleotide,genbank,resultdir,databases,coverages,identities,indir,path,threads = arg_parse()
    if path:
        path = os.path.abspath(path)
    curent_dir = sys.path[0].rstrip('/')+'/../BacAnt'
    database = databases.split(",")
    ResDB,IntegronDB,TransposonDB="","",""
    for dbname in database:
        if dbname=="ResDB":
            ResDB="ResDB"
        elif dbname=="IntegronDB":
            IntegronDB="IntegronDB"
        elif dbname=="TransposonDB":
            TransposonDB="TransposonDB"
    coverage = coverages.split(",")
    cov0 = coverage[0]
    if cov0:
        cov0 = float(cov0)
    cov1 = coverage[1]
    if cov1:
        cov1 = float(cov1)
    cov2 = coverage[2]
    if cov2:
        cov2 = float(cov2)
    identity = identities.split(",")
    ident0 = identity[0]
    if ident0:
        ident0 = float(ident0)
    ident1 = identity[1]
    if ident1:
        ident1 = float(ident1)
    ident2 = identity[2]
    if ident2:
        ident2 = float(ident2)
    blastn_path,blastp_path = check_dependencies()
    if blastn_path and blastp_path:
        mkdir(resultdir)
        #dir input
        if indir:
            process_dir(blastn_path,indir,resultdir)
        else:
            #genbank input
            if genbank:
                fileFormat = getFileFormat(genbank)
                if fileFormat == "genbank":
                    pass
                else:
                    print("Please check your file format:",genbank)
                    sys.exit(-1)
                print ("Analysing file",os.path.abspath(genbank)," at "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                parse_genbank(genbank,resultdir)
                name = re.sub('[^\w-]','',genbank.split("/")[-1].split(".")[0])
                seq_number,contig_names = parse_fasta(name,resultdir+'/gb.fasta',resultdir)
                nucleotide = resultdir+"/nucleotide.fasta"
                
            #fasta input
            else:
                fileFormat = getFileFormat(nucleotide)
                if fileFormat == "fasta":
                    pass
                else:
                    print("Please check your file format:",nucleotide)
                    sys.exit(-1)
                print ("Analysing file",os.path.abspath(nucleotide)," at "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                name = re.sub('[^\w-]','',nucleotide.split("/")[-1].split(".")[0])
                seq_number,contig_names = parse_fasta(name,nucleotide,resultdir)
                nucleotide = resultdir+"/nucleotide.fasta"

            #input sequence length
            seq_len = 0
            for rec in SeqIO.parse(nucleotide,'fasta'):
                length = len(str(rec.seq))
                seq_len = seq_len + length
            with open(resultdir+'/seqLen.txt','w') as w:
                w.write(str(seq_len))
            if path:
                print("Use your defined databases!")
            #replicon
            replicon_search(nucleotide,resultdir,blastn_path,curent_dir,threads=threads)
            #integron
            if IntegronDB:
                if path:
                    if os.path.exists(path+'/IntegronDB/Integron.fasta'):
                        database = path+'/IntegronDB/Integron'
                    else:
                        print(red+path+'/IntegronDB/Integron.fasta Not Found! Back to default Database'+end)
                        database = curent_dir+'/IntegronDB/Integron'
                else:
                    database = curent_dir+'/IntegronDB/Integron'
                integron_finder(curent_dir,nucleotide,resultdir,blastn_path,database,threads=threads)
            #resistance
            if ResDB:
                if path:
                    if os.path.exists(path+'/ResDB/Res.fasta'):
                        database = path+'/ResDB/Res'
                    else:
                        print(red+path+'/ResDB/Res.fasta Not Found! Back to default Database'+end)
                        database = curent_dir+'/ResDB/Res'
                else:
                    database = curent_dir+'/ResDB/Res'
                AMR(nucleotide,resultdir,database,blastn_path,cov0,ident0,threads=threads)
            #transposon
            if TransposonDB:
                if path:
                    if os.path.exists(path+'/TransposonDB/Transposon.fasta'):
                        database = path+'/TransposonDB/Transposon'
                    else:
                        print(red+path+'/TransposonDB/Transposon.fasta Not Found! Back to default Database'+end)
                        database = curent_dir+'/TransposonDB/Transposon'
                else:
                    database = curent_dir+'/TransposonDB/Transposon'
                transposon(nucleotide,resultdir,blastn_path,cov2,ident2,database,threads=threads)
            if IntegronDB:
                while 1:
                    if os.path.exists(resultdir+"/integron.finished"):
                        os.remove(resultdir+"/integron.finished")
                        break
                    else:
                        time.sleep(1)            
            
            catFlag = False
            query_list = []
            for file in os.listdir(resultdir):
                if 'gff' in file:
                    name = '.'.join(file.split('.')[:-2])
                    if name not in query_list:
                        query_list.append(name)
                    catFlag = True
            query_list.sort()
            final_result_list = []
            if catFlag:
                for query1 in query_list:
                    os.system("cat \"%s/%s\".*.gff >> \"%s/%s\".gff"%(resultdir,query1,resultdir,query1))
                    final_result_list.append("%s/%s.gff"%(resultdir,query1))
            if final_result_list:
                for i,final_result in enumerate(final_result_list):
                    f = open(final_result)
                    datas = f.readlines()
                    f.close()
                    with open(final_result+'3','w') as w:
                        w.write('')
                    newDatas = sorted(datas,key = lambda data:(int(data.split('\t')[3].strip())))
                    for newData in newDatas:
                        with open(final_result+'3','a') as w:
                            w.write(newData)
                    gb_file = resultdir+'/'+query_list[i]+".annotation.gbk"
                    file = resultdir+'/multi_contig/'+query_list[i]+'.fa'
                    convert(final_result+"3",file,resultdir,gb_file)
                    os.system("cat \"%s3\" >>\"%s/annotation.tsv\""%(final_result,resultdir))
            for file in os.listdir(resultdir):
                if '.gbk' in file:
                    infile1 = os.path.join(resultdir,file)
                    name1 = '.'.join(file.split('.')[:-2])
                    flag = file.split('.')[-2]
                    out = resultdir+'/'+flag+'.gb'
                    os.system("cat \"%s\" >>\"%s\""%(infile1,out))
            if os.path.exists(resultdir+'/annotation.gb'): 
                merge_genbank(resultdir)
                get_data(resultdir)
            if os.path.exists(resultdir+'/tmp.gb'):
                os.remove(resultdir+'/tmp.gb')

            if catFlag:
                os.system("rm "+resultdir+"/*.gff")
                os.system("rm "+resultdir+"/*.gff3")
                os.system("rm "+resultdir+"/*.gbk")
            if os.path.exists(resultdir+'/gb_location.txt'):
                os.remove(resultdir+'/gb_location.txt')
            if os.path.exists(resultdir+"/nucleotide_all.fasta"):
                os.remove(resultdir+"/nucleotide_all.fasta")
            if os.path.exists(resultdir+"/nucleotide.fasta"):
                os.remove(resultdir+"/nucleotide.fasta")
            if os.path.exists(resultdir+"/gb.fasta"):
                os.remove(resultdir+"/gb.fasta")
            if os.path.exists(resultdir+"/integron.blast.out"):
                os.remove(resultdir+"/integron.blast.out")
            if os.path.exists(resultdir+"/integron.blast.out2"):
                os.remove(resultdir+"/integron.blast.out2")
            if os.path.exists(resultdir+"/integron.fa"):
                os.remove(resultdir+"/integron.fa")
            if os.path.exists(resultdir+"/seqLen.txt"):
                os.remove(resultdir+"/seqLen.txt")
            if os.path.exists(resultdir+"/nucleotide.integrons"):
                os.rename(resultdir+"/nucleotide.integrons",resultdir+"/integrons.detail.xls")
            if os.path.exists(resultdir+"/multi_contig"):
                shutil.rmtree(resultdir+"/multi_contig")
            for file in os.listdir(resultdir):
                if '.xls' in file:
                    file1 = os.path.join(resultdir,file)
                    file2 = file1.replace('.xls','.tsv')
                    os.system("mv %s %s"%(file1,file2))
            if os.path.exists(resultdir+"/Results_Integron_Finder_nucleotide"):
                os.system("rm -r %s/Results_Integron_Finder_nucleotide"%resultdir)
            rename_dir(resultdir)

            if os.path.exists(resultdir+'/query_name.list'):
                os.remove(resultdir+'/query_name.list')
        print("All Done"," at "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    else:
        print("program terminated because lack of dependencies")
        sys.exit(-1)




if __name__ == "__main__":
    run()