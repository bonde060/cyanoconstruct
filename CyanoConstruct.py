

import random
import copy

##=====================================================================================
def get_data_list(fname): ##opens, parses through excel sheet
    contents = []
    try:
        fname = open(fname, "r")
        for line in fname.readlines():
            line = line.split(",")
            contents.append(line)
        return contents
    except FileNotFoundError:
        return -1

## Go through optimal list first 
##=====================================================================================
def findseq(term): #returns sequence associated with elm. name
    assemblycode = get_data_list("assemblycode.csv")
    GOIstart = assemblycode.index(['GOI', 'GOIseq\n'])
    GOIend = assemblycode.index(['Term', 'Termseq\n'])
    seq = ""
    for i in range(len(assemblycode)):
        if assemblycode[i][0] == term:
            
            if i >= GOIstart and i <= GOIend: ##if term is a gene of interest, TG appended to start
                seq += "TG"
            seq += assemblycode[i][1]
            return seq
    return "(Entry not in Data)"

##=====================================================================================

def choice_spacer(ls): ##creates randomly ordered spacer list, variety of fidelity
    options = ["A", "G", "C", "T"]
    spacerchoice = str(input("Spacer fidelity (98.5%, 98.1%, 95.8%, or 91.7%): "))
    firstspacers = []
    endspacers = []
    if spacerchoice == "98.5%":
        spacers = ['TGCC', 'GCAA', 'ACTA', 'TTAC', 'CAGA', 'TGTG', 'GAGC', 'AGGA', 'ATTC', 'CGAA', 'ATAG', "AAGG", "AAAA", "ACCG"]
    elif spacerchoice == "98.1%":
        spacers = ['AGTG', 'CAGG', 'ACTC', 'AAAA', 'AGAC', 'CGAA', 'ATAG', 'AACC', 'TACA', 'TAGA', 'ATGC', 'GATA', 'CTCC', 'GTAA', 'CTGA', 'ACAA','AGGA', 'ATTA', 'ACCG', 'GCGA']
    elif spacerchoice == "95.8%":
        spacers = ['CCTC', 'CTAA', 'GACA', 'GCAC', 'AATC', 'GTAA', 'TGAA','ATTA', 'CCAG', 'AGGA', 'ACAA', 'TAGA', 'CGGA', 'CATA', 'CAGC', 'AACG', 'CTCC', 'ACCA', 'AGTG', 'GGTA', 'GCGA', 'AAAA', 'ATGA']
    elif spacerchoice == "91.7%":
        spacers = ['TACA', 'CTAA', 'GGAA', 'GCCA', 'CACG', 'ACTC', 'CTTC', 'TCAA', 'GATA', 'ACTG', 'AAGC', 'CATA', 'GACC', 'AGGA', 'ATCG', 'AGAG', 'ATTA', 'CGGA', 'TAGA', 'AGCA', 'TGAA', 'CCAG', 'GTGA', 'ACGA', 'ATAC', 'AAAA', 'AAGG', 'CAAC']
    elif spacerchoice == "random" or spacerchoice == "Random":
        spacers = makespacers(ls)
    for i in range(len(spacers)):
        firstspacers.append(random.choice(options) + random.choice(options) + spacers[i])
        endspacers.append(spacers[i]+random.choice(options) + random.choice(options[:3]))
    random.shuffle(firstspacers, random.random)
    random.shuffle(endspacers, random.random)
    while len(firstspacers) < len(ls)-1:
        firstspacers.append(str(random.choice(options)+random.choice(options)+random.choice(options)
              +random.choice(options)+random.choice(options)+random.choice(options[:3])))
        endspacers.append(str(random.choice(options)+random.choice(options)+random.choice(options)
              +random.choice(options)+random.choice(options)+random.choice(options[:3])))
    return (firstspacers, endspacers)


##====================================================================================


def makespacers(ls):  ##creates a 6-nucleotide random seq for each spacer, no repeats
    spacers = []
    options = ["A", "G", "C", "T"]
    for i in range(len(ls)): 
        new = str(random.choice(options)+random.choice(options)+random.choice(options)
              +random.choice(options)+random.choice(options)+random.choice(options[:3]))
        while new in spacers:
            new = str(random.choice(options)+random.choice(options)+random.choice(options)+
              random.choice(options)+random.choice(options)+random.choice(options[:3]))
        spacers.append(new)
    return spacers

##======================================================================================

def createseq():
    sequence =(input("Enter your sequence (Choose Pr, RBS, GOI, Term. Serperate with commas.): "))
    sequence = sequence.split(", ")
    elements = copy.deepcopy(sequence)
    start = "GAAGAC"
    end = "GTCTTC"
    names = copy.deepcopy(sequence)
        
##ERROR TO FIX: Does not recognize invalid entry until reaching that elm
    for i in range(len(sequence)): #gets specific inputs for each element
        if sequence[i]== "Pr" or sequence[i]== "pr" or sequence[i]== "PR":
            names[i] = str(input("Enter the promoter: "))
            elements[i] = names[i]
        elif sequence[i] == "RBS" or sequence[i] == "rbs":
            names[i] = str(input("Enter the ribosome binding site: "))
            elements[i] = names[i]
        elif sequence[i] == "GOI" or sequence[i] == "goi" :
            names[i] = str(input("Enter the gene of interest: "))
            elements[i] = names[i]
        elif sequence[i] == "Term" or sequence[i] == "term" or sequence[i] == "TERM" :
            names[i] = str(input("Enter the terminator: "))
            elements[i] = names[i]
        else:
            return print("Invalid Entry, close program and restart.")
        elements[i] = findseq(elements[i]) #converts inputs to sequence in datasheet

    firstspacers, endspacers =  choice_spacer(elements)

    print("\n Sequence with spaces between spacers and elements: ") ##Prints with spaces, each element on own line
    print("\n"+"("+"TTTGCC  ", elements[0], endspacers[0]+end+")")
    if len(elements) > 1:
        for i in range(len(elements)-2):
            print("("+start+firstspacers[i],elements[i+1], endspacers[i+1]+end+")")
        print("("+start+firstspacers[-1], elements[-1], "  GCAAGG"+")")
    
    print("\n Sequence without spaces between spacers and elements: ")##Prints without spaces, each element on own line
    print("\n"+"TTTGCC"+elements[0]+endspacers[0]+end)
    if len(elements) > 1:
        for i in range(len(elements)-2):
            print(start+firstspacers[i]+elements[i+1]+endspacers[i+1]+end)
        print(start+firstspacers[-1]+elements[-1]+"GCAAGG")

    tmgoal = float(input(" Enter your primer TM: ")) #asks for tm value
    #prints with spaces and breaks at tm value
    firstTM, firstseq,gccontent1, lastTM, lastseq, gccontent2 = findTM(elements[0], tmgoal)
    print("\n Sequence with elements split at the goal TM, spaces between elements and spacers: ")##Prints with spaces, each element on own line, each element split at TM melting spots
    print("\n"+"Left primer for "+names[0])
    print("Left spacer: "+"TTTGCC "+"\n"+"TM: "+str(firstTM)+
          "\nPrimer sequence: "+firstseq+"\nPrimer length: "+str(len(firstseq))+"\nGC Content: "+str(gccontent1)+
          "\n\nRight primer for "+names[0] +"\nRight spacer: "+endspacers[0]+end+"\nTM: "+
          str(lastTM)+"\nPrimer sequence: "+lastseq[:-1]+"\nPrimer length: "+str(len(lastseq)-1)+
          "\nGC Content: "+str(gccontent2)+"\n")   
    if len(elements) > 1:
        for i in range(1, len(elements)-1):
            firstTM, firstseq,gccontent1, lastTM, lastseq, gccontent2 = findTM(elements[i], tmgoal)
            print("\n"+"Left primer for "+names[i])
            print("Left spacer: "+start+firstspacers[i]+"\n"+"TM: "+str(firstTM)+
                  "\nPrimer sequence: "+firstseq+"\nPrimer length: "+str(len(firstseq))+"\nGC Content: "+str(gccontent1)+
                  "\n\nRight primer for "+names[i] +"\nTM: "+str(lastTM)+
                  "\nPrimer sequence: "+lastseq[:-1]+"\nPrimer length: "+str(len(lastseq)-1)+"\n"+"Right spacer: "+endspacers[i]+end+"\nGC Content: "+str(gccontent2))
        firstTM,firstseq, gccontent1,lastTM, lastseq, gccontent2 = findTM(elements[-1], tmgoal)
        print("\n"+"Left primer for "+names[-1])
        print("Left spacer: "+start+firstspacers[-1]+"\n"+"TM: "+str(firstTM)+
              "\nPrimer sequence: "+firstseq+"\nPrimer length: "+str(len(firstseq))+"\nGC Content: "+str(gccontent1)+
              "\n\nRight primer for "+names[-1] +"\nTM: "+str(lastTM)+
              "\nPrimer sequence: "+lastseq[:-1]+"\nPrimer length: "+str(len(lastseq)-1)+"\n"+"Right spacer: "+"GCAAGG"+"\nGC Content: "+str(gccontent2)) 
    input("Press Enter to Quit")


##==================================================
## add GC%
## add primer len
## label primer pieces
##
##
##====================================================================================
##TM Calculation 
## finds TM of promoter seq, adds Tm of end into string
def findTM(seq, TMgoal):
    try:
        TM = 0
        numA = 0
        numT = 0
        numG = 0
        numC = 0
        i = 0
        seq = list(seq)
        while TM - TMgoal > 1 or TM -TMgoal < -1:
            if seq[i] == "A":
                numA +=1
            elif seq[i] == "T":
                numT +=1
            elif seq[i] == "G":
                numG +=1
            elif seq[i] == "C":
                numC +=1
            TM = 64.9 + 41*(numG+numC-16.4)/(numA+numT+numG+numC)
            i += 1
        seq = ''.join(seq)
        gccontent1 = (numG +numC)/(len(seq[0:i]))
        gccontent1 = round(gccontent1, 4) * 100
        gccontent1 = str(gccontent1)+" %"
        j, TM2, gccontent2 = findsecondTM(seq, TMgoal)
        if i +j > len(seq):
            return("TM not possible", "No sequence possible","No GC %", "TM not possible", "No sequence possible", "No GC%")
        return(round(TM, 4), seq[0:i], gccontent1, round(TM2,4), seq[j:], gccontent2)
    except IndexError:
        seq = ''.join(seq)
        return("TM not possible", "No sequence possible", "", "", "", "")

def findsecondTM(seq, TMgoal):
    TM2 = 0
    numA = 0
    numT = 0
    numG = 0
    numC = 0
    i = -2 ## compensates for the "\n" at the end of elm.
    seq = list(seq)
    while TM2 - TMgoal > 1 or TM2 -TMgoal < -1:
        if seq[i] == "A":
            numA +=1
        elif seq[i] == "T":
            numT +=1
        elif seq[i] == "G":
            numG +=1
        elif seq[i] == "C":
            numC +=1
        TM2 = 64.9 + 41*(numG+numC-16.4)/(numA+numT+numG+numC)
        i -= 1
    gccontent2 = (numG +numC)/(len(seq[i:]))
    gccontent2 = round(gccontent2, 4) * 100
    gccontent2 = str(gccontent2)+" %"
    seq = ''.join(seq)
    return(i, TM2, gccontent2)



createseq()

    
