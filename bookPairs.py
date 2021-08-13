#s et up SparkContext for WordCount application
import pyspark
from pyspark import SparkContext
from pyspark.sql.functions import explode
sc = SparkContext("local", "bookPairs")

def line_to_list(s):
    temp = []
    s = s.split(",")
    s = list(map(int, s))
    for i in range(len(s)):
        for j in range(i+1, len(s)):
            temp.append((s[i],s[j]))
    return temp


lines = sc.textFile("/home/cs143/data/goodreads.user.books")
temps = lines.flatMap(lambda line: line.split(":")[1:])
temps = temps.flatMap(lambda line: line_to_list(line))
book_pairs = temps.map(lambda line: (line, 1))
book_pair_counts = book_pairs.reduceByKey(lambda a, b: a+b)
book_pair_counts = book_pair_counts.filter(lambda a: a[1] > 20)
book_pair_counts.saveAsTextFile("output")
