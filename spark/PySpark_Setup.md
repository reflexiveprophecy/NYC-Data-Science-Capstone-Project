# PySpark Setup
---
1. Install PySpark
    - Make sure you use `anaconda` or `conda` as you main packages manganer.
    - run `conda install pyspark` to install PySpark
    - Confirm installation by run `pyspark` in Terminal
    - It's normal to see warning message like:
        > NativeCodeLoader:62 - Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
    
    - You can safely ignore this warning as it is associated with 32bits and 64bits compilation of Hadoop, it would cause negative impact for our scale of work.

2. Set local Spark path
    - At the root of your terminal open `.bash_profile` with any text editor.
    - Insert the following two path. Make sure you change `YourName`.
        `export SPARK_HOME=/Users/YourName/anaconda3/lib/python3.6/site-packages/pyspark`
        `export PATH=$SPARK_HOME/bin:$PATH`

3. Integrate with Jupyter Notebook.
    - run `pip install findspark`
    - open a new jupyter notebook `jupyter notebook`
    - run `import findspark` and `findspark.init()` to initialize a local spark cluster.
    - If no error shown when after execution, you are ready to go!

4. Run a test to see the Spark power.
    - A simple script to simulate **pi** with 100million calculation
    - We can see that the end result ~= 3.1415 in a relatively short timeframe (**100 mil calculations in a few seconds**).
    ```python
    import findspark
    findspark.init()
    import pyspark
    import random
    sc = pyspark.SparkContext(appName="Pi")
    num_samples = 100000000
    def inside(p):     
        x, y = random.random(), random.random()
        return x*x + y*y < 1
    count = sc.parallelize(range(0, num_samples)).filter(inside).count()
    pi = 4 * count / num_samples
    print(pi)
    sc.stop()
    ```
    This exmaple is borrowed from [here](https://blog.sicara.com/get-started-pyspark-jupyter-guide-tutorial-ae2fe84f594f).
