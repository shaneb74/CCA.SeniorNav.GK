# Senior Navigator (patch)

- Folder renamed to avoid dots: `cca_seniornav_gk/`
- `app.py` and `logic.py` live in the same folder so `import logic` works.
- Optional `__init__.py` included; not required for Streamlit but harmless.

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
