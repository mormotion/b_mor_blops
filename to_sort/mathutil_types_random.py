from mathutils import Vector, Matrix, Euler
import random

def seed(seed):
    random.seed(seed)

def sequenced_random_values(min_val, max_val):
    """ From a pair of uniform length number sequences, return a list of 
        random values in their paired ranges """
    values = []
    for a, b in zip(min_val, max_val):
        values.append(random.uniform(a, b))
    return values

def rand_translation_vector(min_val, max_val):
    """ Returns a random vector whose components are in the range 
        of the components of min_val and max_val """
    return Vector(tuple(sequenced_random_values(min_val, max_val)))

def rand_translation_matrix(min_val, max_val):
    """ Returns a random 4x4 translation matrix whose components are in 
        the range of the components of min_val and max_val """
    rand_vec = rand_translation_vector(min_val, max_val).to_3d()
    return Matrix.Translation(rand_vec)

def rand_euler_angle(min_val, max_val):
    """ Returns a euler angle whose components are in the range of the
        components of min_val and max_val """
    return Euler(tuple(sequenced_random_values(min_val, max_val)))

def rand_rotation_matrix(min_val, max_val):
    """ Returns a random 4x4 translation matrix whose components are in 
        the range of the components of min_val and max_val """
    return Euler(tuple(sequenced_random_values(min_val, max_val))).to_matrix()
