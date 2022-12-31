class CRT:
    cycle = 1
    reg_x = 1
    sig_strength_at_cycle = {cycle: 0 for cycle in [20, 60, 100, 140, 180, 220]}

    def run_cycle(self):
        self.draw_pixel()
        if self.cycle in self.sig_strength_at_cycle:
            self.sig_strength_at_cycle[self.cycle] = self.signal_strength()
        self.cycle += 1

    def addx(self, num: int):
        self.run_cycle()
        self.run_cycle()
        self.reg_x += num

    def noop(self):
        self.run_cycle()

    def signal_strength(self):
        return self.cycle * self.reg_x

    def draw_pixel(self):
        crt_pos = (self.cycle - 1) % 40
        sprite_range = (self.reg_x - 1, self.reg_x, self.reg_x + 1)
        pixel = "#" if crt_pos in sprite_range else "."
        print(pixel, end="\n" if crt_pos == 39 else "")


def create_crt_from_input(path_input: str) -> CRT:
    crt = CRT()
    for line in open(path_input):
        match line.strip().split():
            case ["addx", arg]:
                crt.addx(int(arg))
            case ["noop"]:
                crt.noop()
            case _:
                raise Exception("Unrecognized input")
    return crt


if __name__ == "__main__":
    crt = create_crt_from_input("input.txt")
    print("Sum inspected signal strengths:", sum(crt.sig_strength_at_cycle.values()))
