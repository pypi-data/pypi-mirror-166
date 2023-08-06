# 2022.9.6
import json, traceback,sys, time,  fileinput, os, en
from collections import Counter

def run(infile):
	''' c4-train.00604-of-01024.docjsonlg.3.4.1.gz -> c4-train.00604-of-01024.postag.gz | 2022.8.22 '''
	outfile = infile.split('.docjson')[0] + f".trp"
	start = time.time()
	si = Counter()
	print ("started:", infile ,  ' -> ',  outfile, flush=True)
	with open(outfile, 'w') as fw: 
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): 
			try:
				arr = json.loads(line.strip()) 
				doc = spacy.from_json(arr) # ('PROPN','NUM','X','SPACE')
				[ si.update({f"{t.dep_} {t.head.pos_} {t.head.lemma_} {t.pos_} {t.lemma_}" : 1 })  for t in doc if t.pos_ not in ('SP','PUNCT','PROPN')]
			except Exception as e:
				print ("ex:", e, sid, line) 
		for s, i in si.items(): 
			fw.write(f"{s}\t{i}\n")
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

if __name__	== '__main__':
	import fire 
	fire.Fire(run)