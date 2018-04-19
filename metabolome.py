#!/usr/bin/env python
# -*- coding: utf-8 -*-
# metabolome.py

import pickle
from collections import OrderedDict, defaultdict
from itertools import product
import locale
import tkinter as tk
from tkinter import filedialog




def parse_hmdb():
    hmdb_id = ''
    mass = 0
    metabolites = defaultdict(list)
    with open('hmdb_metabolites.xml', 'r', encoding='utf-8') as o:
        for l in o:
            if '<metabolite>' in l:
                if mass and hmdb_id:
                    metabolites[mass].append(hmdb_id)
                    mass = 0
                    hmdb_id = ''
            if '<accession>' in l and not hmdb_id:
                hmdb_id = l.split('>')[1].split('<')[0]
            if '<monisotopic_molecular_weight>' in l and not mass:
                mass = float(l.split('>')[1].split('<')[0])
                
    metabolites = OrderedDict(sorted(metabolites.items(), key=lambda t: t[0]))
    with open('dict.txt', 'wb') as d:
        pickle.dump(metabolites, d)

def find_mass(metabolites=''):
    all_mass = []
    error = 0.01
    if not metabolites:
        with open('dict.txt', 'rb') as d:
            metabolites = pickle.load(d)
    #for a, b in metabolites.items():
    #    print(a, b)
    with open('table1.txt', 'r', encoding='utf-8') as o:
        for molecule_mass in o:
            all_mass.append(float(molecule_mass))
    for mass, hmdb_ids in metabolites.items():
        for molecule_mass in all_mass:
            #print(molecule_mass, mass)
            if abs(molecule_mass - mass) < error:
                print('Found!!! {} {} {}'.format(hmdb_id, mass, molecule_mass))
            elif mass-molecule_mass > error:
                break
            
def find_mass2(n, file_path='table1', metabolites=''):
    all_mass = []
    b = []
    error = 0.01
    old_i = 0
    mets = []
    if not metabolites:
        with open('dict.txt', 'rb') as d:
            metabolites = pickle.load(d)
    with open(file_path, 'r', encoding='utf-8') as o:
        for molecule_mass in o:
            all_mass.append(float(molecule_mass) + n)
    min_error = min(product(all_mass, all_mass), key=key_sort)
    #print(abs(min_error[0] - min_error[1]))
    #error = abs(min_error[0] - min_error[1])
    a = sorted(product(metabolites.keys(), all_mass), key=lambda t: abs(t[0]-t[1]))
    
    with open('temp.txt', 'wb') as temp:
        pickle.dump(a, temp)
    for i in a:
        if abs(i[0]-i[1]) < error: #and len(metabolites[i[0]]) == 1:
            b.append(i)
    b = sorted(b, key=lambda t: t[1])
    for i in b:
        if old_i == i[1]:
            continue
        else:
            old_i = i[1]
        #pass
        locale.setlocale(locale.LC_ALL, "")
        for m in metabolites[i[0]]:
            mets.append(m+ '\t'+ locale.format("%g",i[1])+'\n')
        #mets.append(' '.join(metabolites[i[0]])+ '\t'+ locale.format("%g",i[1])+'\n')
        print(metabolites[i[0]][0]+ '\t'+ locale.format("%g",i[1]))       
        #print(metabolites[i[0]], i[0]-i[1])
    with open('out.txt', 'w') as w:
        for m in mets:
            w.write(m)
    #print(len(b))
def key_sort(t):
    if t[0] == t[1]:
        return 100
    else:
        return abs(t[0]-t[1])
#parse_hmdb()
#for i in range(-5*2,6*2):
    #find_mass2(i/2.0)

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
find_mass2(-1, file_path)
