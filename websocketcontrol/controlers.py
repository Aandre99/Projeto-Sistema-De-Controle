from websocketcontrol.ControlLib import Control


# Controlador proporcional


class P(Control):
    def __init__(self, T):
        super().__init__(T, 2)
        self.kp = 0

    def control(self):
        u = self.kp * self.e(0)
        return u

    def set_values(self, kp, ki, kd):
        self.kp = kp


# Controlador proporcional integrativo


class PI(Control):
    def __init__(self, T):

        super().__init__(T, 2)
        self.kp = 0
        self.ki = 0
        self.proporcional_error = 0
        self.integral_error = 0
        self.error_integ = 0

    def control(self):
        self.error_integ += self.e(0)

        self.proporcional_error = self.kp * self.e(0)
        self.integral_error = self.ki * self.error_integ

        u = self.proporcional_error + self.integral_error

        return u

    def set_values(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki

    def get_components_erros(self):
        return self.proporcional_error, 0, self.integral_error


# controlador proporcional derivativo


class PD(Control):
    def __init__(self, T):

        super().__init__(T, 2)
        self.kp = 0
        self.kd = 0
        self.error_deriv = 0
        self.proporcional_error = 0
        self.derivative_error = 0

    def control(self):
        self.error_deriv = self.e(0) - self.e(-1)

        self.proporcional_error = self.kp * self.e(0)
        self.derivative_error = self.kd * self.error_deriv
        u = self.proporcional_error + self.derivative_error
        return u

    def set_values(self, kp, ki, kd):
        self.kp = kp
        self.kd = kd

    def get_components_erros(self):
        return self.proporcional_error, self.derivative_error, 0


# controlador porporcional derivativo e integral


class PID(Control):
    def __init__(self, T):

        super().__init__(T, 2)
        self.kp = 0
        self.ki = 0
        self.kd = 0
        self.error_integ = 0
        self.error_deriv = 0

        self.proporcional_error = 0
        self.derivative_error = 0
        self.integral_error = 0

    def control(self):

        self.error_integ += self.e(0)
        self.error_deriv = self.e(0) - self.e(-1)

        self.proporcional_error = self.kp * self.e(0)
        self.integral_error = self.ki * self.error_integ
        self.derivative_error = self.kd * self.error_deriv

        u = self.proporcional_error + self.derivative_error + self.integral_error

        if u > 100000:
            u = self.y(-1)

        return u

    def set_values(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def get_components_erros(self):
        return self.proporcional_error, self.derivative_error, self.integral_error


# Variação PI-D do PID


class PI_D(Control):
    def __init__(self, T):

        super().__init__(T, 2)
        self.kp = 0
        self.td = 0
        self.ti = 0
        self.error_integ = 0
        self.error_deriv = 0

        self.proporcional_error = 0
        self.integral_error = 0
        self.derivative_error = 0

    def control(self):

        self.error_integ += self.e(0)
        self.error_deriv = self.e(0) - self.e(-1)

        self.proporcional_error = self.kp * self.e(0)
        self.integral_error = self.kp * (1 / self.ti) * self.e(0) * self.error_integ
        self.derivative_error = self.kp * self.y(0) * self.td * self.error_deriv

        u = self.proporcional_error + self.derivative_error + self.integral_error

        if u > 100000 or u < -100000:
            u = self.y(-1)

        return u

    def set_values(self, kp, ki, kd):

        self.kp = kp
        self.td = kd / kp
        self.ti = kp / ki

    def get_components_erros(self):
        return self.proporcional_error, self.derivative_error, self.integral_error


# Variação I-PD do PID


class I_PD(Control):
    def __init__(self, T):

        super().__init__(T, 2)
        self.kp = 0
        self.td = 0
        self.ti = 0

        self.error_integ = 0
        self.error_deriv = 0

        self.proporcional_error = 0
        self.integral_error = 0
        self.derivative_error = 0

    def control(self):

        self.error_integ += self.e(0)
        self.error_deriv = self.e(0) - self.e(-1)

        part1 = self.ti * self.error_integ * self.e(0)
        part2 = self.y(0)
        part3 = self.y(0) * self.error_deriv * self.td

        self.proporcional_error = self.kp * self.y(0)
        self.integral_error = self.kp * self.ti * self.error_integ * self.e(0)
        self.derivative_error = self.kp * self.y(0) * self.error_deriv * self.td

        u = self.integral_error - self.proporcional_error - self.derivative_error

        if u > 100000 or u < -100000:
            u = self.y(-1)

        return u

    def set_values(self, kp, ki, kd):

        self.kp = kp
        self.td = kd / kp
        self.ti = kp / ki

    def get_components_erros(self):
        return self.proporcional_error, self.derivative_error, self.integral_error
