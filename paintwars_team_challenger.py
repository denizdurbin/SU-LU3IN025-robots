# Projet "robotique" IA&Jeux 2021
#
# Binome:
# Prénom Nom: Deniz Ali DURBIN 21111116
import math
import random
from typing import Union, Any

memory = 0


def get_team_name():
    return "team Roomba"


def get_extended_sensors(sensors):
    for key in sensors:
        sensors[key]["distance_to_robot"] = 1.0
        sensors[key]["distance_to_wall"] = 1.0
        if sensors[key]["isRobot"] == True:
            sensors[key]["distance_to_robot"] = sensors[key]["distance"]
        else:
            sensors[key]["distance_to_wall"] = sensors[key]["distance"]

    return sensors


def step(robotId, sensors):
    global memory
    sensors = get_extended_sensors(sensors)
    memory += 1

    # Robot with ID 1 uses the parameters found with genetic algorithms, TME2 ex3
    if robotId % 8 == 1:
        translation, rotation = genetic_algorithm(sensors)

    # Subsomption:
    # ->>>> Follow enemy robot / turn away from friendly robot
    # ->>> Avoid wall
    # ->> If iteration multiple of 200, advance with random rotation
    # -> Advance with a slight random turn

    elif robot_detection_front(sensors):
        # If there is a robot in front, follow it if it is an enemy, turn right if it is not
        if not is_same_team_front(sensors):
            translation, rotation = love_bot(sensors)
        else:
            translation, rotation = spread_out(sensors)

    # Robots with IDs 6 and 7 follow walls
    elif robotId % 8 in [5, 6, 7]:
        if sensors["sensor_right"]["distance_to_wall"] < 1 and sensors["sensor_left"]["distance_to_wall"] < 1:
            translation, rotation = suivre_murs_droite(sensors)
        elif sensors["sensor_right"]["distance_to_wall"] < 1:
            translation, rotation = suivre_murs_droite(sensors)
        else:
            translation, rotation = suivre_murs_gauche(sensors)

    elif wall_detection_front(sensors):
        translation, rotation = hate_wall(sensors)

    elif memory % 200 == 0:
        translation, rotation = avancer_rand_rotation(sensors)

    else:
        translation, rotation = tout_droit(sensors)

    translation = max(-1, min(translation, 1))
    rotation = max(-1, min(rotation, 1))
    return translation, rotation


# COMPORTEMENTS
def tout_droit(sensors):
    translation = 1
    rotation = random.uniform(-0.25, 0.25)
    return translation, rotation


def avancer_rand_rotation(sensors):
    translation = 1
    rotation = random.uniform(-1, 1)
    return translation, rotation


def hate_wall(sensors):
    translation = 1 * sensors["sensor_front"]["distance_to_wall"]
    rotation = (-1) * sensors["sensor_front_left"]["distance_to_wall"] + (1) * sensors["sensor_front_right"][
        "distance_to_wall"] + 1 * sensors["sensor_front"]["distance_to_wall"] - 1
    return translation, rotation


def love_bot(sensors):
    translation = 1 * sensors["sensor_front"]["distance"]
    rotation = (1) * sensors["sensor_front_left"]["distance_to_robot"] + (-1) * sensors["sensor_front_right"][
        "distance_to_robot"]
    return translation, rotation


def hate_bot(sensors):
    translation = 1 * sensors["sensor_front"]["distance_to_robot"]
    rotation = (-1) * sensors["sensor_front_left"]["distance_to_robot"] + (1) * sensors["sensor_front_right"][
        "distance_to_robot"] + 1 * sensors["sensor_front"]["distance_to_robot"] - 1
    return translation, rotation


def spread_out(sensors):
    translation = 1 * sensors["sensor_front"]["distance_to_robot"]
    rotation = 1
    return translation, rotation


def suivre_murs_droite(sensors):
    translation = 1
    rotation = 0
    # Continue straight if possible
    if (sensors["sensor_front"]["distance_to_wall"] * sensors["sensor_right"]["distance_to_wall"] == 1):
        translation = 1
        rotation = 0
    # Turn left to keep following wall in front
    elif (sensors["sensor_front"]["distance_to_wall"] < 1 or sensors["sensor_front_right"]["distance_to_wall"] < 1):
        translation = 1 * sensors["sensor_front"]["distance_to_wall"] * sensors["sensor_front_right"][
            "distance_to_wall"]
        rotation = -1
    # Follow wall to the right
    elif (sensors["sensor_front"]["distance_to_wall"] == 1):
        if (sensors["sensor_right"]["distance_to_robot"] < 0.2):
            rotation = -0.2
        elif (sensors["sensor_right"]["distance_to_robot"] > 0.8):
            rotation = 0.2

    return translation, rotation


def suivre_murs_gauche(sensors):
    translation = 1
    rotation = 0
    if (sensors["sensor_front"]["distance_to_wall"] * sensors["sensor_left"]["distance_to_wall"] == 1):
        translation = 1
        rotation = 0
    elif (sensors["sensor_front"]["distance_to_wall"] < 1 or sensors["sensor_front_left"]["distance_to_wall"] < 1):
        translation = 1 * sensors["sensor_front"]["distance_to_wall"] * sensors["sensor_front_left"]["distance_to_wall"]
        rotation = 1
    elif (sensors["sensor_front"]["distance_to_wall"] == 1):
        if (sensors["sensor_left"]["distance_to_robot"] < 0.2):
            rotation = +0.2
        elif (sensors["sensor_left"]["distance_to_robot"] > 0.8):
            rotation = -0.2

    return translation, rotation


def genetic_algorithm(sensors):
    translation = math.tanh(
        1 + 1 * sensors["sensor_front_left"]["distance"] + 1 * sensors["sensor_front"]["distance"] + 0 *
        sensors["sensor_front_right"]["distance"]);
    rotation = math.tanh(
        -1 + -1 * sensors["sensor_front_left"]["distance"] + 1 * sensors["sensor_front"]["distance"] + 1 *
        sensors["sensor_front_right"]["distance"]);
    return translation, rotation


# DETECTION
def wall_detection_front(sensors):
    return sensors["sensor_front"]["distance_to_wall"] * sensors["sensor_front_left"]["distance_to_wall"] * \
        sensors["sensor_front_right"]["distance_to_wall"] < 0.5


def wall_detection_sides(sensors):
    return sensors["sensor_right"]["distance_to_wall"] * sensors["sensor_left"]["distance_to_wall"] < 0.5


def robot_detection_front(sensors):
    return sensors["sensor_front"]["distance_to_robot"] * sensors["sensor_front_left"]["distance_to_robot"] * \
        sensors["sensor_front_right"]["distance_to_robot"] < 1


def robot_detection_back(sensors):
    return sensors["sensor_back"]["distance_to_robot"] * sensors["sensor_back_left"]["distance_to_robot"] * \
        sensors["sensor_back_right"]["distance_to_robot"] < 1


def is_same_team_front(sensors):
    return sensors["sensor_front"]["isSameTeam"] or sensors["sensor_front_left"]["isSameTeam"] or \
        sensors["sensor_front_right"]["isSameTeam"]


def wall_detection_right_or_left(sensors):
    return sensors["sensor_front_left"]["distance_to_wall"] * sensors["sensor_front_right"][
        "distance_to_wall"] < 0, 25 and sensors["sensor_front"]["distance_to_wall"] == 1.0
