import seaborn as sns
import numpy as np
from scipy.stats import mode
import argparse
from Bio import AlignIO
from matplotlib import pyplot as plt
from pathlib import Path


def get_names_coordinates(alignment_bio):

    """
    Function returns sequence names and sequence start
    and end coordinates from an instance of 'Bio.Align.MultipleSeqAlignment' class

    :param alignment_bio: instance of Bio.Align.MultipleSeqAlignment, file with alignment
    :return: names: list of strings, names of sequences
    :return: starts: list of integers, start coordinates
    :return: ends: list of integers, end coordinates
    """
    names, starts, ends = [], [], []

    length = alignment_bio.get_alignment_length()
    for sequence in alignment_bio:
        if '/' in sequence.id:
            coordinates = sequence.id.split('/')[1]
            start = int(coordinates.split('-')[0])
            end = int(coordinates.split('-')[1])
            name = sequence.id.split('/')[0]
        else:
            name = str(sequence.id)
            start = 1
            end = length
        names.append(name)
        starts.append(int(start))
        ends.append(int(end))
    return names, starts, ends


def get_frequencies(alignment):
    """
    Get list of the most frequent characters in each column of matrix.
    Calculates frequencies of most common amino-acids (AAs) in each column of.
    Calculates gap frequencies if a gap is the most character.

    :param alignment: 2D np.array, with AAs
    :return:  frequent_aa: np.ndarray, most freq characters in each column
    :return:  aa_freq: np.ndarray, freq of AAs
    :return:  gap_freq: np.ndarray, freq of gaps
    """

    n_seq = alignment.shape[0]
    frequent_aa, aa_counts_i = mode(alignment)
    aa_counts = np.copy(aa_counts_i)
    aa_counts[frequent_aa == '-'] = 0
    aa_freq = aa_counts / n_seq

    gap_counts = np.copy(aa_counts_i)
    gap_counts[frequent_aa != '-'] = 0
    gap_freq = gap_counts / n_seq

    return frequent_aa, aa_freq, gap_freq


def aminoacid_to_numbers(alignment):
    """
    Converts AAs and '-' (gap) into numbers

    :param  alignment: 2D np.array, with AAs

    :return: alignment_numeric: 2D np.array, with int
             corresponding to each AA
    """

    AA = ['-', 'A', 'C', 'D', 'E',
          'F', 'G', 'H', 'I', 'K',
          'L', 'M', 'N', 'P', 'Q',
          'R', 'S', 'T', 'V', 'W',
          'Y']
    aa_to_number_dic = {AA:n for AA, n in zip(AA, range(0, 22))}
    alignment_numeric = np.copy(alignment)
    for amino_acid, number in aa_to_number_dic.items():
        alignment_numeric[alignment_numeric == amino_acid] = number
    return alignment_numeric.astype(int)


def plot_MSA(alignment, alignment_numeric,
             seq_names, msa_length, n_seqs,
             fig_name, path_to_save):
    """
    Function to plot MSA and save the figure

    :param alignment: 2D np.array, with AAs
    :param alignment_numeric: 2D np.array, with int
                              corresponding to each AA
    :param seq_names: list, seq names
    :param msa_length: int, length of sequences
    :param n_seqs: int, n of seqs in the alignment
    :param fig_name: str, figure name
    :param path_to_save: str, path to save the figure
    """

    if n_seqs < 10:
        height = 10
    else:
        height = int(n_seqs * 0.5 * 1.2)
    if msa_length < 100:
        width = 20
    else:
        width = int(msa_length * 0.7)
    fig, [ax1, ax2] = plt.subplots(2, 1, figsize=(width, height), sharex='col',
                           gridspec_kw={'height_ratios': [0.8, 0.2]})
    aa_names, aa_freq, gap_freq = get_frequencies(alignment)

    sns.heatmap(alignment_numeric, annot=alignment,
                fmt='', ax=ax1, cmap='YlGnBu', yticklabels=seq_names, cbar=False)
    ax2.set_xlabel('Position on the alignment')
    x_ticks = [aa + str(ind+1) for ind, aa in enumerate(aa_names[0])]
    x_tick_pos = [i + 0.7 for i in range(len(x_ticks))]


    ax2.bar(x_tick_pos, aa_freq[0], align='center', label='AA')
    ax2.bar(x_tick_pos, gap_freq[0], align='center', label='Gap')
    ax2.set_xticks(x_tick_pos)
    ax2.set_xticklabels(x_ticks, fontsize=8, rotation=90)
    ax2.legend(loc='upper center')
    plt.subplots_adjust(hspace=0.01)

    plt.show()
    fig.savefig(Path(path_to_save) / f'{fig_name}.png', dpi=300)

def make_MSA_plot(msa_file_name, directory):

    """
    Plots a chooses MSA file and saves fig

    :param msa_file_name: str, MSA file name
    :param directory: str, dir with MSA file (the fig will be saved there too)

    """

    msa_full_path = Path(directory) / f'{msa_file_name}.sto'
    alignment_bio = AlignIO.read(msa_full_path, 'stockholm')
    alignment_aa = np.array(alignment_bio)
    alignment_int = aminoacid_to_numbers(alignment_aa)
    n_seq = alignment_aa.shape[0]
    alignment_length = alignment_aa.shape[1]
    alignment_names = [record.id for record in alignment_bio]
    plot_MSA(alignment_aa, alignment_int,
             alignment_names, alignment_length, n_seq,
             msa_file_name, directory)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--directory', required=True,
                    help='MSA file name, it should be in Stockholm format')
    ap.add_argument('-m_f', '--msa_file', required=True,
                    help='Directory to save the fig (must contain the MSA file)')

    args = ap.parse_args()
    make_MSA_plot(args.msa_file, args.directory)


