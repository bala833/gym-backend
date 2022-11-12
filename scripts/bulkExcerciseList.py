from workout.models import Excerciseslist

from urllib.request import urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

# if you get like this warning then please use def run() function for run individual function
# Try running with a higher verbosity level like: -v2 or -v3
# CommandError: An error has occurred running scripts. See errors above.

from django.db import transaction
import json, os
def bulkFireQuery():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Opening JSON file
    # f = open('gym-backend//common_function//excercise.json')
    json_file = open(os.path.join(BASE_DIR, 'common_function/excercise.json'))

    # returns JSON object as
    # a dictionary
    data = json.load(json_file)

    # Excerciseslist = []
    count = 1
    with transaction.atomic():
	    for ex in data:
	    	print(ex['bodyPart'])
	    	reCord = Excerciseslist.objects.create(bodypart= ex['bodyPart'],equipment= ex['equipment'],gif_url= ex['gifUrl'],name= ex['name'],target= ex['target'])
	    	# print(reCord.id)
	    	# print(count+1)
	    	print('--------------')

        # data = {'bodyPart' : ex['bodyPart'], 'equipment' : ex['equipment'], 'gifUrl' : ex['gifUrl'], 'id' : ex['id'], 'name' : ex['name'], 'target' : ex['target']}
        # Excerciseslist.append(data)

    # filterData = Excerciseslist.objects.filter(gif_url='http://d205bpvrqc9yn1.cloudfront.net/0002.gif')
    # for i in filterData:
    # 	print(i.id, i.name)
    print('query fire successfully')
    # print(Excerciseslist)




# def saveImageFromUrlInModel():
# 	my_obj = Excerciseslist()
# 	imageModel = Excerciseslist.objects.all()
# 	with transaction.atomic():
# 		for imgUrl in imageModel:
# 			getModel = Excerciseslist.objects.get(id = imgUrl.id)
# 			my_obj.get_image_from_url(getModel.gif_url)
# 			# getModel.save()



def run():
	bulkFireQuery()
	# saveImageFromUrlInModel()