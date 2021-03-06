#!/usr/bin/env python3


# Another reference:
# https://www.tensorflow.org/get_started/mnist/beginners

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


# If minst data does not exists, it will be downloaded automatically
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)


def add_layer(inputs, in_size, out_size, activation_function=None):
    # Weights = tf.Variable(tf.random_normal([in_size, out_size]))
    Weights = tf.Variable(tf.zeros([in_size, out_size]))
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    Wx_plus_b = tf.matmul(inputs, Weights) + biases
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)

    return outputs


def compute_accuracy(sess, prediction, v_xs, v_ys):
    y_pre = sess.run(prediction, feed_dict={xs: v_xs})
    correct_prediction = tf.equal(tf.argmax(y_pre, 1), tf.argmax(v_ys, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    result = sess.run(accuracy, feed_dict={xs: v_xs, ys: v_ys})
    return result


IN_SIZE = 28 * 28
OUT_SIZE = 10
xs = tf.placeholder(tf.float32, (None, IN_SIZE))
ys = tf.placeholder(tf.float32, (None, OUT_SIZE))

prediction = add_layer(xs, IN_SIZE, OUT_SIZE, activation_function=tf.nn.softmax)

# loss
# Call this "naive cross_entropy"
# cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction),
#                                                reduction_indices=[1]))
# FIXME: It looks convergence speed is much slower with softmax_cross_entropy_with_logits
# than the above manually write corssentropy
cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=ys, logits=prediction))

train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for i in range(1000):
        batch_xs, batch_ys = mnist.train.next_batch(100)
        sess.run(train_step, feed_dict={xs: batch_xs, ys: batch_ys})
        if i % 50 == 0:
            print(compute_accuracy(
                sess, prediction,
                mnist.test.images, mnist.test.labels))


# FIXME: I HAVE NO IDEA WHY ???????
# It is very interesting that:
# 1. with weights initialized by random_normal:
# 1.1 naive cross_entropy convergent fast.
# 1.2 softmax_cross_entropy_with_logits convergent very slow.
#
# 2. with weights initialized by zeros:
# 1.1 naive cross_entropy convergent a little faster than softmax_cross_entropy_with_logits
# 1.2 softmax_cross_entropy_with_logits fast
