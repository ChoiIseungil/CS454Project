# Test Data Generation Using Parallel Genetic Algorithm

KAIST 2020 Fall CS470 Artificial Intelligence Based Software Engineering

# Style-Preserving Image Translation from Korean to English

KAIST 2020 Fall CS470 Introduction to Artificial Intelligence

Authorized [Jongchan Park](https://github.com/KAIST-JongchanPark)

Authorized [Jungyeon Jeon](https://github.com/Minguinho99)

Authorized [Donghwan Kim](https://github.com/DonghwanKIM0101)

Authorized [Seungil Lee](https://github.com/ChoiIseungil)

-----------

## Introduction
Test data is necessary for debugging, but test data generation is time-consuming and annoying process. We want to generate test data automatically using Parallel Genetic Algorithm.

[Test Data Generation Using Parallel Genetic Algorithm]()

## Genetic algorithm and Parallel Genetice Algorithm

Genetic Algorithm (GA) is a search heuristic that is inspired by Charles Darwin’s theory of natural evolution. 

## Results
<img src="Results/네온사인.jpg" height="300px"></img>

# Usage

We implement both GA and PGA to compare the performance.

* Clone this repository:

        git clone https://github.com/ChoiIseungil/CS454Project.git
        cd CS454Project

* Experiment environments:

[correction range for tester](https://github.com/ChoiIseungil/CS454Project/blob/main/main.py#L54)

[Quit option for GA](https://github.com/ChoiIseungil/CS454Project/blob/main/GA.py#L71)

[save performance with population size](https://github.com/ChoiIseungil/CS454Project/blob/main/GA.py#L82) or [with time](https://github.com/ChoiIseungil/CS454Project/blob/main/GA.py#L83) in GA

[Quit option for PGA](https://github.com/ChoiIseungil/CS454Project/blob/main/PGA.py#L46)

[save performance with population size](https://github.com/ChoiIseungil/CS454Project/blob/main/PGA.py#L67) or [with time](https://github.com/ChoiIseungil/CS454Project/blob/main/PGA.py#L68) in PGA

* Hyper parameters

[n, m, k in PGA](https://github.com/ChoiIseungil/CS454Project/blob/main/main.py#L57)

        python main.py -p True -m 0.1 -n 3 -l 100 -c 15 -r 0.5

arguments when running program

-p: "True" for PGA and "False" for GA (default = "False")

-m: mutation rate (default = 0.05)

-n: arg_num for tester (default = 5)

-l: max_value for tester (default = 20)

-c: condition_range for tester (default = 5)

-r: error_rate for tester (default = 0.3)

## References
* [SynthText](https://github.com/ankush-me/SynthText): Used to synthesize background image and text to generate train dataset

* [EasyOCR](https://github.com/JaidedAI/EasyOCR): Recoginze Korean text and its bounding box in the image 

* [SRNet](https://github.com/Niwhskal/SRNet): The twin discriminator generative adversarial network that can edit text in any image while maintaining context of the background, font style and color

* [Google Clound Translation](https://cloud.google.com/translate/?hl=ko) : API to translate Korean to English

