import tensorflow as tf
import tensorflow.keras.layers as layers
from BASNET.RefUnet import RefUnet
from BASNET.Resnet34Layers import reslayer1,reslayer2,reslayer3,reslayer4
from BASNET.ResidualBlock import basicBlock


class BasNet(tf.keras.Model):
    '''
    BasNet Model
    '''

    def __init__(self):
        super(BasNet, self).__init__()
        # ------------Encoeder------------------

        self.inconv = layers.Conv2D(64, 3, strides=1, padding='same')
        self.inbn = layers.BatchNormalization()
        self.inrelu = layers.Activation('relu')

        # stage 1
        self.encoder1 = reslayer1()  # 64
        # stage 2
        self.encoder2 = reslayer2()  # 128
        # stage 3
        self.encoder3 = reslayer3()  # 256
        # stage 4
        self.encoder4 = reslayer4()  # 512

        # stage 5
        self.pool4 = layers.MaxPool2D(strides=(2, 2))
        self.resb5_1 = basicBlock(512, downsamples=True)
        self.resb5_2 = basicBlock(512)
        self.resb5_3 = basicBlock(512)

        # stage 6
        self.pool5 = layers.MaxPool2D(strides=(2, 2))
        self.resb6_1 = basicBlock(512)
        self.resb6_2 = basicBlock(512)
        self.resb6_3 = basicBlock(512)

        # ----------------Bridge------------------------
        # stage bridge
        self.convbg_1 = layers.Conv2D(512, 3, dilation_rate=2, padding='same')
        self.bnbg_1 = layers.BatchNormalization()
        self.relubg_1 = layers.Activation('relu')
        self.convbg_2 = layers.Conv2D(512, 3, dilation_rate=2, padding='same')
        self.bnbg_2 = layers.BatchNormalization()
        self.relubg_2 = layers.Activation('relu')
        self.convbg_3 = layers.Conv2D(512, 3, dilation_rate=2, padding='same')
        self.bnbg_3 = layers.BatchNormalization()
        self.relubg_3 = layers.Activation('relu')

        # -------------------Decoder----------------------

        # stage 6d
        self.convd6_1 = layers.Conv2D(512, 3, padding='same')
        self.bnd6_1 = layers.BatchNormalization()
        self.relud6_1 = layers.Activation('relu')

        self.convd6_2 = layers.Conv2D(512, 3, dilation_rate=2, padding='same')
        self.bnd6_2 = layers.BatchNormalization()
        self.relud6_2 = layers.Activation('relu')

        self.convd6_3 = layers.Conv2D(512, 3, dilation_rate=2, padding='same')
        self.bnd6_3 = layers.BatchNormalization()
        self.relud6_3 = layers.Activation('relu')

        # stage 5d
        self.convd5_1 = layers.Conv2D(512, 3, padding='same')
        self.bnd5_1 = layers.BatchNormalization()
        self.relud5_1 = layers.Activation('relu')

        self.convd5_2 = layers.Conv2D(512, 3, padding='same')
        self.bnd5_2 = layers.BatchNormalization()
        self.relud5_2 = layers.Activation('relu')

        self.convd5_3 = layers.Conv2D(512, 3, padding='same')
        self.bnd5_3 = layers.BatchNormalization()
        self.relud5_3 = layers.Activation('relu')

        # stage 4d
        self.convd4_1 = layers.Conv2D(512, 3, padding='same')
        self.bnd4_1 = layers.BatchNormalization()
        self.relud4_1 = layers.Activation('relu')

        self.convd4_2 = layers.Conv2D(512, 3, padding='same')
        self.bnd4_2 = layers.BatchNormalization()
        self.relud4_2 = layers.Activation('relu')

        self.convd4_3 = layers.Conv2D(256, 3, padding='same')
        self.bnd4_3 = layers.BatchNormalization()
        self.relud4_3 = layers.Activation('relu')

        # stage 3d
        self.convd3_1 = layers.Conv2D(256, 3, padding='same')
        self.bnd3_1 = layers.BatchNormalization()
        self.relud3_1 = layers.Activation('relu')

        self.convd3_2 = layers.Conv2D(256, 3, padding='same')
        self.bnd3_2 = layers.BatchNormalization()
        self.relud3_2 = layers.Activation('relu')

        self.convd3_3 = layers.Conv2D(128, 3, padding='same')
        self.bnd3_3 = layers.BatchNormalization()
        self.relud3_3 = layers.Activation('relu')

        # stage 2d
        self.convd2_1 = layers.Conv2D(128, 3, padding='same')
        self.bnd2_1 = layers.BatchNormalization()
        self.relud2_1 = layers.Activation('relu')

        self.convd2_2 = layers.Conv2D(128, 3, padding='same')
        self.bnd2_2 = layers.BatchNormalization()
        self.relud2_2 = layers.Activation('relu')

        self.convd2_3 = layers.Conv2D(64, 3, padding='same')
        self.bnd2_3 = layers.BatchNormalization()
        self.relud2_3 = layers.Activation('relu')

        # stage 1d
        self.convd1_1 = layers.Conv2D(64, 3, padding='same')
        self.bnd1_1 = layers.BatchNormalization()
        self.relud1_1 = layers.Activation('relu')

        self.convd1_2 = layers.Conv2D(64, 3, padding='same')
        self.bnd1_2 = layers.BatchNormalization()
        self.relud1_2 = layers.Activation('relu')

        self.convd1_3 = layers.Conv2D(64, 3, padding='same')
        self.bnd1_3 = layers.BatchNormalization()
        self.relud1_3 = layers.Activation('relu')

        # ----------------------Bilinear upsampling-----------------
        self.upscore6 = layers.UpSampling2D(32, interpolation='bilinear')
        self.upscore5 = layers.UpSampling2D(16, interpolation='bilinear')
        self.upscore4 = layers.UpSampling2D(8, interpolation='bilinear')
        self.upscore3 = layers.UpSampling2D(4, interpolation='bilinear')
        self.upscore2 = layers.UpSampling2D(2, interpolation='bilinear')

        ## -------------Side Output--------------
        self.outconvb = layers.Conv2D(1, 3, padding='same')
        self.outconv6 = layers.Conv2D(1, 3, padding='same')
        self.outconv5 = layers.Conv2D(1, 3, padding='same')
        self.outconv4 = layers.Conv2D(1, 3, padding='same')
        self.outconv3 = layers.Conv2D(1, 3, padding='same')
        self.outconv2 = layers.Conv2D(1, 3, padding='same')
        self.outconv1 = layers.Conv2D(1, 3, padding='same')

        ## -------------Refine Module-------------
        self.refunet = RefUnet(64)

    def call(self, x):
        hx = x
        # -----------------Encoder------------------
        hx = self.inconv(hx)
        hx = self.inbn(hx)
        hx = self.inrelu(hx)
        # ----------------e1---------------
        h1 = self.encoder1(hx)
        # ----------------e2---------------
        h2 = self.encoder2(h1)
        # ----------------e3---------------
        h3 = self.encoder3(h2)
        # ----------------e4---------------
        h4 = self.encoder4(h3)

        hx = self.pool4(h4)

        hx = self.resb5_1(hx)
        hx = self.resb5_2(hx)
        h5 = self.resb5_3(hx)

        hx = self.pool5(h5)

        hx = self.resb6_1(hx)
        hx = self.resb6_2(hx)
        h6 = self.resb6_3(hx)

        # -----------------------Bridge-------------------

        hx = self.relubg_1(self.bnbg_1(self.convbg_1(h6)))
        hx = self.relubg_2(self.bnbg_2(self.convbg_2(hx)))
        hbg = self.relubg_3(self.bnbg_3(self.convbg_3(hx)))

        # -----------------------Decoder--------------------

        hx = self.relud6_1(self.bnd6_1(self.convd6_1(layers.concatenate([hbg, h6], -1))))
        hx = self.relud6_2(self.bnd6_2(self.convd6_2(hx)))
        hd6 = self.relud6_3(self.bnd6_3(self.convd6_3(hx)))

        hx = self.upscore2(hd6)

        hx = self.relud5_1(self.bnd5_1(self.convd5_1(layers.concatenate([hx, h5], -1))))
        hx = self.relud5_2(self.bnd5_2(self.convd5_2(hx)))
        hd5 = self.relud5_3(self.bnd5_3(self.convd5_3(hx)))

        hx = self.upscore2(hd5)

        hx = self.relud4_1(self.bnd4_1(self.convd4_1(layers.concatenate([hx, h4], -1))))
        hx = self.relud4_2(self.bnd4_2(self.convd4_2(hx)))
        hd4 = self.relud4_3(self.bnd4_3(self.convd4_3(hx)))

        hx = self.upscore2(hd4)

        hx = self.relud3_1(self.bnd3_1(self.convd3_1(layers.concatenate([hx, h3], -1))))
        hx = self.relud3_2(self.bnd3_2(self.convd3_2(hx)))
        hd3 = self.relud3_3(self.bnd3_3(self.convd3_3(hx)))

        hx = self.upscore2(hd3)

        hx = self.relud2_1(self.bnd2_1(self.convd2_1(layers.concatenate([hx, h2], -1))))
        hx = self.relud2_2(self.bnd2_2(self.convd2_2(hx)))
        hd2 = self.relud2_3(self.bnd2_3(self.convd2_3(hx)))

        hx = self.upscore2(hd2)

        hx = self.relud1_1(self.bnd1_1(self.convd1_1(layers.concatenate([hx, h1], -1))))
        hx = self.relud1_2(self.bnd1_2(self.convd1_2(hx)))
        hd1 = self.relud1_3(self.bnd1_3(self.convd1_3(hx)))

        # ------------------------------side output------------------------

        db = self.outconvb(hbg)
        db = self.upscore6(db)

        d6 = self.outconv6(hd6)
        d6 = self.upscore6(d6)

        d5 = self.outconv5(hd5)
        d5 = self.upscore5(d5)

        d4 = self.outconv4(hd4)
        d4 = self.upscore4(d4)

        d3 = self.outconv3(hd3)
        d3 = self.upscore3(d3)

        d2 = self.outconv2(hd2)
        d2 = self.upscore2(d2)

        d1 = self.outconv1(hd1)

        # -----------------------------Refine Module--------------
        dout = self.refunet(d1)

        return tf.sigmoid(dout)