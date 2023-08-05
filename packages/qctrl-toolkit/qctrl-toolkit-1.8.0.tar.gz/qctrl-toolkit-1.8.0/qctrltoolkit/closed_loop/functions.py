# Copyright 2022 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

"""
Utilities for the closed-loop optimizer.
"""

from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Dict,
    Optional,
)

import numpy as np
from qctrlcommons.preconditions import (
    check_argument,
    check_argument_integer,
    check_argument_non_negative_scalar,
)

from qctrltoolkit.namespace import Namespace
from qctrltoolkit.toolkit_utils import expose


@expose(Namespace.CLOSED_LOOP)
class Optimizer(ABC):
    """
    Abstract class for optimizers used in closed-loop control.

    To create an optimizer, use one of the concrete classes in the closed-loop optimization
    toolkit. For example to create a cross entropy optimizer with an elite fraction of 0.1
    `optimizer=qctrl.closed_loop.CrossEntropy(elite_fraction=0.1)`.
    """

    method_name: str

    @abstractmethod
    def create_optimizer(self, qctrl, bounds):
        """
        Return the initialized optimizer.

        Parameters
        ----------
        qctrl : qctrl.Qctrl
            Boulder Opal session object.
        bounds : np.ndarray
            The per-parameter bounds on the test points.
            The bounds must be a NumPy array of shape ``(parameter count, 2)`` where the
            trailing axis are the bounds for each parameter (with the lower bound first, followed
            by the upper bound).
        """
        raise NotImplementedError


@expose(Namespace.CLOSED_LOOP)
@dataclass
class Cmaes(Optimizer):
    """
    The covariance matrix adaptation evolution strategy (CMA-ES) optimizer.

    Parameters
    ----------
    initial_mean : np.ndarray, optional
        The array of the initial means of the parameters for the multivariate normal
        distribution.
        Defaults to an array of ones.
    initial_step_size : float, optional
        The initial step size for the multivariate normal distribution from which new test
        points are sampled.
        Defaults to one.
    initial_covariance : np.ndarray, optional
        The initial covariance matrix between the different parameters
        for the multivariate normal distribution, as a 2D square array.
        Defaults to the identity matrix.
    seed : int, optional
        Seed for the random number generator.
        Use this option to generate deterministic results from the optimizer.
    """

    initial_mean: Optional[np.ndarray] = None
    initial_step_size: Optional[float] = None
    initial_covariance: Optional[np.ndarray] = None
    seed: Optional[int] = None
    method_name = "CMA-ES"

    def __post_init__(self):
        if self.initial_mean is not None:
            check_argument(
                isinstance(self.initial_mean, np.ndarray)
                and self.initial_mean.ndim == 1,
                "The initial mean must be a 1D np.ndarray.",
                {"initial_mean": self.initial_mean},
            )
        if self.initial_covariance is not None:
            check_argument(
                isinstance(self.initial_covariance, np.ndarray)
                and self.initial_covariance.ndim == 2
                and self.initial_covariance.shape[0]
                == self.initial_covariance.shape[1],
                "The initial covariance must be a 2D square np.ndarray.",
                {"initial_covariance": self.initial_covariance},
            )

        if self.initial_mean is not None and self.initial_covariance is not None:
            check_argument(
                len(self.initial_mean) == len(self.initial_covariance),
                "The initial mean and initial covariance must have the same dimension.",
                {
                    "initial_mean": self.initial_mean,
                    "initial_covariance": self.initial_covariance,
                },
            )

        if self.seed is not None:
            check_argument_integer(self.seed, "seed")

    def create_optimizer(self, qctrl: Any, bounds: np.ndarray):
        _check_bounds(bounds)

        if self.initial_mean is not None:
            check_argument(
                len(self.initial_mean) == len(bounds),
                "The initial mean and the bounds must have the same length.",
                {"initial_mean": self.initial_mean, "bounds": bounds},
            )

        if self.initial_covariance is not None:
            check_argument(
                len(self.initial_covariance) == len(bounds),
                "The initial covariance and the bounds must have the same dimension.",
                {"initial_covariance": self.initial_covariance, "bounds": bounds},
            )

        def convert_to_list(array):
            if array is None:
                return None
            return array.tolist()

        initializer = qctrl.types.closed_loop_optimization_step.CmaesInitializer(
            bounds=_convert_bounds(qctrl, bounds),
            initial_mean=convert_to_list(self.initial_mean),
            initial_step_size=self.initial_step_size,
            initial_covariance=convert_to_list(self.initial_covariance),
            rng_seed=self.seed,
        )
        return qctrl.types.closed_loop_optimization_step.Optimizer(
            cmaes_initializer=initializer
        )


@expose(Namespace.CLOSED_LOOP)
@dataclass
class CrossEntropy(Optimizer):
    """
    The cross entropy optimizer.

    Parameters
    ----------
    elite_fraction : float
        The top fraction of test points that the algorithm uses to generate the next distribution.
        Must be between 0 and 1.
    seed : int, optional
        Seed for the random number generator.
        Use this option to generate deterministic results from the optimizer.
    """

    elite_fraction: float
    seed: Optional[int] = None
    method_name = "cross entropy"

    def __post_init__(self):
        check_argument(
            0.0 < self.elite_fraction < 1.0,
            "The elite fraction must be between 0 and 1.",
            {"elite_fraction": self.elite_fraction},
        )

        if self.seed is not None:
            check_argument_integer(self.seed, "seed")

    def create_optimizer(self, qctrl: Any, bounds: np.ndarray):
        _check_bounds(bounds)

        initializer = qctrl.types.closed_loop_optimization_step.CrossEntropyInitializer(
            bounds=_convert_bounds(qctrl, bounds),
            elite_fraction=self.elite_fraction,
            rng_seed=self.seed,
        )
        return qctrl.types.closed_loop_optimization_step.Optimizer(
            cross_entropy_initializer=initializer
        )


@expose(Namespace.CLOSED_LOOP)
@dataclass
class GaussianProcess(Optimizer):
    """
    The Gaussian process optimizer.

    Parameters
    ----------
    length_scale_bounds : np.ndarray, optional
        The per-parameter length scale bounds on the test points.
        The bounds must be a NumPy array of shape ``(parameter count, 2)`` where the trailing
        axis are the bounds for each parameter (with the lower bound first, followed by the upper
        bound).
    seed : int, optional
        Seed for the random number generator.
        Use this option to generate deterministic results from the optimizer.
    """

    length_scale_bounds: Optional[np.ndarray] = None
    seed: Optional[int] = None
    method_name = "Gaussian process"

    def __post_init__(self):
        if self.length_scale_bounds is not None:
            _check_bounds(self.length_scale_bounds, "length scale bounds")

        if self.seed is not None:
            check_argument_integer(self.seed, "seed")

    def create_optimizer(self, qctrl: Any, bounds: np.ndarray):
        _check_bounds(bounds)

        if self.length_scale_bounds is not None:
            check_argument(
                len(self.length_scale_bounds) == len(bounds),
                "The length scale bounds and the bounds must have the same length.",
                {"length_scale_bounds": self.length_scale_bounds, "bounds": bounds},
            )

        initializer = (
            qctrl.types.closed_loop_optimization_step.GaussianProcessInitializer(
                bounds=_convert_bounds(qctrl, bounds),
                length_scale_bounds=_convert_bounds(qctrl, self.length_scale_bounds),
                rng_seed=self.seed,
            )
        )
        return qctrl.types.closed_loop_optimization_step.Optimizer(
            gaussian_process_initializer=initializer
        )


@expose(Namespace.CLOSED_LOOP)
@dataclass
class NeuralNetwork(Optimizer):
    """
    The neural network optimizer.

    Parameters
    ----------
    seed : int, optional
        Seed for the random number generator.
        Use this option to generate deterministic results from the optimizer.
    """

    seed: Optional[int] = None
    method_name = "neural network"

    def __post_init__(self):
        if self.seed is not None:
            check_argument_integer(self.seed, "seed")

    def create_optimizer(self, qctrl: Any, bounds: np.ndarray):
        _check_bounds(bounds)

        initializer = (
            qctrl.types.closed_loop_optimization_step.NeuralNetworkInitializer(
                bounds=_convert_bounds(qctrl, bounds),
                rng_seed=self.seed,
            )
        )
        return qctrl.types.closed_loop_optimization_step.Optimizer(
            neural_network_initializer=initializer
        )


@expose(Namespace.CLOSED_LOOP)
@dataclass
class SimulatedAnnealing(Optimizer):
    r"""
    The simulated annealing optimizer.

    Parameters
    ----------
    temperatures : np.ndarray
        The array of initial per-parameter annealing temperatures :math:`T_0` used to generate
        new test points.
        Higher temperatures correspond to higher exploration.
        The per-parameter adjustments from the current test point are sampled from Cauchy
        distributions with scales given by temperatures.
        The temperatures are currently implemented to decay such that each temperature
        at the k-th step is set according to :math:`T_k=\frac{T_0}{1+k}`.
        All temperatures must be positive.
    temperature_cost : float
        The parameter for controlling the optimizer’s greediness.
        A high cost temperature allows the optimizer to explore test points which may not
        immediately improve the cost. A higher level of exploration can be helpful for
        more difficult optimization problems. The cost temperature is set to decay
        according to the same schedule as the temperatures.
        Must be positive.
    seed : int, optional
        Seed for the random number generator.
        Use this option to generate deterministic results from the optimizer.
    """

    temperatures: np.ndarray
    temperature_cost: float
    seed: Optional[int] = None
    method_name = "simulated annealing"

    def __post_init__(self):
        check_argument(
            all(self.temperatures > 0),
            "All parameter temperatures must be positive.",
            {"temperatures": self.temperatures},
        )

        check_argument(
            self.temperature_cost > 0,
            "The cost temperature must be positive.",
            {"temperature_cost": self.temperature_cost},
        )

        if self.seed is not None:
            check_argument_integer(self.seed, "seed")

    def create_optimizer(self, qctrl: Any, bounds: np.ndarray):
        _check_bounds(bounds)

        check_argument(
            len(self.temperatures) == len(bounds),
            "The temperatures and the bounds must have the same length.",
            {"temperatures": self.temperatures, "bounds": bounds},
        )

        initializer = (
            qctrl.types.closed_loop_optimization_step.SimulatedAnnealingInitializer(
                bounds=_convert_bounds(qctrl, bounds),
                temperatures=list(self.temperatures),
                temperature_cost=self.temperature_cost,
                rng_seed=self.seed,
            )
        )
        return qctrl.types.closed_loop_optimization_step.Optimizer(
            simulated_annealing_initializer=initializer
        )


def _convert_bounds(qctrl, bounds):
    """
    Convert bounds to box constraints, if the bounds are passed as a NumPy array.
    If the bounds are not a NumPy array None is returned.
    """
    if isinstance(bounds, np.ndarray):
        return [
            qctrl.types.closed_loop_optimization_step.BoxConstraint(
                lower_bound=bound[0], upper_bound=bound[1]
            )
            for bound in bounds
        ]
    return None


def _check_bounds(bounds: np.ndarray, name: str = "bounds"):
    """Check that the bounds are well-defined."""
    check_argument(
        isinstance(bounds, np.ndarray) and bounds.ndim == 2 and bounds.shape[1] == 2,
        f"The {name} must be a 2D np.ndarray with two components in the second axis.",
        {name: bounds},
    )
    check_argument(
        all(bounds[:, 1] > bounds[:, 0]),
        "The upper bound (second component) must be greater than the lower bound "
        f"(first component) for each element in the {name} array.",
        {name: bounds},
    )


@expose(Namespace.CLOSED_LOOP)
def optimize(
    qctrl: Any,
    cost_function: Callable,
    initial_test_parameters: np.ndarray,
    optimizer: Optimizer,
    bounds: np.ndarray,
    cost_uncertainty: Optional[float] = None,
    target_cost: Optional[float] = None,
    max_iteration_count: int = 100,
    callback: Optional[Callable] = None,
    verbose: bool = True,
) -> Dict:
    """
    Run a closed-loop optimization to find a minimum of the given cost function.

    This is an iterative process, where the optimizer generates and tests a set of points.
    After several iterations the distribution of generated test points should converge
    to low values of the cost function. You can use this approach when your system is too
    complicated to model, or the computation of gradient is expensive or impossible.

    Parameters
    ----------
    qctrl : qctrl.Qctrl
        Boulder Opal session object.
    cost_function : Callable
        A function that takes the parameters as an argument and returns an array of costs values.
        The function should take a NumPy array of input parameters with shape
        ``(test point count, parameter count)`` and return the costs in a 1D array of length test
        point count.
    initial_test_parameters : np.ndarray
        The initial values of the parameters to use in the optimization.
        A 2D NumPy array of shape ``(test point count, parameter count)``.
    optimizer : ~closed_loop.Optimizer
        The optimizer to be used in the minimization of the cost function.
    bounds : np.ndarray
        The per-parameter bounds on the test points.
        The bounds must be a NumPy array of shape ``(parameter count, 2)`` where the trailing
        axis are the bounds for each parameter (with the lower bound first, followed by the upper
        bound).
    cost_uncertainty : float, optional
        The standard deviation in the value of the cost.
        Must be non-negative.
    target_cost : float, optional
        The target cost, if the best cost is below this the optimization is halted.
    max_iteration_count : int, optional
        The maximum number of iterations.
        Defaults to 100.
    callback : Callable, optional
        A function that takes in the current set of parameters, a 2D NumPy array of shape
        ``(test point count, parameter count)``, and returns a bool.
        The function is evaluated once during each iteration with the
        current parameters. If it returns True, the optimization is halted.
    verbose : bool, optional
        Whether to print out information about the optimization cycle.
        Defaults to True.

    Returns
    -------
    dict
        A dictionary containing the results of the optimization, namely, the best parameters
        `best_parameters`, their associated cost `best_cost`, and
        the history of best cost values `best_cost_history`.
    """

    def verbose_print(message):
        if verbose:
            print(message)

    check_argument(
        isinstance(initial_test_parameters, np.ndarray)
        and np.ndim(initial_test_parameters) == 2,
        "The initial test parameters must be a 2D np.ndarray.",
        {"initial_test_parameters": initial_test_parameters},
    )

    if cost_uncertainty is not None:
        check_argument_non_negative_scalar(cost_uncertainty, "cost uncertainty")

    verbose_print(
        f"""Running closed loop optimization
----------------------------------------
  Optimizer            : {optimizer.method_name}
  Number of test points: {initial_test_parameters.shape[0]}
  Number of parameters : {initial_test_parameters.shape[1]}
----------------------------------------
"""
    )

    closed_loop_optimizer = optimizer.create_optimizer(qctrl, bounds)

    test_parameters = initial_test_parameters

    # Obtain initial costs.
    verbose_print("Calling cost function…")
    costs = cost_function(test_parameters)

    best_cost_overall, best_parameters_overall = min(
        zip(costs, test_parameters), key=lambda params: params[0]
    )
    verbose_print(f"  Initial best cost: {best_cost_overall:.3f}")

    # Store the cost history.
    best_cost_history = [best_cost_overall]

    # Run the optimization loop until a halting condition is met.
    for iteration_count in range(max_iteration_count):
        # Organize the costs into the proper input format.
        results = [
            qctrl.types.closed_loop_optimization_step.CostFunctionResult(
                parameters=parameters, cost=cost, cost_uncertainty=cost_uncertainty
            )
            for parameters, cost in zip(test_parameters, costs)
        ]

        # Call the automated closed-loop optimizer and obtain the next set of test points.
        verbose_print("\nRunning optimizer…")
        optimization_result = qctrl.functions.calculate_closed_loop_optimization_step(
            optimizer=closed_loop_optimizer,
            results=results,
            test_point_count=test_parameters.shape[0],
        )

        # Retrieve the optimizer state and create a new optimizer object.
        closed_loop_optimizer = qctrl.types.closed_loop_optimization_step.Optimizer(
            state=optimization_result.state
        )

        # Organize the data returned by the automated closed-loop optimizer.
        test_parameters = np.array(
            [test_point.parameters for test_point in optimization_result.test_points]
        )

        # Obtain costs.
        verbose_print("Calling cost function…")
        costs = cost_function(test_parameters)

        # Record the best results after this round.
        best_cost, best_parameters = min(
            zip(costs, test_parameters), key=lambda params: params[0]
        )

        # Compare last best results with best result overall.
        if best_cost < best_cost_overall:
            best_cost_overall = best_cost
            best_parameters_overall = best_parameters

        # Print the current best cost.
        verbose_print(
            f"  Best cost after {iteration_count+1} iterations: {best_cost_overall:.3f}"
        )

        # Store the current best cost.
        best_cost_history.append(best_cost_overall)

        if callback is not None:
            if callback(test_parameters):
                verbose_print(
                    "\nCallback condition satisfied. Stopping the optimization."
                )
                break

        # Check if desired threshold has been achieved.
        if target_cost is not None:
            if best_cost_overall < target_cost:
                verbose_print("\nTarget cost reached. Stopping the optimization.")
                break

    else:
        verbose_print("\nMaximum iteration count reached. Stopping the optimization.")

    return {
        "best_cost": best_cost_overall,
        "best_parameters": best_parameters_overall,
        "best_cost_history": best_cost_history,
    }
