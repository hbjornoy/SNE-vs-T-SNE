import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
Axes3D
from ipywidgets import *
import pickle
from matplotlib import offsetbox

np.random.seed(123)

def plot_inter(color,var,Z,i,variable,transformation,error=None,times=None,difference=None,error_type=None):
    """
  
    Parameters
    -------------
    color: the colors of Z
    var: a list of the variable that is changing
    Z: A list of t-SNE transformations, with different perplexities s.t. Z[i] has perplexity per[i]. 
    i: the index of the transformation we want to plot
    variable: 'per', 'threshold', 'learning_rate'

    Output
    -------------
 
    """
    if variable=='per':
        print('The perplexity is', var[i])
    if variable=='learning_rate':
        print('The learning rate is', var[i])
    if variable=='threshold':
        print('The threshold is', var[i])
    if variable=='early_exaggeration': 
        print('The early exaggeration is', var[i])
    if variable=='n_neighbors': 
        print('The n_neighbors is', var[i])   
    if variable=='reg': 
        print('The regularization term is', var[i]) 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(transformation)
    ax.scatter(Z[i][:, 0], Z[i][:, 1], c=color, cmap=plt.cm.Spectral)
    if error is not None:
        plot_error_dist_and_time(var, error,times,difference,variable,error_type=error_type, i=i)
    plt.show()


def plot_inter_grid(colors,var1,var2, Z,j, i,data_augmentation,variable,transformation,error=None,times=None,difference=None,error_type=None):
    """
    Function 
    Parameters
    -------------

    colors: A list of the colors of each dataset 
    var1: a list of the first variable that is changing (eg noise, holes...))
    var2: a list of the second variable that is changing (eg reg, number of neighbours, perplexity)
    Z: A list of a list of transformed data. Z[var1[0]][var2[0]] gives the transformation with for example noise 0 and regularisation 0
    j: the index of the first variable that we want to plot
    i: the index of the second variable that we want to plot
    data_augmentation: Description of the difference in dataset, eg 'noise', 'holes'.. 
    variable: Name of the hyperparameter we are changing (var2),'per', 'threshold', 'learning_rate'
    transformation: 'lle' or 't-sne'
    error: a matrix containing  kl-divergence or reconstuction error for each value of var1 and var2
    times: a matrix containing  computational time for each value of var1 and var2
    difference:a matrix containing  changes in 2d difference for each value of var1 and var2
    error_type: 'kl divergence' or 'reconstruction error' 
    
    Output
    -------------
    A plot showing the transformation at index i, j and a plot of changes in error, time and changes in 2d difference.  
    """
    
    if data_augmentation=='noise':
        print('The noise is ', var1[j])
    elif data_augmentation=='distribution':
        distributions=['uniform','normal','mixed_normal','beta']
        print('The distribution is ', distributions[j])
    elif data_augmentation=='datapoints':
        print('The number of datapoints is ', var1[j])
    elif data_augmentation=='holes':
        str_holes=['1: 1 hole, size 2', '2: 1 hole, size 5','3: 2 holes, size 2', '4: 2 holes, size 5','5: 3 holes, size 2', '6: 3 holes, size 5'] 
        print(str_holes[j])
    if variable=='per':
        print('The perpelxity is', var2[i])
    elif variable=='learning_rate':
        print('The learning rate is', var2[i])
    elif variable=='threshold':
        print('The threshold is', var2[i])
    elif variable=='early_exaggeration': 
        print('The early exaggeration is', var2[i])
    elif variable=='n_neighbors': 
        print('The n_neighbors is', var2[i])   
    elif variable=='reg': 
        print('The regularization term is', var2[i]) 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(transformation)
    ax.scatter(Z[j][i][:, 0], Z[j][i][:, 1], c=colors[j], cmap=plt.cm.Spectral)
    if error is not None:
        plot_error_dist_and_time(var1, error[:,i],times[:,i],difference[:,i],data_augmentation,error_type=error_type, i=j)
    plt.show()


def plot_error_dist_and_time(var, error,times,difference,variable='variable', filename=False, error_type=False, i=False):
    """
    Parameters
    -------------
    var: the hyper parameter you are interested in, eg perplexity, number of neighbours
    error: a vector containing the error (kl divergence or reconstruction error) for each value of var
    times: a vector containing the time taken to compute the transformations for each value of var
    difference: a vector containing the difference in 2d distances for each value of var
    variable: the name of the variable var, eg 'perplexity'
    filename: if you want to save the figure, wirte a filename here. 
    error_type: y label when plotting error, 'kl divergence' og 'reconstructon error'
    i: The index of var on whihc you want a vertical red line. Default false (no red line)
    
     Output
    -------------
    A figure, with 3x1 plots 
    """
    fig = plt.figure(figsize=(20,5))
    ax = fig.add_subplot(131)
    ax.plot(var,error,'go--')
    ax.axvline(x=var[i],  color='r', linestyle='--')
    if (variable=="threshold" or variable=='reg'):
        plt.xscale('log')
    #ax.set_title("t-SNE, KL divergence")
    if error_type:
        ax.set_ylabel(error_type)
    else:
        ax.set_ylabel('Error')
    ax.set_xlabel('%s' %variable)
    ax = fig.add_subplot(132)
    ax.plot(var,times,'go--')
    ax.axvline(x=var[i],  color='r', linestyle='--')
    if (variable=="threshold" or variable=='reg'):
        plt.xscale('log')
    ax.set_ylabel('Time, s')
    ax.set_xlabel('%s' %variable)
    ax = fig.add_subplot(133)
    ax.plot(var,difference,'go--')
    ax.axvline(x=var[i],  color='r', linestyle='--')
    if (variable=="threshold" or variable=='reg'):
        plt.xscale('log')
    ax.set_ylabel('Difference in 2d distance')
    ax.set_xlabel('%s' %variable)
    #ax.set_title("t-SNE, Computational time")
    plt.show()
    if filename: 
        plt.savefig(filename)
        

def plot_embedding(X_orig, X_trans, y, title=None, fig=None, subplot_pos=111, images=False, im_thres=3e-3):
    """
    Plots the manifold embedding with the some of the original images across the data.
    
    Strongly inspired and based on sklearn docs examples:
    http://scikit-learn.org/stable/auto_examples/manifold/plot_lle_digits.html
    # Authors: Fabian Pedregosa <fabian.pedregosa@inria.fr>
    #          Olivier Grisel <olivier.grisel@ensta.org>
    #          Mathieu Blondel <mathieu@mblondel.org>
    #          Gael Varoquaux
    # License: BSD 3 clause (C) INRIA 2011
    
    Parameters
    -------------
    
    X_orig: original data to be able to print its pictures (nb_samples, pixels)
    X_trans: transformed data (nb_samples, nb_components=2)
    y: labels for inputdata to print numbers as colors
    title: title of plot
    fig: matplotlib figure object
    subplot_pos: (three-digit integer) symbolizes position in subplot. Look at matplotlib documentation for subplots for more.
    images: (boolean) if you want to have images sporadically over your plot
    im_thres: (float) if images enabled, how far abort should they pop up
    
     Output
    -------------
    ax of plot with colored classes and possible pictures
    """
    
    
    SMALL_SIZE = 15
    MEDIUM_SIZE = 25
    BIGGER_SIZE = 30

    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
    

    x_min, x_max = np.min(X_trans, 0), np.max(X_trans, 0)
    # multiplied scalar to the range to get the point away from the plot range
    X_trans = ((X_trans - x_min) / ((x_max - x_min)*1.1))+0.05
    
    if fig is None:
        fig = plt.figure(figsize=(10,10))

    ax = fig.add_subplot(subplot_pos)
    for i in range(X_trans.shape[0]):
        plt.text(X_trans[i, 0], X_trans[i, 1], str(int(y[i])),
                 color=plt.cm.Set1(y[i] / 10.),
                 fontdict={'weight': 'bold', 'size': 9})
    
    # the pictures are too big
    if images:
        # only print thumbnails with matplotlib > 1.0
        shown_images = np.array([[1, 1]])  # just something big
        for i in range(X_trans.shape[0]):
            dist = np.sum((X_trans[i] - shown_images) ** 2, 1)
            if np.min(dist) < im_thres:
                # don't show points that are too close
                continue
            shown_images = np.r_[shown_images, [X_trans[i]]]
            imagebox = offsetbox.AnnotationBbox(
                offsetbox.OffsetImage(X_orig[i].reshape((int(np.sqrt(X_orig.shape[1])),int(np.sqrt(X_orig.shape[1])))), 
                                      cmap=plt.cm.gray_r, zoom=0.6),
            X_trans[i])
            ax.add_artist(imagebox)
    
    #plt.xticks([]), plt.yticks([])
    if title is not None:
        plt.title(title)
    return ax
        


def plot_augmented_swissrolls(Xs, colors, var, variable_name):
    """ Plots 3D swiss roll 
    Parameters
    -------------
    
    Xs: a list of the 3D- swiss rolls
    colors: a list of the corresponding colors
    var: a vector containing the value of the augmented aspect of the swiss roll (eg noise levels, hole IDs)
    variable_name: name of the agumented aspect, eg 'noise', 'holes'
    
     Output
    -------------
    3D plot of each of the datasets in Xs, with correct title
    
    """
    fig = plt.figure(figsize=(15,10))
    
    for i in range(len(Xs)):
        X=Xs[i]
        ax = fig.add_subplot(230+i+1, projection='3d')
        ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=colors[i], cmap=plt.cm.Spectral)
        if variable_name is 'distribution':
            ax.set_title( var[i] +'-distributed points')
        else: 
            ax.set_title(variable_name+': %1.2f' %var[i])
    plt.show()

    
def plot_digits_samples(inputs, row_dim, col_dim):
    """
    This function plots the first samples of pictures in picture format
    
    Parameters
    -------------
    inputs: data from MNIST dataset in the form (nb_samples, pixels)
    row_dim: (int) how many rows of picture you want to print
    col_dim: (int) how many col of picture you want to print
    """
    
    # calculate pixelwidth
    pixel_width = int(np.sqrt(inputs.shape[1]))
    image = np.zeros(((pixel_width+2)*row_dim, (pixel_width+2)*col_dim))
    
    # map the inputs "unstructured" data to the two-dimensional picture
    for i in range(row_dim):
        x = (pixel_width+2)*i + 1

        for j in range (col_dim):
            y = (pixel_width+2)*j + 1
            image[x:x+pixel_width, y:y+pixel_width] = inputs[i*col_dim + j].reshape((pixel_width,pixel_width))

    plt.imshow(image, cmap=plt.cm.binary)
    plt.xticks([])
    plt.yticks([])
    plt.title("Samples from MNIST, handwritten digits")
    plt.savefig("images/MNIST_examples_of_data.pdf")
    plt.show()

