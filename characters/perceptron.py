import sys
from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection
from pybrain.datasets import ClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.utilities           import percentError

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
    NUMBER_OF_OUTPUT_CLASSES = 8 # because in output we have 8 classes
    inLayer = LinearLayer( NUMBER_OF_INPUT_BYTES )
    hiddenLayer = SigmoidLayer( NUMBER_OF_HIDDEN_LAYERS )
    outLayer = LinearLayer( NUMBER_OF_OUTPUT_CLASSES )
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
    d_morse_array = '100' # ( 1, 0, 0 ) # D -.. - 100
    g_morse_array = '110' # ( 1, 1, 0 ) # G --. - 110
    k_morse_array = '101' # ( 1, 0, 1 ) # K -.- - 101
    o_morse_array = '111' # ( 1, 1, 1 ) # O --- - 111
    r_morse_array = '010' # ( 0, 1, 0 ) # R .-. - 010
    s_morse_array = '000' # ( 0, 0, 0 ) # S ... - 000
    u_morse_array = '001' # ( 0, 0, 1 ) # U ..- - 001
    w_morse_array = '011' # ( 0, 1, 1 ) # W .-- - 011
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
    dataset = ClassificationDataSet( 1600, nb_classes=8, class_labels=[d_morse_array,g_morse_array,k_morse_array,o_morse_array,r_morse_array,s_morse_array,u_morse_array,w_morse_array] )
    # add all samples to dataset
    dataset.addSample( d_array, [0] )
    dataset.addSample( g_array, [1] )
    dataset.addSample( k_array, [2] )
    dataset.addSample( o_array, [3] )
    dataset.addSample( r_array, [4] )
    dataset.addSample( s_array, [5] )
    dataset.addSample( u_array, [6] )
    dataset.addSample( w_array, [7] )
    dataset._convertToOneOfMany( )
    return dataset

def train_network( network, dataset ):
    TRAIN_EPOCHS = 300
    LEARNING_RATE = 0.0165
    LRDECAY = 1.0
    MOMENTUM = 0.6
    VERBOSE = False
    BATCHLEARNING = False
    WEIGHTDECAY = 0.0
    trainer = BackpropTrainer( network, dataset ,learningrate=LEARNING_RATE, lrdecay=LRDECAY, momentum=MOMENTUM, verbose=VERBOSE, batchlearning=BATCHLEARNING, weightdecay=WEIGHTDECAY )
    trainer.trainEpochs( TRAIN_EPOCHS )
    return trainer

def check_clasify_result( result_vector, letter_number ):
    max_value = max( result_vector )
    return result_vector[letter_number] == max_value


def test_letter( network, letter, letter_index ):
    HOW_MUCH_TESTS_TO_DO = 100
    good_classification = 0
    for test in range(HOW_MUCH_TESTS_TO_DO):
        result_vector = network.activate( letter )
        if check_clasify_result( result_vector, letter_index ):
            good_classification = good_classification + 1

    return good_classification

def test_not_malformed_letters( network ):
    RESULT_FILE_NAME = "result.txt"
    APPEND_FLAG = "a"
    result_file = open( RESULT_FILE_NAME, APPEND_FLAG )
    d_index = 0
    g_index = 1
    k_index = 2
    o_index = 3
    r_index = 4
    s_index = 5
    u_index = 6
    w_index = 7

    d_array = read_array( "d" )
    g_array = read_array( "g" )
    k_array = read_array( "k" )
    o_array = read_array( "o" )
    r_array = read_array( "r" )
    s_array = read_array( "s" )
    u_array = read_array( "u" )
    w_array = read_array( "w" )

    result_file.write( "\nTesting NOT MALFORMED letters\n" )
    print "Testing NOT MALFORMED letters"

    d_result = test_letter( network, d_array, d_index )
    g_result = test_letter( network, g_array, g_index )
    k_result = test_letter( network, k_array, k_index )
    o_result = test_letter( network, o_array, o_index )
    r_result = test_letter( network, r_array, r_index )
    s_result = test_letter( network, s_array, s_index )
    u_result = test_letter( network, u_array, u_index )
    w_result = test_letter( network, w_array, w_index )

    print "d Result: " + str(d_result)
    result_file.write( "d Result: " + str( d_result ) + "\n" )
    print "g Result: " + str(g_result)
    result_file.write( "g Result: " + str( g_result ) + "\n" )
    print "k Result: " + str(k_result)
    result_file.write( "k Result: " + str( k_result ) + "\n" )
    print "o Result: " + str(o_result)
    result_file.write( "o Result: " + str( o_result ) + "\n" )
    print "r Result: " + str(r_result)
    result_file.write( "r Result: " + str( r_result ) + "\n" )
    print "s Result: " + str(s_result)
    result_file.write( "s Result: " + str( s_result ) + "\n" )
    print "u Result: " + str(u_result)
    result_file.write( "u Result: " + str( u_result ) + "\n" )
    print "w Result: " + str(w_result)
    result_file.write( "w Result: " + str( w_result ) + "\n" )

    result_file.close()

def main():
    network = create_network()
    dataset = prepare_dataset()
    trainer = train_network( network, dataset )
    test_not_malformed_letters( network )

if __name__ == "__main__":
    main()
