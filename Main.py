import time
from imdbsurfer.SetMovieIndex import SetMovieIndex

if __name__ == '__main__':
    start_time = time.time()
    smi = SetMovieIndex()
    print('SetMovieIndex, begin')
    smi.process()
    elapsed_time = time.time() - start_time
    print('SetMovieIndex, end: {1}'.format(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))
