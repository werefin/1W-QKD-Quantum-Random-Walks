import os
import subprocess
import json
import numpy as np
from noise_models import Noise_Models
from qkd_protocol import QKD_Protocol

# Fixed parameters
num_iterations = 10000
F = 'I'
coin_type = 'generic_rotation'
phi = 0
theta = np.pi / 4

# Initialize noise models
noise_models = Noise_Models()
# Parameter for generalized Pauli noise (single qubit)
p_1q = 0.333 # approximately uniform in X, Y, Z bit flips

# Store results in a dictionary
results = []

# Clone the private repository
GITHUB_USERNAME = "Werefin"
GITHUB_PAT = "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"
REPO_NAME = "1W-QKD-Quantum-Random-Walks"
REPO_URL = f"https://{GITHUB_USERNAME}:{GITHUB_PAT}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

# Clone the repository (if not already cloned)
repo_dir = REPO_NAME + "/results/"
if not os.path.exists(repo_dir):
    print("Cloning private repository...")
    subprocess.run(["git", "clone", REPO_URL], check=True)
    print("Repository cloned successfully!")
else:
    print("Repository already cloned...")

# Access JSON files
circle_json_path = os.path.join(repo_dir, "c_qrw_circle_results.json")
hypercube_json_path = os.path.join(repo_dir, "c_qrw_hypercube_results.json")

# Ensure both files exist
if not os.path.exists(circle_json_path):
    raise FileNotFoundError(f"Circle JSON file not found at {circle_json_path}")
if not os.path.exists(hypercube_json_path):
    raise FileNotFoundError(f"Hypercube JSON file not found at {hypercube_json_path}")

# Load parameters from JSON files
with open(circle_json_path, 'r') as circle_file:
    circle_parameters = json.load(circle_file)
with open(hypercube_json_path, 'r') as hypercube_file:
    hypercube_parameters = json.load(hypercube_file)

# Process circle parameters
print("Processing QKD protocol with QRW circle parameters...")
for entry in circle_parameters:
    P = entry['P']
    optimal_t = entry['optimal_t']
    print(f"Starting simulation for QRW circle: P={P}, optimal_t={optimal_t}")
    noise_model = noise_models.create_generalized_pauli_noise(P=P, error_rate=p_1q, qrw_type='circle')
    protocol = QKD_Protocol(num_iterations=num_iterations, P=P, t=optimal_t, F=F, coin_type=coin_type, phi=phi, theta=theta, qrw_type='circle', noise_model=noise_model)
    result = protocol.run_protocol(noise_model=noise_model)
    print(f"Protocol results for P={P}, optimal_t={optimal_t}:")
    print(f"QER (Z-basis): {result['qer_z']:.6f}")
    print(f"QER (QW-basis): {result['qer_qw']:.6f}")
    results.append({'type': 'circle', 'n_iterations': num_iterations, 'P': P, 'F': F, 'coin_type': coin_type,
                    'phi': phi, 'theta': theta, 't': optimal_t, 'qer_z': result['qer_z'], 'qer_qw': result['qer_qw']})

# Process hypercube parameters
print("Processing QKD protocol with QRW hypercube parameters...")
for entry in hypercube_parameters:
    P = entry['P']
    optimal_t = entry['optimal_t']
    print(f"Starting simulation for QRW hypercube: P={P}, optimal_t={optimal_t}")
    noise_model = noise_models.create_generalized_pauli_noise(P=P, error_rate=p_1q, qrw_type='hypercube')
    protocol = QKD_Protocol(num_iterations=num_iterations, P=P, t=optimal_t, F=F, coin_type=coin_type, phi=phi, theta=theta, qrw_type='hypercube', noise_model=noise_model)
    result = protocol.run_protocol(noise_model=noise_model)
    print(f"Protocol results for P={P}, optimal_t={optimal_t}:")
    print(f"QER (Z-basis): {result['qer_z']:.6f}")
    print(f"QER (QW-basis): {result['qer_qw']:.6f}")
    results.append({'type': 'hypercube', 'n_iterations': num_iterations, 'P': P, 'F': F, 'coin_type': coin_type,
                    'phi': phi, 'theta': theta, 't': optimal_t, 'qer_z': result['qer_z'], 'qer_qw': result['qer_qw']})

# Save results to JSON file
results_file = os.path.join(repo_dir, '1w_qkd_simulation_results.json')
with open(results_file, 'w') as results_file_obj:
    json.dump(results, results_file_obj, indent=4)
