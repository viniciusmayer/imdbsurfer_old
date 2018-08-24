import time
from imdbsurfer.SetMovieIndex import SetMovieIndex

if __name__ == '__main__':
    print('SetMovieIndex begin')
    start_time = time.time()
    smi = SetMovieIndex()
    smi.process()
    elapsed_time = time.time() - start_time
    print('SetMovieIndex end: {0}'.format(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))
