import tensorflow as tf
import tensorflow.keras.layers as layers

class RefUnet(tf.keras.Model):
    '''
    Residual Refinement Module
    filters : Number of filters for Convolution2D layer.
    '''

    def __init__(self, filters):
        super(RefUnet, self).__init__()
        self.conv0 = layers.Conv2D(filters, 3, padding='same')

        self.conv1 = layers.Conv2D(64, 3, padding='same')
        self.bn1 = layers.BatchNormalization()
        self.relu1 = layers.Activation('relu')

        self.pool1 = layers.MaxPool2D(strides=(2, 2))

        self.conv2 = layers.Conv2D(64, 3, padding='same')
        self.bn2 = layers.BatchNormalization()
        self.relu2 = layers.Activation('relu')

        self.pool2 = layers.MaxPool2D(strides=(2, 2))

        self.conv3 = layers.Conv2D(64, 3, padding='same')
        self.bn3 = layers.BatchNormalization()
        self.relu3 = layers.Activation('relu')

        self.pool3 = layers.MaxPool2D(strides=(2, 2))

        self.conv4 = layers.Conv2D(64, 3, padding='same')
        self.bn4 = layers.BatchNormalization()
        self.relu4 = layers.Activation('relu')

        self.pool4 = layers.MaxPool2D(strides=(2, 2))
        ######
        self.conv5 = layers.Conv2D(64, 3, padding='same')
        self.bn5 = layers.BatchNormalization()
        self.relu5 = layers.Activation('relu')

        ####

        self.convd_4 = layers.Conv2D(64, 3, padding='same')
        self.bnd_4 = layers.BatchNormalization()
        self.relud_4 = layers.Activation('relu')

        self.convd_3 = layers.Conv2D(64, 3, padding='same')
        self.bnd_3 = layers.BatchNormalization()
        self.relud_3 = layers.Activation('relu')

        self.convd_2 = layers.Conv2D(64, 3, padding='same')
        self.bnd_2 = layers.BatchNormalization()
        self.relud_2 = layers.Activation('relu')

        self.convd_1 = layers.Conv2D(64, 3, padding='same')
        self.bnd_1 = layers.BatchNormalization()
        self.relud_1 = layers.Activation('relu')

        self.convd_0 = layers.Conv2D(1, 3, padding='same')
        self.upscore2 = layers.UpSampling2D(2, interpolation='bilinear')

    def call(self, x):
        hx = x
        hx = self.conv0(hx)

        hx1 = self.relu1(self.bn1(self.conv1(hx)))
        hx = self.pool1(hx1)

        hx2 = self.relu2(self.bn2(self.conv2(hx)))
        hx = self.pool2(hx2)

        hx3 = self.relu3(self.bn3(self.conv3(hx)))
        hx = self.pool3(hx3)

        hx4 = self.relu4(self.bn4(self.conv4(hx)))
        hx = self.pool4(hx4)

        hx5 = self.relu5(self.bn5(self.conv5(hx)))

        hx = self.upscore2(hx5)

        d4 = self.relud_4(self.bnd_4(self.convd_4(layers.concatenate([hx, hx4], -1))))
        hx = self.upscore2(d4)

        d3 = self.relud_3(self.bnd_3(self.convd_3(layers.concatenate([hx, hx3], -1))))
        hx = self.upscore2(d3)

        d2 = self.relud_2(self.bnd_2(self.convd_2(layers.concatenate([hx, hx2], -1))))
        hx = self.upscore2(d2)

        d1 = self.relud_1(self.bnd_1(self.convd_1(layers.concatenate([hx, hx1], -1))))

        residual = self.convd_0(d1)

        return x + residual