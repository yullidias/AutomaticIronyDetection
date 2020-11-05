def progress_bar(iteration, total, prefix='Progress:', suffix='Complete',
                 decimals=1, length=50, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
        iteration (Int): current iteration
        total (Int): total iterations
        prefix (Str): prefix string
        suffix (Str): suffix string
        decimals (Int): positive number of decimals in percent complete
        length (Int): character length of bar
        fill (Str): bar fill character
        print_end (Str): end character (e.g. "\r", "\r\n")
    Source:
    https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console

    """
    percent = ("{0:." + str(decimals) + "f}") \
        .format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=print_end)

    if iteration == total:
        print()
