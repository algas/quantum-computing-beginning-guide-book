import math
import itertools

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import execute, Aer

def chain(*functions):
    [f for f in functions]

def get_result(qc, shots=1):
    simulator = Aer.get_backend('qasm_simulator')
    return execute(qc, simulator, shots=shots).result().get_counts(qc)

def get_unitary(qc):
    simulator = Aer.get_backend('unitary_simulator')
    return execute(qc, simulator).result().get_unitary(qc)

def exec_unitary():
    q2 = QuantumRegister(2)
    c2 = ClassicalRegister(2)
    qc2 = QuantumCircuit(q2,c2)
    qc2.h([0,1])
    print(qc2)
    print(get_unitary(qc2))
    qc2 = QuantumCircuit(q2,c2)
    qc2.cz(0,1)
    print(qc2)
    print(get_unitary(qc2))
    qc2 = QuantumCircuit(q2,c2)
    qc2.x(0)
    qc2.cz(0,1)
    qc2.x(0)
    print(qc2)
    print(get_unitary(qc2))
    qc2 = QuantumCircuit(q2,c2)
    qc2.x(1)
    qc2.cz(0,1)
    qc2.x(1)
    print(qc2)
    print(get_unitary(qc2))
    qc2 = QuantumCircuit(q2,c2)
    qc2.h([0,1])
    qc2.x([0,1])
    qc2.cz(0,1)
    qc2.x([0,1])
    qc2.h([0,1])
    qc2.x([0,1])
    qc2.cz(0,1)
    qc2.x([0,1])
    qc2.h([0,1])
    print(qc2)
    print(get_unitary(qc2))
    qc2.measure(q2,c2)
    print(get_result(qc2, 100))

### 1bit
def exec_1bit():
    print('1bit')
    q1 = QuantumRegister(1)
    c1 = ClassicalRegister(1)
    qc1 = QuantumCircuit(q1,c1)
    print(get_unitary(qc1))
    qc1.measure(q1,c1)
    print(get_result(qc1))

    print('pauli-x')
    qc1 = QuantumCircuit(q1,c1)
    qc1.x(0)
    print(get_unitary(qc1))
    qc1.measure(q1,c1)
    print(get_result(qc1))

    print('hadamard')
    qc1 = QuantumCircuit(q1,c1)
    qc1.h(0)
    print(get_unitary(qc1))
    qc1.measure(q1,c1)
    print(get_result(qc1, 100))

### 2bit
def exec_2bit():
    print('2bit')
    q2 = QuantumRegister(2)
    c2 = ClassicalRegister(2)
    qc2 = QuantumCircuit(q2,c2)
    qc2.x(0)
    qc2.measure(q2,c2)
    print('before cx')
    print(get_result(qc2))
    qc2 = QuantumCircuit(q2,c2)
    qc2.x(0)
    qc2.cx(0,1)
    qc2.measure(q2,c2)
    print('after cx')
    print(get_result(qc2))

    def swap(qc):
        qc.cx(1,0)
        qc.cx(0,1)
        qc.cx(1,0)

    qc2 = QuantumCircuit(q2,c2)
    qc2.x(0)
    qc2.measure(q2,c2)
    print('before swap')
    print(get_result(qc2))
    qc2 = QuantumCircuit(q2,c2)
    qc2.x(0)
    swap(qc2)
    qc2.measure(q2,c2)
    print('after swap')
    print(get_result(qc2))

### 3bit
def exec_3bit():
    print('3bit')
    q3 = QuantumRegister(3)
    c3 = ClassicalRegister(3)
    qc3 = QuantumCircuit(q3,c3)
    qc3.x([0,1,2])
    qc3.measure(q3,c3)
    print('before ccx')
    print(get_result(qc3))
    qc3 = QuantumCircuit(q3,c3)
    qc3.x([0,1,2])
    qc3.ccx(0,1,2)
    qc3.measure(q3,c3)
    print('after ccx')
    print(get_result(qc3))

def or_gate(qc, a=0, b=1, r=2):
    qc.x(a)
    qc.x(b)
    qc.ccx(a,b,r)
    qc.x([a,b,r])

def exec_or():
    q = QuantumRegister(3)
    c = ClassicalRegister(3)
    qc = QuantumCircuit(q,c)
    qc.x(0)
    qc.measure(q,c)
    print('before or')
    print(get_result(qc))
    qc = QuantumCircuit(q,c)
    qc.x(0)
    or_gate(qc,0,1,2)
    print(qc)
    qc.measure(q,c)
    print('after or')
    print(get_result(qc))

## HalfAdder
def _half_adder(a, b):
    c = a & b
    s = a ^ b
    return (c, s)

def classical_half_adder(a, b):
    (c, s) = _half_adder(a, b)
    print('{0} + {1} = {2}{3}'.format(a,b,c,s))

def quantum_half_adder(qc, a=0, b=1, c=2):
    qc.ccx(a,b,c)
    qc.cx(a,b)

def exec_half_adder(a, b):
    q = QuantumRegister(3)
    c = ClassicalRegister(3)
    qc = QuantumCircuit(q,c)
    if a == 1:
        qc.x(0)
    if b == 1:
        qc.x(1)
    quantum_half_adder(qc,0,1,2)
    print(qc)
    qc.measure(q,c)
    r = list(get_result(qc).keys())[0]
    print('{0} + {1} = {2}{3}'.format(a,b,r[0],r[1]))

def main_half_adder():
    print('Classical Half Adder')
    classical_half_adder(0, 0)
    classical_half_adder(0, 1)
    classical_half_adder(1, 0)
    classical_half_adder(1, 1)
    print('Quantum Half Adder')
    exec_half_adder(0, 0)
    exec_half_adder(0, 1)
    exec_half_adder(1, 0)
    exec_half_adder(1, 1)

## Full Adder
def _full_adder(a, b, x):
    (tc, ts) = _half_adder(a, b)
    (c, s) = _half_adder(x, ts)
    return (tc | c, s)

def classical_full_adder(a, b, x):
    (c, s) = _full_adder(a, b, x)
    print('{0} + {1} + {2} = {3}{4}'.format(a, b, x, c, s))

def quantum_full_adder(qc, a=0, b=1, ci=2, c1=3, c2=4, co=5):
    quantum_half_adder(qc, a, b, c1)
    quantum_half_adder(qc, b, ci, c2)
    or_gate(qc, c1, c2, co)

def exec_full_adder(a, b, x):
    q = QuantumRegister(6)
    c = ClassicalRegister(6)
    qc = QuantumCircuit(q,c)
    if a == 1:
        qc.x(0)
    if b == 1:
        qc.x(1)
    if x == 1:
        qc.x(2)
    quantum_full_adder(qc,0,1,2,3,4,5)
    print(qc)
    qc.measure(q,c)
    r = list(get_result(qc).keys())[0]
    print('{0} + {1} + {2} = {3}{4}'.format(a,b,x,r[0],r[3]))

def main_full_adder():
    print('Classical Full Adder')
    classical_full_adder(0,0,1)
    classical_full_adder(0,1,1)
    classical_full_adder(1,1,0)
    classical_full_adder(1,1,1)
    print('Quantum Full Adder')
    exec_full_adder(0,0,1)
    exec_full_adder(0,1,1)
    exec_full_adder(1,1,0)
    exec_full_adder(1,1,1)


if __name__ == "__main__":
    # exec_unitary()
    exec_1bit()
    exec_2bit()
    exec_3bit()
    exec_or()
    main_half_adder()
    main_full_adder()


