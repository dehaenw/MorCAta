from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator
from rdkit import DataStructs
import pickle
import argparse


def create_bit_dict(fp_size,radius):
    """
    create a dictionary where the keys are every index of the fingerprint and
    the items a non existent atom (that has a single radius 0 on bit at the 
    index of interest).
    """
    bit_dict={}
    i=0
    for i in range(127):
        if len(bit_dict.keys())==fp_size:
            break
        for k in range(64):
            for a in range(88,119):
                atom = f'[#{a}H{i}-{k}]'
                try:
                    amol = Chem.MolFromSmiles(atom)
                    idx = mfpgen.GetFingerprint(amol).GetOnBits()[0]
                    bit_dict[idx] = atom
                except:
                    print(k,i)
                    pass
    with open(f'{fp_size}_{radius}.pickle', 'wb') as handle:
        pickle.dump(bit_dict, handle, protocol = pickle.HIGHEST_PROTOCOL)
    return bit_dict

def populate_fp(fp,bit_dict):
    hitatoms=[bit_dict[bit] for bit in fp.GetOnBits()]
    return Chem.MolFromSmiles(".".join(hitatoms))

if __name__=="__main__":
    parser = argparse.ArgumentParser(prog='MorCAta',
                    description='Morgan fingerprint Collision Attacker')
    parser.add_argument('-i','--input', required=True)
    parser.add_argument('-o','--output', default="output.sdf", required=False)
    parser.add_argument('-l', '--length', default=2048, type=int, required=False)
    parser.add_argument('-r', '--radius', default=2, type=int, required=False) 
    args = parser.parse_args()
    mfpgen=rdFingerprintGenerator.GetMorganGenerator(fpSize=args.length,radius=args.radius)
    try:
        with open(f'{args.length}_{args.radius}.pickle', 'rb') as handle:
            bit_dict = pickle.load(handle)
    except:
        print("dont have bitdict for fpsize yet, creating")
        bit_dict = create_bit_dict(args.length,args.radius)
    suppl = Chem.SDMolSupplier(args.input)
    with Chem.SDWriter(args.output) as w:
        for mol in suppl:
            if mol:
                fp1 = mfpgen.GetFingerprint(mol)
                m = populate_fp(fp1,bit_dict)
                TS=DataStructs.TanimotoSimilarity(fp1,mfpgen.GetFingerprint(m))
                assert TS==1.0, "error. you are probably doing something wrong. try deleting the pickled dict in the folder"
                w.write(m)

