import numpy as np
from pyqpanda import *
from dotenv import load_dotenv



def alice_prepare_and_measure():
    # 加载.env文件
    load_dotenv()

    # 从环境变量中读取API密钥
    online_api_key = os.getenv("API_KEY")

    # 初始化在线量子虚拟机
    machine = QCloud()
    machine.set_configure(24, 24)
    machine.init_qvm(online_api_key, True)

    # 初始化量子比特和经典寄存器
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)  # 需要3个经典寄存器来存储测量结果

    # 创建量子程序
    prog = QProg()

    # 准备纠缠对
    prog << H(q[1]) << CNOT(q[1], q[2])

    # Alice对她的量子比特和纠缠对中的一个进行Bell基测量
    prog << CNOT(q[0], q[1])
    prog << H(q[0])
    prog << Measure(q[0], c[0])
    prog << Measure(q[1], c[1])

    # 在云端执行量子程序
    measure_result = machine.real_chip_measure(prog, 8192, real_chip_type.origin_72)

    print("Alice的测量结果：", measure_result)

    # 释放量子虚拟机资源
    machine.finalize()

    return measure_result

if __name__ == "__main__":
    alice_prepare_and_measure()