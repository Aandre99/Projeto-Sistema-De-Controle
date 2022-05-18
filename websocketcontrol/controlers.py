from websocketcontrol.ControlLib import Control

class P(Control):
    def __init__(self, T, kp):
        super().__init__(T, 2)
        self.kp = kp

    def control(self):
        u = self.kp * self.e(0)
        print(f"Entrad do controle P = {u}")
        return u

    def set_values(self, kp, ki, kd):
        self.kp = kp

class PI(Control):
    def __init__(self, T, kp, ki):

        super().__init__(T, 2)
        self.kp = kp
        self.ki = ki
        self.erro_sum = 0

    def control(self):
        self.erro_sum += self.e(0)
        u = self.kp * self.e(0) + self.ki * self.erro_sum
        return u

    def set_values(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki