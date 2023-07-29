import os
import sys

# 封装的 Microsoft PnP 工具

# 运行
run = lambda _: os.popen(_).read()


def lines2dict(text):
    data_list = []
    enum_info = text.split()
    data = {}
    for i, x in enumerate(enum_info):
        if i == len(enum_info) - 1:
            data.update({list(data.keys())[-1]: enum_info[-1]})
            # print(data)
            data_list.append(data)
        if x.startswith("ID:"):
            if data:
                # print(data)
                data_list.append(data)
                data = {}
        if ":" in x:
            end_index = i + 1
            for _ in range(1, 7):
                if i + _ < len(enum_info) and enum_info[i + _].endswith(":"):
                    end_index += 1
                    break
            data.update({x.strip(":"): "".join(enum_info[i + 1:end_index])})
    return data_list


# 枚举系统上的所有设备
def enum_devices(connected=True, drivers=False, dev_class=None, data_list=[]):
    """
    :param connected: True 已连接设备 False 断开的设备
    :param drivers: True 显示匹配和已安装的驱动程序
    :param dev_class: 设备类名称 如："USB"
    :return:data_list
    """
    enum_row_info = None

    if sys.platform == "win32":
        if drivers:
            enum_row_info = run(f"PNPUTIL /enum-devices /drivers")
        if dev_class:
            enum_row_info = run(f"PNPUTIL /enum-devices /class {dev_class}")
        else:
            # 已连接的设备
            if connected:
                enum_row_info = run("PNPUTIL /enum-devices /connected")
            # 断开的设备
            else:
                enum_row_info = run("PNPUTIL /enum-devices /disconnected")

        if enum_row_info:
            # print(enum_row_info)
            data_list = lines2dict(enum_row_info)
    else:
        data_list = run("lsusb").split("\n")
    return data_list


# 启用设备
def enable_device(deviceid=None):
    if deviceid:
        result = run(rf'PNPUTIL /enable-device "{deviceid}" /force')
        print(result)
        return result


# 禁用设备
def disable_device(deviceid=None):
    if deviceid:
        result = run(rf'PNPUTIL /disable-device "{deviceid}" /force')
        print(result)
        return result


# 重启设备
def restart_device(deviceid=None):
    if deviceid:
        result = run(rf'PNPUTIL /restart-device "{deviceid}" /force')
        print(result)
        return result


# 移除设备
def remove_device(deviceid=None):
    result = None
    if deviceid:
        if sys.platform == "win32":
            result = run(rf'PNPUTIL /remove-device "{deviceid}"')
        else:
            result = run(f'eject -c "{deviceid}"')
    print(result)
    return result


# 设备控制
def device_ctrl(**kwargs):
    if kwargs.get("event") and kwargs.get("id"):
        result = run(rf"""PNPUTIL /{kwargs['event']} "{kwargs['id']}" """)
        print(result)
        return result


# 搜索设备
def device_search(*args):
    devices = enum_devices(connected=True)
    search_list = []
    for d in devices:
        for v in d.values():
            if args:
                if args[0] in v:
                    search_list.append(d)
                    break
            else:
                search_list.append(d)
    # search_list = subprocess.getoutput("PowerShell -Command \"& {Get-PnpDevice | Select-Object Status,Class,FriendlyName,InstanceId | ConvertTo-Json}\"")
    # search_list = loads(search_list)
    return search_list


if __name__ == '__main__':
    # import sys
    # print(sys.argv)
    # rs = enum_devices(drivers=True)
    # id_list = {r["ID"] for r in rs}
    # print(len(id_list), id_list)
    # rs = [r for r in rs if "Rev" in r["ID"]]
    # print(rs)
    devices = device_search("Rev")
    print(devices)
    # deviceid = devices[0]["ID"]
    # disable_device(deviceid)
    # enable_device(deviceid)
    # remove_device(deviceid)
