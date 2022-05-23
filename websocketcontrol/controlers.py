from websocketcontrol.ControlLib import Control


# Controlador proporcional


class P(Control):
    def __init__(self, T, kp):
        super().__init__(T, 2)
        self.kp = kp

    def control(self):
        u = self.kp * self.e(0)
        return u

    def set_values(self, kp, ki, kd):
        self.kp = kp


# Controlador proporcional integrativo


class PI(Control):
    def __init__(self, T, kp, ki):

        super().__init__(T, 2)
        self.kp = kp
        self.ki = ki
        self.erro_sum = 0

    def control(self):
        self.erro_sum += self.e(0)
        u = -self.kp * self.e(0) - self.ki * self.erro_sum

        return u

    def set_values(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki


# controlador proporcional derivativo


class PD(Control):
    def __init__(self, T, kp, kd):

        super().__init__(T, 2)
        self.kp = kp
        self.kd = kd
        self.error = 0

    def control(self):
        error_diff = self.e(0) - self.error
        self.error = self.e(0)

        u = -self.kp * self.e(0) - self.kd * error_diff
        return u

    def set_values(self, kp, ki, kd):
        self.kp = kp
        self.kd = kd


# controlador porporcional derivativo e integral


class PID(Control):
    def __init__(self, T, kp, ki, kd):

        super().__init__(T, 2)
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.erro_sum = 0
        self.error = 0

    def control(self):

        self.erro_sum += self.e(0)
        error_diff = self.e(0) - self.error

        u = -self.kp * self.e(0) - self.ki * self.erro_sum - self.kd * error_diff

        return u

    def set_values(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

