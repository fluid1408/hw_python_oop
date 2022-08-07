from dataclasses import dataclass, fields


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = ('Тип тренировки:{};'
               'Длительность: {:.3f} ч.; '
               'Дистанция: {:.3f} км; '
               'Ср. скорость: {:.3f} км/ч; '
               'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        """Информационное сообщение о тренировке."""
        return self.MESSAGE.format(
            self.training_type,
            self.duration,
            self.distance,
            self.speed,
            self.calories
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP = 0.65
    M_IN_KM = 1000
    M_IN_HR = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        mean_speed = self.get_distance() / self.duration
        """Получить среднюю скорость движения."""
        return mean_speed

    def get_spent_calories(self) -> None:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type=type(self).__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    M_IN_HR = 60

    def get_spent_calories(self) -> float:
        AVERAGE_FOR_SPEED_MULTIPLIER = 18
        awerage_for_speed = 20
        """Подсчёт расхода калорий для бега."""
        return (
            (AVERAGE_FOR_SPEED_MULTIPLIER * self.get_mean_speed()
             - awerage_for_speed)
            * self.weight / self.M_IN_KM * (self.duration * self.M_IN_HR)
        )


@dataclass
class SportsWalking(Training):
    height: float

    def get_spent_calories(self) -> float:
        coeff_calorie_3 = 0.035
        coeff_calorie_4 = 0.029
        """Получить количество затраченных калорий."""
        return (
            coeff_calorie_3 * self.weight
            + (self.get_mean_speed() ** 2 // self.height)
            * coeff_calorie_4 * self.weight) * (self.duration / self.M_IN_KM
                                                )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: int
    LEN_STEP = 1.38
    CALCULATION_OF_CALORIES_1 = 1.1
    CALCULATION_OF_CALORIES_2 = 2

    def get_mean_speed(self) -> float:
        mean_speed_swim = (
            self.length_pool
            * self.count_pool / self.M_IN_KM / self.duration
        )
        return mean_speed_swim

    def get_spent_calories(self):
        spent_calories_swim = (
            (self.get_mean_speed() + self.CALCULATION_OF_CALORIES_1)
            * self.CALCULATION_OF_CALORIES_2 * self.weight
        )
        """Тренировка: плавание."""
        return spent_calories_swim


TRAINING_CODES = {'SWM': (Swimming, len(fields(Swimming))),
                  'RUN': (Running, len(fields(Running))),
                  'WLK': (SportsWalking, len(fields(SportsWalking)))
                  }


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TRAINING_CODES:
        raise AttributeError(f'Передан неизвестный аргумент {workout_type}')
    training, number_of_fields = TRAINING_CODES[workout_type]
    if number_of_fields != len(data):
        raise AttributeError(f'Неверное количество передаваемых значений'
                             f'для класса {workout_type}.'
                             f'Было принято {len(data)},'
                             f' а нужно {number_of_fields}')
    return training(*data)


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
