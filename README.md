# sparky

## 1. PySpark in VS Code Virtual Environment  
1. Created & activated a Python venv in VS Code:  
   ```bash
   python3 -m venv ./venv
   source venv/bin/activate
   ```  
2. Installed PySpark into the venv:  
   ```bash
   pip install pyspark
   ```  
3. Verified import works in a notebook/REPL:  
   ```python
   import pyspark
   print(pyspark.__version__)
   ```

## 2. Install & Point to Java  
1. Installed OpenJDK 17 (via Homebrew).  
2. In `~/.zshrc`, set:  
   ```zsh
   export JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
   export PATH="$JAVA_HOME/bin:$PATH"
   ```  
3. Confirmed with:  
   ```bash
   java -version  # showed OpenJDK 17.0.14
   ```

## 3. Download & Configure Spark Distribution  
1. Unpacked Spark 3.5.4 (Hadoop 3) to `~/spark-3.5.4-bin-hadoop3`.  
2. In `~/.zshrc`, set:  
   ```zsh
   export SPARK_HOME=~/spark-3.5.4-bin-hadoop3
   export PATH="$SPARK_HOME/bin:$PATH"
   ```  
3. Verified with:  
   ```bash
   $SPARK_HOME/bin/pyspark --version
   ```

## 4. Enable the BigQuery Connector  
### A. Via `spark-defaults.conf`  
1. Under `$SPARK_HOME/conf`, created `spark-defaults.conf` from the `.template` if needed.  
2. Added the line:  
   ```
   spark.jars.packages com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.32.2
   ```  
3. Launched Spark with verbose output to see the connector download:  
   ```bash
   export SPARK_PRINT_LAUNCH_COMMAND=1
   $SPARK_HOME/bin/pyspark --verbose
   ```  

### B. (Alternate) Explicit `--packages` on Launch  
- Direct command:  
  ```bash
  $SPARK_HOME/bin/pyspark \
    --packages com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.32.2
  ```  
- Or add to `~/.zshrc` as an alias:  
  ```zsh
  alias pyspark_bq='$SPARK_HOME/bin/pyspark --packages com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.32.2'
  ```

## 5. Verify the Connector Is Loaded  
1. In your shell, confirm the defaults file is in place:  
   ```bash
   ls $SPARK_HOME/conf/spark-defaults.conf
   grep spark.jars.packages $SPARK_HOME/conf/spark-defaults.conf
   ```  
2. Run `pyspark` (or `pyspark_bq`) and watch for Maven download logs:  
   ```
   :: resolving dependencies ::
   Downloading: …spark-bigquery-with-dependencies_2.12-0.32.2.jar
   ```

## 6. Test Read/Write to BigQuery  
1. Point at your service account JSON:  
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
   ```  
2. In PySpark shell or script:  
   ```python
   df = spark.read.format("bigquery") \
       .option("project", "my-gcp-proj") \
       .option("dataset", "my_dataset") \
       .option("table", "my_table") \
       .load()
   df.show(5)

   df.write.format("bigquery") \
       .option("table", "my-gcp-proj:my_dataset.new_table") \
       .mode("overwrite") \
       .save()
   ```  
3. Verify in BigQuery console that `new_table` exists and contains your data.