from imdbsurfer.SetMovieIndex import SetMovieIndex

if __name__ == '__main__':
    smi = SetMovieIndex()
    print('SetMovieIndex: {0}'.format('begin'))
    smi.process()
    print('SetMovieIndex: {0}'.format('end'))