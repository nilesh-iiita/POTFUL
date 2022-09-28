#!/usr/bin/env python
# coding: utf-8

__author__ = "\x1b[0;5;37;40m Nilesh Kumar \x1b[0;1;30;47m"
__copyright__ = "Copyright 2022, UAB"
__credits__ = ["Nilesh Kumar"]
__license__ = "GPL"
__version__ = "0.1.1"
__maintainer__ = "Nilesh Kumar"
__email__ = "nilesh.iiita@gmail.com"
__status__ = "Production"


import pandas as pd
import numpy as np
from glob2 import glob
from collections import defaultdict
from pathlib import Path
import gseapy as gp
import plotly.express as px
import networkx as nx
import sys
from math import floor
from pyvis import network as net
import sys
import pprint

pp = pprint.PrettyPrinter(depth=4)

import logging
logging.basicConfig(filename='POTFUL.log', filemode='w', encoding='utf-8', level=logging.INFO)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class POTFUL:

    def __init__(self):
        
        print("\x1b[0;6;31;40m POTFUL \x1b[0;5;30;0m")
        
        Logo = """[0;34;40m                                        [0m
[0;34;40m                                        [0m
[0;34;40m                                        [0m
[0;34;40m                                        [0m
[0;34;40m        [0;1;30;40mS[0;5;36;40mt[0;5;31;40mX[0;34;40m;[0;32;40m.  [0;1;30;40m@[0;5;36;40m:[0;5;30;40mX[0;31;40m;[0;34;40m.[0;32;40m     [0;34;40m               [0m
[0;34;40m       :[0;5;33;40m [0;5;37;40m8[0;1;30;47m8[0;5;32;40mS[0;31;40m  ;[0;5;37;40mX8[0;1;30;47m8[0;5;30;40m@[0;32;40m   .[0;34;40m.[0;31;40m     [0;34;40m           [0m
[0;34;40m      [0;32;40m [0;5;30;40m8[0;1;30;47m8[0;5;37;40m88[0;1;30;40mX[0;34;40m .[0;5;30;40mX[0;1;30;47m8[0;5;37;40m8X[0;32;40m;[0;34;40m.[0;31;40m [0;1;30;40m8[0;5;37;40mS[0;5;33;40m [0;1;30;40m@[0;31;40m   [0;34;40m            [0m
[0;34;40m     [0;32;40m [0;31;40m [0;5;33;40m;[0;5;37;40m8[0;1;30;47m8[0;5;35;40m [0;34;40m:[0;31;40m.[0;34;40m.[0;5;33;40m [0;1;30;47m8[0;5;37;40m8[0;5;35;40m [0;34;40m:[0;31;40m.[0;32;40m:[0;5;35;40m [0;1;30;47mX8[0;5;30;40mX[0;31;40m    [0;34;40m           [0m
[0;34;40m     [0;31;40m [0;34;40m.[0;5;35;40m;[0;5;37;40mSS[0;1;30;40m8[0;31;40m.[0;32;40m [0;1;30;40m8[0;5;37;40m8[0;1;30;47m8[0;5;37;40m8[0;1;30;40m@[0;31;40m .[0;5;30;40mX[0;1;30;47m8[0;5;37;40m8X[0;31;40mt[0;34;40m.[0;32;40m.[0;34;40m             [0m
[0;34;40m    [0;31;40m  [0;32;40m  :[0;34;40m:[0;31;40m.[0;32;40m  [0;5;33;40m.[0;5;37;40m88[0;5;36;40m [0;31;40m:[0;32;40m.[0;34;40m.[0;5;35;40m [0;1;30;47m88[0;5;36;40m [0;32;40m.[0;34;40m.[0;32;40m [0;34;40m             [0m
[0;34;40m    [0;32;40m    [0;31;40m.[0;32;40m.   [0;5;36;40m:[0;5;37;40m88[0;5;30;40mX[0;34;40m.[0;32;40m .[0;5;35;40m [0;5;37;40m8X[0;1;30;40m8[0;34;40m.[0;32;40m     [0;34;40m          [0m
[0;34;40m    [0;32;40m     [0;34;40m [0;32;40m  [0;31;40m  :[0;34;40m;[0;32;40m.[0;31;40m  .[0;34;40m.[0;31;40m;[0;34;40m:[0;32;40m.      [0;34;40m  t[0;5;30;40m8[0;5;36;40m8%[0;1;30;46m8[0;5;36;40m [0;30;44m8[0;32;40m:[0m
[0;34;40m    [0;32;40m     [0;34;40m [0;32;40m  [0;31;40m [0;34;40m [0;32;40m.[0;31;40m.[0;32;40m    ...[0;31;40m   [0;32;40m   [0;34;40m;[0;5;34;40mS[0;5;36;40mS[0;36;47m888[0;1;36;47mXX8[0;30;44m8[0;31;40m;[0m
[0;34;40m ;[0;5;36;40mX%t[0;1;30;46m8[0;5;36;40m.[0;1;30;46m8[0;5;36;40m.[0;1;30;46m8[0;5;36;40m.[0;1;30;46m8[0;5;36;40m.[0;1;30;46m8[0;5;36;40m.[0;1;30;46m8[0;5;36;40m.[0;1;30;46m8[0;5;36;40m.[0;1;30;46m8[0;5;36;40m.[0;1;30;46m8[0;5;36;40m.[0;1;30;46m8[0;5;36;40m.[0;1;30;46m8[0;5;36;40m.[0;1;30;46m8[0;1;30;47m8[0;37;46m8[0;36;47m8[0;1;36;47m@8[0;1;34;47m8[0;36;47m8[0;5;34;44m8[0;5;35;40mX[0;34;40m8[0;31;40m;[0;32;40m.[0m
[0;34;40m [0;5;30;40m8[0;36;47m8[0;1;36;47m8@[0;1;34;47mX[0;1;36;47m8[0;36;47m@[0;1;36;47m@[0;1;34;47m@[0;1;36;47m@[0;36;47m@[0;1;36;47m@[0;1;34;47m@[0;1;36;47m@[0;36;47m@[0;1;36;47m@[0;1;34;47m@[0;1;36;47m@[0;36;47m@[0;1;36;47m@[0;1;34;47m@[0;1;36;47m@[0;36;47m@[0;1;36;47m@[0;1;34;47m@[0;1;36;47m@@[0;1;34;47m8[0;1;36;47m8[0;5;36;40mS[0;35;44mX[0;30;44m@[0;34;40m@t[0;32;40m;[0;34;40m.[0;32;40m..[0;34;40m [0m
[0;34;40m @[0;36;47m8[0;1;34;47m@[0;1;36;47m8[0;1;30;44mt[0;34;40m888@8[0;30;44m8[0;34;40m@@8[0;30;44m8[0;34;40m8@8[0;30;44m8[0;34;40m8@8[0;30;44m8[0;34;40m8@[0;5;36;40m;[0;1;36;47m8[0;1;34;47m@[0;1;30;46m8[0;30;44m8[0;31;40m:[0;32;40m:[0;31;40m:..[0;34;40m    [0m
[0;34;40m %[0;36;47m88[0;1;34;47m@[0;5;36;40m%[0;34;40m;[0;31;40m;:.:::.:::::::::::[0;34;40m%[0;1;30;47m8[0;1;34;47m8[0;1;36;47m8[0;5;35;40mX[0;34;40mt.[0;31;40m [0;32;40m.  [0;34;40m    [0m
[0;34;40m .[0;1;30;44m8[0;36;47m8[0;1;36;47m8[0;36;47m@[0;5;36;40mt[0;1;30;44m@[0;32;40m;[0;34;40m;[0;32;40m:[0;34;40m;[0;32;40m:[0;34;40m;[0;32;40m;[0;34;40m;[0;32;40m;[0;34;40m;[0;32;40m:[0;34;40m;[0;32;40m;[0;34;40m;[0;32;40m;[0;34;40m%[0;5;36;40m8;[0;1;36;47m8[0;36;47m8[0;5;36;44mt[0;5;30;40m8[0;32;40m   [0;34;40m [0;32;40m  [0;34;40m    [0m
[0;34;40m [0;32;40m [0;34;40m:[0;1;30;44m8[0;36;47m8[0;1;36;47m@[0;1;34;47m8[0;1;36;47m@[0;36;47m8888888888888888@[0;1;36;47m8[0;1;34;47m8[0;36;47m8[0;5;34;40m8[0;32;40m       [0;34;40m    [0m
[0;34;40m [0;32;40m  [0;34;40m;[0;30;44mX[0;5;36;40mt[0;36;47m88[0;1;34;47m8[0;1;36;47m8[0;1;34;47m@[0;1;36;47m8[0;1;34;47m@[0;1;36;47m8[0;1;34;47m@[0;1;36;47m8[0;1;34;47m8[0;1;36;47m8[0;1;34;47m@[0;1;36;47m8[0;1;34;47m8[0;1;36;47m8[0;1;34;47m@[0;1;36;47m8[0;1;34;47m8[0;37;46m8[0;1;30;44m8[0;34;40m8[0;32;40m.        [0;34;40m   [0m
[0;34;40m [0;32;40m  [0;31;40m.[0;34;40m:%S88888888888888888S%;[0;31;40m:[0;32;40m.       [0;34;40m    [0m
[0;34;40m [0;32;40m   [0;31;40m  [0;34;40m [0;31;40m..[0;32;40m:[0;31;40m;[0;32;40m;[0;31;40m;[0;32;40m;[0;31;40mt[0;32;40m;[0;31;40mt[0;32;40m;[0;31;40mt[0;32;40m;[0;31;40mt[0;32;40m;[0;31;40m;:...[0;32;40m.[0;31;40m [0;32;40m        [0;34;40m   [0m
[0;34;40m [0;32;40m  [0;31;40m   [0;34;40m  [0;31;40m.[0;32;40m.[0;31;40m.[0;34;40m.[0;31;40m.[0;34;40m.[0;32;40m.[0;31;40m.[0;34;40m.[0;31;40m.[0;32;40m.[0;31;40m.[0;32;40m.[0;31;40m.[0;32;40m..[0;34;40m [0;32;40m   [0;31;40m [0;32;40m        [0;34;40m   [0m
[0;34;40m  [0;32;40m [0;31;40m   [0;34;40m     [0;32;40m .[0;31;40m  [0;34;40m [0;32;40m  [0;34;40m  .    [0;32;40m             [0;34;40m  [0m
"""
        
        # with open("POTFUL_Animate/POT1.ansi_c.txt") as fh:
        sys.stdout.write("\r" + Logo)
          
        
        logging.info("\x1b[0;6;31;40m POTFUL \x1b[0;5;30;0m")
        # with open("POTFUL_Animate/POT1.ansi_c.txt") as fh:
        logging.info(Logo)
        
        
        self.sym ="\U0001F372"
        self.ok = "\U0001F44C"
        self.err ="\U0001F646"
        
        self.Auxiliary_File = defaultdict(dict)
        self.Auxiliary_Data = defaultdict(dict)
        self.File = defaultdict(dict)
        self.Data = defaultdict(dict)
        self.Plots = defaultdict(dict)
        self.Samples = []
        
        self.OutDir = "POTFUL_OUT/"
        Path(self.OutDir).mkdir(parents=True, exist_ok=True)
        
        logging.info(f"{self.sym}Intialized\n")
        
        print(f"Results will be saved in '{self.OutDir}' folder")
        
        
    
    def LOCATE_FILE(self, F):
        logging.info(f"\nLOCATE_FILE START")
        if not F:
            logging.error(f"Invalid file!")
            raise ValueError(f"Invalid file!")
            
        P = Path(F)
        if not P.is_file():
            logging.error(f"{F} Not Found ! {self.err} Please make sure file is in the path and try again")
            raise ValueError(f"{self.sym}POTFUL Not initialized yet! ADD {F} files.")
            
        logging.info(f"LOCATE_FILE END\n")
        
    def Load_Auxiliary_Files(self, WGCNA_COLOR_MAP=None, TF_Targets=None, TF_Family=None):
        logging.info(f"\nLoad_Auxiliary_Files START")
        
        self.Auxiliary_File={
            'WGCNA_COLOR_MAP' : WGCNA_COLOR_MAP,
            'TF_Targets' : TF_Targets,
            "TF_Family"  : TF_Family
        }
        
        # WGCNA_COLOR_MAP #############################################
        self.LOCATE_FILE(self.Auxiliary_File['WGCNA_COLOR_MAP'])
        WGCNA_COL_DF = pd.read_csv(self.Auxiliary_File['WGCNA_COLOR_MAP'])
        cols = list(WGCNA_COL_DF)
        if len(cols) != 2:
            logging.error(f"{self.Auxiliary_File['WGCNA_COLOR_MAP']} Invalid file!")
            raise ValueError(f"{self.Auxiliary_File['WGCNA_COLOR_MAP']} Invalid file!")
        WGCNA_COL_DF = WGCNA_COL_DF.set_index(cols[0])
        WGCNA_COL_DIC = WGCNA_COL_DF.to_dict()[cols[1]]
        
        logging.info(WGCNA_COL_DF.head(5))
        
        self.Auxiliary_Data["WGCNA_COL_DIC"] = WGCNA_COL_DIC
        self.Auxiliary_Data["WGCNA_COL_DF"] = WGCNA_COL_DF
        
        logging.info('# self.Auxiliary_Data')
        # logging.info(self.Auxiliary_Data)
        
    
        # TF_Family ##################################################
        self.LOCATE_FILE(self.Auxiliary_File['TF_Family'])
        tfdf = pd.read_csv(self.Auxiliary_File['TF_Family'], sep=",")
        cols = list(tfdf)
        if len(cols) != 2:
            logging.error(f"{self.Auxiliary_File['TF_Family']} Invalid file!")
            raise ValueError(f"{self.Auxiliary_File['TF_Family']} Invalid file!")

        self.Auxiliary_Data["TFs"] = list(set(tfdf[cols[0]].values.tolist()))
        
        logging.info(self.Auxiliary_Data["TFs"][:5])
                
        # TF_Targets ############################################
        self.LOCATE_FILE(self.Auxiliary_File['TF_Targets'])
        df = pd.read_csv(self.Auxiliary_File['TF_Targets'], nrows=5, sep="\t")
        cols = list(df)
        if len(cols) != 3:
            logging.error(f"{self.Auxiliary_File['TF_Family']} Invalid file!")
            raise ValueError(f"{self.Auxiliary_File['TF_Family']} Invalid file!")
            
        logging.info('# TF_Targets')
        logging.info(df)
        
        print(f"{self.sym}Auxiliary File {pp.pprint(self.Auxiliary_File)}")
        logging.info('# Auxiliary_File')
        logging.info(pp.pprint(self.Auxiliary_File))
        
        logging.info(f"Load_Auxiliary_Files END\n")


        
    def Load_Files(self, Sample_name=None, NODE_File = None, EDGE_File = None, GRN_File=None):
        logging.info(f"\nLoad_Files START")
        
        print(Sample_name)
        print(f"{self.sym}Sample {Sample_name}")
        logging.info('# Sample name')
        logging.info(Sample_name)
        
        
        if not isinstance(Sample_name, str):
            logging.error(f"Invalid Sample name.")
            raise ValueError(f"Invalid Sample name.")
            
        if Sample_name not in self.Samples:
            self.Samples.append(Sample_name)
            
        self.File[Sample_name]["WGCNA"]={
            'NODE' : NODE_File,
            'EDGE' : EDGE_File,
        }
        self.File[Sample_name]["GRN"] = GRN_File
        
        # NODE_File
        self.LOCATE_FILE(self.File[Sample_name]["WGCNA"]['NODE'])
        
        df = pd.read_csv(self.File[Sample_name]["WGCNA"]['NODE'], nrows=3, sep="\t")
        cols = list(df)
        if len(cols) != 3:
            print("Columns: ",cols)
            logging.error(f"{self.File[Sample_name]['WGCNA']['NODE']} Invalid file!")
            raise ValueError(f"{self.File[Sample_name]['WGCNA']['NODE']} Invalid file!")
              
        logging.info('# NODE FILE')
        logging.info(self.File[Sample_name]["WGCNA"]['NODE'])
        logging.info(df)
        
        # EDGE_File
        self.LOCATE_FILE(self.File[Sample_name]["WGCNA"]["EDGE"])
        df = pd.read_csv(self.File[Sample_name]["WGCNA"]['EDGE'], nrows=3, sep="\t")
        cols = list(df)
        if len(cols) < 3:
            print("Cols: ", cols)
            logging.error(f"{self.File[Sample_name]['WGCNA']['EDGE']} Invalid file!")
            raise ValueError(f"{self.File[Sample_name]['WGCNA']['EDGE']} Invalid file!")
                    
        logging.info('# EDGE FILE')
        logging.info(self.File[Sample_name]['WGCNA']['EDGE'])
        logging.info(df)
        
        
        # GRN_File
        self.LOCATE_FILE(self.File[Sample_name]["GRN"])
        print(self.File[Sample_name]["GRN"])
        df = pd.read_csv(self.File[Sample_name]["GRN"], nrows=3, sep="\t")
        cols = list(df)
        if len(cols) != 3:
            logging.error(f"{self.File[Sample_name]['GRN']} Invalid file!")
            raise ValueError(f"{self.File[Sample_name]['GRN']} Invalid file!")
            
            
        logging.info('# GRN FILE')
        logging.info(self.File[Sample_name]['GRN'])
        logging.info(df)
        # print(df)
        
        print(f"{self.sym} Files {pp.pprint(self.File)}")
        
        logging.info(f"{self.sym} Files {pp.pprint(self.File)}")
        
        logging.info(f"Load_Files END\n")


    #######################################
    @staticmethod
    def PlotBar(df):
        logging.info(f"\nPlotBar START")
        import plotly.graph_objects as go

        colors = [i.upper() for i in df.hex.values.tolist()]


        fig = go.Figure(data=[go.Bar(
            x=df.Module.values.tolist(),
            y=df.Count.values.tolist(),
            marker_color=colors # marker color can be a single color value or an iterable
        )])
        
        logging.info(f"PlotBar END\n")

        return fig
    
    def Bucket(self, File, Sample_name = None, Step=10, Print=False):
        logging.info(f"\nBucket START")
                
        df = pd.read_csv(File, sep="\t")
        # print(df.head())
        Cols = list(df)
        # print(Cols)
        df = df.rename(columns={Cols[0]: "ID", Cols[1]: "Symbol", Cols[2] : "Module"})
        # print(df.head())
        Module = df.Module.values.tolist()
        Color_hex = []

        for i in Module:
            Color_hex.append(self.Auxiliary_Data["WGCNA_COL_DIC"][i])
        df["Color_hex"] = Color_hex

        Dic = defaultdict(list)
        for ID, Symbol, Module, hex_color in df.values:
            Dic[Module].append(ID)

        Dic_count = {}
        for i in Dic:
            Dic[i] = set(Dic[i])
            Dic_count[i] = len(Dic[i])

        df_count = pd.DataFrame(Dic_count.items(), columns=['Module', 'Count'])
        df_count.sort_values('Count', ascending=False, inplace=True)
        df_count["hex"] = df_count["Module"]

        df_count.replace({"hex": self.Auxiliary_Data["WGCNA_COL_DIC"]}, inplace=True)
        # print(df_count)
        
        ## barPlot 
        fig_bar = self.PlotBar(df_count)
        fig_bar.update_layout(title_text=f'"{Sample_name}" WGCNA module Barplot.')
        if Sample_name:
            self.Plots[Sample_name]["WGCNA_BarPlot"] = fig_bar
            self.Data[Sample_name]["WGCNA_BarPlot"] = df_count
        else:
            self.Plots[File]["WGCNA_BarPlot"] = fig_bar
            self.Data[File]["WGCNA_BarPlot"] = df_count
            
        ##########################

        for i in Dic:
            Dic[i] = set(Dic[i])
            if Print:
                print(f"Number of gene in {i} bucket : {len(Dic[i])}")
        logging.info("Bucket END\n")
        return dict(Dic)
    
    
    
    def Dict_to_gmt(self, Dic, discription="NA", file_name = "WGCNA_file"):
        logging.info("\nDict_to_gmt START")
        
        from pathlib import Path
        Elements = []

        GMT_Dir = "GMT_base/"
        Path(GMT_Dir).mkdir(parents=True, exist_ok=True)

        file_name = GMT_Dir + file_name + ".gmt"
        fh = open(file_name, "w")
        for i in Dic:
            set_name = i
            Items = '\t'.join(set(Dic[i]))
            for j in Dic[i]:
                Elements.append(j)
            print(set_name, discription, Items, sep="\t", file=fh)
            # print(set_name, discription, len(set(Dic[i])))

        fh.close()
        Elements = list(set(Elements))
        print(file_name, len(Elements))
        
        logging.info("Dict_to_gmt END\n")
        return file_name, Elements
    
    def WGCNA_Bucket_GMT(self):
        logging.info("\nWGCNA_Bucket_GMT START")
        
        for Sample in self.File:
            
            logging.info(">"+Sample)
            
            Node_File = self.File[Sample]['WGCNA']['NODE']
            # print(Node_File)
            Buckets = self.Bucket(Node_File, Sample_name=Sample)
            self.Data[Sample]["WGCNA_Bucket"] = Buckets
            
            GMT_file, Elements = self.Dict_to_gmt(self.Data[Sample]["WGCNA_Bucket"], discription="WGCNA" + Sample, file_name = "POTFUL-" + Sample)
            self.File[Sample]['GMT'] = GMT_file
            self.Data[Sample]['Elements'] = Elements
            
        logging.info("WGCNA_Bucket_GMT END\n")


    def Module_Enrichment(self,Gene_set_name, gmt, Genes, Gene_set, sig = 'Adjusted P-value', col_name = "Target"):
        logging.info("\nModule_Enrichment START")

        enr = gp.enrichr(gene_list=Gene_set,
                         gene_sets=gmt, 
                        #  description='test_name',
                         outdir='test',
                         background=Genes,
                         cutoff=1 
                        )

        if enr.results.empty:
            logging.info('DataFrame is empty!')
            return pd.DataFrame(columns=[col_name, sig, 'Overlap'])

        # print(list())
        enr.results['Gene_set'] = Gene_set_name
        df = enr.results


        enr.results = enr.results.rename(columns={'Term':col_name})
        
        logging.info("Module_Enrichment END\n")
        return enr.results[[col_name, sig, 'Overlap']], df


    def Bucket_Enrichment(self,x_GMTfile, y_Bucket, x_Genes, y_Genes):
        logging.info("\nBucket_Enrichment START")
        Genes = list(set(x_Genes + y_Genes))

        print(f"\nTotal Number of genes in {len(Genes)}")
        logging.info(f"\nTotal Number of genes in {len(Genes)}")
        
        df_list = []
        df_list_all = []

        for S in y_Bucket:
            # print(S)

            Gene_set = list(y_Bucket[S])
            # print(Gene_set)
            Df, all_df = self.Module_Enrichment(S, x_GMTfile, Genes, Gene_set)
            ench_Df = Df.copy()
            df_list_all.append(all_df)
            ench_Df['Source'] = S

            # print(ench_Df)

            ench_Df.loc[ench_Df['Adjusted P-value'] > 0.05, 'Significance'] = 'NE'
            ench_Df.loc[ench_Df['Adjusted P-value'] <= 0.05, 'Significance'] = '*'
            ench_Df.loc[ench_Df['Adjusted P-value'] <= 0.01,'Significance'] = '**'
            ench_Df.loc[ench_Df['Adjusted P-value'] <  0.001, 'Significance'] = '***'
            df_list.append(ench_Df)
            # break
            
        logging.info("Bucket_Enrichment END\n")
        return df_list, df_list_all
    
        
    def Plot_gseapy_Enrichment(self,df_gseapy, Xlab = "X", Ylab = "Y", axis_order = None, width=500, height=500):
        logging.info("\nPlot_gseapy_Enrichment START")

        fig = px.scatter(df_gseapy, x="Target", y="Source", color="Significance", symbol = "Significance", 
                        category_orders={"Target": axis_order,
                                         "Source": axis_order[::-1],
                                         "Significance" : ['***', "**", "*", "NC"],                
                                        },
                         color_discrete_map={
                        '***' : "#88C408",
                        '**' : "#A69363",
                        '*': "#FFD602",
                        "NE": "#808285"
                         },

                         symbol_map ={
                        '***' : 200,
                        '**' : 200,
                        '*': 200,
                        "NE": 33
                         },
                         template="plotly_white",
                        )

        fig.update_traces(marker=dict(size=15,
                                      line=dict(width=2,
                                                color='#144B39')),
                          selector=dict(mode='markers')
                         )

        fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
        fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True)

        # Size of the plot   
        fig.update_layout(
            title=f"wk-Shell Enrichment",
            autosize=False,
            # width=width,
            # height=height,
            # paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title=Xlab
            ),
            yaxis=dict(
                title=Ylab
            ),
            font=dict(
                family="Arial",
                size=14,
                # color="black"
            )
        )


        # Update legend
        fig.update_layout(
            legend=dict(title = f'Enrichment',
                orientation="v",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
                # traceorder="reversed",
                title_font_family="Times New Roman",
                font=dict(
                    family="Arial",
                    size=12,
                    # color="black"
                ),
                bgcolor="rgba(0,0,0,0)",
                bordercolor="Black",
                borderwidth=2
            )
        )
        logging.info("Plot_gseapy_Enrichment END\n")
        return fig
###############################################

    def common_order_bucket(self, b1,b2):
        logging.info("\ncommon_order_bucket START")
        if len(b1) >= len(b2):
            s1,s2 = set(list(b1)), set(list(b2))
        else:
            s2,s1 = set(list(b1)), set(list(b2))
            
        # print(len(b1) ,len(b2))
        logging.info(f"{len(b1)} ,{len(b2)}")
        
        cb = s1.intersection(s2)
        # order
        # print("<><><>", cb)
        logging.info(f"<><><>{ cb}")
        
        cbo = [] # common bucket order
        for i in self.Auxiliary_Data["WGCNA_COL_DF"].index.values:
            if i in cb:
                cbo.append(i)
        
        logging.info(cbo)
        logging.info("common_order_bucket END\n")
        return cbo
######################################################
    
    def WGCNA_Module_Enrichment(self, Sample1=None, Sample2=None):
        logging.info("\nWGCNA_Module_Enrichment START")
        
        print(Sample1, Sample2)
        logging.info(f"Samples {Sample1} {Sample2}")
        
        x_GMTfile, y_GMTfile = self.File[Sample1]['GMT'], self.File[Sample2]['GMT']
        x_Bucket, y_Bucket =   self.Data[Sample1]['WGCNA_Bucket'],  self.Data[Sample2]['WGCNA_Bucket']
        x_Genes, y_Genes = self.Data[Sample1]['Elements'],  self.Data[Sample2]['Elements']
        

        cbo = self.common_order_bucket(x_Bucket,y_Bucket) # common bucket order
        # cbo = cbo[:20]
        
        df_list, df_list_all = self.Bucket_Enrichment(x_GMTfile, y_Bucket, x_Genes, y_Genes)
        # df_gseapy = pd.concat(df_list)
        
        ###############################################
        All_enrichment_data = pd.concat(df_list_all)

        Cols = list(All_enrichment_data)
        All_enrichment_data.rename(columns={Cols[1]:Cols[1]+" ("+Sample1+") "}, inplace=True)
        All_enrichment_data.rename(columns={Cols[0]:Cols[0]+" ("+Sample2+") "}, inplace=True)
        All_enrichment_data = All_enrichment_data[All_enrichment_data['Adjusted P-value']<=0.05]


        All_enrichment_data.loc[All_enrichment_data['Adjusted P-value'] > 0.05, 'Significance'] = 'NE'
        All_enrichment_data.loc[All_enrichment_data['Adjusted P-value'] <= 0.05, 'Significance'] = '*'
        All_enrichment_data.loc[All_enrichment_data['Adjusted P-value'] <= 0.01,'Significance'] = '**'
        All_enrichment_data.loc[All_enrichment_data['Adjusted P-value'] <  0.001, 'Significance'] = '***'

        Cols = list(All_enrichment_data)
        Cols[-1] = 'Genes'
        Cols[-2] = 'Significance'
        All_enrichment_data = All_enrichment_data[Cols]
        ##############################################
        
        df_gseapy = pd.concat(df_list)
        df_gseapy.Target.unique()

        fig_ench_dot = self.Plot_gseapy_Enrichment(df_gseapy, Xlab = Sample1, Ylab = Sample2, axis_order = cbo)#, width=1500, height=1000)
        
        self.Plots["Enrichment_Dotplot"] = fig_ench_dot
        self.Data["Enrichment_Dotplot"] = All_enrichment_data

        fig_ench_dot.write_image(self.OutDir +  Sample1 +"__"+ Sample2 +"Enri_dot.svg")
        fig_ench_dot.write_image(self.OutDir +  Sample1 +"__"+ Sample2 +"Enri_dot.png")
        
        logging.info("WGCNA_Module_Enrichment END\n")


    
    @staticmethod
    def Rescale_GRN(data):
        # data = pd.read_csv(S_GRN_File, sep="\t")
        # Min-Max Normalization
        logging.info("\nRescale_GRN START")
        
        df = data['importance']
        df_norm = (df-df.min())/(df.max()-df.min())
        #df_norm = pd.concat((df_norm, data), 1)

        print("Scaled Dataset Using Pandas")
        logging.info("Scaled Dataset Using Pandas")
        
        data["importance"] = list(df_norm)
        
        logging.info("Rescale_GRN END\n")
        return data

    # @staticmethod
    def TF_dic(self, TFT_File, rescale=False):
        logging.info("\nTF_dic START")
        
        Dic = {}
        df = pd.read_csv(TFT_File, sep="\t")
        df = df.dropna()
        if rescale:
            df = self.Rescale_GRN(df)


        for TF,T,W in df.values:
            # print(TF,T)
            try:
                TFT = "_".join([TF,T])
                Dic[TFT] = W
            except:
                print(TF,T)

        print(f"Total number of TFT pairs in {TFT_File} :{len(Dic)}")
        logging.info(f"Total number of TFT pairs in {TFT_File} :{len(Dic)}")
        
        logging.info("TF_dic END\n")
        return Dic
    
    
    ####################################################
    # merge_TF_reg
    ####################################################
        
    def merge_TF_reg(self, Sample_name):
        logging.info("\nmerge_TF_reg START")
        
        TFT_File, GRN_File = self.Auxiliary_File['TF_Targets'], self.File[Sample_name]["GRN"]
        print(Sample_name, TFT_File, GRN_File)
        
        TFT_Dic = self.TF_dic(TFT_File)
        GRN_Dic = self.TF_dic(GRN_File, rescale=True)

        TFT_Dic_set = set(TFT_Dic)
        GRN_Dic_set = set(GRN_Dic)

        Common = GRN_Dic_set.intersection(TFT_Dic_set)
        print(f"Total number of common pairs:{len(Common)}")
        logging.info(f"Total number of common pairs:{len(Common)}")


        GRN_TFT_Dic = {}
        for i in Common:
            GRN_TFT_Dic[i] = GRN_Dic[i]

        print(f"Total number of common pairs:{len(GRN_TFT_Dic)}")
        logging.info(f"Total number of common pairs:{len(GRN_TFT_Dic)}")

        # self.Auxiliary_Data['GRN_TFT_Dic'] =  GRN_TFT_Dic
        self.Data[Sample_name]["GRN_TFT_Dic"] = GRN_TFT_Dic
        
        logging.info("merge_TF_reg END\n")

    ####################################################
    # merge_reg_coexp
    ####################################################
    
    def merge_reg_coexp(self, Sample_name):
        logging.info("\nmerge_reg_coexp START")
        
        GRN_TFT_Dic = self.Data[Sample_name]["GRN_TFT_Dic"]
        Edge_File = self.File[Sample_name]['WGCNA']['EDGE']
        # print(Edge_File, GRN_TFT_Dic)
        # return 
        print(f"{Edge_File}")
        logging.info(f"{Edge_File}")


        # print(df_edge)

        Coexp_Dic = {}
        df_edge = pd.read_csv(Edge_File, sep="\t", usecols=[0,1,2])
        df_edge = df_edge.dropna()


        for IDa, IDb, W in df_edge.values:
            # print(TF,T)
            try:
                AB = "_".join([IDa, IDb])
                BA = "_".join([IDb, IDa])
                Coexp_Dic[AB] = W
                Coexp_Dic[BA] = W
            except:
                print(IDa, IDb)

        print(f"Total number of coexpressed combo-pairs:{len(Coexp_Dic)}")
        logging.info(f"Total number of coexpressed combo-pairs:{len(Coexp_Dic)}")

        GRN_TFT_Dic_set = set(GRN_TFT_Dic)
        Coexp_Dic_set = set(Coexp_Dic)

        Common = GRN_TFT_Dic_set.intersection(Coexp_Dic_set)
        print(f"Total number of common pairs:{len(Common)}")
        logging.info(f"Total number of common pairs:{len(Common)}")
        

        GRN_TFT_coexp_Dic = {}
        for i in Common:
            GRN_TFT_coexp_Dic[i] = GRN_TFT_Dic[i]

        print(f"Total number of common pairs:{len(GRN_TFT_coexp_Dic)}")
        logging.info(f"Total number of common pairs:{len(GRN_TFT_coexp_Dic)}")

        Network_out_file = self.OutDir + Sample_name + "_Coexp_GRN.tsv" #Edge_File.replace(".txt", "_Coexp_GRN.tsv")

        LOL = []
        for k,v in GRN_TFT_coexp_Dic.items():
            TF,T = k.split("_")
            LOL.append([TF,T,v])
        df_net = pd.DataFrame(LOL)
        df_net.columns = ['TF', 'Target', 'importance']
        df_net.to_csv(Network_out_file, sep="\t", index=False)

        G = nx.from_pandas_edgelist(df_net, "TF", "Target", "importance", create_using=nx.DiGraph())

        print(Network_out_file, G)
        logging.info(f"{Network_out_file} {G}")
        
        self.Data[Sample_name]["GRN_TFT_coexp_Dic"] = GRN_TFT_coexp_Dic
        self.Data[Sample_name]["df_net"] = df_net
        self.Data[Sample_name]["Network"] = G
        self.File[Sample_name]["Network_file"] = Network_out_file
        
        logging.info("merge_reg_coexp END\n")

        # return GRN_TFT_coexp_Dic, df_net    
    
    @staticmethod
    def Centrality_to_lable(G, cuttoff=7.5):
        logging.info("\nCentrality_to_lable START")
        
        Degree_L = []
        Betweenness_L = []
        CC_L = []
        for n in G.nodes:
            # print(n, G.nodes[n]['Degree'])
            Degree_L.append((n, G.nodes[n]['Degree_nx']))
            Betweenness_L.append((n, G.nodes[n]['Betweenness_nx']))
            CC_L.append((n, G.nodes[n]['Clustering_coefficient_nx']))

        Degree_L = sorted(Degree_L, key=lambda x: x[1], reverse=True)
        Betweenness_L = sorted(Degree_L, key=lambda x: x[1], reverse=True)
        CC_L = sorted(Degree_L, key=lambda x: x[1], reverse=True)


        Top_n = floor(G.number_of_nodes()*cuttoff/100)

        def gene_lable_dict(sLOT, Top_n, Lable=np.nan):
            Count = 1
            Dic_attr = {}
            for i in range(len(sLOT)):
                Flag = Lable
                if Count > Top_n:
                    Flag = np.nan
                # print(Top_n, i, Count, sLOT[i][0], Flag)
                Dic_attr[sLOT[i][0]] = Flag
                Count += 1
            return(Dic_attr)

        Degree_Lable_attr = gene_lable_dict(Degree_L, Top_n, Lable="Hub")
        nx.set_node_attributes(G, Degree_Lable_attr, "Degree_Hub")

        Betweenness_Lable_attr = gene_lable_dict(Betweenness_L, Top_n, Lable="Bottleneck")
        nx.set_node_attributes(G, Betweenness_Lable_attr, "Betweennes_bottleneck")

        CC_Lable_attr = gene_lable_dict(CC_L, Top_n, Lable="Top_7.5")
        nx.set_node_attributes(G, CC_Lable_attr, "CC_Top")
        
        logging.info("Centrality_to_lable END\n")
        return G
    
    
    
    # @staticmethod
    def Network_analysis(self, G, cuttoff=7.5):
        logging.info("\nNetwork_analysis START")
        logging.info(G)
        print(G)

        # Degree_Centrality
        deg = nx.degree(G)
        Deg_dic = {i[0]:i[1] for i in deg}
        print(f"Degree Dict {isinstance(Deg_dic, dict)}")
        logging.info(f"Degree Dict {isinstance(Deg_dic, dict)}")
        nx.set_node_attributes(G, Deg_dic, "Degree_nx")
        # print(G.nodes['P42669']["Degree"])


        # betweenness_centrality
        bb = nx.betweenness_centrality(G)
        print(f"Betweenness Dict {isinstance(bb, dict)}")
        logging.info(f"Betweenness Dict {isinstance(bb, dict)}")
        nx.set_node_attributes(G, bb, "Betweenness_nx")
        # print(G.nodes['Q9DC51']["Betweenness"])

        # Degree_Centrality
        degc = nx.degree_centrality(G)
        print(f"Degree Dict {isinstance(degc, dict)}")
        logging.info(f"Degree Dict {isinstance(degc, dict)}")
        
        nx.set_node_attributes(G, degc, "Degree_Centrality_nx")
        # print(G.nodes['Q9DC51']["Degree_Centrality"])

        # Degree_Centrality
        clust = nx.clustering(G)
        print(f"clust Dict {isinstance(clust, dict)}")
        logging.info(f"clust Dict {isinstance(clust, dict)}")
        
        nx.set_node_attributes(G, clust, "Clustering_coefficient_nx")
        # print(G.nodes['Q9Z2U0']["Clustering_coefficient"])
        
        logging.info("Network_analysis END\n")
        return self.Centrality_to_lable(G, cuttoff=7.5)
    
    def network_centrality(self, Sample_name, cuttoff=7.5):
        logging.info("\nnetwork_centrality START")
        
        if Sample_name not in self.Data:
            raise Exception(f"{Sample_name} 'Sample not found!' ")
        
        else:
            if "Network" not in self.Data[Sample_name]:
                raise Exception(f"{Sample_name} 'Graph not found!' 'run merge_reg_coexp()'")
                
        print(self.Data[Sample_name]["Network"])
        logging.info(self.Data[Sample_name]["Network"])
        
        G = self.Network_analysis(self.Data[Sample_name]["Network"])
        self.Data[Sample_name]["Network"] = G
        
        logging.info("network_centrality END\n")
    
    def Graph_vis(self, Sample_name):
        logging.info("\nGraph_vis START")
        
        G = self.Data[Sample_name]["Network"]
        g = net.Network(notebook=True)
        g.from_nx(G)

        # g.show_buttons()
        HTML_FILE = self.OutDir + Sample_name + "_Network.html" #self.File[Sample_name]['WGCNA']['NODE'].replace(".txt", ".html")
        g.save_graph(HTML_FILE)
        self.Plots[Sample_name]['Network_Viz'] = g
        self.File[Sample_name]["Network_HTML"] = HTML_FILE
        
        logging.info("Graph_vis END\n")
        
        
        
    def generate_graphml_out(self, Sample_name, ID_Column = "ID"): #df_net, Node_File):
        """
        Sample_name = Sample index number [0,1,2...]
        ID_Column = Of the WGCNA node file which column should be taken into consideration, ID/First col (default) or AltName/ Second col. In genral For micro array AltName/ Second col and for RNA-Seq ID/First col. 
        """
        
        logging.info("\ngenerate_graphml_out START")
        
        G = self.Data[Sample_name]["Network"]
        print(G)
        logging.info(G)
        
        Nodes = G.nodes

        Gene_color = {}
        WGCNA_Module = {}
        TF_Flag = {}
        df = pd.read_csv(self.File[Sample_name]['WGCNA']['NODE'], sep="\t")
        for ID,AltName, Module in df.values:
            
            if ID_Column != "ID":
                ID = AltName
            
            Gene_color[ID] = self.Auxiliary_Data['WGCNA_COL_DIC'][Module]
            WGCNA_Module[ID] = Module
            if ID_Column in self.Auxiliary_Data['TFs']:
                TF_Flag[ID] = "TF"
            else:
                TF_Flag[ID] = "Non_TF"
                
        
        attrs = {}
        for node in Nodes:
            # print(node, Gene_color)
            
            d = {"color": Gene_color[node], "TF": TF_Flag[node], "WGCNA_Module": WGCNA_Module[node]}
            attrs[node] = d
        # Gene_color
        # TF_Flag
        attrs

        nx.set_node_attributes(G, attrs)
        
        ######################
        attrs_size = {}

        for node in G.nodes:
            # print(node, G.nodes[node]['TF'])
            size = 10
            if G.nodes[node]['TF']=="TF":
                size = 20
                
            d = {"size":size}
            attrs_size[node] = d
        nx.set_node_attributes(G, attrs_size)
        
        ####################

        Ws = []
        for e in G.edges:
            Ws.append(G.edges[e]['importance'])
        Ws.sort()
        bins = np.array([max(Ws)*1, max(Ws)*.75, max(Ws)*.5, max(Ws)*.25, max(Ws)*.0])
        BIN = lambda x: (7-np.digitize(np.array([x]),bins,right=True)[0])/2
        np.digitize(np.array([0.10598739]),bins,right=True)[0]
        e_attr = {}
        for e in G.edges:
            e_attr[e] = {"weight":BIN(G.edges[e]['importance'])}
        nx.set_edge_attributes(G, e_attr)


        graphml_out = self.OutDir + Sample_name + "_Network.graphml" #self.File[Sample_name]['WGCNA']['NODE'].replace(".txt", ".graphml")
        nx.write_graphml_lxml(G, graphml_out)
        self.File[Sample_name]["Network_GraphML"] = graphml_out
        
        self.Data[Sample_name]["Network"] = G
        
        logging.info("generate_graphml_out END\n")
    
    
    ##################################################
    def network_overlap(self, sample1, sample2):
        logging.info("\nnetwork_overlap START")
        
        # print(G1, G2, POT.Auxiliary_Data['TFs'])
        G1 = self.Data[sample1]["Network"]
        G2 = self.Data[sample2]["Network"]
        
        Nodes1 = set(G1.nodes())
        Nodes2 = set(G2.nodes())

        # sample1, sample2 = "pH", "Sulfur"

        Overlapping_nodes = Nodes1.intersection(Nodes2)
        self.Data[sample1][sample2] = {"Intersection":Overlapping_nodes, 
                                       "Symmetric_difference": Nodes1 ^ Nodes2, 
                                       "Difference":Nodes1 - Nodes2}
        
        self.Data[sample2][sample1] = {"Intersection":Overlapping_nodes, 
                                       "Symmetric_difference":Nodes2 ^ Nodes1, # Same as Nodes1 ^ Nodes2
                                       "Difference":Nodes2 - Nodes1}
        
        if not len(Overlapping_nodes):
            warnings.warn(f"{self.sym} {self.sym} There no common node between pair of Graphs")
            logging.info(f"{self.sym} {self.sym} There no common node between pair of Graphs")
            return
        else:
            print(f"{self.sym} {self.ok} There are {len(Overlapping_nodes)} nodes overlapping between pair of Graphs")
            logging.info(f"{self.sym} {self.ok} There are {len(Overlapping_nodes)} nodes overlapping between pair of Graphs")


        print(Overlapping_nodes)
        logging.info(Overlapping_nodes)
        
        # self.Data["Overlapping_nodes"] = Overlapping_nodes
        
        G = nx.compose(G1,G2)
        # print(G.nodes['AT1G25400'])
        edgelist = G.edges()
        # reset attributes
        G = nx.from_edgelist(edgelist)

        attr = {}
        for n in G.nodes:
            color = "#FFD602"
            size = 10
            TF = "NON_TF"
            Net = sample1

            if n in Nodes1 and n not in Nodes2:
                color = "#1E6B52" #yellow
                Net = sample1
            if n in Nodes2 and n not in Nodes1:
                color = "#A69363" #yellow
                Net = sample2
            if n in Overlapping_nodes:
                color = "#FFD602" #yellow
                Net = " ".join([sample1, "and", sample2])

            if n in self.Auxiliary_Data['TFs']:
                size = 20
                TF = "TF"

            d = {"color":color, "TF":TF, "size":size, "Net":Net}
            attr[n]=d

        nx.set_node_attributes(G, attr)

        # self.Data["Overlap_Network"] = G
        self.Data[sample1][sample2]["Network"]=G
        self.Data[sample2][sample1]["Network"]=G

        # G = self.Data[Sample_name]["Network"]
        g = net.Network(notebook=True)
        g.from_nx(G)

        # g.show_buttons()
        HTML_FILE = self.OutDir+sample1+"_"+sample2+"_"+"Overlapping_network.html"
        g.save_graph(HTML_FILE)
        self.Plots[sample1+"_"+sample2+"_"+'Overlap_Network_Viz'] = g
        self.File[sample1+"_"+sample2+"_"+"Overlap_Network_HTML"] = HTML_FILE
        
        nx.write_graphml_lxml(G, self.OutDir+"Overlapping_network.graphml")
        
        logging.info("network_overlap END\n")
        logging.info(f"{self.sym} END!!")
        
        logging.shutdown()
        
        

