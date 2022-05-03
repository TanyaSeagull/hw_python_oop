from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_km = self.action * self.LEN_STEP / self.M_IN_KM
        return distance_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration_h
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(type(self).__name__,
                                   self.duration_h,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""
    MEAN_SPEED_MULTIPLE: int = 18
    MEAN_SPEED_DEDUCTED: int = 20
    MIN_IN_HOUR: int = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        training_min = self.duration_h * self.MIN_IN_HOUR
        spent_calories = ((self.MEAN_SPEED_MULTIPLE * self.get_mean_speed()
                          - self.MEAN_SPEED_DEDUCTED) * self.weight_kg
                          / self.M_IN_KM * training_min)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    USER_WGHT__MULTIPLE_1: float = 0.035
    USER_WGHT__MULTIPLE_2: float = 0.029
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_m = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        training_min = self.duration_h * self.MIN_IN_HOUR
        spent_calories = ((self.USER_WGHT__MULTIPLE_1 * self.weight_kg
                           + (self.get_mean_speed()**2 // self.height_m)
                           * self.USER_WGHT__MULTIPLE_2 * self.weight_kg)
                          * training_min)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SPEED_SWM_MULTIPLE: float = 1.1
    SPEED_SWM_DEDUCTED: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_km = self.action * self.LEN_STEP / self.M_IN_KM
        return distance_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = (self.length_pool_m * self.count_pool
                      / self.M_IN_KM / self.duration_h)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = ((self.get_mean_speed() + self.SPEED_SWM_MULTIPLE)
                          * self.SPEED_SWM_DEDUCTED * self.weight_kg)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type_dict = {'SWM': Swimming,
                          'RUN': Running,
                          'WLK': SportsWalking}
    if workout_type not in training_type_dict:
        raise Exception("Произошло что-то плохое!")
    return training_type_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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