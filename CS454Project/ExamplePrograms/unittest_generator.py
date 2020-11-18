def _import_line_writer(code, filename, funcname):
    code.write('from {} import {}\n'.format(filename, funcname))

def import_writer(code, filename, funcname):
    '''
    from unittest import Testcase
    from filename import funcname

    '''

    _import_line_writer(code, 'unittest', 'TestCase')
    _import_line_writer(code, filename, funcname)
    code.write('\n')

def _func_writer(code, input, filename, funcname, indent, i):
    testname = 'test{}'.format(i)
    func_input = str(tuple(input))

    func = getattr(__import__(filename), funcname)

    func_ans = func(*input)

    code.write('{}def {}(self):\n'.format('\t'*indent, testname))
    code.write('{}self.assertEqual({}{}, {})\n'.format('\t'*(indent+1), funcname, func_input, func_ans))
    code.write('\n')


def _class_writer(code, inputs, filename, funcname):
    code.write("class Test(Testcase):\n")
    for i in range(len(inputs)):
        _func_writer(code, inputs[i], filename, funcname, 1, i+1)


def unittest_writer(code, inputs, filename, funcname):
    '''
    class Test(Testcase):
        def test1(self):
            self.assertEqual(funcname(input1), result) # result는 funcname(input) 값
        
        def test2(self):
            self.assertEqual(funcname(input2), result) # result는 funcname(input) 값
        
        ...
    '''
    _class_writer(code, inputs, filename, funcname)

def unittest_generator(filename, funcname, inputs):
    # filename, funcname, inputs = 'calculator', 'mul', [(1,2), (3,4)]
    
    code = open('unittest.py', 'w')
    import_writer(code, filename, funcname)
    unittest_writer(code, inputs, filename, funcname)
    
    code.close()

if __name__== "__main__":
    unittest_generator('calculator', 'mul', [(1,2), (4,4)])