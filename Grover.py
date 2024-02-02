import numpy as np
from pyqpanda import *
from dotenv import load_dotenv


def grovers_algorithm():
    # 加载.env文件
    load_dotenv()

    # 从环境变量中读取API密钥
    online_api_key = os.getenv("API_KEY")

    # 初始化在线量子虚拟机
    machine = QCloud()
    machine.set_configure(24,24)
    machine.init_qvm(online_api_key, True)

    # 分配量子比特和经典寄存器
    q = machine.qAlloc_many(2)  # 使用2个量子比特
    c = machine.cAlloc_many(2)  # 对应的经典寄存器

    # 创建量子程序
    prog = QProg()

    # 准备初始状态：将所有量子比特置于叠加态
    for i in range(2):
        prog << H(q[i])

    # 构建Oracle（这里假设标记的状态是|11>）
    prog << X(q[0]) << X(q[1])
    prog << H(q[1])
    prog << CNOT(q[0], q[1])
    prog << H(q[1])
    prog << X(q[0]) << X(q[1])

    # 构建Grover's diffusion operator
    for i in range(2):
        prog << H(q[i]) << X(q[i])
    prog << H(q[1])
    prog << CNOT(q[0], q[1])
    prog << H(q[1])
    for i in range(2):
        prog << X(q[i]) << H(q[i])

    # 测量量子比特
    for i in range(2):
        prog << Measure(q[i], c[i])

    # 对量子程序进行分解，以适应实际的量子硬件限制
    decomposed_prog = ldd_decompose(prog)

    # 在云端执行量子程序
    measure_result = machine.real_chip_measure(decomposed_prog, 8192, real_chip_type.origin_72)

    print("Grover's算法的测量结果：", measure_result)

    # 释放量子虚拟机资源
    machine.finalize()

if __name__ == "__main__":
    grovers_algorithm()
