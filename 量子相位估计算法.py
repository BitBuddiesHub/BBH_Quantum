import numpy as np
from pyqpanda import *
from dotenv import load_dotenv



def main():
    # 加载.env文件
    load_dotenv()

    # 从环境变量中读取API密钥
    online_api_key = os.getenv("API_KEY")

    # 初始化在线量子虚拟机
    machine = QCloud()
    machine.set_configure(72,72)
    machine.init_qvm(online_api_key, True)

    # 初始化量子比特和经典寄存器
    qubits = machine.qAlloc_many(4)
    cbits = machine.cAlloc_many(3)

    # 创建量子程序
    prog = QProg()

    # 应用Hadamard门
    prog << H(qubits[0]) << H(qubits[1]) << H(qubits[2])
    
    # 应用受控RZ门
    prog << RZ(qubits[3], np.pi/4).control([qubits[0]])
    prog << RZ(qubits[3], np.pi/2).control([qubits[1]])
    prog << RZ(qubits[3], np.pi).control([qubits[2]])
    
    # 应用IQFT的部分步骤
    prog << H(qubits[2])
    prog << CR(qubits[2], qubits[1], np.pi/2)
    prog << H(qubits[1])
    prog << CR(qubits[1], qubits[0], np.pi/4)
    prog << CR(qubits[2], qubits[0], np.pi/2)
    prog << H(qubits[0])
    
    # 交换量子比特
    prog << SWAP(qubits[0], qubits[2])
    
    # 测量
    prog << Measure(qubits[0], cbits[0])
    prog << Measure(qubits[1], cbits[1])
    prog << Measure(qubits[2], cbits[2])

    # 对量子程序进行分解，以适应实际量子芯片的限制
    decomposed_prog = ldd_decompose(prog)
    
    # 在真实量子芯片或云模拟器上执行量子程序
    measure_result = machine.real_chip_measure(decomposed_prog, 1000, real_chip_type.origin_72)

    print(measure_result)

    # 释放量子虚拟机资源
    machine.finalize()

if __name__ == "__main__":
    main()
