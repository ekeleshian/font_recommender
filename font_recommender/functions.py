import glob2 as glob
from PIL import ImageFont, Image, ImageDraw
import numpy as np
import pandas as pd
from pdb import set_trace
from font_recommender import helpers

def picture_paths(pname="font_recommender"):
    font_paths = glob.glob(pname + '/static/*.png', )
    # Here we could also add more background
    # information to the particular font into its dictionary
    # in order to feed it to the HTML

    fonts = [
        dict([("picture", path[len(pname):])]) for path in font_paths
    ]

    return fonts



def generate_sentences(font_list = [20,21,22,23,24],
        font_infos = pd.read_csv("font_recommender/static/font_infos.csv")):

    font_list = list(font_infos.iloc[font_list,1])
    font_list = [f"font_recommender/static/fonts/{font}.ttf" for font in font_list]

    png_paths = []
    for font in font_list:
        png = helpers.reconstruct_img(font, scale=0, border = 2500)
        png_paths.append(f'font_recommender/static/{png}')

    scales = helpers.get_scales(png_paths)

    for idx,path in enumerate(font_list):
        helpers.reconstruct_img(path, scale=scales[idx], border = 1500)

    shifts = helpers.get_shifts(png_paths)

    for idx, path in enumerate(font_list):
        helpers.reconstruct_img(path, scale=scales[idx], border = 1500,
                       x_shift = shifts[idx][0], y_shift = shifts[idx][1])

    return "printed sentences!"




def generate_font_selection(font_id=np.random.randint(low=0,high=300), #TO BE CHANGED
                            max_distance=400,
                            distance_matrix=pd.read_csv("font_recommender/static/distance_matrix.csv",index_col=0),
                            mode="exploration"):
    '''
    Receives id of the font that has been clicked and a radius (max_distance)
    It has two modes:
        - Exploration: in order to sample from a larger radius
        - Exploitation: in order to find nearest neighbors

    Returns selection of new fonts that can be fed into the sentence generator.
    '''
    relevant_set = np.array(distance_matrix.iloc[[font_id], :]).reshape(-1)

    if mode=="exploration":
        relevant_set = np.where((relevant_set>0) & (relevant_set<max_distance))[0]
        font_choice = np.random.choice(relevant_set,5,replace=False)
    if mode=="exploitation":
        font_choice = relevant_set.argsort()[1:7]
        # set_trace()

    return font_choice





#DOES NOT WORK YET!
def generate_font_list(path="font_recommender/static/"):
    
    #Font names
    font_names = glob.glob(path+"fonts/*.ttf")
    font_names = [font.split("/")[-1].split(".")[0] for font in font_names]
    
    df = pd.DataFrame(font_names,columns=["font_names"])
    df.to_csv(path+"font_infos.csv")
    
    return None 
