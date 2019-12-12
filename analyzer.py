import sys, os.path
from aubio import pvoc, source, float_type
from numpy import zeros, log10, vstack

# example file
# https://github.com/aubio/aubio/blob/master/python/demos/demo_spectrogram.py

def get_spectrogram(filename, samplerate = 0):
    win_s = 512                                        # fft window size
    hop_s = win_s // 2                                 # hop size
    fft_s = win_s // 2 + 1                             # spectrum bins

    a = source(filename, samplerate, hop_s)            # source file
    if samplerate == 0: samplerate = a.samplerate
    pv = pvoc(win_s, hop_s)                            # phase vocoder
    specgram = zeros([0, fft_s], dtype=float_type)     # numpy array to store spectrogram

    # analysis
    while True:
        samples, read = a()                              # read file
        specgram = vstack((specgram,pv(samples).norm))   # store new norm vector
        if read < a.hop_size: break

    def get_rounded_ticks( top_pos, step, n_ticks ):
        top_label = top_pos * step
        # get the first label
        ticks_first_label = top_pos * step / n_ticks
        # round to the closest .1
        ticks_first_label = round ( ticks_first_label * 10. ) / 10.
        # compute all labels from the first rounded one
        ticks_labels = [ ticks_first_label * n for n in range(n_ticks) ] + [ top_label ]
        # get the corresponding positions
        ticks_positions = [ ticks_labels[n] / step for n in range(n_ticks) ] + [ top_pos ]
        # convert to string
        ticks_labels = [  "%.1f" % x for x in ticks_labels ]
        # return position, label tuple to use with x/yticks
        return ticks_positions, ticks_labels
    
    print(get_rounded_ticks ( len(specgram), time_step, n_xticks ))
    #x_ticks, x_labels = get_rounded_ticks ( len(specgram), time_step, n_xticks )
    #y_ticks, y_labels = get_rounded_ticks ( len(specgram[0]), (samplerate / 1000. / 2.) / len(specgram[0]), n_yticks )