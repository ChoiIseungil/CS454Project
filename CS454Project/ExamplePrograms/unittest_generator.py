'''
사용법:

from unittest_generator import unittest_generator로 module로서 사용가능

이후 unittest_generator(filename, funcname, inputs)로 함수 호출시 unittest.py 파일 생성
filename = 테스트할 py파일 이름, funcname = 테스트할 함수 이름, inputs = 테스트 input들 (list of tuples or list of lists)
ex) unittest_generator('calculator', 'mul', [(1,2), (4,4)]) -> unittest.py 생성

'''


def _import_line_writer(code, filename, funcname):
    code.write('from {} import {}\n'.format(filename, funcname))

def import_writer(code, filename, funcname):
    _import_line_writer(code, 'unittest', 'TestCase')
    _import_line_writer(code, filename, funcname)
    code.write('\n')


def _func_writer(code, input, filename, funcname, indent, i):
    testname = 'test{}'.format(i) # test unit 이름
    func_input = str(tuple(input)) # function input for passing into str format

    func = getattr(__import__(filename), funcname) # 테스트할 function import

    try:
        func_ans = func(*input) # original function answer / update 필요: func_ans의 결과가 error인 경우

        code.write('{}def {}(self):\n'.format('\t'*indent, testname))
        code.write('{}self.assertEqual({}{}, {})\n'.format('\t'*(indent+1), funcname, func_input, func_ans))
        code.write('\n')
    except:
        code.write('{}def {}(self):\n'.format('\t' * indent, testname))
        code.write('{}with self.assertRaises(Exception):\n'.format('\t' * (indent + 1)))
        code.write('{}{}{}\n'.format('\t' * (indent + 2), funcname, func_input))
        code.write('\n')


def _class_writer(code, inputs, filename, funcname):
    code.write("class Test(TestCase):\n")
    for i in range(len(inputs)):
        _func_writer(code, inputs[i], filename, funcname, 1, i+1)


def unittest_writer(code, inputs, filename, funcname):
    _class_writer(code, inputs, filename, funcname)


def unittest_generator(filename, funcname, inputs):
    # filename, funcname, inputs = 'calculator', 'mul', [(1,2), (3,4)]
    
    code = open('test_calculator2.py', 'w')
    import_writer(code, filename, funcname)
    unittest_writer(code, inputs, filename, funcname)
    
    code.close()


if __name__== "__main__":
    unittest_generator('calculator', 'mul', [(1,2), (3,0)])