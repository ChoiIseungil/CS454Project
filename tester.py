import random
import copy


class SingletonInstane:  # Singleton 포맷의 클래스. 한번 Tester 클래스를 호출하여 작업하면 이후 Tester 클래스의 새로운 instance를 만들어도 이전의 상태를 유지.
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance


'''
기본 클래스 사용법
instance 만들기: new_instance = Tester.instance()
Tester의 False condition initialize: new_instance.reset(argnum, max_value, condition_range, error_rate, correction_range),
argnum은 테스트할 파라미터 개수를 입력, max_value는 파라미터의 value의 최대값, condition_range는 parameter의 condition range, error_rate는 전체 가능한 value 조합중 error 의 비율, correction_range는 parameter를 고정하고싶은 특정 range.
False condition 갱신: 위와 같음. new_instance.reset(argnum, max_value, condition_range, error_rate, correction_range)
실제 테스트 진행: new_instance.run(arglist), arglist 는 테스트 input(2-dimension 리스트) 입력 ex) [[1,2,3], [-1,-2,-3]]. self.condition의 각각의 range에 대하여 False condition에 해당하는 경우 (-1, condition)를 반환, 아니면 (0, condition).
최종 결과는 ( (False condition coverage, False condition 의 비율, False condition 개수, 전체 condition 개수), [[첫번째 input의 각 condition별 결과], [두번째 ...], ...] ) 를 반환함.
False condition 값 확인: new_instance.get_range(), False condition 범위를 리스트로 반환. range()의 list 형태를 가지고 있음.
1. instance 생성 -> new_instance = Tester.instance()
2. False condition initialize(처음 한번 필수) -> new_instance.reset(argnum, max_value, condition_range, error_rate, correction_range)
3. Test 실행 -> new_instance.run(input)
이후 필요에 따라 reset() 이나 get_range() 적절히 활용
현재 버전은 parameter의 condition이 [0, max_value) 범위 중에서 10만큼의 range가 False인 경우로 지정. 원하는 error_rate를 만족하지 못하면 condition을 추가.
원하는 확률로 특정 parameter를 특정 range로 고정할수 있음. correction_range = 원하는 range ex) [[(parameter index, range(a, b), correction_rate), ...], [(), ..], ..]
각각의 리스트들은 개별적인 constraint condition으로 적용. [A, B, C]라는 세 조건이 주어질 경우, error condition마다 A B C중 하나가 랜덤으로 선택.
ex) parameter 3개: [ [range(11,21), range(30,40), range(44, 54)], [range(2,12), range(51,61), range(99, 109)], ... ]
ex2) parameter 2개 with correction: [[(1, range(10,20), 0.5)]] : [ [range(11,21), range(10, 20)], [range(2,12), range(51,61)], [range(52,62), range(10, 20)], [range(86,96), range(32,42)], ... ]
'''


class Tester(SingletonInstane):
    def __init__(self):
        self.argnum = 0  # 테스트할 parameter 개수
        self.max_value = 0  # parameter의 최댓값
        self.error_rate = 0  # 모든 경우 중 error case 비율
        self.condition = []  # parameter 별 False condition을 담고있는 list
        self._initCondition()

    def _initCondition(self, condition_range=10,
                       correction_range=[]):  # 클래스 구현용 내부함수. self.condition을 initialize 하는 함수.
        self.condition = []
        constraint = []

        current_error_rate = 0

        while current_error_rate < self.error_rate:
            temp_condition = []
            temp_error_rate = 1

            if len(correction_range) > 0:
                constraint = random.choice(correction_range)

            for i in range(self.argnum):
                for correction in constraint:
                    # print(correction, '\n')
                    if correction != None and correction[0] == i and random.random() <= correction[2]:
                        temp_condition.append(correction[1])
                        temp_error_rate *= condition_range / self.max_value
                        break
                else:
                    rand_range_start = random.randrange(0, self.max_value - condition_range)
                    temp_condition.append(range(rand_range_start, rand_range_start + condition_range))
                    temp_error_rate *= condition_range / self.max_value

            if temp_condition not in self.condition:
                self.condition.append(temp_condition)
                current_error_rate += temp_error_rate

            # self.condition.append(lambda x: x[i] in temp_condition[i] for i in range(self.argnum))

    def reset(self, argnum=0, max_value=0, condition_range=10, error_rate=0,
              correction_range=[]):  # condition을 initialize 하기위한 함수.
        self.argnum = argnum
        self.max_value = max_value
        self.error_rate = error_rate
        self._initCondition(condition_range, correction_range)

    def run(self, arglist):  # 실제로 테스트 할 때 사용하는 함수.
        result = []
        condition_num = 0
        answer_num = 0

        detected_condition = set()

        for args in arglist:
            assert (len(args) == self.argnum)
            result_temp = []
            condition_num += 1
            for condition in self.condition:
                for i in range(len(args)):
                    if not args[i] in condition[i]:
                        break
                else:
                    answer_num += 1
                    result_temp.append((-1, condition))
                    detected_condition.add(str(condition))
                    continue
                result_temp.append((0, condition))

            result.append(result_temp)

        return (
        (len(detected_condition) / len(self.condition), answer_num / condition_num, answer_num, condition_num), result)

    def get_range(self):  # 디버깅용 함수. self.condition 안의 조건을 반환하는 함수.
        return self.condition


if __name__ == "__main__":
    test = Tester.instance()