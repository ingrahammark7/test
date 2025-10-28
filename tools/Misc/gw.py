# Semi-empirical penetration (de Marre style) + calibration template
# Drop into your toolchain. Python 3, requires numpy and sklearn (or use numpy only).
import numpy as np
from sklearn.linear_model import LinearRegression

def de_marre_predict(mass, velocity, diameter, params=None):
    """
    Predict penetration (P, in meters) using a log-linear "de Marre" style law:
      log P = a0 + a1*log(m) + a2*log(v) + a3*log(d)
    mass [kg], velocity [m/s], diameter [m]
    params: dict with 'a0','a1','a2','a3' (if None, uses example defaults)
    Returns P in meters.
    """
    if params is None:
        # Example initial guesses (you should fit these to a naval dataset)
        params = {'a0': -2.0, 'a1': 0.4, 'a2': 1.1, 'a3': -0.8}
    a0,a1,a2,a3 = params['a0'], params['a1'], params['a2'], params['a3']
    logP = a0 + a1*np.log(mass) + a2*np.log(velocity) + a3*np.log(diameter)
    return np.exp(logP)

def fit_de_marre(X, P_obs):
    """
    Fit the log-linear model to data.
    X: Nx3 array with columns [mass, velocity, diameter]
    P_obs: Nx1 observed penetration (meters)
    Returns params dict and sklearn reg object.
    """
    # transform to logs
    Xlog = np.log(X)
    ylog = np.log(P_obs)
    reg = LinearRegression(fit_intercept=True).fit(Xlog, ylog)
    a0 = reg.intercept_
    a1,a2,a3 = reg.coef_
    params = {'a0': float(a0), 'a1': float(a1), 'a2': float(a2), 'a3': float(a3)}
    return params, reg

# Example usage:
if __name__ == "__main__":
    # example dataset (replace with naval test data or paired Tate->observed penetration)
    # columns: mass (kg), velocity (m/s), diameter (m)
    X_example = np.array([
        [204.0, 1500.0, 0.176],   # your 44cm x 17.6cm example (mass from DU)
        [28.0, 1500.0, 0.03],     # slender APFSDS example
        [50.0, 1200.0, 0.05],     # example
        [300.0, 1000.0, 0.2],     # hypothetical
    ])
    # observed penetrations (m) — **replace** these with trusted naval test values
    P_obs = np.array([1.07, 2.0, 1.5, 1.8])  # placeholder values

    params, reg = fit_de_marre(X_example, P_obs)
    print("Fitted params:", params)
    # Predict for your round
    m,v,d = 204.0, 1500.0, 0.176
    P_pred = de_marre_predict(m, v, d, params=params)
    print("Predicted penetration (m):", P_pred)