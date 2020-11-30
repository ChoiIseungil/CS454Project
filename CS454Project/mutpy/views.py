import ast
import datetime
import inspect
import os
import traceback
from difflib import unified_diff

import jinja2
import yaml

from mutpy import codegen, termcolor, utils


class ViewNotifier:
    PREFIX = 'notify_'

    def __init__(self, views):
        self.views = views

    def add_view(self, views):
        self.views.append(views)

    def del_view(self, views):
        self.views.remove(views)

    def notify_all_views(self, notify, *args, **kwargs):
        for views in self.views:
            if hasattr(views, notify):
                attr = getattr(views, notify)
                attr(*args, **kwargs)

    def __getattr__(self, name):
        if name.startswith(ViewNotifier.PREFIX):
            notify = name[len(ViewNotifier.PREFIX):]
            return lambda *args, **kwargs: self.notify_all_views(notify, *args, **kwargs)
        else:
            raise AttributeError(name)


class QuietTextView:

    def __init__(self, colored_output=False):
        self.colored_output = colored_output

    def end(self, score, duration):
        # self.level_print('Mutation score {}: {}'.format(
        #     self.time_format(duration),
        #     self.decorate('{:.1f}%'.format(score.count()), 'blue', attrs=['bold']),
        # ))
        return(score.count())
        # f = open('mutScore.txt', 'w')
        # scoreStr = '{:.1f}%'.format(score.count())
        # f.write(scoreStr)
        # f.close()

    def level_print(self, msg, level=1, ended=True, continuation=False):
        end = "\n" if ended else ""

        if continuation:
            print(msg, end=end)
        else:
            if level == 1:
                prefix = self.decorate('[*]', 'blue')
            elif level == 2:
                prefix = self.decorate('   -', 'cyan')

            print('{} {}'.format(prefix, msg), end=end)

    def decorate(self, text, color=None, on_color=None, attrs=None):
        if self.colored_output:
            return termcolor.colored(text, color, on_color, attrs)
        else:
            return text

    @staticmethod
    def time_format(time=None):
        if time is None:
            return '[    -    ]'
        else:
            return '[{:.5f} s]'.format(time)


class TextView(QuietTextView):

    def __init__(self, colored_output=False, show_mutants=False):
        super().__init__(colored_output)
        self.show_mutants = show_mutants

    def initialize(self, targets, tests):
        self.level_print('Start mutation process:')
        self.level_print('targets: {}'.format(', '.join(targets)), 2)
        self.level_print('tests: {}'.format(', '.join(tests)), 2)

    def start(self):
        self.level_print('Start mutants generation and execution:')

    def end(self, score, duration):
        super().end(score, duration)
        self.level_print('all: {}'.format(score.all_mutants), 2)

        if score.all_mutants:
            self.level_print('killed: {} ({:.1f}%)'.format(score.killed_mutants,
                                                           100 * score.killed_mutants / score.all_mutants), 2)
            self.level_print('survived: {} ({:.1f}%)'.format(score.survived_mutants,
                                                             100 * score.survived_mutants / score.all_mutants), 2)
            self.level_print('incompetent: {} ({:.1f}%)'.format(score.incompetent_mutants,
                                                                100 * score.incompetent_mutants / score.all_mutants), 2)
            self.level_print('timeout: {} ({:.1f}%)'.format(score.timeout_mutants,
                                                            100 * score.timeout_mutants / score.all_mutants), 2)
            if score.all_nodes:
                self.level_print('Coverage: {} of {} AST nodes ({:.1f}%)'.format(
                    score.covered_nodes, score.all_nodes,
                    100 * score.covered_nodes / score.all_nodes
                ))

    def passed(self, tests, number_of_tests):
        self.level_print('{} tests passed:'.format(number_of_tests))

        for test, target, time in tests:
            test_name = test.__name__ + ('.' + target if target else '')
            self.level_print('{} {}'.format(test_name, self.time_format(time)), 2)

    def original_tests_fail(self, result):
        self.level_print(self.decorate('Tests failed:', 'red', attrs=['bold']))

        for fail in result.failed:
            self.level_print('fail in {} - {}'.format(fail.name, fail.short_message), 2)
        if result.is_incompetent():
            self.level_print(str(result.get_exception()), 2)

    def mutation(self, number, mutations, module, mutant):
        for mutation in mutations:
            self.level_print(
                '[#{:>4}] {:<3} {}: '.format(number, mutation.operator.name(), module.__name__),
                ended=False,
                level=2,
            )
            if mutation != mutations[-1]:
                print()
            if self.show_mutants:
                self.print_code(mutant, ast.parse(inspect.getsource(module)))

    def cant_load(self, name, exception):
        self.level_print(self.decorate('Can\'t load module: ', 'red', attrs=['bold']) + '{} ({}: {})'.format(name,
                                                                                                             exception.__class__.__name__,
                                                                                                             exception))

    def print_code(self, mutant, original):
        mutant_src = codegen.to_source(mutant)
        mutant_src = codegen.add_line_numbers(mutant_src)
        original_src = codegen.to_source(original)
        original_src = codegen.add_line_numbers(original_src)
        self._print_diff(mutant_src, original_src)

    def _print_diff(self, mutant_src, original_src):
        diff = self._create_diff(mutant_src, original_src)
        diff = [line for line in diff if not line.startswith(('---', '+++', '@@'))]
        diff = [self.decorate(line, 'blue') if line.startswith('- ') else line for line in diff]
        diff = [self.decorate(line, 'green') if line.startswith('+ ') else line for line in diff]
        print("\n{}\n".format('-' * 80) + "\n".join(diff) + "\n{}".format('-' * 80))

    @staticmethod
    def _create_diff(mutant_src, original_src):
        return list(unified_diff(original_src.split('\n'), mutant_src.split('\n'), n=4, lineterm=''))

    def killed(self, time, killer, *args, **kwargs):
        self.level_print(self.time_format(time) + ' ' + self.decorate('killed', 'green') + ' by ' + str(killer),
                         continuation=True)

    def survived(self, time, *args, **kwargs):
        self.level_print(self.time_format(time) + ' ' + self.decorate('survived', 'red'), continuation=True)

    def timeout(self, time, *args, **kwargs):
        self.level_print(self.time_format(time) + ' ' + self.decorate('timeout', 'yellow'), continuation=True)

    def incompetent(self, time, *args, **kwargs):
        self.level_print(self.time_format(time) + ' ' + self.decorate('incompetent', 'cyan'), continuation=True)


class DebugView:

    def print_exception(self, exception):
        print("\n" + "".join(traceback.format_exception(None, exception, None)))

    def incompetent(self, time, exception, tests_run, *args, **kwargs):
        self.print_exception(exception)

    def killed(self, time, killer, exception_traceback, *args, **kwargs):
        print('\n' + exception_traceback)


class AccReportView:

    def __init__(self):
        self.mutation_info = []

    def initialize(self, target, tests):
        self.target = target

    def passed(self, tests, number_of_tests):
        self.tests = tests
        self.number_of_tests = number_of_tests

    def mutation(self, number, mutations, module, mutant):
        mutations = [{'operator': mutation.operator.name(), 'lineno': mutation.node.lineno} for mutation in mutations]
        self.current_mutation = {
            'number': number,
            'mutations': mutations,
            'module': module,
        }

    def killed(self, time, killer, exception_traceback, tests_run, *args, **kwargs):
        self.end_mutation(
            'killed',
            time=time,
            killer=str(killer),
            tests_run=tests_run,
            exception_traceback=exception_traceback,
        )

    def survived(self, time, tests_run, *args, **kwargs):
        self.end_mutation('survived', time=time, tests_run=tests_run)

    def incompetent(self, time, exception, tests_run, *args, **kwargs):
        self.end_mutation('incompetent', time=time, tests_run=tests_run)

    def timeout(self, time, *args, **kwargs):
        self.end_mutation('timeout', time=time)

    def end_mutation(self, status, time=None, killer=None, tests_run=None, exception_traceback=None):
        self.current_mutation['status'] = status
        self.current_mutation['time'] = time
        self.current_mutation['killer'] = killer
        self.current_mutation['tests_run'] = tests_run
        self.current_mutation['exception_traceback'] = exception_traceback
        self.mutation_info.append(self.current_mutation)


class YAMLReportView(AccReportView):

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name

    def end(self, score, duration):
        with open(self.file_name, 'w') as report_file:
            yaml.dump({
                'targets': self.target,
                'tests': [{'name': test.__name__, 'target': target, 'time': time} for test, target, time in self.tests],
                'number_of_tests': self.number_of_tests,
                'mutations': self.mutation_info,
                'total_time': duration,
                'time_stats': dict(utils.TimeRegister.executions),
                'mutation_score': score.count(),
                'coverage': {
                    'covered_nodes': score.covered_nodes,
                    'all_nodes': score.all_nodes,
                }
            }, report_file, default_flow_style=False)


class HTMLReportView(AccReportView):

    def __init__(self, dir_name):
        super().__init__()
        self.dir_name = dir_name
        os.makedirs(dir_name, exist_ok=True)
        os.makedirs(os.path.join(dir_name, 'mutants'), exist_ok=True)
        templates_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=templates_path))

    def mutation(self, number, mutations, module, mutant):
        super().mutation(number, mutations, module, mutant)
        self.current_mutation['mutant'] = mutant

    def end_mutation(self, *args, **kwargs):
        super().end_mutation(*args, **kwargs)
        template = self.env.get_template('detail.html')
        context = {
            'mutant_code': codegen.to_source(self.current_mutation['mutant']),
        }
        context.update(self.current_mutation)
        report = template.render(context)
        file_path = os.path.join(self.dir_name, 'mutants', '{}.html'.format(self.current_mutation['number']))
        with open(file_path, 'w') as report_file:
            report_file.write(report)

    def end(self, score, duration):
        template = self.env.get_template('index.html')
        context = {
            'targets': self.target,
            'tests': self.tests,
            'number_of_tests': self.number_of_tests,
            'score': score,
            'duration': duration,
            'mutations': self.mutation_info,
            'date_now': datetime.datetime.now(),
        }
        report = template.render(context)
        file_path = os.path.join(self.dir_name, 'index.html')
        with open(file_path, 'w') as report_file:
            report_file.write(report)
