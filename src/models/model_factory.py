"""
Unified Model Factory for Shortlisted Architectures (Subheading 2.c Audit Enhancement).
Provides a single interface to instantiate any shortlisted model with standardized capacity constraints and pre-configured preprocessing pipelines.
"""

from typing import Any, Dict, Optional
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C, Matern, WhiteKernel
from sklearn.svm import SVR

from src.models.model_selector import get_shortlisted_architectures


def instantiate_candidate_model(name: str, random_state: int = 42, **kwargs) -> Any:
    """
    Instantiates a shortlisted model with pre-configured small-N hyperparameters and scaling.
    """
    shortlisted = get_shortlisted_architectures()
    if name not in shortlisted:
        raise ValueError(f"Model '{name}' is not in shortlisted architectures: {shortlisted}")
        
    if name == "Ridge_Regression":
        alpha = kwargs.get("alpha", 1.0)
        return Pipeline([
            ("scaler", StandardScaler()),
            ("regressor", Ridge(alpha=alpha, random_state=random_state))
        ])
    elif name == "ElasticNet":
        alpha = kwargs.get("alpha", 0.1)
        l1_ratio = kwargs.get("l1_ratio", 0.5)
        return Pipeline([
            ("scaler", StandardScaler()),
            ("regressor", ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=random_state, max_iter=2000))
        ])
    elif name == "Random_Forest":
        max_depth = kwargs.get("max_depth", 3)
        n_estimators = kwargs.get("n_estimators", 50)
        min_samples_split = kwargs.get("min_samples_split", 4)
        min_samples_leaf = kwargs.get("min_samples_leaf", 2)
        return RandomForestRegressor(
            max_depth=max_depth,
            n_estimators=n_estimators,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=random_state
        )
    elif name == "Gradient_Boosting":
        max_depth = kwargs.get("max_depth", 3)
        n_estimators = kwargs.get("n_estimators", 50)
        learning_rate = kwargs.get("learning_rate", 0.05)
        subsample = kwargs.get("subsample", 0.8)
        min_samples_leaf = kwargs.get("min_samples_leaf", 2)
        return GradientBoostingRegressor(
            max_depth=max_depth,
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            subsample=subsample,
            min_samples_leaf=min_samples_leaf,
            random_state=random_state
        )
    elif name == "Gaussian_Process_Matern":
        length_scale = kwargs.get("length_scale", kwargs.get("length_scale_init", 2.0))
        noise_level = kwargs.get("noise_level", kwargs.get("noise_level_init", 0.1))
        nu = kwargs.get("nu", 2.5)
        kernel = C(1.0, (1e-2, 1e2)) * Matern(length_scale=length_scale, nu=nu, length_scale_bounds=(1e-1, 50.0)) + WhiteKernel(noise_level=noise_level, noise_level_bounds=(1e-3, 1.0))
        return Pipeline([
            ("scaler", StandardScaler()),
            ("regressor", GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=5, random_state=random_state))
        ])
    elif name == "Support_Vector_Regression_RBF":
        C_param = kwargs.get("C", 5.0)
        epsilon = kwargs.get("epsilon", 0.1)
        gamma = kwargs.get("gamma", "scale")
        return Pipeline([
            ("scaler", StandardScaler()),
            ("regressor", SVR(kernel="rbf", C=C_param, epsilon=epsilon, gamma=gamma))
        ])
    else:
        raise ValueError(f"Unhandled shortlisted model: {name}")
