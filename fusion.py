import cv2
import numpy as np
import pywt


def channelTransform(ch1, ch2, shape):
    coefficient1 = pywt.dwt2(ch1, 'db5', mode='periodization')  # dwt2(data, wavelet, mode), db5 is Daubechies (wavelet family)
    coefficient2 = pywt.dwt2(ch2, 'db5', mode='periodization')

    cA1, (cH1, cV1, cD1) = coefficient1
    cA2, (cH2, cV2, cD2) = coefficient2

    # Single - level discrete 2-D wavelet transform
    cA = (cA1 + cA2) / 2
    cH = (cH1 + cH2) / 2
    cV = (cV1 + cV2) / 2
    cD = (cD1 + cD2) / 2

    fincoC = cA, (cH, cV, cD)
    outImageC = pywt.idwt2(fincoC, 'db5', mode='periodization')
    outImageC = cv2.resize(outImageC, (shape[0], shape[1]))

    return outImageC


def fusion(img1, img2):
    # FUSION_METHOD = 'mean'  # Can be 'min' || 'max || anything you choose according theory

    # Read the two image
    I1 = cv2.imread(img1)
    I2 = cv2.imread(img2)

    # Resizing image if both are in different shapes
    I2 = cv2.resize(I2, (I1.shape[1], I1.shape[0]))

    # Separating channels
    iR1 = I1.copy()
    iR1[:, :, 1] = iR1[:, :, 2] = 0
    iR2 = I2.copy()
    iR2[:, :, 1] = iR2[:, :, 2] = 0

    iG1 = I1.copy()
    iG1[:, :, 0] = iG1[:, :, 2] = 0
    iG2 = I2.copy()
    iG2[:, :, 0] = iG2[:, :, 2] = 0

    iB1 = I1.copy()
    iB1[:, :, 0] = iB1[:, :, 1] = 0
    iB2 = I2.copy()
    iB2[:, :, 0] = iB2[:, :, 1] = 0

    shape = (I1.shape[1], I1.shape[0])
    # Wavelet transformation on red channel
    outImageR = channelTransform(iR1, iR2, shape)
    outImageG = channelTransform(iG1, iG2, shape)
    outImageB = channelTransform(iB1, iB2, shape)

    outImage = I1.copy()
    outImage[:, :, 0] = outImage[:, :, 1] = outImage[:, :, 2] = 0
    outImage[:, :, 0] = outImageR[:, :, 0]
    outImage[:, :, 1] = outImageG[:, :, 1]
    outImage[:, :, 2] = outImageB[:, :, 2]

    outImage = np.multiply(np.divide(outImage - np.min(outImage), (np.max(outImage) - np.min(outImage))), 255)
    outImage = outImage.astype(np.uint8)

    # x = random.randint(1000, 2000)
    # loc = 'demo/out' + str(x) + '.jpg'
    # cv2.imwrite(loc, outImage)

    return outImage


if __name__ == "__main__":
    # print(pywt.Modes.modes) # ['zero', 'constant', 'symmetric', 'periodic', 'smooth', 'periodization', 'reflect', 'antisymmetric', 'antireflect']
    img = fusion("images/f1.jpg", "images/f2.jpg")
    i1 = cv2.imread("images/f1.jpg")
    i2 = cv2.imread("images/f2.jpg")
    cv2.imshow("PAN image", i1)
    cv2.imshow("multi spectral image", i2)
    cv2.imshow('img', img)
    cv2.waitKey(0)
