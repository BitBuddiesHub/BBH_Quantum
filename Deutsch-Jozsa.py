from pyqpanda import *
import numpy as np
from dotenv import load_dotenv



def deutsch_jozsa_algorithm():
    # 加载.env文件
    load_dotenv()

    # 从环境变量中读取API密钥
    online_api_key = os.getenv("API_KEY")

    # 初始化在线量子虚拟机
    machine = QCloud()
    machine.set_configure(24, 24)
    machine.init_qvm(online_api_key, True)

    # 分配量子比特和经典寄存器
    qubits = machine.qAlloc_many(3)  # 包括2个输入量子比特和1个辅助量子比特
    c = machine.cAlloc_many(2)  # 只需要测量输入量子比特

    # 创建量子程序
    prog = QProg()

    # 准备初始状态
    prog << X(qubits[2])  # 将辅助量子比特置为|1>
    for i in range(3):
        prog << H(qubits[i])  # 将所有量子比特置于叠加态

    # 应用Oracle函数，这里以恒定函数为例（实际应用中需替换为具体问题的Oracle）
    # 对于平衡函数的Oracle，将根据具体问题实现不同的量子门操作

    # 应用另一次Hadamard变换到输入量子比特
    for i in range(2):
        prog << H(qubits[i])

    # 测量输入量子比特
    for i in range(2):
        prog << Measure(qubits[i], c[i])

    # 在云端执行量子程序
    measure_result = machine.real_chip_measure(prog, 8192, real_chip_type.origin_72)

    print("Deutsch-Jozsa算法的测量结果：", measure_result)

    # 释放量子虚拟机资源
    machine.finalize()

if __name__ == "__main__":
    deutsch_jozsa_algorithm()
