from __future__ import print_function

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

node1 = tf.constant(3.0, tf.float64)
node2 = tf.constant(4.0, tf.float64)

print('TensorFlow version: {0}'.format(tf.__version__))
print(node1, node2)

sess = tf.Session()

print(sess.run([node1,node2]))

node3 = tf.add(node1, node2)
print("node3: ", node3)

print("sess.run(node3): ", sess.run(node3))

a = tf.placeholder(tf.float32)
b = tf.placeholder(tf.float32)
adder = a + b # + provides a shortcut for tf.add(a, b)

print(sess.run(adder, {a:1, b:3}))
print(sess.run(adder, {a:[11,22], b:[22,33]}))

add_and_triple = adder * 3
print(sess.run(add_and_triple, {a:3, b:4.5}))

W = tf.Variable([0.3], tf.float32)
b = tf.Variable([-0.3], tf.float32)
x = tf.placeholder(tf.float32)
line_model = W * x + b
init = tf.global_variables_initializer()
sess.run(init)
print(sess.run(line_model,{x:[1,2,3,4]}))

y = tf.placeholder(tf.float32)
square_delta = tf.square(line_model - y)
loss = tf.reduce_sum(square_delta)
print(sess.run(loss,{x:[1,2,3,4],y:[0,-1,-2,-3]}))

fixW = tf.assign(W,[-1.])
fixb = tf.assign(b,[1.])
sess.run([fixW,fixb])

print(sess.run(line_model,{x:[1,2,3,4]}))
print(sess.run(loss,{x:[1,2,3,4],y:[0,-1,-2,-3]}))

optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(loss)

sess.run(init) #reset values to incorrect defaults
for i in range(5000):
    sess.run(train,{x:[1,2,3,4],y:[0,-1,-2,-3]})

print(sess.run([W,b]))

print(sess.run(loss,{x:[1,2,3,4],y:[0,-1,-2,-3]}))

def test_graph():
    '''
    Graph and Loss visualization using Tensorboard.
    This example is using the MNIST database of handwritten digits
    (http://yann.lecun.com/exdb/mnist/)
    Author: Aymeric Damien
    Project: https://github.com/aymericdamien/TensorFlow-Examples/
    '''


    # Import MNIST data

    mnist = input_data.read_data_sets("/tmp/data/", one_hot = True)

    # Parameters
    learning_rate = 0.01
    training_epochs = 25
    batch_size = 100
    display_step = 1
    logs_path = '/tmp/tensorflow_logs/example'

    # tf Graph Input
    # mnist data image of shape 28*28=784
    x = tf.placeholder(tf.float32, [None, 784], name = 'InputData')
    # 0-9 digits recognition => 10 classes
    y = tf.placeholder(tf.float32, [None, 10], name = 'LabelData')

    # Set model weights
    W = tf.Variable(tf.zeros([784, 10]), name = 'Weights')
    b = tf.Variable(tf.zeros([10]), name = 'Bias')

    # Construct model and encapsulating all ops into scopes, making
    # Tensorboard's Graph visualization more convenient
    with tf.name_scope('Model'):
        # Model
        pred = tf.nn.softmax(tf.matmul(x, W) + b)  # Softmax
    with tf.name_scope('Loss'):
        # Minimize error using cross entropy
        cost = tf.reduce_mean(-tf.reduce_sum(y * tf.log(pred), reduction_indices = 1))
    with tf.name_scope('SGD'):
        # Gradient Descent
        optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)
    with tf.name_scope('Accuracy'):
        # Accuracy
        acc = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
        acc = tf.reduce_mean(tf.cast(acc, tf.float32))

    # Initializing the variables
    init = tf.global_variables_initializer()

    # Create a summary to monitor cost tensor
    tf.summary.scalar("loss", cost)
    # Create a summary to monitor accuracy tensor
    tf.summary.scalar("accuracy", acc)
    # Merge all summaries into a single op
    merged_summary_op = tf.summary.merge_all()

    # Launch the graph
    with tf.Session() as sess:
        sess.run(init)

        # op to write logs to Tensorboard
        summary_writer = tf.summary.FileWriter(logs_path, graph = tf.get_default_graph())

        # Training cycle
        for epoch in range(training_epochs):
            avg_cost = 0.
            total_batch = int(mnist.train.num_examples / batch_size)
            # Loop over all batches
            for i in range(total_batch):
                batch_xs, batch_ys = mnist.train.next_batch(batch_size)
                # Run optimization op (backprop), cost op (to get loss value)
                # and summary nodes
                _, c, summary = sess.run([optimizer, cost, merged_summary_op],
                                         feed_dict = {x: batch_xs, y: batch_ys})
                # Write logs at every iteration
                summary_writer.add_summary(summary, epoch * total_batch + i)
                # Compute average loss
                avg_cost += c / total_batch
            # Display logs per epoch step
            if (epoch + 1) % display_step == 0:
                print("Epoch:", '%04d' % (epoch + 1), "cost=", "{:.9f}".format(avg_cost))

        print("Optimization Finished!")

        # Test model
        # Calculate accuracy
        print("Accuracy:", acc.eval({x: mnist.test.images, y: mnist.test.labels}))

        print("Run the command line:\n" \
              "--> tensorboard --logdir=/tmp/tensorflow_logs " \
              "\nThen open http://0.0.0.0:6006/ into your web browser")

test_graph()






