from sage.all import *

import os
import functools

dirnow = os.path.dirname(os.path.abspath(__file__))

# 获取小于等于 11 crossing 的所有扭结名称
@functools.cache
def get_knot_name_list() -> list:
    hom_file = os.path.join(dirnow, "HOMFLY-PT-reg.txt")
    arr = []
    for line in open(hom_file):
        arr.append(line.strip().split("|")[-1][:-1])
    return arr

# 获取完整的 pd_code 信息文件
@functools.cache
def get_pd_code_list_file() -> list:
    pd_code_file = os.path.join(dirnow, "pd_code_list.txt")
    arr = []
    for line in open(pd_code_file):
        arr.append(line.strip())
    return arr

# 计算扭结连通和
def get_connected_sum(pd_code_1: list, pd_code_2: list) -> str:
    k1 = Knot(pd_code_1)
    k2 = Knot(pd_code_2)
    return  k1.connected_sum(k2).pd_code()

# 计算扭结的镜像扭结
def get_mirror_code(pd_code):
    return Knot(pd_code).mirror_image().pd_code()

# 根据扭结名称获取扭结 pd_code
@functools.cache
def get_pd_code_by_prime_knot_name(knot_name: str) -> list:
    assert knot_name.find(",") == -1 # 必须是素扭结
    mirror = False
    if knot_name.startswith("m"):
        mirror = True
        knot_name = knot_name[1:]
    ans = None
    for line in get_pd_code_list_file():
        if line.startswith("[%s|" % knot_name):
            ans = eval(line.split("|")[-1][:-1])
            break
    ans = get_mirror_code(ans) if mirror else ans # 计算镜像
    return ans

# 根据非素扭结或者素扭结名称确定扭结 pd_code
def get_pd_code_by_knot_name(knot_name: str) -> list:
    pd_arr = []
    knot_name_list = knot_name.split(",")
    for sub_name in knot_name_list:
        pd_arr.append(get_pd_code_by_prime_knot_name(sub_name))
    for i in range(1, len(knot_name_list)):
        pd_arr[0] = get_connected_sum(pd_arr[0], pd_arr[i])
    return pd_arr[0]

# 获取扭结 pd_code 列表
@functools.cache
def get_pd_code_list_for_all_knot() -> str:
    arr = ""
    for knot_name in get_knot_name_list():
        arr += "[%s|%s]\n" % (knot_name, str(get_pd_code_by_knot_name(knot_name)))
    return arr

if __name__ == "__main__":
    fp = open("com_pd_code_list.txt", "w")
    fp.write(get_pd_code_list_for_all_knot())
    fp.close()