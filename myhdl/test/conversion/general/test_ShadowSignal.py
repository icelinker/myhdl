from __future__ import absolute_import
import pytest
import myhdl
from myhdl import *

@pytest.mark.verify_convert
@block
def test_SliceSignal():

    s = Signal(intbv(0)[8:])
    a, b, c = s(7), s(5), s(0)
    d, e, f, g = s(8,5), s(6,3), s(8,0), s(4,3)
    N = len(s)

    @instance
    def check():
        for i in range(N):
            s.next = i
            yield delay(10)
            print(int(a))
            print(int(b))
            print(int(c))
            print(d)
            print(e)
            print(f)
            print(g)

    return check


@pytest.mark.verify_convert
@block
def test_ConcatSignal():

    a = Signal(intbv(0)[5:])
    b = Signal(bool(0))
    c = Signal(intbv(0)[3:])
    d = Signal(intbv(0)[4:])

    s = ConcatSignal(a, b, c, d)

    I_max = 2**len(a)
    J_max = 2**len(b)
    K_max = 2**len(c)
    M_max = 2**len(d)
    @instance
    def check():
        for i in range(I_max):
            for j in range(J_max):
                for k in range(K_max):
                    for m in range(M_max):
                        a.next = i
                        b.next = j
                        c.next = k
                        d.next = m
                        yield delay(10)
                        print(s)

    return check


@pytest.mark.verify_convert
@block
def test_ConcatSignalWithConsts():

    a = Signal(intbv(0)[5:])
    b = Signal(bool(0))
    c = Signal(intbv(0)[3:])
    d = Signal(intbv(0)[4:])
    e = Signal(intbv(0)[1:])

    c1 = "10"
    c2 = intbv(3)[3:]
    c3 = '0'
    c4 = bool(1)
    c5 = intbv(42)[8:]  # with leading zeroes

    s = ConcatSignal(c1, a, c2, b, c3, c, c4, d, c5, e)

    I_max = 2**len(a)
    J_max = 2**len(b)
    K_max = 2**len(c)
    M_max = 2**len(d)
    @instance
    def check():
        for i in range(I_max):
            for j in range(J_max):
                for k in range(K_max):
                    for m in range(M_max):
                        for n in range(2**len(e)):
                            a.next = i
                            b.next = j
                            c.next = k
                            d.next = m
                            e.next = n
                            yield delay(10)
                            print(s)

    return check


@pytest.mark.verify_convert
@block
def test_TristateSignal():
    s = TristateSignal(intbv(0)[8:])
    a = s.driver()
    b = s.driver()
    c = s.driver()

    @instance
    def check():
        a.next = None
        b.next = None
        c.next = None
        yield delay(10)
        #print s
        a.next = 1
        yield delay(10)
        print(s)
        a.next = None
        b.next = 122
        yield delay(10)
        print(s)
        b.next = None
        c.next = 233
        yield delay(10)
        print(s)
        c.next = None
        yield delay(10)
        #print s

    return check


@block
def permute(x, a, mapping):

    p = [a(m) for m in mapping]

    q = ConcatSignal(*p)

    @always_comb
    def assign():
        x.next = q

    return assign


@pytest.mark.verify_convert
@block
def test_permute(conv=False):

    x = Signal(intbv(0)[3:])
    a = Signal(intbv(0)[3:])
    mapping = (0, 2, 1)

    if conv:
        dut = conv(permute(x, a, mapping))
    else:
        dut = permute(x, a, mapping)

    @instance
    def stimulus():
        for i in range(2**len(a)):
            a.next = i
            yield delay(10)
            print("%d %d" % (x, a))
            assert x[2] == a[0]
            assert x[1] == a[2]
            assert x[0] == a[1]
        raise StopSimulation()

    return dut, stimulus
