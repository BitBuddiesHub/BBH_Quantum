from pyqpanda import *
import numpy as np
from dotenv import load_dotenv


def quantum_fourier_transform():
    # 加载.env文件
    load_dotenv()

    # 从环境变量中读取API密钥
    online_api_key = os.getenv("API_KEY")


    # 初始化在线量子虚拟机
    machine = QCloud()
    machine.set_configure(24, 24)
    machine.init_qvm(online_api_key, True)

    # 分配量子比特
    qubits = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)  # 为每个量子比特分配一个经典寄存器以存储测量结果

    # 创建量子程序
    prog = QProg()

    # 应用量子傅里叶变换
    for j in range(3):
        prog << H(qubits[j])
        for k in range(j+1, 3):
            angle = np.pi / (2 ** (k-j))
            prog << CR(qubits[k], qubits[j], angle)
    
    # 将量子比特顺序颠倒以完成QFT
    for j in range(3//2):
        prog << SWAP(qubits[j], qubits[3-j-1])
    
    # 对每个量子比特进行测量
    for i in range(3):
        prog << Measure(qubits[i], c[i])

    # 在云端执行量子程序
    measure_result = machine.real_chip_measure(prog, 8192, real_chip_type.origin_72)

    print("量子傅里叶变换的测量结果：", measure_result)

    # 释放量子虚拟机资源
    machine.finalize()

if __name__ == "__main__":
    quantum_fourier_transform()
