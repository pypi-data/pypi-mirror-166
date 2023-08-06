import pandas as pd  # manipulação de dado em formato de dataframe
import statsmodels.api as sm  # biblioteca de modelagem estatística
import statsmodels.formula.api as smf

# Definição de uma função overdisp.


def overdisp(model, data):
    """

    Overdisp test for Statsmodels GLM Poisson model

    """

    # dictionary that identifies the type of the inputed model
    models_types = {
        "<class 'statsmodels.genmod.generalized_linear_model.GLM'>": "GLM"}

    try:
        # identify model type
        model_type = models_types[str(type(model.model))]
    except:
        raise Exception("The model is not yet supported...",
                        "Suported types: ", list(models_types.values()))

    # dictionary that identifies the family type of the inputed glm model
    glm_families_types = {
        "<class 'statsmodels.genmod.families.family.Poisson'>": "Poisson"}

    try:
        # identify family type
        glm_families_types[str(type(model.family))]

    except:
        raise Exception("This family is not supported...",
                        "Suported types: ", list(glm_families_types.values()))

    formula = model.model.data.ynames + " ~ " + \
        ' + '.join(model.model.data.xnames[1:])

    df = pd.concat([model.model.data.orig_endog.astype("int"),
                    model.model.data.orig_exog], axis=1)

    # adjust column names with special characters from categorical columns
    df.columns = df.columns.str.replace('[', '', regex=True)
    df.columns = df.columns.str.replace('.', '_', regex=True)
    df.columns = df.columns.str.replace(']', '', regex=True)

    # adjust formula with special characters from categorical columns
    formula = formula.replace("[", "")
    formula = formula.replace('.', "_")
    formula = formula.replace(']', "")

    print("Estimating model...: \n", model_type)

    df = df.drop(columns=["Intercept"])

    if model_type == "Poisson":
        model = smf.glm(formula=formula, data=df,
                        family=sm.families.Poisson()).fit()

    # find lambda
    df['lmbda'] = model.fittedvalues

    # creating ystar
    df['ystar'] = (((data[model.model.data.ynames]-df['lmbda'])**2)
                   - data[model.model.data.ynames])/df['lmbda']

    # ols estimation
    modelo_auxiliar = sm.OLS.from_formula("ystar ~ 0 + lmbda", df).fit()

    print(modelo_auxiliar.summary2(), "\n")

    print("==================Result======================== \n")
    print(f"p-value: {modelo_auxiliar.pvalues[0]} \n")

    if modelo_auxiliar.pvalues[0] > 0.05:
        print("Indicates equidispersion at 95% confidence level")
    else:
        print("Indicates overdispersion at 95% confidence level")
