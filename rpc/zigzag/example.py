class VarInt(object):
    @classmethod
    def _zigzag_encode(cls, num):
        retval =  num * 2 if num >= 0 else -2 * num - 1
        return int(retval)

    @classmethod
    def _zigzag_decode(cls, num):
        retval = - (num + 1) / 2 if num % 2 else num / 2
        return int(retval)

    @classmethod
    def int_to_var(cls, num):
        num = cls._zigzag_encode(num)
        front = rear = count = 0
        while True:
            if num >> 7:
                temp = num & 0x7f
                if rear:
                    rear += (temp | 0x80) << 8
                else:
                    rear = temp
                count += 1
                num >>= 7
            else:
                front = num
                break
        if count:
            front = (front | 0x80) << count * 8
        return front + rear

    @classmethod
    def var_to_int(cls, num):
        front = rear = count = 0
        while True:
            if num >> 8:
                temp = num & 0x7f
                if rear:
                    rear |= temp << 7
                else:
                    rear = temp
                count += 1
                num >>= 8
            else:
                front = num & 0x7f
                break
        if count:
            front <<= count * 7
        return cls._zigzag_decode(front + rear)
