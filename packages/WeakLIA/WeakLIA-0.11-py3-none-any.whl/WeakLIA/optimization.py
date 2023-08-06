#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  11 12:04:23 2021

@author: daniel
"""
import sys 
import random
import numpy as np
from warnings import filterwarnings
filterwarnings("ignore", category=FutureWarning)

import optuna
from optuna.integration import TFKerasPruningCallback
from tensorflow.keras.backend import clear_session 
from tensorflow.keras.callbacks import EarlyStopping
optuna.logging.set_verbosity(optuna.logging.WARNING)
from WeakLIA.data_augmentation import augmentation, resize
from WeakLIA import data_processing, cnn_model


class objective_cnn(object):
    """
    Optimization objective function for pyBIA's convolutional neural network. 
    This is passed through the hyper_opt() function when optimizing with
    Optuna. The Optuna software for hyperparameter optimization was published in 
    2019 by Akiba et al. Paper: https://arxiv.org/abs/1907.10902

    Unlike the objective functions for the ensemble algorithms, this takes as input
    the two classes directly, instead of the traditional data (data_x) and accompanying
    label array (data_y). This is because the cnn_model.pyBIA_model() function takes as input the
    two classes, after which it automatically assigns the 0 and 1 label, respectively. 

    Note:
        If opt_aug is enabled, then the class1 sample will be the data that will augmented.
        It is best to keep both class sizes the same after augmentation, therefore balance=True
        by default, which will truncate the class2 sample to meet the augmented class1 size.

        For example, if class1 contains only 100 images, opt_aug will identify the ideal number 
        of augmentations to perform. If this ideal quantity is 10, then each of the 100 class1 images will 
        be augmented 10 times, and thus only the first 1000 images in the class2 sample will be used so
        as to keep the final sample sizes the same. 

        Since the maximum number of augmentations allowed is batch_max per each sample, in practice class2 
        should contain batch_max times the size of class1. During the optimization procedure, if an 
        augmentation batch size of 200 is assesed, then 100*200=20000 augmented images will be created, 
        and therefore during that particular trial 20000 images from class2 will be used, and so forth. 
        If class2 does not contain 20000 samples, then all will be used.

        To use the entire class2 sample regardless of the number augmentations performed, set balance_val=False.

    Args:
        class1
        class2
        img_num_channels
    """

    def __init__(self, class1, class2, img_num_channels=1, normalize=True, min_pixel=0,
        max_pixel=100, val_class1=None, val_class2=None, train_epochs=25, patience=20, limit_search=True, 
        opt_aug=False, batch_min=10, batch_max=250, image_size_min=50, image_size_max=100, 
        balance_val=True, opt_min_pix=None, opt_max_pix=None, metric='loss'):

        self.class1 = class1
        self.class2 = class2
        self.img_num_channels = img_num_channels
        self.normalize = normalize 
        self.min_pixel = min_pixel
        self.max_pixel = max_pixel
        self.val_class1 = val_class1
        self.val_class2 = val_class2
        self.train_epochs = train_epochs
        self.patience = patience 
        self.limit_search = limit_search
        self.opt_aug = opt_aug
        self.batch_min = batch_min 
        self.batch_max = batch_max 
        self.image_size_min = image_size_min
        self.image_size_max = image_size_max
        self.balance_val = balance_val
        self.opt_min_pix = opt_min_pix
        self.opt_max_pix = opt_max_pix
        self.metric = metric 

        if self.metric == 'val_loss' or self.metric == 'val_accuracy':
            if self.val_class1 is None and self.val_class2 is None:
                raise ValueError('No validation data input, change the metric to either "loss" or "accuracy".')

        if self.opt_min_pix is not None:
            if self.opt_max_pix is None:
                raise ValueError('To optimize min/max normalization pixel value, both opt_min_pix and opt_max_pix must be input')

        if self.opt_max_pix is not None:
            if self.opt_min_pix is None:
                raise ValueError('To optimize min/max normalization pixel value, both opt_min_pix and opt_max_pix must be input')

    def __call__(self, trial):

        if self.opt_aug:
            if self.img_num_channels == 1:
                channel1, channel2, channel3 = self.class1, None, None 
            elif self.img_num_channels == 2:
                channel1, channel2, channel3 = self.class1[:,:,:,0], self.class1[:,:,:,1], None 
            elif self.img_num_channels == 3:
                channel1, channel2, channel3 = self.class1[:,:,:,0], self.class1[:,:,:,1], self.class1[:,:,:,2]
            else:
                raise ValueError('Only three filters are supported!')

        clear_session()

        if self.metric == 'loss' or self.metric == 'val_loss':
            mode = 'min'
        elif self.metric == 'accuracy' or self.metric == 'val_accuracy':
            mode = 'max'

        if self.opt_aug:
            batch = trial.suggest_int('batch', self.batch_min, self.batch_max, step=5)
            image_size = trial.suggest_int('image_size', self.image_size_min, self.image_size_max, step=1)
            shift = trial.suggest_int('shift', 0, 25)
            horizontal = trial.suggest_categorical('horizontal', [True, False])
            vertical = trial.suggest_categorical('vertical', [True, False])
            rotation = trial.suggest_int('rotation', 0, 360, step=360)

            augmented_images = augmentation(channel1=channel1, channel2=channel2, channel3=channel3, batch=batch, 
                width_shift=shift, height_shift=shift, horizontal=horizontal, vertical=vertical, rotation=rotation, 
                image_size=image_size)

            if self.img_num_channels > 1:
                class_1=[]
                if self.img_num_channels == 2:
                    for i in range(len(augmented_images[0])):
                        class_1.append(data_processing.concat_channels(augmented_images[0][i], augmented_images[1][i]))
                else:
                    for i in range(len(augmented_images[0])):
                        class_1.append(data_processing.concat_channels(augmented_images[0][i], augmented_images[1][i], augmented_images[2][i]))
                class_1 = np.array(class_1)
            else:
                class_1 = augmented_images

            if self.balance_val:
                class_2 = self.class2[:len(class_1)]   
            else:
                class_2 = self.class2   

            if self.img_num_channels == 1:
                class_2 = resize(class_2, size=image_size)
            else:
                channel1 = resize(class_2[:,:,:,0], size=image_size)
                channel2 = resize(class_2[:,:,:,1], size=image_size)
                if self.img_num_channels == 2:
                    class_2 = data_processing.concat_channels(channel1, channel2)
                else:
                    channel3 = resize(class_2[:,:,:,2], size=image_size)
                    class_2 = data_processing.concat_channels(channel1, channel2, channel3)

            print("class_2 shape "+str(class_2.shape))
            print("class_1 shape "+str(class_1.shape))

            #Need to also crop the validation images
            if self.val_class1 is not None:
                if self.img_num_channels == 1:
                    val_class_1 = resize(self.val_class1, size=image_size)
                else:
                    val_channel1 = resize(self.val_class1[:,:,:,0], size=image_size)
                    val_channel2 = resize(self.val_class1[:,:,:,1], size=image_size)
                    if self.img_num_channels == 2:
                        val_class_1 = data_processing.concat_channels(val_channel1, val_channel2)
                    else:
                        val_channel3 = resize(self.val_class1[:,:,:,2], size=image_size)
                        val_class_1 = data_processing.concat_channels(val_channel1, val_channel2, val_channel3)
            else:
                val_class_1 = None 

            if self.val_class2 is not None:
                if self.img_num_channels == 1:
                    val_class_2 = resize(self.val_class2, size=image_size)
                elif self.img_num_channels > 1:
                    val_channel1 = resize(self.val_class2[:,:,:,0], size=image_size)
                    val_channel2 = resize(self.val_class2[:,:,:,1], size=image_size)
                    if self.img_num_channels == 2:
                        val_class_2 = data_processing.concat_channels(val_channel1, val_channel2)
                    else:
                        val_channel3 = resize(self.val_class2[:,:,:,2], size=image_size)
                        val_class_2 = data_processing.concat_channels(val_channel1, val_channel2, val_channel3)
            else:
                val_class_2 = None 

            print("class_val_2 shape "+str(val_class_2.shape))
            print("class_val_1 shape "+str(val_class_1.shape))

        else:
            class_1, class_2 = self.class1, self.class2
            val_class_1, val_class_2 = self.val_class1, self.val_class2

        if self.opt_min_pix is not None:
            min_pix = trial.suggest_int('min_pixel', self.opt_min_pix, self.opt_max_pix, step=1)
            max_pix = trial.suggest_int('max_pixel', self.opt_min_pix, self.opt_max_pix, step=1)
        else:
            min_pix, max_pix = self.min_pixel, self.max_pixel

        batch_size = trial.suggest_int('batch_size', 16, 64)
        lr = trial.suggest_float('lr', 1e-6, 0.1, step=0.05)
        decay = trial.suggest_float('decay', 0, 0.1, step=0.001)
        maxpool_size_1 = trial.suggest_int('maxpool_size_1', 2, 25)
        maxpool_stride_1 = trial.suggest_int('maxpool_stride_1', 1, 15)
        maxpool_size_2 = trial.suggest_int('maxpool_size_2', 2, 25)
        maxpool_stride_2 = trial.suggest_int('maxpool_stride_2', 1, 15)
        maxpool_size_3 = trial.suggest_int('maxpool_size_3', 2, 25)
        maxpool_stride_3 = trial.suggest_int('maxpool_stride_3', 1, 15)
        filter_1 = trial.suggest_int('filter_1', 12, 408, step=12)
        filter_size_1 = trial.suggest_int('filter_size_1', 1, 11, step=2)
        strides_1 = trial.suggest_int('strides_1', 1, 15)
        filter_2 = trial.suggest_int('filter_2', 12, 408, step=12)
        filter_size_2 = trial.suggest_int('filter_size_2', 1, 11, step=2)
        strides_2 = trial.suggest_int('strides_2', 1, 15)
        filter_3 = trial.suggest_int('filter_3', 12, 408, step=12)
        filter_size_3 = trial.suggest_int('filter_size_3', 1, 11, step=2)
        strides_3 = trial.suggest_int('strides_3', 1, 15)
        filter_4 = trial.suggest_int('filter_4', 12, 408, step=12)
        filter_size_4 = trial.suggest_int('filter_size_4', 1, 11, step=2)
        strides_4 = trial.suggest_int('strides_4', 1, 15)
        filter_5 = trial.suggest_int('filter_5', 12, 408, step=12)
        filter_size_5 = trial.suggest_int('filter_size_5', 1, 11, step=2)
        strides_5 = trial.suggest_int('strides_5', 1, 15)

        if self.limit_search is False:
            momentum = trial.suggest_float('momentum', 0.0, 1.0, step=0.05)
            nesterov = trial.suggest_categorical('nesterov', [True, False])
            dropout = trial.suggest_float('dropout', 0, 0.5, step=0.05)
            activation_conv = trial.suggest_categorical('activation_conv', ['relu',  'sigmoid', 'tanh'])
            activation_dense = trial.suggest_categorical('activation_dense', ['relu', 'sigmoid', 'tanh'])

        if self.patience != 0:
            callbacks = [EarlyStopping(monitor=self.metric, mode=mode, patience=self.patience), TFKerasPruningCallback(trial, monitor=self.metric),]
        else:
            callbacks = None

        if self.limit_search is False:
            try:
                model, history = cnn_model.pyBIA_model(class_1, class_2, img_num_channels=self.img_num_channels, normalize=self.normalize, 
                    min_pixel=min_pix, max_pixel=max_pix, val_class1=val_class_1, val_class2=val_class_2, epochs=self.train_epochs, 
                    batch_size=batch_size, lr=lr, momentum=momentum, decay=decay, nesterov=nesterov, activation_conv=activation_conv, 
                    activation_dense=activation_dense, dropout=dropout, maxpool_size_1=maxpool_size_1, maxpool_stride_1=maxpool_stride_1, 
                    maxpool_size_2=maxpool_size_2, maxpool_stride_2=maxpool_stride_2, maxpool_size_3=maxpool_size_3, maxpool_stride_3=maxpool_stride_3, 
                    filter_1=filter_1, filter_size_1=filter_size_1, strides_1=strides_1, filter_2=filter_2, filter_size_2=filter_size_2, strides_2=strides_2,
                    filter_3=filter_3, filter_size_3=filter_size_3, strides_3=strides_3, filter_4=filter_4, filter_size_4=filter_size_4, strides_4=strides_4,
                    filter_5=filter_5, filter_size_5=filter_size_5, strides_5=strides_5, early_stop_callback=callbacks, checkpoint=False)
            except: 
                print("Invalid hyperparameter combination, skipping trial.")
                return 0.0
        else:
            try:
                model, history = cnn_model.pyBIA_model(class_1, class_2, img_num_channels=self.img_num_channels, normalize=self.normalize, 
                    min_pixel=min_pix, max_pixel=max_pix, val_class1=val_class_1, val_class2=val_class_2, epochs=self.train_epochs, batch_size=batch_size, 
                    lr=lr, decay=decay,  maxpool_size_1=maxpool_size_1, maxpool_stride_1=maxpool_stride_1, maxpool_size_2=maxpool_size_2, maxpool_stride_2=maxpool_stride_2, 
                    maxpool_size_3=maxpool_size_3, maxpool_stride_3=maxpool_stride_3, filter_1=filter_1, filter_size_1=filter_size_1, strides_1=strides_1, 
                    filter_2=filter_2, filter_size_2=filter_size_2, strides_2=strides_2, filter_3=filter_3, filter_size_3=filter_size_3, strides_3=strides_3, 
                    filter_4=filter_4, filter_size_4=filter_size_4, strides_4=strides_4, filter_5=filter_5, filter_size_5=filter_size_5, strides_5=strides_5, 
                    early_stop_callback=callbacks, checkpoint=False)
            except:
                print("Memory allocation issue, probably due to large batch size, skipping trial.")
                return 0.0

        final_score = history.history[self.metric][-1]

        if self.metric == 'loss' or self.metric == 'val_loss':
            final_score = 1 - final_score

        return final_score


def hyper_opt(class1, class2, n_iter=25, return_study=True, img_num_channels=1, 
    normalize=True, min_pixel=0, max_pixel=100, val_class1=None, val_class2=None, 
    train_epochs=25, patience=5, limit_search=True, opt_aug=True, batch_min=10, batch_max=300, 
    image_size_min=50, image_size_max=100, balance_val=True, opt_min_pix=None, opt_max_pix=None,  
    metric='loss'):
    """
    Optimizes hyperparameters using a k-fold cross validation splitting strategy, unless a CNN
    is being optimized, in which case no cross-validation is performed during trial assesment.
    
    Note:
        If save_study=True, the Optuna study object will be the third output. This
        object can be used for various analysis, including optimization visualization.

        See: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html

        >>> from optuna.visualization.matplotlib import plot_contour
        >>> 
        >>> model, params, study = hyper_opt(class1, class2, save_study=True) 
        >>> plot_contour(study)
        
    Args:
        class1 (ndarray): The samples for the first class, which will
            automatically be assigned the label '0'.
        class2 (ndarray, str): The samples for the first class, which will
            automatically be assigned the label '0'.
        n_iter (int, optional): The maximum number of iterations to perform during 
            the hyperparameter search. Defaults to 25.
        return_study (bool, optional): If True the Optuna study object will be returned. This
            can be used to review the method attributes, such as optimization plots. Defaults to True.
        img_num_channels (int): The number of filters used. Defaults to 1, as pyBIA version 1
            has been trained with only blue broadband data. Only used when clf = 'cnn'.
        normalize (bool, optional): If True the data will be min-max normalized using the 
            input min and max pixels. Defaults to True. Only used when clf = 'cnn'.
        min_pixel (int, optional): The minimum pixel count, defaults to 0. Pixels with counts 
            below this threshold will be set to this limit. Only used when clf = 'cnn'.
        max_pixel (int, optional): The maximum pixel count, defaults to 100. Pixels with counts 
            above this threshold will be set to this limit. Only used when clf = 'cnn'.
        val_X (array, optional): 3D matrix containing the 2D arrays (images)
            to be used for validation.
        val_Y (array, optional): A binary class matrix containing the labels of the
            corresponding validation data. This binary matrix representation can be created
            using tensorflow, see example in the Notes.
        train_epochs (int): Number of epochs used for training. The model accuracy will be
            the validation accuracy at the end of this epoch. 
        patience (int): Number of epochs without improvement before  the optimization trial
            is terminated. 
        metric (str): Assesment metric to use when both pruning and scoring the hyperparameter
            optimization trial.
        limit_search (bool): If True the CNN or XGB optimization search space will be limited,
            for computational and time purposes. Defaults to True.
            
    Returns:
        The first output is the classifier with the optimal hyperparameters.
        Second output is a dictionary containing the optimal hyperparameters.
        If save_study=True, the Optuna study object will be the third output.
    """

    sampler = optuna.samplers.TPESampler()#seed=1909 
    study = optuna.create_study(direction='maximize', sampler=sampler)
    print('Starting hyperparameter optimization, this will take a while...')
    #If binary classification task, can deal with imbalance classes with weights hyperparameter
  
    objective = objective_cnn(class1, class2, img_num_channels=img_num_channels, normalize=normalize, min_pixel=min_pixel, max_pixel=max_pixel, 
        val_class1=val_class1, val_class2=val_class2, train_epochs=train_epochs, patience=patience, metric=metric, limit_search=limit_search, opt_aug=opt_aug, 
        batch_min=batch_min, batch_max=batch_max, image_size_min=image_size_min, image_size_max=image_size_max, balance_val=balance_val,
        opt_min_pix=opt_min_pix, opt_max_pix=opt_min_pix)
    
    if limit_search:
        print('NOTE: To expand hyperparameter search space, set limit_search=False, although this may increase the optimization time significantly.')
    
    study.optimize(objective, n_trials=n_iter, show_progress_bar=True)
    params = study.best_trial.params

    final_score = study.best_value

    print('Hyperparameter optimization complete! Best validation accuracy: {}'.format(np.round(final_score, 4)))
    if return_study:
        return params, study
    return params


