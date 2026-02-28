import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

df = pd.read_csv("saber11_bogota_limpio1.csv")

df["estrato_num"] = df["estrato_num"].astype("category")

print(df["punt_global"].describe())

print(df["estrato_num"].value_counts())

anova_model = smf.ols("punt_global ~ C(estrato_num)", data=df).fit()
anova_table = sm.stats.anova_lm(anova_model, typ=2)
print(anova_table)

groups = [group["punt_global"].values for name, group in df.groupby("estrato_num")]
kruskal_result = stats.kruskal(*groups)
print(kruskal_result)