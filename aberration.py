from __future__ import division #Force float division
import math #for math.cos

def NewCoordinate(k, Kmax, beta):
    '''
     Given a index k with range Kmax and a velocity beta, 
    associates each index with a cosTheta, where Theta goes from
    -pi/2 to pi/2, uses aberration of light to find the new angle
    and then finds the equivalent index to the new angle

    Returns the new index rounded to a integer
    '''

    #Theta = pi/2 * (1-2*k/Kmax-1) so that the pixels in the center
    #of the image get theta = 0, and the pixels in the extreme are in
    #theta +- pi/2
    cos = math.cos((1-2*k/(Kmax))*math.pi/2)

    #applies relativistic aberration of light
    cosnew = (cos + beta)/(1+cos*beta)

    #recover the new index
    knew = (1-(2/math.pi)*math.acos(cosnew))*(Kmax)/2

    '''
    Since cos is symetric in -pi/2 to 0 and 0 to pi/2, we find in which
    side of the maximum k was originaly and put knew in the same side
    '''
    if(k>Kmax/2):
        knew = (Kmax)-knew
    
    return int(round(knew))


from PIL import Image

def DoTheAberration(fileName, inExtension, beta):
    '''
    Given a file name, an extension, a velocity beta, applies
    aberration of light to the whole image and saves it in a 
    .png image with name:
    
    filneName + decimal part of beta + .png

    Returns the File Name

    '''
    inName = fileName + inExtension
    outName = fileName+str(beta)[2:]+'.png'
    
    img = Image.open(inName)
    pixelMap = img.load()
    
    imgNew = Image.new(img.mode, img.size)
    pixelNew = imgNew.load()

    Imax = img.size[0]
    Jmax = img.size[1]

    for i in range(Imax):
        for j in range(Jmax):
            inew = NewCoordinate(i,Imax, beta)
            jnew = NewCoordinate(j, Jmax, beta)
            
            pixelNew[inew,jnew] = pixelMap[i,j]
        

    imgNew.save(outName)
    return outName


fileName='bc'
inExtension ='.jpeg'
#betaArray = [0.1, 0.2, 0.3, 0.4 ,0.5, 0.7, 0.9, 0.99, 0.999]
betaArray = [0.0, 0.1, 0.2, 0.3]

for b in betaArray:
    DoTheAberration(fileName, inExtension, b)

#Next Tasks:
#A Function that Given a directory does aberration in all the files
#from that directory, it can do it in a range of beta, simulating acceleration

#bash macro to get frames from a video and store them in a directory

#Try both with a sample video
