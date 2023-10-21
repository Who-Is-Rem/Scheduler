import sys
sys.path.append('../SchedulerV1.1.0')

from data import *

def dr1_test():
    dr = DataRange(0, 0)
    assert dr.getString() == "0"
    assert dr.getMax() == 0
    assert dr.getMin() == 0
    assert dr.add(dr) == DataRange(0,0)
    print("dr1_test passed")

def dr2_test():
    try:
        DataRange(1, 0)
    except:
        print("dr2_test passed")

def dr3_test():
    dr1 = DataRange(0, 10)
    dr2 = DataRange(1, 1)
    dr3 = DataRange(5, 11)

    dr4 = dr1.add(dr2)
    dr5 = dr4.add(dr3)

    assert dr4.getMin() == 1
    assert dr4.getMax() == 11
    assert dr4.getString( )== "1-11"

    assert dr5.getMin() == 6
    assert dr5.getMax() == 22
    assert dr5.getString() == "6-22"

    print("dr3_test passed")

def dr4_test():
    try:
        DataRange(-1, 0)
    except:
        print("dr4_test passed")

dr1_test()
dr2_test()
dr3_test()
dr4_test()

def s1_test():
    s= Service("Manicure", "M", DataRange(15), DataRange(30))
    assert s.getName() == "Manicure"
    assert s.getPrice().getString() == "15"
    assert s.getShort() == "M"
    assert s.getTime().getString() == "30"
    print("s1_test passed")

s1_test()

def c1_test():
    sl = []
    for i in range(3):
        s = Service(str(i), str(i), DataRange(i), DataRange(i*10))
        sl.append(s)

    c = Customer("Bob", "Uchiha", "0987654321", sl)
    assert c.getFullName() == "Bob Uchiha"
    assert c.getName() == "Bob"
    assert c.getNumber() == "0987654321"
    assert c.getServices() == sl
    i = 0
    for s in c.getServices():
        assert s.getName() == f"{i}"
        assert s.getShort() == f"{i}"
        assert s.getPrice() == DataRange(i)
        assert s.getTime() == DataRange(i*10)
        i += 1
    
    print("c1_test passed")

def c2_test():
    c = Customer("TEst", "t", "1234567890")
    assert c.getLocked() == False
    assert c.getServed() == False
    c.setLocked(True)
    c.setServed(True)
    assert c.getLocked() == True
    assert c.getServed() == True

    print("c2_test passed")

c1_test()
c2_test()

def e1_test():
    e = Employee("1", "1", "1234567890")
    assert e.getFullName() == "1 1"
    assert e.getName() == "1"
    assert e.getNumber() == "1234567890"
    assert e.getCustomers() == []

    print("e1_test passed")

def e2_test():
    sl = []
    for i in range(3):
        s = Service(str(i), str(i), DataRange(i), DataRange(i*10))
        sl.append(s)

    c = Customer("Bob", "Uchiha", "0987654321", sl)

    sl1 = []
    for i in range(5):
        s = Service(str(i), str(i), DataRange(i), DataRange(i*20))
        sl1.append(s)

    c1 = Customer("Bo0", "Uchiha", "1234567890", sl1)

    e = Employee("Test", "test", "0000000000")
    e.addCustomer(c)
    e.addCustomer(c1)

    assert e.getFullName() == "Test test"
    assert e.getName() == "Test"
    assert e.getNumber() == "0000000000"
    assert len(e.getCustomers()) == 2

    cust1 = e.getCustomers()[0]
    assert cust1.getFullName() == "Bob Uchiha"
    assert cust1.getName() == "Bob"
    assert cust1.getNumber() == "0987654321"
    assert len(cust1.getServices()) == 3

    cust2 = e.getCustomers()[1]
    assert cust2.getFullName() == "Bo0 Uchiha"
    assert cust2.getName() == "Bo0"
    assert cust2.getNumber() == "1234567890"
    assert len(cust2.getServices()) == 5

    print("e2_test passed")

e1_test()
e2_test()

    



        
    
