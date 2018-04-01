# import os
# import logging
# import pyspark
# import random

# # Create logging info
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# # Build sparkQuery class
# class sparkQuery(object):
#     """
#     Simple spark query test class
#     """

#     def __init__(self, sc, upperLimit=10):
#         """Initialize"""
#         logger.info("Construct the Spark RDD...")
#         self.sc = sc
#         targetRange = range(upperLimit)
#         self.dataSet = self.sc.parallelize(targetRange)
#         # return (self.dataSet.count())

#     def moreThan(self, target):
#         """Get even nums"""
#         logger.info("Now getting count of numbers more than target...")
#         temp = self.dataSet.filter(lambda x: x > target)
#         evenResult = temp.count()
#         return evenResult

#     def getEven(self):
#         """Get even nums"""
#         logger.info("Now getting all the even numbers...")
#         temp = self.dataSet.filter(lambda x: x % 2 == 0)
#         evenResult = temp.collect()
#         return evenResult

#     def getOdd(self):
#         """Get odd nums"""
#         logger.info("Now getting all the odd numbers...")
#         temp = self.dataSet.filter(lambda x: x % 2 != 0)
#         oddResult = temp.collect()
#         return oddResult

# # from pyspark import SparkContext
# # sc = SparkContext("local", "Simple App")
# # tempRDD = sparkQuery(sc=sc, upperLimit=10)
# # print(tempRDD.dataSet.count())
# # sc.stop()
# # print("something is right")

# # dataPath = "./diamonds.csv"

# # # Initiate spark
# # sc = SparkContext('local')
# # sc = pyspark.SparkContext(appName="Pi")


# # def inside(p):
# #     x, y = random.random(), random.random()
# #     return x * x + y * y < 1
# # count = sc.parallelize(range(0, num_samples)).filter(inside).count()
# # pi = 4 * count / num_samples
# # print(pi)
# # sc.stop()

