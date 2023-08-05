import tensorflow as tf

def iou(y_true, y_pred):
    '''
    Calculates Intersection Over Union
    '''
    y_true_flat = tf.keras.backend.flatten(y_true)
    y_pred_flat = tf.keras.backend.flatten(y_pred)
    intersection = tf.keras.backend.sum(y_true_flat * y_pred_flat)
    union = tf.keras.backend.sum(y_true_flat + y_pred_flat - y_true_flat * y_pred_flat)

    return intersection / union

def iou_loss(y_true ,y_pred):
    '''
    Returns Iou Loss
    '''
    return 1 - iou(y_true ,y_pred)

def binary_crossentropy(y_true ,y_pred):
    '''
    Returns Binary CrossEntropy loss
    '''
    bce = tf.keras.losses.BinaryCrossentropy(from_logits=False)
    return bce(y_true ,y_pred)

def ssim_loss(y_true,y_pred):
    '''
    Returns SSIM  loss
    '''
    return 1 - tf.image.ssim(y_true,y_pred,max_val=1)