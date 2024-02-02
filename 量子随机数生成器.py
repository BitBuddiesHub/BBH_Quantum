import numpy as np
from pyqpanda import *
from dotenv import load_dotenv




def quantum_random_number_generator():
    # 加载.env文件
    load_dotenv()

    # 从环境变量中读取API密钥
    online_api_key = os.getenv("API_KEY")

    # 初始化在线量子虚拟机
    machine = QCloud()
    machine.set_configure(24, 24)  # 设置使用72个量子比特
    machine.init_qvm(online_api_key, True)

    # 分配量子比特和经典寄存器，这次我们尝试使用最大数量的量子比特
    q = machine.qAlloc_many(24)  # 假设我们可以使用最多72个量子比特
    c = machine.cAlloc_many(24)  # 对应的经典寄存器

    # 创建量子程序
    prog = QProg()

    # 将所有量子比特置于叠加态并测量，以生成宽范围的随机数
    for i in range(24):
        prog << H(q[i]) << Measure(q[i], c[i])

    # 对量子程序进行分解，以适应实际的量子硬件限制
    decomposed_prog = ldd_decompose(prog)

    # 在云端执行量子程序
    measure_result = machine.real_chip_measure(decomposed_prog, 10, real_chip_type.origin_72)

    # 创建一个空的列表来存储转换后的结果
    decimal_result = []

    # 遍历输出结果的键
    for key in measure_result.keys():
        # 将二进制字符串转换为十进制整数
        decimal_number = int(key, 2)
        # 将十进制整数添加到列表中
        decimal_result.append(decimal_number)

    # 输出转换后的结果
    print("生成的随机数是：", decimal_result)


    # 释放量子虚拟机资源
    machine.finalize()

if __name__ == "__main__":
    quantum_random_number_generator()
