from os import walk
import pygame


def importa_pasta(path):
    surface_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path +'/'+ image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

def importa_dicionario(path):
    surface_dic = {}

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path +'/'+ image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_dic[image.split('.')[0]] = image_surf

        return surface_dic