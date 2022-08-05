

class InfoMessage:
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Информационное сообщение о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    action: int
    duration: float
    weight: float

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        """Получить дистанцию в км."""
        return distance

    def get_mean_speed(self) -> float:
        mean_speed = self.get_distance() / self.duration
        """Получить среднюю скорость движения."""
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        return (
            (self.get_mean_speed() + coeff_calorie_1)
            * coeff_calorie_2
            * self.weight)

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(training_type=type(self).__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())
        """Вернуть информационное сообщение о выполненной тренировке."""


class Running(Training):
    action: int
    duration: float
    weight: float

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        """Тренировка: бег."""
        return (
            coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2
            * self.weight / self.M_IN_KM * (self.duration * 60)
        )


class SportsWalking(Training):
    action: int
    duration: float
    weight: float

    def __init__(
        self, action: int, duration: float,
            weight: float, height: float) -> None:
        self.height = height
        super().__init__(action, duration, weight
                         )

    def get_spent_calories(self) -> float:
        coeff_calorie_3 = 0.035
        coeff_calorie_4 = 0.029
        """Получить количество затраченных калорий."""
        return (
            coeff_calorie_3 * self.weight
            + (self.get_mean_speed()**2 // self.height)
            * coeff_calorie_4 * self.weight) * (self.duration * 60
                                                )


class Swimming(Training):
    LEN_STEP: float = 1.38
    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: int

    def __init__(
        self, action: int,
        duration: float, weight: float, length_pool: float,
            count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed_swim = (
            self.length_pool
            * self.count_pool / self.M_IN_KM / self.duration
        )
        return mean_speed_swim

    def get_spent_calories(self):
        spent_calories_swim = ((self.get_mean_speed() + 1.1) * 2 * self.weight)
        """Тренировка: плавание."""
        return spent_calories_swim


def read_package(workout_type: str, data: list) -> Training:
    training_codes = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    """Прочитать данные полученные от датчиков."""
    return training_codes[workout_type](*data)


def main(training: Training) -> None:
    info = training.show_training_info()
    """Главная функция."""
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
