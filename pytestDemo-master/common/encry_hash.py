from hashids import Hashids
import binascii

def str_to_hexStr(string):
    str_bin = string.encode('utf-8')
    return binascii.hexlify(str_bin).decode('utf-8')

def hexStr_to_str(hex_str):
    hex = hex_str.encode('utf-8')
    str_bin = binascii.unhexlify(hex)
    return str_bin.decode('utf-8')

def hashids_encode(vaule):
    hashids = Hashids(salt='eXVueXU=', min_length=64,alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
    str_hex = str_to_hexStr(vaule)
    encode_value=hashids.encode_hex(str_hex)
    return encode_value


def hashids_decode(vaule):
    hashids = Hashids(salt='eXVueXU=', min_length=64,alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
    decode_value = hashids.decode_hex(vaule)
    value_str = hexStr_to_str(decode_value)
    return value_str


if __name__ == '__main__':
    vaule_amdin = hashids_encode('administrator')
    value_passwd = hashids_encode('Test!123')
    value_de = hashids_decode('Kk0w4LAaV6Oo1r8lQPYEBq5MZE5bOmXNI3rrr6oDk0qxX5J3WNjMd2GmRZeDpyzb')
    print(vaule_amdin,value_passwd,value_de)