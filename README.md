# SPL_Classification_Linux

This repository extends the original [SPL-Classification project](https://github.com/spgroup/SPL-Classification) and focuses on **identifying code changes from Linux commits** or other projects with a similar structure (i.e., projects that use **Kconfig** and **Makefile** to manage variability).

## Overview

The tool automates the classification of commits based on the Software Product Line (SPL) taxonomy.  
It is designed to handle repositories such as the Linux kernel and projects.

## Prerequisites

- Python 3.8 or higher  
- Git

## Installation and Usage

1. **Clone this repository**
   ```bash
   git clone git@github.com:karinegmg/SPL-Classifier.git
   # or
   git clone https://github.com/karinegmg/SPL-Classifier.git

2. **Install the required dependencies**
    ```bash
    pip install -r requirements.txt
3. **Configure your environment**
   Open the .envExample file, and add the SPL repository link you want to classify automatically in the REPOSITORY_PATH variable:
     ```bash
    REPOSITORY_PATH="https://github.com/Dasharo/coreboot.git"

4. **Run the tool**
     ```bash
    python myRepo.py
