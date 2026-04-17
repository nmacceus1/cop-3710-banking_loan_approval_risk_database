# Usage

## Setup

1. Create a `.env` file with the appropriate values for your FreeSQL schema:
    ```
    DB_USER=
    DB_PASS=
    DB_DSN=
    LIB_DIR=
    ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. If CSV data has not been generated, run:
    ```
    python3 ./preprocess.py
    ```

4. Upload data to your FreeSQL database:
    ```
    python3 ./dataload.py
    ```

5. Launch the Streamlit app:
    ```
    python3 -m streamlit run ./app.py
    ```