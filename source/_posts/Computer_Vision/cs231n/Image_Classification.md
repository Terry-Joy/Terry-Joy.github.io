## 图像分类
**目标**：对于输入图像，从已有固定的分类标签集合中选择分类标签分配给输入图像。

+ 图像是三维数组，

**挑战**：
+ **Viewpoint variation**: 同一个物体，不同视角展现。
+ **Scale variation**: 物体大小变化。
+ **Deformation**: 物体形变。
+ **Occlusion**: 目标物体会被遮挡，只有物体小部分可见
+ **Illumination conditions**: 在像素层面上，光照影响较大。
+ **Background clutter**: 物体混入背景中难以辨认。
+ **Intra-class variation**：物体的品种不同，难以具体识别。
  
<br/>

**数据驱动方法**
实现某个具体识别某类图像的方法并不容易，考虑通过输入数据，建立模型，并使得建立的模型不断贴合数据，这种根据数据修改模型，以达到某种效果的方法就叫数据驱动方法。

**模型驱动方法**
让数据贴合模型，比较各个数据，看看哪个数据更贴合模型。

**图像分类过程**：
**输入**：输入包含$N$个图像的集合，每个图像带有$K$种分类标签中的一种，称为训练集。
**学习**：根据训练集学习每种分类标签到底是怎么样的。训练出图像分类器。
**评价**：通过要求分类器预测一组它以前从未见过的新图像的标签来评估分类器的质量。然后将这些图像的真实标签与分类器预测的标签进行比较。

**Nearest Neighbor Classifier**
+ 最近领域算法
对于训练集单纯记录数据和标签，对于评估的图像，根据设定的距离度量函数直接扫一遍训练集找出最相似的即可。

+ 度量函数
  + L1 distance
    $d(I1, I2) = \sum | I_1^p - I_2^p|$
    [![XaEaqO.jpg](https://s1.ax1x.com/2022/06/03/XaEaqO.jpg)](https://imgtu.com/i/XaEaqO)

   下面考虑代码实现
   下面的Xtr是大小为50000 * 32 * 32 * 3的训练集图像，Ytr对应长度为50000的一维数组，存有每个图像的分类标签，0-9。
   <br/>
  
    **图像读入并拉长为一个行向量**。
   ```python
  Xtr, Ytr, Xte = load_CIFAR10('data/cifar10')
  Xtr_rows = Xtr.reshape(Xtr.shape[0], 32 * 32 * 3) 
  Xte_rows = Xte.reshape(Xte.shape[0], 32 * 32 * 3)
   ```

   **训练并评价一个分类器**
   ```python
   nn = NearestNeighbors()
   nn.train(Xtr_rows, Ytr)
   Yte_predict = nn.predict(Xte_rows)

   print 'accuracy : %f' % (np.mean(Yte_predict == Yte))
   ```

   下面给出整个流程包括分类器的代码
   ```python
   import numpy as np

   class NearestNeighbor(object):
      def __init__(self):
         pass

      def train(self, X, y):
        """ X is N x D where each row is an example. Y is 1-dimension of size N """
        # the nearest neighbor classifier simply remembers all the training data
        self.Xtr = X
        self.ytr = y

      def predict(self, X):
        """ X is N x D where each row is an example we wish to predict label for """
        num_test = X.shape[0]
        # make sure that the output type matches the input type
        Ypred = np.zeros(num_test, dtype = self.ytr.dtype)
     
        # loop over all test rows
        for i in range(num_test):
          # find the nearest training image to the i'th test image
          # using the L1 distance (sum of absolute value differences)
          distances = np.sum(np.abs(self.Xtr - X[i,:]), axis = 1)
          min_index = np.argmin(distances) # get the index with smallest distance
          Ypred[i] = self.ytr[min_index] # predict the label of the nearest example

        return Ypred

  from cs231n.data_utils import load_CIFAR10
  Xtr, Ytr, Xte, Yte = load_CIFAR10('data\CIFAR10') # a magic function we provide
  # flatten out all images to be one-dimensional
  Xtr_rows = Xtr.reshape(Xtr.shape[0], 32 * 32 * 3) # Xtr_rows becomes 50000 x 3072
  Xte_rows = Xte.reshape(Xte.shape[0], 32 * 32 * 3) # Xte_rows becomes 10000 x 3072

  nn = NearestNeighbor() # create a Nearest Neighbor classifier class
  nn.train(Xtr_rows, Ytr) # train the classifier on the training images and labels

  Yte_predict = nn.predict(Xte_rows) # predict labels on the test images
  # and now print the classification accuracy, which is the average number
  # of examples that are correctly predicted (i.e. label matches)

  print ('accuracy: %f' % (np.mean(Yte_predict == Yte)))

   ```

  + L2 distance
    $d(I1, I2) = \sqrt{\sum\limits_p (I_1^p - I_2^p)^2}$

    **L2 distance**只需要替换上面的计算代码即可
    ```python
    distances = np.sqrt(np.sum(np.square(self.Xtr - X[i, :]), axis = 1))
    ```

  **差异**
  对于两个图像之间的差异，L2比L1更不能容忍差异。即对于1个差异较大的情况，L2更倾向接受多个中等程度差异。

### K-Nearest Neighbor (KNN) 分类器

+ 算法思路
对于输入图像，根据距离度量选取最相似的$k$个图片的标签，针对测试图片投票，把票数最高的标签作为测试图片的预测。

+ 更高的k值可以让分类的效果更平滑，使得分类器对于异常值更有抵抗力。或者说，用这种方法来检索相邻数据时，会对噪音产生更大的鲁棒性，即噪音产生不确定的评价值对评价结果影响很小。

[![XwMSEt.png](https://s1.ax1x.com/2022/06/05/XwMSEt.png)](https://imgtu.com/i/XwMSEt)
+ 上图是训练集中二维平面的点表示，点的颜色代表不同的类别。不同颜色区域代表分类器决策边界。根据相邻的点来切割空间并进行着色；K=3时，绿色点簇中的黄色噪点不再会导致周围的区域被划分为黄色，由于使用多数投票，中间的整个绿色区域，都将被分类为绿色；k=5时，蓝色和红色区域间的这些决策边界变得更加平滑，针对测试数据$generation$能力更好。


### Hyperparmeter
+ 有关算法本身设置的参数就叫做超参数。例如KNN中的k值与距离函数等。
+ 一般将数据分为三组：训练集（大部分集合），验证集（从训练集选出小部分数据，用于调优），测试集。在训练集用不同超参数训练算法，在验证集评估，选一组在验证集中表现最好的超参数，在测试集上跑，告诉你在从未出现过的数据的表现效果。

**分割训练集和验证集如下**
```python
# assume we have Xtr_rows, Ytr, Xte_rows, Yte as before
# recall Xtr_rows is 50,000 x 3072 matrix
Xval_rows = Xtr_rows[:1000, :] # take first 1000 for validation
Yval = Ytr[:1000]
Xtr_rows = Xtr_rows[1000:, :] # keep last 49,000 for train
Ytr = Ytr[1000:]

# find hyperparameters that work best on the validation set
validation_accuracies = []
for k in [1, 3, 5, 10, 20, 50, 100]:

  # use a particular value of k and evaluation on validation data
  nn = NearestNeighbor()
  nn.train(Xtr_rows, Ytr)
  # here we assume a modified NearestNeighbor class that can take a k as input
  Yval_predict = nn.predict(Xval_rows, k = k)
  acc = np.mean(Yval_predict == Yval)
  print 'accuracy: %f' % (acc,)

  # keep track of what works on the validation set
  validation_accuracies.append((k, acc))
```

+ 只有训练集意味着测试集和训练集重合，过拟合。没有验证集同理，使用测试集进行超参数选择。
+ **必须分割验证集和测试集**
  + 机器学习中，并非尽可能的拟合训练集，而是让分类器和方法在训练集以外的未知数据表现更好
  + 不要用测试集调整超参数，会使得模型过拟合，最后在模型部署的时候效果更差。**测试集只在训练完成后评价最后的模型使用**

+ 交叉验证
对于训练集和验证集较小的时候，可以采用交叉验证方法。
平均分为多份，分别拿每份验证，然后计算出指定超参数下的平均值作为验证的效果。基本参考下图。一般训练集份数越多，直线越平滑

  + 交叉验证需要大量计算资源，常用于小数据，深度学习中不常用
  + 一般直接把训练集按照50%-90%的比例分成训练集和验证集。

[![XwM94f.png](https://s1.ax1x.com/2022/06/05/XwM94f.png)](https://imgtu.com/i/XwM94f)

### KNN分类器的缺点
+ 训练时间短，直接存储输入数据及标签。但是由于要比较输入图像和训练集，所以需要花费大量时间计算。我们对模型的关注点是测试效率远高于训练效率。
+ 维度灾难：KNN分类器可以看成是通过训练数据把样本空间分成几块。然而如果我们希望分类器效果更好，需要训练数据密集分布在空间中，否则最近邻点相差太远，导致与样本的相似性不高，**所以随着数据维度增大，对数据的需求呈指数增大**。
+ 不能直接体现图像语义区别，而是图像背景、颜色差异。
+ 在低维度下可能是好选择，但很少用于图像分类。高维度向量之间的距离通常反直觉，基于像素的相似与感官和语义上的相似是不同的。

### 线性分类器
待补



