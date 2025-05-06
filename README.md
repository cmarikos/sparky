# Spark & BigQuery Setup Documentation

Welcome to the **sparky** project! This guide walks you through every step needed to:

1. Install and configure **Apache Spark** on your local machine
2. Initialize and organize the **Git** repository for `sparky`
3. Enable and connect to **BigQuery** in Google Cloud
4. Write, run, and understand the **test_table.py** script to read and write data
5. Authenticate using a **Google Cloud service account** securely

> **Audience:** You should be comfortable writing SQL queries, using BigQuery’s web UI, and writing basic Python code. This guide explains any command‑line steps and setup details.

---

## 1. Install Apache Spark

Spark is a distributed data processing engine. Even though we’ll run it locally, you still need to install the full Spark distribution.

1. **Download Spark**
   - Visit https://spark.apache.org/downloads.html and select:
     - **Spark version:** 3.5.4
     - **Hadoop version:** 3.x (e.g. `Pre-built for Apache Hadoop 3.3 and later`)
   - This gives you a `spark-3.5.4-bin-hadoop3.tgz` file.

2. **Extract Spark**
   Open a Terminal (macOS/Linux) or PowerShell (Windows) and run:
   ```bash
   # Replace paths as needed
   tar -xzf ~/Downloads/spark-3.5.4-bin-hadoop3.tgz
   mv spark-3.5.4-bin-hadoop3 ~/spark-3.5.4-bin-hadoop3
   ```
   - This unpacks Spark into `~/spark-3.5.4-bin-hadoop3`.

3. **Configure Environment Variables**
   When you install Spark, you need to tell your shell where it lives.
   - Open your shell profile file:
     - **macOS/Linux**: `nano ~/.zshrc` or `nano ~/.bashrc`
     - **Windows PowerShell**: set environment variables in System Settings or `$PROFILE`
   - Add these lines:
     ```bash
     # Point SPARK_HOME to your Spark directory
     export SPARK_HOME=~/spark-3.5.4-bin-hadoop3
     # Add Spark’s executables to your PATH
     export PATH="$SPARK_HOME/bin:$PATH"
     ```
   - Save and **reload** your profile:
     ```bash
     source ~/.zshrc  # or ~/.bashrc
     ```

4. **Verify Installation**
   Run:
   ```bash
   spark-shell --version
   ```
   You should see output that mentions Spark 3.5.4.

---

## 2. Initialize the `sparky` Git Repository

In this step, you’ll use both your **CLI** (command‑line interface) and **VS Code** to set up the project structure and version control.

### 2.1 Using the CLI

1. **Create the project folder & initialize Git**
   ```bash
   # In your terminal (or VS Code integrated terminal):
   mkdir ~/projects/sparky
   cd ~/projects/sparky
   git init
   ```
   This creates a new folder and turns it into a Git repository.

2. **Set up a Python virtual environment**
   ```bash
   python3 -m venv .venv       # Create the virtual environment
   source .venv/bin/activate   # Activate it (you’ll see (.venv) in your prompt)
   ```
   You’ll keep Python dependencies isolated here.

3. **Install Python dependencies**
   ```bash
   pip install --upgrade pip
   pip install pyspark google-cloud-bigquery
   ```


### 2.2 Using VS Code

1. **Open the project in VS Code**
   - Launch VS Code, then **File → Open Folder…** and select `~/projects/sparky`.

2. **Confirm your virtual environment**
   - In the bottom‑left corner VS Code should show `Python 3.x.x (venv)`. If not:
     1. Press ⌘+Shift+P (or Ctrl+Shift+P).
     2. Type **Python: Select Interpreter** and pick the `.venv` environment.

3. **Create or view files**
   - Use the VS Code **Explorer** pane to see your `.venv` folder and any files.

4. **Create the `.gitignore`**
   - We never want to push credentials
   - In the Explorer pane: right-click in your repo root and select **New File** → name it `.gitignore`.
   - Open `.gitignore` in the editor and add:
     ```gitignore
     # Python virtual environment
     .venv/

     # Spark output directories
     spark-warehouse/

     # Local scripts or test outputs
     test_table.py
     *.csv

     # Credentials folder
     credentials/*.json
     ```
   - Save the file, then stage & commit via the integrated terminal:
     ```bash
     git add .gitignore
     git commit -m "chore: add .gitignore"
     ```

5. **Use the integrated terminal**
   - Open the terminal via **View → Terminal**.
   - All CLI commands you ran previously (Git init, pip install) can be re‑run here.

By combining CLI commands in VS Code’s integrated terminal with file editing and creation in the Explorer, you get a smooth workflow for repo setup and environment configuration.

### 2.3 (continued...)


1. **Open the project in VS Code**
   - Launch VS Code, then **File → Open Folder…** and select `~/projects/sparky`.

2. **Confirm your virtual environment**
   - In the bottom‑left corner VS Code should show `Python 3.x.x (venv)`. If not:
     1. Press ⌘+Shift+P (or Ctrl+Shift+P).
     2. Type **Python: Select Interpreter** and pick the `.venv` environment.

3. **Create or view files**
   - Use the VS Code **Explorer** pane to see your `.gitignore` and `.venv` folder.
   - You can also open a new file (e.g. `README.md`) or edit `.gitignore` visually.

4. **Use the integrated terminal**
   - Open the terminal via **View → Terminal**.
   - All CLI commands you ran previously (Git init, pip install) can be re‑run here.

By combining CLI commands in VS Code’s integrated terminal with file editing in the Explorer, you get a smooth workflow for repo setup and environment configuration.

## 3. Enable BigQuery & Set Up Service Account
 Enable BigQuery & Set Up Service Account

To let Spark write to BigQuery, we need:
- The **BigQuery API** enabled in GCP
- A **service account** with the right permissions
- A **JSON key file** stored locally (but not in GitHub!)

1. **Enable the BigQuery API**
   - Open the [Google Cloud Console](https://console.cloud.google.com/apis/library).
   - Search for **BigQuery API**, click **Enable**.

2. **Create a service account**
   - Navigate to IAM & Admin → Service Accounts.
   - Click **Create Service Account**.
     - **Name:** sparky-sa
     - **Description:** “Spark ↔ BigQuery connector”
   - Grant roles:
     - BigQuery Data Viewer (to read tables)
     - BigQuery Data Editor (to create and write tables)
     - Storage Object Admin (for temporary GCS staging)
   - **Create Key** (JSON) and **download** it.

3. **Store the key securely**
   - Place the file under `credentials/spark-bigquery-sa.json`
   - It’s already ignored by our `.gitignore`.

---

## 4. Write the `test_table.py` Script

This script shows a full round‑trip: read a local CSV, then write it into BigQuery.

1. **Create** `test_table.py` in your repo root.

2. **Paste the following**:
   ```python
   from pyspark.sql import SparkSession
   from pyspark import SparkFiles

   # Grab the service account JSON shipped with --files
   cred_path = SparkFiles.get("spark-bigquery-sa.json")

   # 1) Start Spark
   spark = SparkSession.builder \
       .appName("TestBigQueryReadWrite") \
       .getOrCreate()

   # 2) Read a CSV file (e.g. your voterfile)
   df = spark.read.csv(
       "/Users/you/Downloads/voterfile.csv",
       header=True,
       inferSchema=True
   )
   print("✅ Read CSV into DataFrame:")
   df.show(5)

   # 3) Write to BigQuery
   df.write.format("bigquery") \
     .option("table", "<PROJECT_ID>:sparky.test_table") \
     .option("temporaryGcsBucket", "<YOUR_GCS_BUCKET>") \
     .option("credentialsFile", cred_path) \
     .save()
   print("✅ Wrote DataFrame to BigQuery table sparky.test_table")

   # 4) Stop Spark
   spark.stop()
   ```
   - Replace `<PROJECT_ID>` and `<YOUR_GCS_BUCKET>` with your values.
   - **SparkFiles.get** lets Spark distribute the JSON key to every executor.

3. **Commit** your script:
   ```bash
   git add test_table.py
   git commit -m "feat: add test_table.py example for BigQuery round-trip"
   ```

---

## 5. Run the Script with `spark-submit`

Instead of `python test_table.py`, Spark jobs need to be submitted with `spark-submit` so that all executors get the right JARs and files.

```bash
$SPARK_HOME/bin/spark-submit \
  --packages com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.32.2 \
  --files credentials/spark-bigquery-sa.json \
  --conf spark.driver.extraJavaOptions="-DGOOGLE_APPLICATION_CREDENTIALS=spark-bigquery-sa.json" \
  --conf spark.executor.extraJavaOptions="-DGOOGLE_APPLICATION_CREDENTIALS=spark-bigquery-sa.json" \
  test_table.py
```

- `--packages` pulls in the Scala BigQuery connector JAR automatically.
- `--files` ships your JSON key to the driver & executors.
- The two `spark.*.extraJavaOptions` flags set the `GOOGLE_APPLICATION_CREDENTIALS` env var inside the JVM.

> **Pro Tip:** If you see errors about “No FileSystem for scheme gs” you need to add the GCS connector:
> ```bash
> --packages com.google.cloud.bigdataoss:gcs-connector:hadoop3-2.2.5,...
> ```

---

## 6. Next Steps

- **Query Interactively:** Use VS Code’s BigQuery extension or the Google Cloud CLI (`bq query ...`).
- **Scaling Up:** Move from local mode to a managed Spark service (Dataproc or Dataflow).
- **Automation:** Schedule this job with Airflow, Cloud Scheduler, or similar.

That’s it! You now have a local Spark + BigQuery integration, a Git repo, and a working example script.
Happy data‑engineering! 🎉

