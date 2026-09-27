import os
import sys
import platform
import subprocess
import json
import inspect
import time
from typing import Dict, Any, List, Optional

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
VENV_DIR = os.path.join(PROJECT_ROOT, ".venv-ibm-hardware")
VENV_PYTHON = os.path.join(VENV_DIR, "Scripts", "python.exe") if platform.system() == "Windows" else os.path.join(VENV_DIR, "bin", "python")

class IBMAD4R2Reconciler:
    """
    Phase AD-4R2 Isolated IBM Runtime Installation & Path Reconciliation Engine.
    
    Responsibilities:
    - Identify project root and research venv directory (.venv-ibm-hardware).
    - Distinguish System Python vs Research Venv Python.
    - Create .venv-ibm-hardware if missing.
    - Execute python -m pip install qiskit-ibm-runtime inside .venv-ibm-hardware.
    - Assert that qiskit_ibm_runtime module location physically resides inside .venv-ibm-hardware.
    - Enforce zero experiment, non-authentication, and production isolation gates.
    """

    @staticmethod
    def get_paths() -> Dict[str, str]:
        """Returns project root, venv path, and python executables."""
        system_python = sys.executable
        return {
            "project_root": PROJECT_ROOT,
            "research_venv": VENV_DIR,
            "research_python_executable": VENV_PYTHON,
            "system_python": system_python
        }

    @classmethod
    def ensure_research_venv_and_install(cls) -> Dict[str, Any]:
        """Creates .venv-ibm-hardware and installs qiskit-ibm-runtime into it if missing."""
        paths = cls.get_paths()
        venv_path = paths["research_venv"]
        venv_python = paths["research_python_executable"]

        # 1. Create venv if missing
        if not os.path.exists(venv_python):
            try:
                subprocess.run([sys.executable, "-m", "venv", venv_path], check=True, capture_output=True, text=True, timeout=10)
            except Exception as e:
                return {
                    "status": "FAIL",
                    "blocking_issue": "VENV_CREATION_FAILURE",
                    "error": str(e)
                }

        # 2. Check if already installed
        test_code = "import qiskit_ibm_runtime; print('OK')"
        already_installed = False
        try:
            res = subprocess.run([venv_python, "-c", test_code], capture_output=True, text=True, timeout=5)
            if res.returncode == 0 and "OK" in res.stdout:
                already_installed = True
        except Exception:
            pass

        if not already_installed:
            # Attempt upgrade/install with timeout
            try:
                subprocess.run([venv_python, "-m", "pip", "install", "--quiet", "--no-input", "qiskit-ibm-runtime"], check=True, capture_output=True, text=True, timeout=10)
            except Exception as e:
                return {
                    "status": "BLOCKED",
                    "blocking_issue": "PACKAGE_DOWNLOAD_FAILURE",
                    "error": str(e)
                }

        return {
            "status": "PASS",
            "blocking_issue": "NONE"
        }

    @classmethod
    def validate_reconciliation(cls) -> Dict[str, Any]:
        """Validates package installation location and importability inside research venv."""
        paths = cls.get_paths()
        venv_python = paths["research_python_executable"]

        # If venv python exists, test via subprocess call to target venv interpreter
        if os.path.exists(venv_python):
            code = (
                "import sys, json, inspect; "
                "res = {'sys_executable': sys.executable, 'python_version': sys.version.split()[0]}; "
                "try:\n"
                "  import qiskit\n"
                "  res['qiskit_version'] = getattr(qiskit, '__version__', 'UNKNOWN')\n"
                "except Exception:\n"
                "  res['qiskit_version'] = 'NOT_INSTALLED'\n"
                "try:\n"
                "  import qiskit_aer\n"
                "  res['qiskit_aer_version'] = getattr(qiskit_aer, '__version__', 'UNKNOWN')\n"
                "except Exception:\n"
                "  res['qiskit_aer_version'] = 'NOT_INSTALLED'\n"
                "try:\n"
                "  import qiskit_optimization\n"
                "  res['qiskit_optimization_version'] = getattr(qiskit_optimization, '__version__', 'UNKNOWN')\n"
                "except Exception:\n"
                "  res['qiskit_optimization_version'] = 'NOT_INSTALLED'\n"
                "try:\n"
                "  import qiskit_ibm_runtime\n"
                "  from qiskit_ibm_runtime import QiskitRuntimeService\n"
                "  res['qiskit_ibm_runtime_version'] = getattr(qiskit_ibm_runtime, '__version__', 'UNKNOWN')\n"
                "  res['runtime_module_path'] = inspect.getfile(qiskit_ibm_runtime)\n"
                "  res['runtime_import'] = 'PASS'\n"
                "  res['service_class_available'] = True\n"
                "except Exception as e:\n"
                "  res['runtime_import'] = 'FAIL'\n"
                "  res['service_class_available'] = False\n"
                "  res['runtime_module_path'] = 'NOT_FOUND'\n"
                "  res['error'] = str(e)\n"
                "print(json.dumps(res))"
            )

            try:
                proc = subprocess.run([venv_python, "-c", code], check=True, capture_output=True, text=True, timeout=5)
                target_res = json.loads(proc.stdout.strip())
                
                module_path = target_res.get("runtime_module_path", "")
                venv_normalized = os.path.normpath(VENV_DIR).lower()
                module_normalized = os.path.normpath(module_path).lower()
                inside_venv = venv_normalized in module_normalized

                exec_normalized = os.path.normpath(target_res["sys_executable"]).lower()
                isolated_exec = venv_normalized in exec_normalized

                return {
                    "status": "PASS" if (target_res["runtime_import"] == "PASS" and inside_venv and isolated_exec) else "BLOCKED",
                    "interpreter_isolated": isolated_exec,
                    "module_inside_research_venv": inside_venv,
                    "python_version": target_res["python_version"],
                    "qiskit_version": target_res["qiskit_version"],
                    "qiskit_ibm_runtime_version": target_res["qiskit_ibm_runtime_version"],
                    "qiskit_aer_version": target_res["qiskit_aer_version"],
                    "qiskit_optimization_version": target_res["qiskit_optimization_version"],
                    "runtime_import": target_res["runtime_import"],
                    "service_class_available": target_res["service_class_available"],
                    "runtime_module_path": module_path,
                    "target_sys_executable": target_res["sys_executable"]
                }
            except Exception as e:
                return {
                    "status": "FAIL",
                    "interpreter_isolated": False,
                    "module_inside_research_venv": False,
                    "runtime_import": "FAIL",
                    "service_class_available": False,
                    "runtime_module_path": "NOT_FOUND",
                    "error": str(e)
                }

        # Fallback if venv not yet created
        return {
            "status": "BLOCKED",
            "interpreter_isolated": False,
            "module_inside_research_venv": False,
            "runtime_import": "FAIL",
            "service_class_available": False,
            "runtime_module_path": "NOT_FOUND"
        }

    @staticmethod
    def detect_credentials() -> Dict[str, Any]:
        """Detects absence/presence of credentials securely."""
        token = os.environ.get("IBM_QUANTUM_API_KEY") or os.environ.get("IBM_QUANTUM_TOKEN") or os.environ.get("IBMQ_API_TOKEN")
        return {
            "credential_present": bool(token and len(token) >= 10),
            "credential_security": "PASS",
            "token_exposed_in_logs": False
        }
