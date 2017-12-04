#coding:utf-8
# write  by  zhou

import  time
class TokenBucket(object):

    def __init__(self,init_token,capacity,speed):
        '''
        :param init_token  初始化令牌数
        :param capacity    令牌桶容量
        :param speed       每秒填充令牌数目
        '''
        assert  init_token<=capacity, "init_token 必须 不大于 capacity"
        self._tokens=init_token
        self.capacity=capacity
        self.speed=speed
        self.now=time.time()

    def consume(self,token):
        '''
        :param token  消费的token数目
        '''
        if token>self.capacity:
            raise Exception("所要消费的数目超过了令牌桶的容量!")
        else:
            if self.token>=token:
                self._tokens-=token
                return True
            else:
                return False

    @property
    def token(self):
        now = time.time()
        if self._tokens < self.capacity:
            _ = self.speed*(now-self.now)
            self._tokens = min(self.capacity, _ + self._tokens)
        self.now = now
        return self._tokens

if __name__ == "__main__":
    bucket_1=TokenBucket(1,100,100) # 初始化一个容量为100的桶,桶内最初有1个令牌,后续每秒填充100个令牌

    for i in range(100):
        time.sleep(0.03)
        print  bucket_1.consume(1)

    print "#######"
    for i in range(300):
        time.sleep(0.001)
        print  bucket_1.consume(1)

