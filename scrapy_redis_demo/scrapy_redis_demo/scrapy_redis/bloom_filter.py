#!/usr/bin/env python
# encoding: utf-8
"""
[Bloom Filter](https://en.wikipedia.org/wiki/Bloom_filter)
为了表达S={x1, x2,…,xn}这样一个n个元素的集合， Bloom Filter使用k个相互独立的哈希函数（Hash Function），
它们分别将集合中的每个元素映射到{1,…,m}的范围中。
m: bit数组的宽度（bit数）
n: 去重集合的元素的个数
k: 使用的hash函数的个数
p: False Positive的比率

设计和应用布隆过滤器的方法:http://blog.csdn.net/zq602316498/article/details/40660235
"""
import math
import mmh3
import BitVector
import redis
import time


class BloomFilter(object):
    def __init__(self, n=1000000000, p=0.00000001, redis_conn=None, key='BloomFilter'):
        """
        由用户决定要添加的元素数n和希望的误差率P
        :param n:
            the number of inserted elements
        :param p:
            false positive probability
        :param redis_conn:
            redis connection handle
        :param key:
            redis Setbit KEY_NAME
        """
        self.m = self.get_bits_number(n, p)
        self.k = self.get_hashfunc_number(n)

        self.mem = math.ceil(self.m/8/1024/1024)
        self.blocknum = math.ceil(self.mem/512)
        print self.mem
        print self.k


        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.redis = redis_conn
        if not self.redis:
            #默认如果没有redis连接，在内存中使用512M的内存块去重
            self.bitset = BitVector.BitVector(size=1 << 32)

        self.key = key

    @staticmethod
    def get_bits_number(n, p):
        return math.ceil(n*math.log(math.e, 2)*math.log(1/p, 2))

    def get_hashfunc_number(self, n):
        return math.ceil(math.log1p(2)*self.m/n)

    def get_hashs(self, value):
        hashs = list()
        N = 2**31-1
        for seed in self.seeds:
            hash = mmh3.hash(value, seed)
            if hash >= 0:
                hashs.append(hash)
            else:
                hashs.append(N - hash)
        return hashs

    def add(self, value):
        name = self.key + "_" + str(ord(value[0])%self.blocknum)
        hashs = self.get_hashs(value)
        for hash in hashs:
            if self.redis:
                self.redis.setbit(name, hash, 1)
            else:
                self.bitset[hash] = 1

    def is_exist(self, value):
        name = self.key + "_" + str(ord(value[0])%self.blocknum)
        hashs = self.get_hashs(value)
        exist = True
        for hash in hashs:
            if self.redis:
                exist = exist & self.redis.getbit(name, hash)
            else:
                exist = exist & self.bitset[hash]
        return exist

