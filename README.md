# Dyadic-Tree-Visualizer
# Dyadic Fraction Tree Visualizer 🔥🌲

An interactive binary decision tree visualizer for modeling the **burning rope puzzle**, enabling **precise representation and decomposition of dyadic time fractions** using **compositions of bisectional functions**.

Inspired by the Resonance article ["Measuring Time with Burning Ropes"](https://doi.org/10.1007/s12045-019-0910-5), this project uses **DFS-based traversal** to simulate and visualize fractional time logic in a structured, explorable format.

## Background
- The famous rope-burning puzzle is extended and displayed visually in the form of a binary tree.
- n ropes burn exactly in 1 hour, but the rate of burning is non-uniform and unknown.
- We need to measure k/(2^n) of an hour exactly using these ropes.
- Each rope may be ignited either from one end or both, but never from the middle.
- Link to the puzzle https://www.interviewbit.com/problems/measure-time-by-burning-ropes/
- Decisions must be taken at each step. These decisions help us to determine the order for burning the ropes in a correct fashion

## Features
- 🔍 Enter any dyadic fraction \( \frac{k}{2^n} \)
- 🌳 View the full binary tree of `'p'`/`'q'` decisions
- 🎯 Automatically highlight the target node in the tree
- 🧠 Models time decomposition logic from the rope puzzle

## Interpretation:
- The number sequence at the bottom means the following:
- A bold number denotes a rope lighted from both ends.
- A number in normal font mean a rope lighted only from 1 end.
- | and { are separators. They separate the intervals in which a particular rope number has burnt.
- {...} mean that the desired time should be measured in the interval enclosed by {}.

## Installation
```bash
pip install PyQt5
python main.py
