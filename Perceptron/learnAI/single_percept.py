'''
Created on Mar 25, 2017

@author: e427632
'''
from functools import reduce
import matplotlib.pyplot as plt
import numpy as np
import regex as re


global lst_weight
global lst_bias
global lst_delta


class single_percept( object ):

    def __init__( self, input_num, activator ):
        #global lst_weight
        #global lst_bias
        #global lst_delta
        '''
        Constructor       
        '''
        self.activator = activator
        # 权重向量初始化为0
        self.weights = [0 for _ in range( input_num )]
        # 偏置项初始化为0
        self.bias = 0

        lst_weight.append(self.weights)
        lst_bias.append(self.bias)
        lst_delta.append(0)
    
    def __str__( self ):
        return 'weights\t:%s\nbias\t:%.3f\n' % ( self.weights, self.bias );
    
    def predict( self, input_vec ):
        '''
                  输入向量，输出感知器的计算结果
        '''
        # 把input_vec[x1,x2,x3...]和weights[w1,w2,w3,...]打包在一起
        # 变成[(x1,w1),(x2,w2),(x3,w3),...]
        # 然后利用map函数计算[x1*w1, x2*w2, x3*w3]
        # 最后利用reduce求和
        
        zipped_vec = zip( input_vec, self.weights ) 
        #mapped_vec = list( map( lambda( x, w ): x * w, zipped_vec ) )
        mapped_vec = list(map(lambda v: v[0] * v[1], zipped_vec))
        reduced_sum = reduce( lambda a, b:a + b, mapped_vec, 0.0 )
        
        return self.activator(reduced_sum + self.bias);
    
    def train( self, input_vecs, targets, iteration, rate ):
            for i in range( iteration ):
                self._one_iteration( input_vecs, targets, rate )
                
    def _one_iteration( self, input_vecs, targets, rate ):
        #global lst_weight
        #global lst_bias


        '''
                    一次迭代，把所有的训练数据过一遍
        '''
        # 把输入和输出打包在一起，成为样本的列表[(input_vec, target), ...]
        # 而每个训练样本是(input_vec, target)
        samples = zip( input_vecs, targets )
        # 对每个样本，按照感知器规则更新权重
        for ( input_vec, target ) in samples:
            # 计算感知器在当前权重下的输出
            output = self.predict( input_vec )
            # 更新权重
            self._update_weights( input_vec, output, target, rate )
            lst_weight.append(self.weights)
            lst_bias.append(self.bias)
            
    def _update_weights( self, input_vec, output, target, rate ):
        #global lst_delta
        '''
                    按照感知器规则更新权重
        '''
        # 把input_vec[x1,x2,x3,...]和weights[w1,w2,w3,...]打包在一起
        # 变成[(x1,w1),(x2,w2),(x3,w3),...]
        # 然后利用感知器规则更新权重
                              
        delta = target - output
        lst_delta.append(delta)

        zipped_in_vec = zip( input_vec, self.weights )
        mapped_in_vec = list( map( lambda v: v[1] + rate*delta*v[0], zipped_in_vec))
        # mapped_in_vec = list( map( lambda(x,w): x + rate*delta*x, zipped_in_vec)
                                      
        self.weights = mapped_in_vec
        
        # self.weights = list( map( 
        #    lambda ( x, w ): w + rate * delta * x,
        #    list( zip( input_vec, self.weights ) ) ) )
        # 更新bias
        self.bias += rate * delta

        print("delta =%.3f weights[%.3f %.3f], bias[%.3f]" % (delta , self.weights[0] , self.weights[1] , self.bias) )


def f_and( x ):
    '''
        定义激活函数f
    '''
    return 1 if x > 0.5 else 0

def get_training_dataset():
    '''
        基于and真值表构建训练数据
    '''
    # 构建训练数据
    # 输入向量列表
    input_vecs = [[0, 0, 0],
                  [0, 0, 1],
                  [0, 1, 0],
                  [0, 1, 1],
                  [1, 0, 0],
                  [1, 0, 1],
                  [1, 1, 0],
                  [1, 1, 1]
                  ]
    # 期望的输出列表，注意要与输入一一对应
    # [1,1] -> 1, [0,0] -> 0, [1,0] -> 0, [0,1] -> 0
    targets = [0, 1, 1, 1, 0, 0, 0, 1]
    #targets = [1, 0, 1, 1]
    return input_vecs, targets    

def train_and_perceptron():
    '''
        使用and真值表训练感知器
    '''
    # 创建感知器，输入参数个数为2（因为and是二元函数），激活函数为f
    p = single_percept( 3, f_and )
    # 训练，迭代10轮, 学习速率为0.1
    input_vecs, targets = get_training_dataset()
    p.train( input_vecs, targets, 6, 0.1 )
    # 返回训练好的感知器
    return p
def test_plot():
    fig = plt.figure()
    x = np.arange(10)
    ax = plt.subplot(111)
    for i in range(5):
        line, = ax.plot(x, i * x, label = '$y = %ix$' % i)

    ax.legend(loc = 'upper center', bbox_to_anchor = (0.5, 1.05),
              ncol = 3, fancybox = True, shadow = True)
    plt.show()

if __name__ == '__main__':
    lst_weight = []
    lst_bias = []
    lst_delta = []

    #test_plot()

    and_perception = train_and_perceptron()
    
    print( and_perception )
    
    print( '1 and 1 = %d' % and_perception.predict( [0, 0, 1] ) )
    print( '0 and 0 = %d' % and_perception.predict( [0, 1, 0] ) )
    print( '1 and 0 = %d' % and_perception.predict( [0, 1, 1] ) )
    print( '0 and 1 = %d' % and_perception.predict( [1, 1, 0] ) )

    fig = plt.figure()
    ax = plt.subplot(111)
    x = np.arange(49)

    ax.plot(x,lst_delta, label= 'delta')
    ax.plot(x,lst_bias, label = 'bias')
    ax.plot(x,lst_weight, label = 'wi')

    ax.legend(loc='upper center', bbox_to_anchor = (0.5,1.05), ncol = 3, fancybox = True, shadow = True)
    plt.show()

    #plt.plot(lst_delta)

    #plt.plot(lst_weight)

    #plt.plot(lst_bias)

    #ax = plt.subplot(111)
    #plt.show()



