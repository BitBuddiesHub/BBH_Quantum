import numpy as np
from pyqpanda import *
from dotenv import load_dotenv



def create_bell_state_and_measure_online():
    # 加载.env文件
    load_dotenv()

    # 从环境变量中读取API密钥
    online_api_key = os.getenv("API_KEY")

    # 初始化在线量子虚拟机
    machine = QCloud()
    machine.set_configure(72,72)  # 根据需要设置
    machine.init_qvm(online_api_key, True)

    # 分配量子比特和经典寄存器
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    # 创建量子程序
    prog = QProg()

    # 构建贝尔态
    prog << H(q[0]) << CNOT(q[0], q[1])

    # 测量量子比特
    prog << Measure(q[0], c[0]) << Measure(q[1], c[1])

    # 对量子程序进行分解以适应实际的量子硬件限制
    decomposed_prog = ldd_decompose(prog)

    # 在云端执行量子程序
    measure_result = machine.real_chip_measure(decomposed_prog, 1000, real_chip_type.origin_72)

    print("测量结果：", measure_result)

    # 释放量子虚拟机资源
    machine.finalize()

if __name__ == "__main__":
    create_bell_state_and_measure_online()