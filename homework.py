from dataclasses import dataclass, fields
from typing import Dict, Sequence, Union


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = ('Тип тренировки: {}; '
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
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

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
    SPEED_MULTIPLIER = 18
    SPEED_SHIFT = 20

    def get_spent_calories(self) -> float:
        """Подсчёт расхода калорий для бега."""
        return (
            (self.SPEED_MULTIPLIER * self.get_mean_speed()
             - self.SPEED_SHIFT)
            * self.weight / self.M_IN_KM * (self.duration * self.M_IN_HR)
        )


@dataclass
class SportsWalking(Training):
    height: float
    WEIGHT_MULTIPLIER_1 = 0.035
    WEIGHT_MULTIPLIER_2 = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.WEIGHT_MULTIPLIER_1 * self.weight
             + (self.get_mean_speed() ** 2 // self.height)
             * self.WEIGHT_MULTIPLIER_2 * self.weight)
            * (self.duration * self.M_IN_HR)
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: int
    LEN_STEP = 1.38
    SPEED_SHIFT_1 = 1.1
    SPEED_MULTIPLIER = 2

    def get_mean_speed(self) -> float:
        return (
            self.length_pool
            * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self):
        """Тренировка: плавание."""
        return (
            (self.get_mean_speed()
             + self.SPEED_SHIFT_1)
            * self.SPEED_MULTIPLIER
            * self.weight
        )


TRAINING = {'SWM': (Swimming, len(fields(Swimming))),
            'RUN': (Running, len(fields(Running))),
            'WLK': (SportsWalking, len(fields(SportsWalking)))
            }
UNKNOWN_ARGUMENT = ('Передан неизвестный аргумент {}')
INCORRECT_NUMBER_OF_VALUES = ('Неверное количество передаваемых значений'
                              'для класса {}.'
                              'Было принято {},'
                              ' а нужно {}')


def read_package(workout_type: str, data: Union[Dict, Sequence]) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type not in TRAINING:
        raise ValueError(UNKNOWN_ARGUMENT.format(workout_type))
    training, number_of_fields = TRAINING[workout_type]
    if number_of_fields != len(data):
        raise ValueError(INCORRECT_NUMBER_OF_VALUES.format(workout_type,
                         len(data), number_of_fields))
    return training(*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
