import numpy as np

from qet_bench.noise import (
    amplitude_damping_channel,
    apply_binary_confusion,
    apply_channel,
    binary_confusion_matrix,
    dephasing_channel,
    depolarizing_channel,
    lift_to_two_qubits,
)


def test_binary_confusion_matrix_convention() -> None:
    confusion = binary_confusion_matrix(0.1, 0.2)
    assert np.allclose(confusion.sum(axis=0), [1.0, 1.0])
    assert np.allclose(apply_binary_confusion([1.0, 0.0], confusion), [0.9, 0.1])
    assert np.allclose(apply_binary_confusion([0.0, 1.0], confusion), [0.2, 0.8])


def test_channels_preserve_trace_when_lifted() -> None:
    rho = np.zeros((4, 4), dtype=np.complex128)
    rho[0, 0] = 1.0
    for channel in (dephasing_channel(0.2), depolarizing_channel(0.2), amplitude_damping_channel(0.3)):
        out = apply_channel(rho, lift_to_two_qubits(channel, qubit=1))
        assert abs(float(np.real(np.trace(out))) - 1.0) < 1.0e-12
