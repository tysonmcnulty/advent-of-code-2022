import unittest
from pathlib import Path

import pytest

from src import load_data
from src.day10 import parse, Noop, Addx, CPU, Program


class Day10Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example_data: list[str] = load_data(
            Path(__file__).parent / "resources/day10/example.txt"
        )
        cls.input_data: list[str] = load_data(
            Path(__file__).parent / "../src/day10/input.txt"
        )
        cls.simple_example_data: list[str] = load_data(
            Path(__file__).parent / "resources/day10/simple_example.txt"
        )

    def test_parse_simple_example(self):
        self.assertEqual(
            [
                Noop(),
                Addx(["3"]),
                Addx(["-5"]),
            ],
            parse(self.simple_example_data),
        )

    def test_run_simple_example(self):
        cpu = CPU()
        program = Program(parse(self.simple_example_data))
        self.assertEqual(1, cpu.X.value)
        next(cpu.run(program))
        self.assertEqual(-1, cpu.X.value)

    def test_run_simple_example_by_cycle(self):
        cpu = CPU()
        program = Program(parse(self.simple_example_data))
        self.assertEqual(0, cpu.cycle_number)
        run_iter = cpu.run(program, cycle_interval=1)
        next(run_iter)
        self.assertEqual(1, cpu.cycle_number)
        self.assertEqual(1, cpu.X.value)
        next(run_iter)
        self.assertEqual(2, cpu.cycle_number)
        self.assertEqual(1, cpu.X.value)
        next(run_iter)
        self.assertEqual(3, cpu.cycle_number)
        self.assertEqual(1, cpu.X.value)
        next(run_iter)
        self.assertEqual(4, cpu.cycle_number)
        self.assertEqual(4, cpu.X.value)
        next(run_iter)
        self.assertEqual(5, cpu.cycle_number)
        self.assertEqual(4, cpu.X.value)
        next(run_iter)
        self.assertEqual(5, cpu.cycle_number)
        self.assertEqual(-1, cpu.X.value)
        with pytest.raises(StopIteration):
            next(run_iter)

    def test_run_example(self):
        cpu = CPU()
        program = Program(parse(self.example_data))
        run_iter = cpu.run(program, cycle_interval=20)
        recordings = [
            (cpu.cycle_number, cpu.X.value)
            for _ in run_iter
            if cpu.cycle_number % 40 == 20
        ]

        self.assertEqual(13140, sum(map(lambda r: r[0] * r[1], recordings)))

    def test_solutions(self):
        cpu = CPU()
        program = Program(parse(self.input_data))
        run_iter = cpu.run(program, cycle_interval=20)
        recordings = [
            (cpu.cycle_number, cpu.X.value)
            for _ in run_iter
            if cpu.cycle_number % 40 == 20
        ]

        self.assertEqual(14720, sum(map(lambda r: r[0] * r[1], recordings)))
