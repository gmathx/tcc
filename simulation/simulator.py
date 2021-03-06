#!/usr/bin/env python
# -*- coding: utf-8 -*-

# function that returns dy/dt and dx/dt
CP = 1010  # Calor especifico do ar (J kg^(-1) K^(-1))
L = 2.5 * 10**(6) # Calor latente da agua (J/kg)
GROUND_REFLECTANCE = 0.681963305054 # 0.781963305054
SPECIFC_MASS_AIR = 1.2

def qgrin_eq(transmittance_g_m, transmittance_s_c, qgrout):
    # return float(transmittance_g_m) * (1.0 - float(GROUND_REFLECTANCE)) * float(qgrout)
    return float(transmittance_g_m) * float(transmittance_s_c) * (1.0 - float(GROUND_REFLECTANCE)) * float(qgrout)
    
def qheater_eq(number_heater, heater_capacity, ground_surface):
    return float(number_heater) * (float(heater_capacity) / float(ground_surface))

def evapo_by_plant_size(qgrout, transmittance_g_m, crop_type):
    if crop_type == "small":
        return (0.00006 * transmittance_g_m * qgrout) + 0.0004
    elif crop_type == "large":
        return (0.0003 * transmittance_g_m * qgrout) + 0.0021
    else:
        return 0.000

def evapotranspiration(cooling, Et):
    Ec = 0.0
    Et = float(Et)/(60.0 * 60.0) # change Et 
    if cooling > 0:
        # c_power = 7.4
        c_power = 14.8
        # Ec = float(c_power)/60.0 # changing Ec unit from "kg/m2*min" to "kg/m2*s"
        Ec = float(c_power)/(24.0 * 60.0 * 60.0) # changing Ec unit from "kg/m2*dia" to "kg/m2*s"

    return Ec + Et

def temperature_model(t_in, t, parameters):
    t_out = parameters["t_out"]
    height = parameters["height"]
    cooling = parameters["cooling"]
    glass_area = parameters["glass_area"]
    ground_area = parameters["ground_area"]
    transmittance_g_m = parameters["transmittance_g_m"]
    transmittance_s_c = parameters["transmittance_s_c"]
    qgrout = parameters["qgrout"]
    number_heater = parameters["number_heater"]
    heater_capacity = parameters["heater_capacity"]
    ventilation_rate = parameters["ventilation_rate"]
    k = parameters["k"]

    # Solar radiation inside greenhouse
    # qgrin = qgrin_eq(transmittance_g_m, qgrout)
    qgrin = qgrin_eq(transmittance_g_m,transmittance_s_c, qgrout)
    
    # Quantidade de calor gerada pelo aquecedor
    qHearter = qheater_eq(number_heater, heater_capacity, ground_area)

    # Evapotranspiration
    evapo = evapo_by_plant_size(qgrout, transmittance_g_m, 'small')
    E = evapotranspiration(cooling, evapo)
    
    # glass area/ground area
    w = float(glass_area) / float(ground_area)
    
    # balance equations
    # Infiltration
    q_iv = L * E + ventilation_rate * CP * SPECIFC_MASS_AIR * (t_in - t_out)
    # The heat flux lost through the glazing
    q_glazing = k * w * (t_in - t_out)

    # print qGlazing + qIV
    # print qgrin + qHearter
    q1 = float(qgrin) + float(qHearter) - float(L) * float(E) - (float(t_in) - float(t_out)) * (float(ventilation_rate) * float(CP) * float(SPECIFC_MASS_AIR) + float(w) * float(k))
    q3 = float(CP) * float(SPECIFC_MASS_AIR) * float(height)

    return (float(q1)/float(q3))
