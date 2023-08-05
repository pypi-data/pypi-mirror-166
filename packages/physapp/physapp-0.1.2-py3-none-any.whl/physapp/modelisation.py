# -*- coding: utf-8 -*-
"""
Module de modélisation de courbes pour la physique appliquée
@author: David Thérincourt
"""

import numpy as np
from scipy.stats import linregress
from scipy.optimize import curve_fit

#--------------------------
# Fonctions mathématiques
#--------------------------

# Fonction linéaire : y=a*x
def lineaire(x, a) :
    """
    Fonction lineaire du type y = a*x

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    a (float) :

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    return a*x


# Fonction parabolique : y = ax^2 + bx  + c
def parabole(x, a, b, c) :
    """
    Fonction parabolique du type y = a*x**2 + b*x + c

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    a (float) :
    b (float) :
    c (float) :

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    return a*x**2+b*x+c

# Fonction exponentielle croissante : y = A*(1-exp(-(x-x0)/tau))
def exponentielle_croissante(x, A, tau, x0=0):
    """
    Fonction exponenetielle croissante du type y = A*(1-exp(-(x-x0)/tau))

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    A (float)  : limite à l'infini.
    tau (float) : constante de temps.

    Paramètre optionnel :
    x0 (0 par défaut) : retard.

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    return A*(1-np.exp(-(x-x0)/tau))

# Fonction exponentielle décroissante : y = A*exp(-(x-x0)/tau)
def exponentielle_decroissante(x, A, tau, x0=0):
    """
    Fonction exponenetielle décroissante du type y = A*exp(-(x-x0)/tau)

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    A (float)  : limite à l'infini.
    tau (float) : constante de temps.

    Paramètre optionnel :
    x0 (0 par défaut) : retard.

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    return A*np.exp(-(x-x0)/tau)

def transmittance_ordre1_passe_bas(f, T0, f0):
    """
    Fonction transmittance d'un système d'ordre 1 passe-bas

    Paramètres :
    f (liste ou tableau Numpy) : fréquence.
    T0 (float)  : Amplification statique.
    f0 (float) : fréquence propre.

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    return T0/np.sqrt(1+(f/f0)**2)

def transmittance_ordre1_passe_haut(f, T0, f0):
    """
    Fonction transmittance d'un système d'ordre 1 passe-bas

    Paramètres :
    f (liste ou tableau Numpy) : fréquence.
    T0 (float)  : Amplification statique.
    f0 (float) : fréquence propre.

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    return T0*(f/f0)/np.sqrt(1+(f/f0)**2)


def transmittance_ordre2_passe_bas(f, T0, f0, m):
    """
    Fonction transmittance d'un système d'ordre 1 passe-bas

    Paramètres :
    f (liste ou tableau Numpy) : fréquence.
    T0 (float)  : Amplification statique.
    f0 (float) : fréquence propre.
    m (float) : coefficient d'amortissement

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    return T0/np.sqrt((1-(f/f0)**2)**2+(2*m*f/f0)**2)

def transmittance_ordre2_passe_haut(f, T0, f0, m):
    """
    Fonction transmittance d'un système d'ordre 1 passe-bas

    Paramètres :
    f (liste ou tableau Numpy) : fréquence.
    T0 (float)  : Amplification statique.
    f0 (float) : fréquence propre.
    m (float) : coefficient d'amortissement

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    return -T0*(f/f0)**2/np.sqrt((1-(f/f0)**2)**2+(2*m*f/f0)**2)

def transmittance_ordre2_passe_bande(f, T0, f0, m):
    """
    Fonction transmittance d'un système d'ordre 1 passe-bas

    Paramètres :
    f (liste ou tableau Numpy) : fréquence.
    T0 (float)  : Amplification statique.
    f0 (float) : fréquence propre.
    m (float) : coefficient d'amortissement

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    return T0*2*m*(f/f0)/np.sqrt((1-(f/f0)**2)**2+(2*m*f/f0)**2)





#---------------------------------------------
# Modélisations
#---------------------------------------------


# Ajustement suivante une fonction linéaire
def ajustement_lineaire(x, y, a_p0=1) :
    """
    Modélisation d'une fonction parabolique du type :
    
    y = a*x

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    y (liste ou tableau Numpy de même dimension que x) : ordonnées.

    Retourne :
    a (float)
    """
    (a), pcov = curve_fit(lineaire,x,y, p0=[a_p0])
    return a



# Ajustement suivante une fonction affine
def ajustement_affine(x, y):
    """
    Modélisation d'une fonction affine de la forme :
    
    y = a*x + b

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    y (liste ou tableau Numpy de même dimension que x) : ordonnées.

    Retourne un tuple (a, b) :
    a (float) : coefficient directeur.
    b (float) : ordonnée à l'origine.
    """
    a, b, _, _, _ = linregress(x,y)
    return a, b


# Ajustement suivante une fonction parabolique
def ajustement_parabolique(x, y) :
    """
    Modélisation d'une fonction parabolique du type :
    
    y = a*x**2 + b*x + c

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    y (liste ou tableau Numpy de même dimension que x) : ordonnées.

    Retourne :
    [a, b, c] (tableau) : coefficients
    """
    return np.polyfit(x, y, 2)


# Ajustement suivante une fonction exponentielle croissante
def ajustement_exponentielle_croissante(x, y, A_p0=1, tau_p0=1) :
    """
    Modélisation d'une série de points (x,y) par une fonction exponentielle croissante
    du type :
    
    y = A*(1-exp(-x/tau))

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    y (liste ou tableau Numpy de même dimension que x) : ordonnées.

    Paramètres optionnels :
    A_p0 (1 par défaut) : valeur de la limite à l'infini aidant à la convergence du modèle.
    tau_p0 (1 par défaut) : valeur de la constante de temps aidant à la convergence du modèle.

    Retourne un tuple (A, tau, x0) :
    A (float)  : limite à l'infini.
    tau (float) : constante de temps.
    """
    (A,tau), pcov = curve_fit(exponentielle_croissante,x,y, p0=[A_p0, tau_p0])
    return A, tau

# Ajustement suivante une fonction exponentielle croissante avec décalage
def ajustement_exponentielle_croissante_x0(x, y, A_p0=1, tau_p0=1, x0_p0=0) :
    """
    Modélisation d'une série de points (x,y) par une fonction exponentielle croissante
    décalée suivant l'abscisse du type :
    
    y = A*(1-exp(-(x-xo)/tau))

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    y (liste ou tableau Numpy de même dimension que x) : ordonnées.

    Paramètres optionnels :
    A_p0 (1 par défaut) : valeur de la limite à l'infini aidant à la convergence du modèle.
    tau_p0 (1 par défaut) : valeur de la constante de temps aidant à la convergence du modèle.
    x0_p0 (0 par défaut) : valeur du retard aidant à la convergence du modèle.

    Retourne un tuple (A, tau, x0) :
    A (float)  : limite à l'infini.
    tau (float) : constante de temps.
    x0 (float) : retard.
    """
    (A,tau,x0), pcov = curve_fit(exponentielle_croissante,x,y, p0=[A_p0, tau_p0, x0_p0])
    return A, tau, x0


# Ajustement suivante une fonction exponentielle décroissante
def ajustement_exponentielle_decroissante(x, y, A_p0=1, tau_p0=1) :
    """
    Modélisation d'une série de points (x,y) par une fonction exponentielle croissante
    du type :
    
    y = A*exp(-x/tau)

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    y (liste ou tableau Numpy de même dimension que x) : ordonnées.

    Paramètres optionnels :
    A_p0 (1 par défaut) : valeur de la limite à l'infini aidant à la convergence du modèle.
    tau_p0 (1 par défaut) : valeur de la constante de temps aidant à la convergence du modèle.

    Retourne un tuple (A, tau, x0) :
    A (float)  : limite à l'infini.
    tau (float) : constante de temps.
    """
    (A,tau), pcov = curve_fit(exponentielle_decroissante, x, y, p0=[A_p0, tau_p0])
    return A, tau


# Ajustement suivante une fonction exponentielle décroissante avec décalage
def ajustement_exponentielle_decroissante_x0(x, y, A_p0=1, tau_p0=1, x0_p0=1) :
    """
    Modélisation d'une série de points (x,y) par une fonction exponentielle croissante
    du type :
    
    y = A*exp(-(x-x0)/tau)

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    y (liste ou tableau Numpy de même dimension que x) : ordonnées.

    Paramètres optionnels :
    A_p0 (1 par défaut) : valeur de la limite à l'infini aidant à la convergence du modèle.
    tau_p0 (1 par défaut) : valeur de la constante de temps aidant à la convergence du modèle.

    Retourne un tuple (A, tau, x0) :
    A (float)  : limite à l'infini.
    tau (float) : constante de temps.
    x0 (float) : retard.
    """
    (A,tau, x0), pcov = curve_fit(exponentielle_decroissante, x, y, p0=[A_p0, tau_p0, x0_p0])
    return A, tau, x0


# Ajustement suivante une fonction de transmittance d'un système d'ordre 1 passe-bas
def ajustement_transmittance_ordre1_passe_bas(f, T, T0_p0=1, f0_p0=1) :
    """
    Modélisation d'une série de points (x,y) par une fonction de transmittance
    d'un système d'ordre 1 passe-bas :
    
    y = T0/sqrt(1+(f/f0)**2)

    Paramètres :
    f (liste ou tableau Numpy) : fréquence.
    T (liste ou tableau Numpy de même dimension que x) : transmittance.

    Paramètres optionnels :
    T0_p0 (1 par défaut) : valeur de T0 aidant à la convergence du modèle.
    f0_p0 (1 par défaut) : valeur de f0 aidant à la convergence du modèle.

    Retourne un tuple (A, tau, x0) :
    T0 (float) : amplification statique.
    f0 (float) : fréquence propre
    """
    (T0, f0), pcov = curve_fit(transmittance_ordre1_passe_bas, f, T, p0=[T0_p0, f0_p0])
    return T0, f0

# Ajustement suivante une fonction de transmittance d'un système d'ordre 1 passe-haut
def ajustement_transmittance_ordre1_passe_haut(f, T, T0_p0=1, f0_p0=1) :
    """
    Modélisation d'une série de points (x,y) par une fonction de transmittance
    d'un système d'ordre 1 passe-bas :
    
    y = T0*(f/f0)/sqrt(1+(f/f0)**2)

    Paramètres :
    f (liste ou tableau Numpy) : fréquence.
    T (liste ou tableau Numpy de même dimension que x) : transmittance.

    Paramètres optionnels :
    T0_p0 (1 par défaut) : valeur de T0 aidant à la convergence du modèle.
    f0_p0 (1 par défaut) : valeur de f0 aidant à la convergence du modèle.

    Retourne un tuple (A, tau, x0) :
    T0 (float) : amplification statique.
    f0 (float) : fréquence propre
    """
    (T0, f0), pcov = curve_fit(transmittance_ordre1_passe_haut, f, T, p0=[T0_p0, f0_p0])
    return T0, f0


# Ajustement suivante une fonction de transmittance d'un système d'ordre 2 passe-bas
def ajustement_transmittance_ordre2_passe_bas(f, T, T0_p0=1, f0_p0=1, m_p0=1) :
    """
    Modélisation d'une série de points (f,T) par une fonction de transmittance
    d'un système d'ordre 2 passe-bas :
    
    T0/np.sqrt((1-(f/f0)**2)**2+(2*m*f/f0)**2)

    Paramètres :
    f (liste ou tableau Numpy) : fréquence.
    T (liste ou tableau Numpy de même dimension que x) : transmittance.

    Paramètres optionnels :
    T0_p0 (1 par défaut) : valeur de T0 aidant à la convergence du modèle.
    f0_p0 (1 par défaut) : valeur de f0 aidant à la convergence du modèle.
    m_p0 (1 par défaut)  : valeur de m  aidant à la convergence du modèle.

    Retourne un tuple (A, tau, x0) :
    T0 (float) : amplification statique.
    f0 (float) : fréquence propre
    """
    (T0, f0, m), pcov = curve_fit(transmittance_ordre2_passe_bas, f, T, p0=[T0_p0, f0_p0, m_p0])
    return T0, f0, m

# Ajustement suivante une fonction de transmittance d'un système d'ordre 2 passe-haut
def ajustement_transmittance_ordre2_passe_haut(f, T, T0_p0=1, f0_p0=1, m_p0=1) :
    """
    Modélisation d'une série de points (f,T) par une fonction de transmittance
    d'un système d'ordre 2 passe-haut : T = -T0*(f/f0)**2/np.sqrt((1-(f/f0)**2)**2+(2*m*f/f0)**2)

    Paramètres :
    f (liste ou tableau Numpy) : fréquence.
    T (liste ou tableau Numpy de même dimension que x) : transmittance.

    Paramètres optionnels :
    T0_p0 (1 par défaut) : valeur de T0 aidant à la convergence du modèle.
    f0_p0 (1 par défaut) : valeur de f0 aidant à la convergence du modèle.
    m_p0 (1 par défaut)  : valeur de m  aidant à la convergence du modèle.

    Retourne un tuple (A, tau, x0) :
    T0 (float) : amplification statique.
    f0 (float) : fréquence propre
    """
    (T0, f0, m), pcov = curve_fit(transmittance_ordre2_passe_haut, f, T, p0=[T0_p0, f0_p0, m_p0])
    return T0, f0, m

# Ajustement suivante une fonction de transmittance d'un système d'ordre 2 passe-bande
def ajustement_transmittance_ordre2_passe_bande(f, T, T0_p0=1, f0_p0=1, m_p0=1) :
    """
    Modélisation d'une série de points (f,T) par une fonction de transmittance
    d'un système d'ordre 2 passe-bande :
    T = T0*2*m*(f/f0)/np.sqrt((1-(f/f0)**2)**2+(2*m*f/f0)**2)

    Paramètres :
    f (liste ou tableau Numpy) : fréquence.
    T (liste ou tableau Numpy de même dimension que x) : transmittance.

    Paramètres optionnels :
    T0_p0 (1 par défaut) : valeur de T0 aidant à la convergence du modèle.
    f0_p0 (1 par défaut) : valeur de f0 aidant à la convergence du modèle.
    m_p0 (1 par défaut)  : valeur de m  aidant à la convergence du modèle.

    Retourne un tuple (A, tau, x0) :
    T0 (float) : amplification statique.
    f0 (float) : fréquence propre
    """
    (T0, f0, m), pcov = curve_fit(transmittance_ordre2_passe_bande, f, T, p0=[T0_p0, f0_p0, m_p0])
    return T0, f0, m





