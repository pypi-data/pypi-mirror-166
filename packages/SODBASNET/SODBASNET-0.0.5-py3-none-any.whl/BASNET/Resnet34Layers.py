import tensorflow as tf
from BASNET.ResidualBlock import basicBlock


class reslayer1(tf.keras.Model):
    '''
    Resnet34 Layer 1
    '''

    def __init__(self):
        super(reslayer1, self).__init__()
        self.convblock1 = basicBlock(64)
        self.convblock2 = basicBlock(64)
        self.convblock3 = basicBlock(64)

    def call(self, x_in):
        x = self.convblock1(x_in)
        x = self.convblock2(x)
        x = self.convblock3(x)
        return x


class reslayer2(tf.keras.Model):
    '''
    Resnet34 Layer 2
    '''

    def __init__(self):
        super(reslayer2, self).__init__()
        self.convblock1 = basicBlock(128, 2, downsamples=True)
        self.convblock2 = basicBlock(128)
        self.convblock3 = basicBlock(128)
        self.convblock4 = basicBlock(128)

    def call(self, x_in):
        x = self.convblock1(x_in)
        x = self.convblock2(x)
        x = self.convblock3(x)
        x = self.convblock4(x)
        return x


class reslayer3(tf.keras.Model):
    '''
    Resnet34 Layer 3
    '''

    def __init__(self):
        super(reslayer3, self).__init__()
        self.convblock1 = basicBlock(256, 2, downsamples=True)
        self.convblock2 = basicBlock(256)
        self.convblock3 = basicBlock(256)
        self.convblock4 = basicBlock(256)
        self.convblock5 = basicBlock(256)
        self.convblock6 = basicBlock(256)

    def call(self, x_in):
        x = self.convblock1(x_in)
        x = self.convblock2(x)
        x = self.convblock3(x)
        x = self.convblock4(x)
        x = self.convblock5(x)
        x = self.convblock6(x)
        return x


class reslayer4(tf.keras.Model):
    '''
    Resnet34 Layer 4
    '''

    def __init__(self):
        super(reslayer4, self).__init__()
        self.convblock1 = basicBlock(512, 2, downsamples=True)
        self.convblock2 = basicBlock(512)
        self.convblock3 = basicBlock(512)

    def call(self, x_in):
        x = self.convblock1(x_in)
        x = self.convblock2(x)
        x = self.convblock3(x)
        return x

