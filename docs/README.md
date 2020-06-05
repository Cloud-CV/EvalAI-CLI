# EvalAI-CLI

<b>Command Line utility - Download_file</b>
Download_file - The below steps define the usage for Download_file.

## Pre-Req:
1. Setup the development environment for EvalAI and make sure that it is running perfectly. Check the Instruction under evalai-cli/readme.md file

## Download_file:

1.	In terminal with the Eval-CLI platform running, enter evalai download_file command with the entire host url you are using as shown in the below example.

    ```bash
      evalai download_file https://evalai.cloudcv.org/web/submission-files?bucket=<s3_bucket_name>&key=<file_path_in_bucket>
    ```
2.	If url is host and has bucket and key, url will be downloaded as a file

3.	If url does not have a bucket or key, below error will flash -
      "please check url or check with admin to get AWS s3 bucket name and key information"
