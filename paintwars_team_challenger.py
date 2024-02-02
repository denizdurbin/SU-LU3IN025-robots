# Projet "robotique" IA&Jeux 2021
#
# Binome:
#  Prénom Nom: _________
#  Prénom Nom: _________

memory = 0

def get_team_name():
    return "[ team with no name ]" # à compléter (comme vous voulez)

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
    translation = 1  # vitesse de translation (entre -1 et +1)
    rotation = 0


    if memory < 5 and robotId%2 == 0:
            rotation = 1

    memory+=1

    if robotId%8 == 0:
        translation = (1) * sensors["sensor_front"]["distance"]
        rotation = (-1) * sensors["sensor_front_left"]["distance"] + (1) * sensors["sensor_front_right"][ "distance"]

        translation = max(-1, min(translation, 1))
        rotation = max(-1, min(rotation, 1))

    if robotId%8 == 1 or robotId%8 == 2:
        if sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == False:
           rotation = 0
        elif(sensors["sensor_front"]["distance_to_wall"] == 1.0):
            if sensors["sensor_front_left"]["isSameTeam"] == False and sensors["sensor_front_right"]["isSameTeam"] == False:
                rotation = (1) * sensors["sensor_front_left"]["distance_to_robot"] + (-1) * sensors["sensor_front_right"]["distance_to_robot"]
        else:
            translation = (1) * sensors["sensor_front"]["distance"]
            rotation = (-1) * sensors["sensor_front_left"]["distance"] + (1) * sensors["sensor_front_right"]["distance"]

        translation = max(-1, min(translation, 1))
        rotation = max(-1, min(rotation, 1))


    else:
        if sensors["sensor_front_left"]["distance"] < 1 or sensors["sensor_front"]["distance"] < 1:
            rotation = 0.5  # rotation vers la droite
        elif sensors["sensor_front_right"]["distance"] < 1:
            rotation = -0.5  # rotation vers la gauche

        if sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == False:
            enemy_detected_by_front_sensor = True # exemple de détection d'un robot de l'équipe adversaire (ne sert à rien)

    return translation, rotation
