# MorCAta
Morgan fingerprint Collision ATtAcker (MorCAta)

## What does this do?

This script generates fingerprint-level collisions for morgan fingerprints. The input to the script is an SDF with a certain amount of molecules in there, the output is an SDF with RDKit parsable molecules in there that have an identical fingerprint despite being chemically unrelated and nonsensical. By making use of nonsensical atoms that have a single bit fingerprint, a matching fingerprint can be built up unconnected atom per unconnected atom.

## How to use

`python morcata.py -i molecules.sdf -o output.sdf -l 2048 -r 2`

The command used to generate a fingerprint matched molecule for every molecule in `molecules.sdf`, using a morgan fingerprint of radius `2` (ECFP4-like) and length of `2048`, and save the results in the sdf file `output.sdf`. You'll need to have a somewhat recent RDKit installed for this to work.

## Can I use this for inverting fingerprints to the actual structure?

No, this method is NOT the same as inverting fingerprints to their parent structure, although if you want to do this check out my repo for "ECFPInvert" here: https://github.com/dehaenw/ECFPinvert, alternatively checkout NeuralDecipher and MolForge for deep learning based approaches to the same problem.

There will be a faster and refactored version of ECFPInvert available fairly soon.

## Why would I want to do this?

This is a proof of concept to show a hash collision attack (treating the entire fingerprint as the hash for a molecule) is viable and fast for the frequently used morgan fingerprint. For any practical purpose you will probably not want to do it like this.

## How fast?

Tested on drug bank: 0.486 ms/molecule/cpu core. The code is not optimized for speed an could be significantly sped up, as it is just based on N dictionary lookups per molecule, with N the total amount of on-bits in the fingerprint. 

## Can I also do this with InChI key

No, although collisions are known for InChI keys, collisions are computationally more demanding to generate and rely on more brute force methods like enumerating diastereomers.
