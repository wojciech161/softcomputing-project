import sys
from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

def read_array( letter ):
    FILE_SIZE = 40 * 40 # image size is 40x40
    letter_filename = "40x40mono/" + letter + "_array.txt"
    print( "Loading: " + letter_filename )
    letter_file = open( letter_filename, 'r' )
    letter_array = []
    for current_byte in range( FILE_SIZE ):
        BYTES_TO_READ = 1
        letter_file.seek( current_byte )
        letter_array.append( letter_file.read( BYTES_TO_READ ) )
    return letter_array

def test_array_print( letter_array ):
    NUMBER_OF_LINES = 40
    NUMBER_OF_COLUMNS = 40
    print "Picture loaded into memory:"
    for line in range( NUMBER_OF_LINES ):
        for column in range( NUMBER_OF_COLUMNS ):
            sys.stdout.write( letter_array[line * NUMBER_OF_LINES + column] )
        sys.stdout.write( "\n" )

def create_network():
    print "Creating network."
    # Create the network itself
    network = FeedForwardNetwork()
    # Create layers
    NUMBER_OF_INPUT_BYTES = 1600 # because at input we have picture 40x40 size
    NUMBER_OF_HIDDEN_LAYERS = 10 # number of hidden layers
    NUMBER_OF_OUTPUT_BYTES = 3 # because in output we have 3 bytes (for example 010: ".-." in morse code)
    inLayer = LinearLayer( NUMBER_OF_INPUT_BYTES )
    hiddenLayer = SigmoidLayer( NUMBER_OF_HIDDEN_LAYERS )
    outLayer = LinearLayer( NUMBER_OF_OUTPUT_BYTES )
    # Create connections between layers
    # We create FullConnection - each neuron of one layer is connected to each neuron of other layer
    in_to_hidden = FullConnection( inLayer, hiddenLayer )
    hidden_to_out = FullConnection( hiddenLayer, outLayer )
    # Add layers to our network
    network.addInputModule( inLayer )
    network.addModule( hiddenLayer )
    network.addOutputModule( outLayer )
    # Add connections to network
    network.addConnection( in_to_hidden )
    network.addConnection( hidden_to_out )
    # Sort modules to make multilayer perceptron usable
    network.sortModules()
    # prepare array to activate network
    d_letter_array = read_array( "d" )
    # activate network
    network.activate( d_letter_array )
    return network

def prepare_dataset():
    # Prepare output coding. "-" is 1 "." is 0
    d_morse_array = ( 1, 0, 0 ) # D -.. - 100
    g_morse_array = ( 1, 1, 0 ) # G --. - 110
    k_morse_array = ( 1, 0, 1 ) # K -.- - 101
    o_morse_array = ( 1, 1, 1 ) # O --- - 111
    r_morse_array = ( 0, 1, 0 ) # R .-. - 010
    s_morse_array = ( 0, 0, 0 ) # S ... - 000
    u_morse_array = ( 0, 0, 1 ) # U ..- - 001
    w_morse_array = ( 0, 1, 1 ) # W .-- - 011
    # Load learning data
    d_array = read_array( "d" )
    g_array = read_array( "g" )
    k_array = read_array( "k" )
    o_array = read_array( "o" )
    r_array = read_array( "r" )
    s_array = read_array( "s" )
    u_array = read_array( "u" )
    w_array = read_array( "w" )
    # Create dataset
    dataset = SupervisedDataSet( 1600, 3 )
    # add all samples to dataset
    dataset.addSample( d_array, d_morse_array )
    dataset.addSample( g_array, g_morse_array )
    dataset.addSample( k_array, k_morse_array )
    dataset.addSample( o_array, o_morse_array )
    dataset.addSample( r_array, r_morse_array )
    dataset.addSample( s_array, s_morse_array )
    dataset.addSample( u_array, u_morse_array )
    dataset.addSample( w_array, w_morse_array )
    return dataset

def train_network():
    network = create_network()
    dataset = prepare_dataset()
    trainer = BackpropTrainer( network, dataset )
    trainer.trainUntilConvergence()

def main():
    train_network()

if __name__ == "__main__":
    main()
