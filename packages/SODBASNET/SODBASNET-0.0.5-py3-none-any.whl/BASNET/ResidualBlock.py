import tensorflow as tf
import tensorflow.keras.layers as layers



class downsample(tf.keras.Model):
    '''
    Used to match the shapes for addition in basicblock.
    filters: Number of filters for Convolution block.
    stride: Strides for convolution block.Default 1
    '''

    def __init__(self, filters, stride=1):
        super(downsample, self).__init__()
        self.conv = layers.Conv2D(filters, 1, strides=stride, padding='same', use_bias=False)
        self.bn = layers.BatchNormalization()
        self.relu = layers.Activation('relu')

    def call(self, x):
        res = x
        x = self.conv(res)
        x = self.bn(x)
        x = self.relu(x)
        return x


class basicBlock(tf.keras.Model):
    '''
    Basic Residual Block
    filters: Number of filters for Convolution block.
    stride: Strides for convolution block.Default 1
    downsamples: Boolean, Whether to apply downsampling to match the input shapes.
    '''

    def __init__(self, filters, stride=1, downsamples=False):
        super(basicBlock, self).__init__()
        self.conv1 = layers.Conv2D(filters, 3, strides=stride, padding='same')
        self.bn1 = layers.BatchNormalization()
        self.relu1 = layers.Activation('relu')
        self.conv2 = layers.Conv2D(filters, 3, strides=1, padding='same')
        self.bn2 = layers.BatchNormalization()
        self.relu2 = layers.Activation('relu')
        self.downsamples = downsamples
        if self.downsamples:
            self.dsmp = downsample(filters, stride)

    def call(self, x_in):
        res = x_in
        x = self.conv1(res)
        x = self.bn1(x)
        x = self.relu1(x)
        x = self.conv2(x)
        x = self.bn2(x)
        if self.downsamples:
            res = self.dsmp(res)
        x = layers.Add()([x, res])
        x = self.relu2(x)

        return x