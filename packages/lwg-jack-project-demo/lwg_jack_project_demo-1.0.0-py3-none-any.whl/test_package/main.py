import operator1
import test_package2.operator2


def get_operators():
    inner_operators = dict()
    inner_operators["operator_func_version"] = "v1.0.0"
    inner_operators["operators"] = {"opreator_1": operator1, "opreator_2": test_package2.operator2}
    return inner_operators


if __name__ == "main":
    ops = get_operators()
    op1 = ops["operators"]["opreator_1"]
    print(op1)
    print(op1.process("{\"testKey\": \"testValue\"}"))
