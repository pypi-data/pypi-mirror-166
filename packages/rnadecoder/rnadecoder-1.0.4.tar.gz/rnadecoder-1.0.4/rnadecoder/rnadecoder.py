class rnadecoder:
  # Constantes
  bases=["A","U","C","G"]
  start = "AUG"
  stops = ["UAA", "UAG", "UGA"]
  codons = {'UUU': 'Fenilalanina', 'UUC': 'Fenilalanina', 'UUA': 'Leucina', 'UUG': 'Leucina', 'UCU': 'Serina', 'UCC': 'Serina', 'UCA': 'Serina', 'UCG': 'Serina', 'UAU': 'Tirosina', 'UAC': 'Tirosina', 'GCA': 'Alanina', 'UGU': 'Cisteina', 'UGC': 'Cisteina', 'GCG': 'Alanina', 'UGG': 'Triptofano', 'CUU': 'Leucina', 'CUC': 'Leucina', 'CUA': 'Leucina', 'CUG': 'Leucina', 'CCU': 'Prolina', 'CCC': 'Prolina', 'CCA': 'Prolina', 'CCG': 'Prolina', 'CAU': 'Histidina', 'CAC': 'Histidina', 'CAA': 'Glutamina', 'CAG': 'Glutamina', 'CGU': 'Arginina', 'CGC': 'Arginina', 'CGA': 'Arginina', 'CGG': 'Arginina', 'AUU': 'Isoleucina', 'AUC': 'Isoleucina', 'AUA': 'Isoleucina', 'AUG': 'Metionina', 'ACU': 'Treonina', 'ACC': 'Treonina', 'ACA': 'Treonina', 'ACG': 'Treonina', 'AAU': 'Asparagina', 'AAC': 'Asparagina', 'AAA': 'Lisina', 'AAG': 'Lisina', 'AGU': 'Serina', 'AGC': 'Serina', 'AGA': 'Arginina', 'AGG': 'Arginina', 'GUU': 'Valina', 'GUC': 'Valina', 'GUA': 'Valina', 'GUG': 'Valina', 'GCU': 'Alanina', 'GCC': 'Alanina', 'GAU': 'Ácido Aspártico', 'GAC': 'Ácido Aspártico', 'GAA': 'Ácido Glutâmico', 'GAG': 'Ácido Glutâmico', 'GGU': 'Glicina', 'GGC': 'Glicina', 'GGA': 'Glicina', 'GGG': 'Glicina'}

  codigo = 'COD: AMINOÁCIDO\nUUU: Fenilalanina\nUUC: Fenilalanina\nUUA: Leucina\nUUG: Leucina\nUCU: Serina\nUCC: Serina\nUCA: Serina\nUCG: Serina\nUAU: Tirosina\nUAC: Tirosina\nUAA: STOP\nUAG: STOP\nGCA: Alanina\nUGU: Cisteina\nUGC: Cisteina\nUGA: STOP\nGCG: Alanina\nUGG: Triptofano\nCUU: Leucina\nCUC: Leucina\nCUA: Leucina\nCUG: Leucina\nCCU: Prolina\nCCC: Prolina\nCCA: Prolina\nCCG: Prolina\nCAU: Histidina\nCAC: Histidina\nCAA: Glutamina\nCAG: Glutamina\nCGU: Arginina\nCGC: Arginina\nCGA: Arginina\nCGG: Arginina\nAUU: Isoleucina\nAUC: Isoleucina\nAUA: Isoleucina\nAUG: Metionina(START)\nACU: Treonina\nACC: Treonina\nACA: Treonina\nACG: Treonina\nAAU: Asparagina\nAAC: Asparagina\nAAA: Lisina\nAAG: Lisina\nAGU: Serina\nAGC: Serina\nAGA: Arginina\nAGG: Arginina\nGUU: Valina\nGUC: Valina\nGUA: Valina\nGUG: Valina\nGCU: Alanina\nGCC: Alanina\nGAU: Ácido Aspártico\nGAC: Ácido Aspártico\nGAA: Ácido Glutâmico\nGAG: Ácido Glutâmico\nGGU: Glicina\nGGC: Glicina\nGGA: Glicina\nGGG: Glicina'

  def codon(cdn):
    return rnadecoder.codons[cdn.upper()]

  def aminoacido(aa):
    for key, value in rnadecoder.codons.items():
      if value.upper() == aa.upper():
        print(key, value)
    
  def info():
    print("============================================")
    print("RNA DECODER")
    print("Coder: Forti, R")
    print("Date: 07.09.2022")
    print("\nDados Básicos:")
    print("Total de Codons Disponíveis: 64")
    print(f"Start Codon(Inicio):",rnadecoder.start)
    print(f"Stop Codons(Término):",rnadecoder.stops)
    print(f"Total de codons codificantes:",len(rnadecoder.codons.keys()))
    print(f"Total de aminoácidos disponíveis:",len(set(rnadecoder.codons.values())))
    print("============================================")
    print("Como usar:\nrnadecoder.traducao(RNAm,\"<tipo de retorno>\")\n\nRNAm -> RNA mensageiro\n\nTipos de retorno:\nG: Imprime na tela um resumo geral da tradução\nC: Retorna total de codons\nT: Retorna total de codons traduzidos\nP: Retorna a sequência de Aminoácidos que forma a proteína.\n\nOutros Comandos:\nrnadecoder.info() -> Imprime essas informações\nrnadecoder.bases -> Retorna as Bases Nitrogenadas Válidas\nrnadecoder.codon(\"<codon>\") -> Retorna o Aminoácido Codificado pelo codon informado\nrnadecoder.aminoacido(\"<Aminoácido>\") -> Imprime os códons referentes ao Aminoácido informado\nprint(rnadecoder.codigo) -> Imprime na tela a lista do código genético")
      
  def traducao(RNAm,t):
    if any(x not in rnadecoder.bases for x in RNAm.upper()):
      print("ATENÇÃO!!!\nVocê informou Bases Nitrogenadas INVÁLIDAS!\nVerifique a sequência informada.")
    else:
      if (len(RNAm) % 3) == 0:
        fator = 3
        num_codons = round(len(RNAm)/fator,0)
        codons_traduzidos = ""
        i = 0
        proteina = ""
        traduzindo = "NAO"
        cdns = [RNAm[i:i+fator].upper() for i in range(0, len(RNAm), fator)]
        for i in cdns:
          if i in rnadecoder.stops:
            break
          else:
            if i == rnadecoder.start:
              traduzindo = "SIM"
            if traduzindo == "SIM":
              codons_traduzidos += i
              proteina += rnadecoder.codons[i] + " - " 
        # print(f"RNAm informado:\n"+RNAm)
        if t.upper() == "G":
          print(f"Total de Codons:",int(num_codons))
          print(f"Codons traduzidos:",int(len(codons_traduzidos) / fator))
          print("Proteína Gerada:")
          print(proteina[:-3])
          return ""
        elif t.upper() == "C":
          return int(num_codons)
        elif t.upper() == "T":
          return int(len(codons_traduzidos) / fator)
        elif t.upper() == "P":
          return proteina[:-3]
        else:
          print("Parâmetro faltando!!!\ncodigo.traducao(RNA,\"<tipo de retorno>\")\nTipos:\nG: Imprime na tela um resumo geral da tradução\nC: Retorna total de codons\nT: Retorna total de codons traduzidos\nP: Retorna a sequência de Aminoácidos que forma a proteína.\n")
      else:
        print("Verifique a quantidade de codons informada,\npois a mesma não corresponde ao número\ncorreto de codons!!!")
