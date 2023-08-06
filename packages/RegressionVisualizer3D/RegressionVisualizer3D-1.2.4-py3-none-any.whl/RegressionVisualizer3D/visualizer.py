import numpy as _np
import pandas as _pd
import matplotlib.pyplot as _plt
import statsmodels.api as _sm
import sys as _sys
from IPython.display import display as _display

# a custom error
class ComputationalError(Exception):
     pass

# ==============================================================================
# Hidden functions

def _set_angles(axes, view_angle=None, view_elevation=None):
    """Hidden function to set the view angle and elevation on plots."""
    # set the view_angle and elevation, if the user has supplied them
    if view_angle is not None and view_elevation is None:
        axes.view_init(azim=view_angle)
    if view_elevation is not None and view_angle is None:
        axes.view_init(elev=view_elevation)
    if view_elevation is not None and view_angle is not None:
        axes.view_init(azim=view_angle, elev=view_elevation)


def _show_table(mod, model_type, show_statsmodels, verbose, intercept,
                predictor1_slope, predictor1_name, predictor2_slope,
                predictor2_name, interaction_slope, outcome_variable_name):
    """
    Hidden function to print out the regression table and true population
    regression equation.
    """
    # show the regression table?
    if show_statsmodels is True:
        print()
        _display(mod.summary())

        # print the true regression equation?
        if verbose is True and model_type == "linear_regression":
            print()
            print("\nTrue population regression equation:")
            print()
            print(f"Y = {intercept} + {predictor1_slope} * X_1 + {predictor2_slope} * X_2 + {interaction_slope} * X_1 * X_2 + error")
            print()
            print("Where:")
            print(f" Y: {outcome_variable_name}")
            print(f" X_1: {predictor1_name}")
            print(f" X_2: {predictor2_name}\n")

        if verbose is True and model_type == "poisson_regression":
            print()
            print("True population regression equation:")
            print()
            print(f"ln(Y) = {intercept} + {predictor1_slope} * X_1 + {predictor2_slope} * X_2 + {interaction_slope} * X_1 * X_2 + error")
            print()
            print("Where:")
            print(f" Y: {outcome_variable_name}")
            print(f" X_1: {predictor1_name}")
            print(f" X_2: {predictor2_name}")

        if verbose is True and model_type == "binary_logistic_regression":
            print()
            print("True population regression equation:")
            print()
            print(f"logit(Y) = {intercept} + {predictor1_slope} * X_1 + {predictor2_slope} * X_2 + {interaction_slope} * X_1 * X_2 + error")
            print()
            print("Where:")
            print(f" Y: {outcome_variable_name}")
            print(f" X_1: {predictor1_name}")
            print(f" X_2: {predictor2_name}")

# ==============================================================================
# User-facing functions

def model_plot(model_type="linear_regression",
               intercept=None,
               predictor1_slope=None,
               predictor2_slope=None,
               interaction_slope=0,
               sample_size=100,
               population_size=1000,
               error_sd=None,
               predictor1_name="Predictor 1",
               predictor2_name="Predictor 2",
               outcome_variable_name="Outcome Variable",
               axis_size = 3,
               show_statsmodels=True,
               legend_loc="lower center",
               view_angle=None,
               view_elevation=None,
               plot_size=(16, 8),
               data_alpha=1,
               surface_alpha=0.7,
               verbose=True):
    """
    This function generates a 3D visualization of several types of 
    regression model. It creates population data, based on parameters 
    supplied as arguments. It then draws a random sample from that 
    population data. A regression model is then fit to the sample data.
    The type of regression model which is fit is specified by the 
    `model_type" argument. N.B. the `model_type` parameter also specifies
    the form of the data-generating process (e.g. `linear_regression` will
    generate population data from a linear equation, the other models involve
    an equation with a link function).

    The regression surfaces and the data are then shown on 3D plots, for
    the population and the sample data. By default, explanations of 
    what the function is doing/showing are printed out for the user.

    The user can set all of the parameters, BUT some combinations may 
    cause computational errors, depending on the type of regression 
    model.

    Parameters
    ----------

    model_type: a string specifying the type of regression model 
    to be visualized. Must be one of "linear_regression", 
    "poisson_regression" or "binary_logistic_regression"

    intercept: the intercept to be used in the population data
    generating process. Default is 1.

    predictor1_slope: the slope of the first predictor, to be used in 
    the population data generating process. Default is None, but if 
    None is a supplied a default will be chosen based on model_type.

    predictor2_slope: the slope of the second predictor, to be used in 
    the population data generating process. Default is None, but if None
    is a supplied a default will be chosen based on model_type.

    interaction_slope: the slope of the interaction between the two 
    predictors to be used in the population data generating process. 
    Default is None, but if None is a supplied a default will be chosen 
    based on model_type.

    sample_size: an integer setting the size of the random sample, 
    drawn from the population data. Default is 100

    population_size: an integer setting the size of the population. 
    Default is 1000.

    error_sd: the standard deviation of the error added to the 
    population regression equation used in the data generating process. 
    Default is None, but if None is supplied a default will be 
    chosen based on model_type.

    predictor1_name: a string setting the name of the first predictor. 
    Default is "Predictor 1".

    predictor2_name: a string setting the name of the second predictor. 
    Default is "Predictor 2".

    outcome_variable_name:  a string setting the name of the outcome 
    variable. Default is "Outcome Variable".

    axis_size: a number setting the axis size 
    (min = -axis_size, max = axis_size). Default is 3.

    show_statsmodels: a Boolean, if True, the regression table from 
    the regression model fit to the sample data will be shown.

    legend_loc: a string setting the location to display the figure 
    legend. Default is "lower center".

    view_angle: a number setting the view angle for the graphs. Default 
    is None, which will use the matplotlib default.

    view_elevation: a number setting the view elevation for the graphs. 
    Default is None, which will use the matplotlib default.

    plot_size: a tuple setting the figure size. Default is (16,8).

    data_alpha: a number between 0 and 1, setting the see-through-ness 
    of the datapoints on the graphs. Default is 1 (opaque).

    surface_alpha: a number between 0 and 1, setting the 
    see-through-ness of the regression surfaces on the graphs. 
    Default is  0.7

    verbose: a Boolean. If True an explanation of what the function 
    is doing will be displayed alongside the graphs (via printouts).
    The true regression equation used in the data generating process
    will also be shown. Default is True.

    Returns
    -------
    None.
    """

    # an array of the legal model types
    model_types = _np.array(
        ["linear_regression", "poisson_regression", "binary_logistic_regression"])

    # if verbose mode is true
    if verbose == True:

        # remove the "_" from the model type name
        formatted_model_type = model_type.replace("_", " ")

        # print out an explanation of what the function is doing/showing
        print()
        print(f"3D {formatted_model_type} visualizer: ")
        print(f"""
A population of {population_size} observations has been generated. A random 
sample of {sample_size} observations has been drawn from that population. 
Two graphs have been created.\n
The lefthand graph shows the population data and the population regression 
surface (e.g. if a regression model were fit to all of the population data).\n
The righthand graph shows the sample which was randomly drawn from the 
population. It also shows the sample regression surface (e.g. from a 
regression model fit to the sample data).""")

        # if the statsmodels table should be shown, let the user know where it 
        # will be displayed
        if show_statsmodels == True:
            print("""
Beneath is the regression table (with slopes and p-values etc.) from the sample
data. The true population regression equation used to generate the data is also
shown.""")

    # check the model_type supplied is legal, raise error if not
    assert model_type in model_types, "The model_type you have specified is not recognized! It should be one of:" + \
        str(model_types)

# ==============================================================================
# LINEAR REGRESSION

    if model_type == model_types[0]:

        # set default intercept, slopes and error sd if none are provided by the user
        if intercept == None:
            intercept = 1

        if predictor1_slope == None:
            predictor1_slope = 0.2

        if predictor2_slope == None:
            predictor2_slope = 3

        if error_sd == None:
            error_sd = 1

        # for the wireframe population regression surface
        x = _np.outer(_np.linspace(-axis_size,
                      axis_size, 32), _np.ones(32))
        y = x.copy().T  # transpose
        z = intercept + predictor1_slope*x + predictor2_slope*y + interaction_slope * x*y

        # population datapoints
        pop_data_x = _np.random.choice(_np.linspace(
            -axis_size, axis_size, 32), size=population_size)
        pop_data_y = _np.random.choice(_np.linspace(
            -axis_size, axis_size, 32), size=population_size)
        pop_data_z = intercept + predictor1_slope*pop_data_x + predictor2_slope*pop_data_y + \
            interaction_slope*pop_data_x*pop_data_y + \
            _np.random.normal(0, error_sd, size=population_size)

        # plot the population regression surface and data
        fig = _plt.figure(figsize=plot_size)
        ax1 = fig.add_subplot(121, projection="3d")
        ax1.plot_wireframe(x, y, z, color="darkred",
                           label="population linear regression surface", alpha=surface_alpha)
        ax1.scatter(pop_data_x, pop_data_y, pop_data_z, color="red",
                    label="population data", alpha=data_alpha)
        ax1.set_zlabel(outcome_variable_name)
        ax1.set_title("Population (N = "+str(population_size)+") :")
        _plt.xlabel(predictor1_name)
        _plt.ylabel(predictor2_name)

        # set the view angle and elevation, if the user has supplied them
        _set_angles(ax1, view_angle=view_angle, view_elevation=view_elevation)

        # get the sample data and fit a linear regression with statsmodels
        population_df = _pd.DataFrame({predictor1_name: pop_data_x,
                                       predictor2_name: pop_data_y,
                                       outcome_variable_name: pop_data_z,
                                       predictor1_name+" * "+predictor2_name: pop_data_x * pop_data_y})

        sample_df = population_df.sample(n=sample_size)

        # try to fit the regression model, warn the user if they generate 
        # computation errors
        try:
            mod = _sm.OLS(sample_df[outcome_variable_name], _sm.add_constant(sample_df[[
                      predictor1_name, predictor2_name, predictor1_name+" * "+predictor2_name]])).fit()
        except Exception as e: 
            raise ComputationalError(f"""
The combination of parameters (slopes etc.) that you supplied generated
computational errors! Please try another combination... The error generated 
was:\n {e}
""")


        # fit the regression model
        mod = _sm.OLS(sample_df[outcome_variable_name], _sm.add_constant(sample_df[[
                      predictor1_name, predictor2_name, predictor1_name+" * "+predictor2_name]])).fit()

        # get the parameters, from the regression model fit to the sample data
        mod_intercept = mod.params["const"]
        mod_predictor1_slope = mod.params[predictor1_name]
        mod_predictor2_slope = mod.params[predictor2_name]
        mod_interaction_slope = mod.params[predictor1_name +
                                           " * "+predictor2_name]

        # wireframe z values based on sample regression model parameters
        sample_z = mod_intercept + mod_predictor1_slope*x + \
            mod_predictor2_slope*y + mod_interaction_slope * x*y

        # plot the sample regression surface and data)
        ax2 = fig.add_subplot(122, projection="3d")
        ax2.plot_wireframe(x, y, sample_z, color="darkblue",
                           label="sample linear regression surface", alpha=surface_alpha)
        ax2.scatter(sample_df[predictor1_name], sample_df[predictor2_name],
                    sample_df[outcome_variable_name], color="blue", label="sample data", alpha=data_alpha)
        ax2.set_zlabel(outcome_variable_name)
        ax2.set_title("Sample (n = "+str(sample_size)+") :")
        _plt.xlabel(predictor1_name)
        _plt.ylabel(predictor2_name)

        # set the view angle and elevation, if the user has supplied them
        _set_angles(ax2, view_angle=view_angle, view_elevation=view_elevation)

        fig.legend(loc=legend_loc)

        # show the regression table and true regression equation, if set to be
        # displayed
        _show_table(mod, model_type, show_statsmodels, verbose, intercept,
                    predictor1_slope, predictor1_name, predictor2_slope,
                    predictor2_name, interaction_slope, outcome_variable_name)
                    
        # show the plot
        _plt.show()

# ==============================================================================
# POISSON REGRESSION

    if model_type == model_types[1]:

        # set default intercept, slopes and error sd if none are provided by the user
        if intercept == None:
            intercept = 1

        if predictor1_slope == None:
            predictor1_slope = 0.6

        if predictor2_slope == None:
            predictor2_slope = 0.2

        if error_sd == None:
            error_sd = 0.1

        # for the wireframe population regression surface
        x = _np.outer(_np.linspace(-axis_size,
                      axis_size, 32), _np.ones(32))
        y = x.copy().T  # transpose
        z = _np.exp(intercept + predictor1_slope*x +
                    predictor2_slope*y + interaction_slope*x*y)

        # population datapoints
        pop_data_x = _np.random.choice(_np.linspace(
            -axis_size, axis_size, 32), size=population_size)
        pop_data_y = _np.random.choice(_np.linspace(
            -axis_size, axis_size, 32), size=population_size)
        pop_data_z = _np.exp(intercept + predictor1_slope*pop_data_x + predictor2_slope*pop_data_y +
                             interaction_slope*pop_data_x*pop_data_y + _np.random.normal(0, error_sd, size=population_size))

        # plot the population regression surface and data
        fig = _plt.figure(figsize=plot_size)
        ax1 = fig.add_subplot(121, projection="3d")
        ax1.plot_wireframe(x, y, z, color="darkred",
                           label="population poisson regression surface", alpha=surface_alpha)
        ax1.scatter(pop_data_x, pop_data_y, pop_data_z, color="red",
                    label="population data", alpha=data_alpha)
        ax1.set_zlabel(outcome_variable_name)
        ax1.set_title("Population (N = "+str(population_size)+") :")
        _plt.xlabel(predictor1_name)
        _plt.ylabel(predictor2_name)
        _set_angles(ax1, view_angle=view_angle, view_elevation=view_elevation)

        # get the sample data and fit a Poisson regression with statsmodels
        population_df = _pd.DataFrame({predictor1_name: pop_data_x,
                                       predictor2_name: pop_data_y,
                                       outcome_variable_name: pop_data_z,
                                       predictor1_name+" * "+predictor2_name: pop_data_x * pop_data_y})

        sample_df = population_df.sample(n=sample_size)

        # try to fit the regression model, warn the user if they generate 
        # computation errors
        try:
            mod = _sm.GLM(sample_df[outcome_variable_name], _sm.add_constant(sample_df[[
                      predictor1_name, predictor2_name, predictor1_name+" * "+predictor2_name]]), family=_sm.families.Poisson()).fit()
        except Exception as e: 
            raise ComputationalError(f"""
The combination of parameters (slopes etc.) that you supplied generated
computational errors! Please try another combination... The error generated 
was:\n {e}
""")

        # fit the regression model, to the sample data
        mod = _sm.GLM(sample_df[outcome_variable_name], _sm.add_constant(sample_df[[
                      predictor1_name, predictor2_name, predictor1_name+" * "+predictor2_name]]), family=_sm.families.Poisson()).fit()

        # get the parameters, from the regression model fit to the sample data
        mod_intercept = mod.params["const"]
        mod_predictor1_slope = mod.params[predictor1_name]
        mod_predictor2_slope = mod.params[predictor2_name]
        mod_interaction_slope = mod.params[predictor1_name +
                                           " * "+predictor2_name]

        # wireframe z values from the sample regression model parameters
        sample_z = _np.exp(mod_intercept + mod_predictor1_slope *
                           x + mod_predictor2_slope*y + mod_interaction_slope * x*y)

        # plot the sample regression surface and data
        ax2 = fig.add_subplot(122, projection="3d")
        ax2.plot_wireframe(x, y, sample_z, color="darkblue",
                           label="sample poisson regression surface", alpha=surface_alpha)
        ax2.scatter(sample_df[predictor1_name], sample_df[predictor2_name],
                    sample_df[outcome_variable_name], color="blue", label="sample data", alpha=data_alpha)
        ax2.set_zlabel(outcome_variable_name)
        ax2.set_title("Sample (n = "+str(sample_size)+") :")
        _plt.xlabel(predictor1_name)
        _plt.ylabel(predictor2_name)

        # set the view angle and elevation, if the user has supplied them
        _set_angles(ax2, view_angle=view_angle, view_elevation=view_elevation)

        fig.legend(loc=legend_loc)

        # show the regression table and true regression equation, if set to be
        # displayed
        _show_table(mod, model_type, show_statsmodels, verbose, intercept,
                    predictor1_slope, predictor1_name, predictor2_slope,
                    predictor2_name, interaction_slope, outcome_variable_name)
                    
        # show the plot
        _plt.show()

# ==============================================================================
# BINARY LOGISTIC REGRESSION

    if model_type == model_types[2]:

        # set default intercept, slopes and error sd if none are provided by the user
        if intercept == None:
            intercept = 1

        if predictor1_slope == None:
            predictor1_slope = 0.7

        if predictor2_slope == None:
            predictor2_slope = 0.5

        if error_sd == None:
            error_sd = 0.6

        # for the wireframe population regression surface
        x = _np.outer(_np.linspace(-axis_size,
                      axis_size, 32), _np.ones(32))
        y = x.copy().T  # transpose
        lin_pop_z = intercept + predictor1_slope*x + \
            predictor2_slope*y + interaction_slope*x*y
        z = _np.exp(lin_pop_z)/(1 + _np.exp(lin_pop_z))

        # population datapoints
        pop_data_x = _np.random.choice(_np.linspace(
            -axis_size, axis_size, 32), size=population_size)
        pop_data_y = _np.random.choice(_np.linspace(
            -axis_size, axis_size, 32), size=population_size)
        lin_pred = intercept + predictor1_slope*pop_data_x + predictor2_slope*pop_data_y + \
            interaction_slope*pop_data_x*pop_data_y + \
            _np.random.normal(0, error_sd, size=population_size)
        pop_data_z = (_np.exp(lin_pred))/(1 + _np.exp(lin_pred))
        pop_data_z = _np.where(pop_data_z >= 0.5, 1, 0)

        # plot the population regression surface and data
        fig = _plt.figure(figsize=plot_size)
        ax1 = fig.add_subplot(121, projection="3d")
        ax1.plot_wireframe(x, y, z, color="darkred",
                           label="population logistic regression surface",
                          alpha=surface_alpha)
        ax1.scatter(pop_data_x[pop_data_z >= 0.5], pop_data_y[pop_data_z >= 0.5],
                   pop_data_z[pop_data_z >= 0.5], color="red", 
                   label=outcome_variable_name+" = 1 (population)",
                   alpha=data_alpha)
        ax1.scatter(pop_data_x[pop_data_z < 0.5], pop_data_y[pop_data_z < 0.5],
                    pop_data_z[pop_data_z < 0.5],
                    marker="x", color="red",
                    label=outcome_variable_name+" = 0 (population)",
                    alpha=data_alpha)
        ax1.set_zticks([0, 1])
        ax1.set_zlabel(outcome_variable_name+"/ Probability")
        ax1.set_zticks([0, 1])
        ax1.set_title("Population (N = "+str(population_size)+") :")
        _plt.xlabel(predictor1_name)
        _plt.ylabel(predictor2_name)
        _set_angles(ax1, view_angle=view_angle, view_elevation=view_elevation)

        # get the sample data and fit a binary logistic regression with statsmodels
        population_df = _pd.DataFrame({predictor1_name: pop_data_x,
                                       predictor2_name: pop_data_y,
                                       outcome_variable_name: pop_data_z,
                                       predictor1_name+" * "+predictor2_name: pop_data_x * pop_data_y})

        sample_df = population_df.sample(n=sample_size)

        # try to fit the regression model, warn the user if they generate 
        # computation errors
        try:
            mod = _sm.Logit(sample_df[outcome_variable_name], _sm.add_constant(sample_df[[
                            predictor1_name, predictor2_name, predictor1_name+" * "+predictor2_name]])).fit()
        except Exception as e: 
            raise ComputationalError(f"""
The combination of parameters (slopes etc.) that you supplied generated
computational errors! Please try another combination... The error generated 
was:\n {e}
""")

        # fit the regression model to the sample data
        mod = _sm.Logit(sample_df[outcome_variable_name], _sm.add_constant(sample_df[[
                        predictor1_name, predictor2_name, predictor1_name+" * "+predictor2_name]])).fit()

        # get the parameters from the regression model fit to the sample data
        mod_intercept = mod.params["const"]
        mod_predictor1_slope = mod.params[predictor1_name]
        mod_predictor2_slope = mod.params[predictor2_name]
        mod_interaction_slope = mod.params[predictor1_name +
                                           " * "+predictor2_name]

        # wireframe z values from the parameters from the regression model fit to the sample data
        sample_z = _np.exp(mod_intercept + mod_predictor1_slope*x + mod_predictor2_slope*y + mod_interaction_slope * x*y)/(
            1 + _np.exp(mod_intercept + mod_predictor1_slope*x + mod_predictor2_slope*y + mod_interaction_slope * x*y))

        # plot the sample regression surface and data
        ax2 = fig.add_subplot(122, projection="3d")
        ax2.plot_wireframe(x, y, sample_z, color="darkblue",
                           label="sample logistic regression surface", alpha=surface_alpha)
        ax2.scatter(sample_df[predictor1_name][sample_df[outcome_variable_name] >= 0.5],
                    sample_df[predictor2_name][sample_df[outcome_variable_name] >= 0.5],
                    sample_df[outcome_variable_name][sample_df[outcome_variable_name] >= 0.5],
                    color="blue", label=outcome_variable_name+" = 1 (sample)",
                    alpha=data_alpha)
        ax2.scatter(sample_df[predictor1_name][sample_df[outcome_variable_name] < 0.5],
                    sample_df[predictor2_name][sample_df[outcome_variable_name] < 0.5],
                    sample_df[outcome_variable_name][sample_df[outcome_variable_name] < 0.5],
                    color="blue", marker="x", label=outcome_variable_name+" = 0 (sample)",
                    alpha=data_alpha)
        ax2.set_zlabel(outcome_variable_name+"/ Probability")
        ax2.set_zticks([0, 1])
        ax2.set_title("Sample (n = "+str(sample_size)+") :")
        _plt.xlabel(predictor1_name)
        _plt.ylabel(predictor2_name)

        # set the view angle and elevation, if the user has supplied them
        _set_angles(ax2, view_angle=view_angle, view_elevation=view_elevation)

        fig.legend(loc=legend_loc)

        # show the regression table and true regression equation, if set to be
        # displayed
        _show_table(mod, model_type, show_statsmodels, verbose, intercept,
                    predictor1_slope, predictor1_name, predictor2_slope,
                    predictor2_name, interaction_slope, outcome_variable_name)

        # show the plot
        _plt.show()