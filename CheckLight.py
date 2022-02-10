import pickle

def Writelight(Stats):
     pickle.dump( Stats, open( "save.p", "wb" ) )

def Readlight():
     light = pickle.load( open( "save.p", "rb" ) )
     return light