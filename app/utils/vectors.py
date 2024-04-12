import numpy as np
import matplotlib.pyplot as plt
import collections
import json
from typing import *
import pandas as pd  # For handling date-time conversion

class Vector:
    '''Vector Maths Class for statistical analysis, visualization, and basic machine learning.'''

    def __init__(self, label: int = 0, data_points: np.array = None, dates: List[str] = None):
        self.label = label
        self.v = np.array([])  # Initialize to empty array for operations
        self.x = np.array([])  # Dates as numerical values
        self.y = np.array([])  # Original data points, remains static
        self.n = 0
        self.dates = dates

        if data_points is not None:
            data_points = np.array(data_points)
            if dates is not None and len(dates) == len(data_points):
                valid_pairs = [(pd.to_datetime(date), dp) for date, dp in zip(dates, data_points) if pd.notnull(date) and pd.notnull(dp)]
                if valid_pairs:
                    dates, data_points = zip(*valid_pairs)
                    self.x = np.array([(date - dates[0]).days for date in dates])
                    self.y = np.array(data_points)
                    self.v = np.copy(self.y)  # Copy y to v for operations
                    self.n = len(self.y)
            elif data_points.ndim == 1:
                self.y = data_points[~np.isnan(data_points)]
                self.x = np.arange(len(self.y))
                self.v = np.copy(self.y)  # Copy y to v for operations
                self.n = len(self.y)
            else:
                raise ValueError("Invalid data_points shape or mismatch with dates.")
   
    def pearson_correlation(self) -> float:
        '''Calculates the Pearson correlation coefficient between x and y.'''
        if self.y is None:
            raise ValueError("Y data points are required for correlation calculation.")
        correlation_matrix = np.corrcoef(self.x, self.y)
        return correlation_matrix[0, 1]

    def normalize_data(self):
        '''Normalizes the data points to a range between 0 and 1.'''
        self.v = (self.v - np.min(self.v)) / (np.max(self.v) - np.min(self.v))
        return self.v
    def standardize_data(self):
        '''Standardizes the data points to have mean 0 and standard deviation 1.'''
        self.v = (self.v - np.mean(self.v)) / np.std(self.v)
        return self.v
    def split_data(self, test_size: float = 0.2) -> Tuple[np.array, np.array, np.array, np.array]:
        '''Splits the data into training and testing sets.'''
        if self.v is None:
            raise ValueError("V data points are required for data splitting.")
        split_index = int(self.n * (1 - test_size))
        return self.x[:split_index], self.x[split_index:], self.v[:split_index], self.v[split_index:]

    def save_to_file(self, filename: str):
        '''Saves the Vector instance to a file.'''
        with open(filename, 'w') as f:
            json.dump({'label': self.label, 'data_points': self.v.tolist()}, f)

    def count(self, array: np.array, value: float) -> int:
        '''Returns count of value in an array.'''
        return len(array[array == value])

    def linear_scale(self):
        histo_gram = collections.Counter(self.v)
        val, cnt = zip(*histo_gram.items())

        n = len(cnt)
        prob_vector = [x / n for x in cnt]
        plt.plot(val, prob_vector, 'x')
        plt.show()

    def log_binning(self) -> Tuple[float, float]:
        """Plot the degree distribution with log binning."""
        histo_gram = collections.Counter(self.v)
        val, cnt = zip(*histo_gram.items())

        n = len(cnt)
        prob_vector = [x / n for x in cnt]
        in_max, in_min = max(prob_vector), min(prob_vector)
        log_bins = np.logspace(np.log10(in_min), np.log10(in_max))
        deg_hist, log_bin_edges = np.histogram(
            prob_vector, bins=log_bins, density=True, range=(in_min, in_max))
        plt.title(f"Log Binning & Scaling")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel('K')
        plt.ylabel('P(K)')
        plt.plot(deg_hist, log_bin_edges[:-1], 'o')
        plt.show()
        return in_min, in_max

    def get_prob_vector(self, axis: int = 0, rounding: int = None) -> Dict[float, float]:
        '''Return probability vector for a given axis.'''
        if axis == 0:
            vector = self.y
    

        if rounding is not None:
            vector = np.round(vector, rounding)

        unique_values = np.unique(vector)
        prob_dict = {value: self.count(
            vector, value) / self.n for value in unique_values}
        return prob_dict

    def plot_pdf(self, bins: int = 'auto'):
        '''Plots the Probability Density Function (PDF) of the vector.'''
        if self.y is not None:
            data = self.y
        else:
            data = self.x

        density, bins, _ = plt.hist(
            data, bins=bins, density=True, alpha=0.5, label='PDF')
        plt.ylabel('Probability')
        plt.xlabel('Data')
        plt.title('Probability Density Function')
        plt.legend()
        plt.show()

    def plot_basic_stats(self):
        '''Plots basic statistics: mean and standard deviation.'''
        if self.y is not None:
            data = self.y
        else:
            data = self.x

        mean = np.mean(data)
        std = np.std(data)

        plt.hist(data, bins='auto', alpha=0.5, label='Data')
        plt.axvline(mean, color='r', linestyle='dashed',
                    linewidth=1, label=f'Mean: {mean:.2f}')
        plt.axvline(mean + std, color='g', linestyle='dashed',
                    linewidth=1, label=f'Std: {std:.2f}')
        plt.axvline(mean - std, color='g', linestyle='dashed', linewidth=1)
        plt.legend()
        plt.show()

    def value_over_time(self):
        plt.plot(self.dates, self.y)
        plt.xlabel('Timestamp')
        plt.ylabel(self.label)
        plt.title(f'{self.label} over Timestamp')
        plt.show()

    def rolling_average(self, window_size: int = 3) -> np.array:
        '''Calculates and returns the rolling average of the vector using numpy.'''
        if self.y is not None:
            data = self.y
        else:
            data = self.x

        ra = [ sum( data[x:window_size+x]) / len(data[x:window_size+x]) for x in range(len(data))]
        return ra
    
    def simple_linear_regression(self):
        '''Performs simple linear regression on x and y data points and plots the result.'''
        if self.y is None:
            raise ValueError("Y data points are required for linear regression.")

        # Calculate the slope (m) and intercept (b) of the regression line
        n = len(self.x)
        sum_x = np.sum(self.x)
        sum_y = np.sum(self.y)
        sum_xy = np.sum(self.x * self.y)
        sum_x2 = np.sum(self.x ** 2)

        m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        b = (sum_y - m * sum_x) / n

        # Plot the data points
        plt.scatter(self.x, self.y, color='blue', label='Data points')

        # Calculate the regression line values
        regression_line = m * self.x + b

        # Plot the regression line
        plt.plot(self.x, regression_line, color='red', label=f'Regression Line: y = {m:.2f}x + {b:.2f}')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Linear Regression')
        plt.legend()
        plt.show()

        return m, b
    
    @staticmethod
    def load_from_file(filename: str) -> 'Vector':
        '''Loads a Vector instance from a file.'''
        with open(filename, 'r') as f:
            data = json.load(f)
        return Vector(label=data['label'], data_points=np.array(data['data_points']))

    @staticmethod
    def knn_classification(test_point: np.array, data_points: List['Vector'], k: int = 3) -> int:
        '''Performs k-Nearest Neighbors classification.'''
        distances = []

        # Calculate Euclidean distance from the test point to all other points
        for point in data_points:
            distance = np.linalg.norm(test_point - point.v)
            distances.append((point, distance))

        # Sort by distance and select the k-nearest neighbors
        distances.sort(key=lambda x: x[1])
        k_nearest = distances[:k]

        # Perform a majority vote among the k-nearest neighbors
        votes = collections.Counter([point[0].label for point in k_nearest])
        majority_vote = votes.most_common(1)[0][0]

        return majority_vote

    @staticmethod
    def calculate_aligned_entropy(vector1, vector2) -> float:
        """
        Calculates the entropy between two aligned probability distributions from Vector instances.
        """

        # Create probability distributions with zeros for missing values in each vector
        prob_dist1 = np.array(list(vector1.get_prob_vector().values()))
        prob_dist2 = np.array(list(vector2.get_prob_vector().values()))

        # Ensure the probability distributions are normalized
        # prob_dist1 = prob_dist1 / np.sum(prob_dist1)
        # prob_dist2 = prob_dist2 / np.sum(prob_dist2)
        # Calculate joint probabilities
        joint_probs = prob_dist1 * prob_dist2

        # Filter out zero probabilities to avoid NaNs in the logarithm
        joint_probs = joint_probs[joint_probs != 0]

        # Calculate entropy
        entropy = -np.sum(joint_probs * np.log2(joint_probs))

        # Calculate the entropy
        return entropy

    @staticmethod
    def set_operations(v1: 'Vector', v2: 'Vector') -> Tuple[Set[float], Set[float], float]:
        '''Performs set operations: union, intersection, and calculates Jaccard index.'''
        set1 = set(v1.x)
        set2 = set(v2.y)

        union = set1.union(set2)
        intersection = set1.intersection(set2)
        jaccard_index = len(intersection) / len(union)

        return union, intersection, jaccard_index

    @staticmethod
    def generate_noisy_sin(start: float = 0, points: int = 100) -> Tuple[np.array, np.array]:
        '''Creates a noisy sine wave for testing.'''
        x = np.linspace(start, 2 * np.pi, points)
        y = np.sin(x) + np.random.normal(0, 0.2, points)
        return np.column_stack((x, y))
    


if __name__ == "__main__":
    # Set parameters
    mean = 50
    std_dev = 10
    sample_size = 2000

    # Generate the sample list
    s1 = np.round(np.random.normal(mean, std_dev, sample_size), 2)
    s2 = np.round(np.random.normal(mean, std_dev, sample_size), 2)

    v1 = Vector('1', s1)
    v2 = Vector('2', s2)
    v1.linear_scale()
    v1.log_binning()
