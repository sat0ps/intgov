# IntGov - Intent-Governed Kubernetes Infrastructure

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Kubernetes](https://img.shields.io/badge/kubernetes-1.24+-326CE5.svg)](https://kubernetes.io/)

A sophisticated Kubernetes-based intent-governed system that implements continuous auditing, drift detection, and automated remediation to maintain infrastructure compliance and desired state.

## Overview

IntGov bridges the gap between declarative infrastructure intent and runtime reality. By continuously monitoring Kubernetes clusters, it detects configuration drift, unauthorized changes, and policy violations, then automatically remediates them to maintain your desired infrastructure state.

### Key Features

- **Intent-Based Configuration**: Define your infrastructure's desired state through declarative intent specifications
- **Continuous Auditing**: Real-time monitoring of cluster state against defined policies
- **Drift Detection**: Automatically identifies deviations from intended configuration
- **Automated Remediation**: Self-healing capabilities to restore compliance
- **Policy Engine**: Flexible policy framework supporting custom rules and constraints
- **Multi-Cluster Support**: Manage and govern multiple Kubernetes clusters from a single control plane
- **Audit Trail**: Comprehensive logging of all changes and remediation actions
- **Integration Ready**: Webhook support for CI/CD pipelines and alerting systems

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        IntGov Controller                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Intent     │  │    Policy    │  │   Audit      │      │
│  │   Parser     │  │    Engine    │  │   Logger     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    Drift     │  │ Remediation  │  │   Webhook    │      │
│  │   Detector   │  │    Engine    │  │   Handler    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │   Kubernetes API      │
            └───────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
    ┌────────┐     ┌────────┐     ┌────────┐
    │Cluster1│     │Cluster2│     │ClusterN│
    └────────┘     └────────┘     └────────┘
```

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Kubernetes cluster (1.24+)
- kubectl configured with cluster access
- Helm 3 (optional, for Helm-based deployment)

### Installation

#### Option 1: Direct Deployment

```bash
# Clone the repository
git clone https://github.com/sat0ps/intgov.git
cd intgov

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure your intent specifications
cp config/intent.example.yaml config/intent.yaml
# Edit config/intent.yaml with your desired state

# Deploy to Kubernetes
kubectl apply -f k8s/deployment.yaml
```

#### Option 2: Helm Deployment

```bash
# Add the IntGov Helm repository
helm repo add intgov https://sat0ps.github.io/intgov-helm
helm repo update

# Install IntGov
helm install intgov intgov/intgov \
  --namespace intgov-system \
  --create-namespace \
  --values custom-values.yaml
```

### Configuration

Create an intent specification file defining your desired infrastructure state:

```yaml
# config/intent.yaml
apiVersion: intgov.io/v1
kind: Intent
metadata:
  name: production-cluster-intent
spec:
  clusters:
    - name: prod-cluster
      policies:
        - name: namespace-protection
          type: immutability
          resources:
            - namespaces: [kube-system, default]
          action: prevent-delete

        - name: resource-limits
          type: constraint
          resources:
            - kind: Pod
              namespaces: [production]
          requirements:
            - resources.requests.memory: required
            - resources.limits.memory: required

      drift:
        detection_interval: 60s
        remediation: auto
        notify_on_drift: true
```

## Usage

### Basic Operations

```bash
# Check system status
intgov status

# Validate intent configuration
intgov validate -f config/intent.yaml

# Apply intent to cluster
intgov apply -f config/intent.yaml

# Monitor drift detection
intgov drift watch

# View audit logs
intgov audit logs --since 1h

# Generate compliance report
intgov report --format pdf --output compliance-report.pdf
```

### Advanced Features

#### Custom Policy Definition

```python
# policies/custom_policy.py
from intgov.policy import BasePolicy

class CustomSecurityPolicy(BasePolicy):
    def evaluate(self, resource):
        """
        Evaluate resource against security requirements
        """
        if resource.kind == "Pod":
            # Check for security context
            if not resource.spec.security_context:
                return self.violation(
                    "Pod must define securityContext"
                )
        return self.compliant()
```

#### Webhook Integration

```bash
# Configure webhook for Slack notifications
intgov webhook add \
  --name slack-notifications \
  --url https://hooks.slack.com/services/YOUR/WEBHOOK/URL \
  --events drift_detected,remediation_failed
```

## Use Cases

### 1. Configuration Drift Prevention
Prevent unauthorized changes to critical infrastructure components by continuously monitoring and reverting unintended modifications.

### 2. Compliance Automation
Ensure clusters remain compliant with security policies, industry standards (PCI-DSS, HIPAA, SOC2), and organizational requirements.

### 3. Multi-Environment Consistency
Maintain consistent configurations across development, staging, and production environments.

### 4. Disaster Recovery
Quickly restore cluster state to known-good configuration after incidents or attacks.

## Development

### Project Structure

```
intgov/
├── src/
│   ├── intgov/
│   │   ├── controllers/      # Main controller logic
│   │   ├── policies/         # Policy engine and rules
│   │   ├── detectors/        # Drift detection algorithms
│   │   ├── remediation/      # Automated remediation
│   │   ├── audit/            # Audit logging system
│   │   └── webhooks/         # Webhook handlers
├── config/                   # Configuration files
├── k8s/                      # Kubernetes manifests
├── tests/                    # Test suites
├── docs/                     # Documentation
└── examples/                 # Example configurations
```

### Running Tests

```bash
# Unit tests
pytest tests/unit

# Integration tests (requires test cluster)
pytest tests/integration

# Coverage report
pytest --cov=intgov --cov-report=html
```

### Building from Source

```bash
# Build Python package
python -m build

# Build Docker image
docker build -t intgov:latest .

# Run locally
docker run -v ~/.kube:/root/.kube intgov:latest
```

## Roadmap

- [ ] Support for custom resource definitions (CRDs)
- [ ] Machine learning-based anomaly detection
- [ ] GitOps integration with ArgoCD/Flux
- [ ] Multi-cloud support (EKS, GKE, AKS)
- [ ] Advanced RBAC policy management
- [ ] Cost optimization recommendations
- [ ] Terraform state synchronization
- [ ] Web-based dashboard and UI
- [ ] Policy marketplace and sharing

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/intgov.git
cd intgov

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run linting
ruff check .

# Format code
black .
```

## Security

IntGov handles sensitive cluster access credentials and configurations. Please review our [Security Policy](SECURITY.md) for best practices and vulnerability reporting.

### Security Features

- RBAC-based access control
- Encrypted secret management
- Audit logging of all operations
- Support for Pod Security Standards
- Integration with OPA (Open Policy Agent)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by Kubernetes Operators and GitOps principles
- Built on top of the Kubernetes Python client
- Policy engine inspired by OPA and Kyverno

## Contact & Support

- **Author**: Satyam Priyam
- **GitHub**: [@sat0ps](https://github.com/sat0ps)
- **Issues**: [GitHub Issues](https://github.com/sat0ps/intgov/issues)

---

**Note**: This project is under active development. APIs and features may change. For production use, please pin to specific versions and thoroughly test in non-production environments first.
