import unittest
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from src import load_data, yes
from src.day10 import CPU, Addx, CPUState, Device, Noop, Program, parse


@dataclass
class SignalRecorder:
    condition: Callable[[CPUState], bool] = yes
    recordings: list[tuple[int, int]] = field(default_factory=list)

    def receive(self, cpu_state: CPUState):
        if self.condition(cpu_state):
            self.recordings.append((cpu_state["cycle_number"], cpu_state["X"]["value"]))


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
        cpu.run(program)
        self.assertEqual(-1, cpu.X.value)

    def test_run_simple_example_by_cycle(self):
        cpu = CPU()
        program = Program(parse(self.simple_example_data))
        signal_recorder = SignalRecorder()
        cpu.receivers["signal_recorder"] = signal_recorder
        self.assertEqual(0, cpu.cycle_number)

        cpu.run(program)
        self.assertEqual(
            [(1, 1), (2, 1), (3, 1), (4, 4), (5, 4)], signal_recorder.recordings
        )

    def test_run_example(self):
        device = Device()
        program = Program(parse(self.example_data))
        signal_recorder = SignalRecorder(
            condition=lambda cpu_state: cpu_state["cycle_number"] % 40 == 20
        )
        device.install("signal_recorder", signal_recorder)

        device.run(program)

        self.assertEqual(
            13140, sum(map(lambda r: r[0] * r[1], signal_recorder.recordings))
        )

    def test_example_display(self):
        device = Device()
        program = Program(parse(self.example_data))

        device.run(program)

        self.assertEqual(
            [
                "##..##..##..##..##..##..##..##..##..##..",
                "###...###...###...###...###...###...###.",
                "####....####....####....####....####....",
                "#####.....#####.....#####.....#####.....",
                "######......######......######......####",
                "#######.......#######.......#######.....",
            ],
            device.crt.render(),
        )

    def test_solutions(self):
        device = Device()
        program = Program(parse(self.input_data))
        signal_recorder = SignalRecorder(
            condition=lambda cpu_state: cpu_state["cycle_number"] % 40 == 20
        )
        device.install("signal_recorder", signal_recorder)

        device.run(program)

        self.assertEqual(
            14720, sum(map(lambda r: r[0] * r[1], signal_recorder.recordings))
        )
        display = device.crt.render()
        self.assertEqual(
            [
                "####.####.###..###..###..####.####.####.",
                "#.......#.#..#.#..#.#..#.#.......#.#....",
                "###....#..###..#..#.###..###....#..###..",
                "#.....#...#..#.###..#..#.#.....#...#....",
                "#....#....#..#.#....#..#.#....#....#....",
                "#....####.###..#....###..#....####.#....",
            ],
            display,
        )
