from nzpyida import IdaDataBase, IdaDataFrame
from nzpyida.ae import NZFunGroupedApply
import pandas as pd
nzpy_dsn ={
        "database":"STOCKS",
        "port" :5480,
        "host" : "9.30.250.118",
        "securityLevel":3,
        "logLevel":0
        }

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
idadb = IdaDataBase(nzpy_dsn, uid="admin",pwd="password", verbose=True)
print(idadb)
idadf = IdaDataFrame(idadb, 'stocks_date')
print(idadf.head())

code_str_host_spus = """def all_stocks_add_features(self,df):
        import nzaeCppWrapper
        imputed_df = df.copy()
        pointer = self.getInputValue(2).pUdsData
        result = nzaeCppWrapper.cdata(pointer,10).encode('latin-1')
        self.output(1, str(result))
"""
output_signature = {'ID': 'int', 'test': 'str' }
nz_tapply = NZFunGroupedApply(df=idadf, code_str=code_str_host_spus, fun_name='all_stocks_add_features', index='TICKER',  output_signature=output_signature)
result = nz_tapply.get_result()
print(result.head(100))